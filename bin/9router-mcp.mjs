#!/usr/bin/env node
import { mkdir, writeFile } from 'node:fs/promises'
import path from 'node:path'
import process from 'node:process'
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js'

export function env(name, fallback = undefined) {
  const value = process.env[name]
  return value == null || value === '' ? fallback : value
}

export function assertInsideRoot(projectRoot, targetPath) {
  const root = path.resolve(projectRoot)
  const out = path.resolve(root, targetPath)
  const relative = path.relative(root, out)
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error(`target_path must stay inside project_root: ${targetPath}`)
  }
  return out
}

export function normalizeSize(width, height) {
  const w = Number(width)
  const h = Number(height)
  if (!Number.isFinite(w) || !Number.isFinite(h) || w <= 0 || h <= 0) {
    return env('NINEROUTER_IMAGE_DEFAULT_SIZE', '1024x1024')
  }
  return `${Math.round(w)}x${Math.round(h)}`
}

export function normalizeQuality(value) {
  const next = String(value || env('NINEROUTER_IMAGE_DEFAULT_QUALITY', 'medium')).toLowerCase()
  if (!['low', 'medium', 'high', 'standard', 'hd', 'auto'].includes(next)) return 'medium'
  return next
}

export function normalizeOutputFormat(format, targetPath = '') {
  const ext = path.extname(targetPath).replace('.', '').toLowerCase()
  const value = String(format || ext || 'png').toLowerCase()
  if (value === 'jpg') return 'jpeg'
  if (!['png', 'webp', 'jpeg'].includes(value)) return 'png'
  return value
}

export function normalizeBackground(background, format) {
  const value = String(background || env('NINEROUTER_IMAGE_DEFAULT_BACKGROUND', 'auto')).toLowerCase()
  if (!['auto', 'transparent', 'opaque'].includes(value)) return 'auto'
  if (value === 'transparent' && ['jpeg', 'jpg'].includes(String(format || '').toLowerCase())) {
    throw new Error('background=transparent requires an alpha-capable format such as png or webp, not jpeg/jpg')
  }
  return value
}

export function authHeaders(token = env('NINEROUTER_KEY', '')) {
  const headers = { 'content-type': 'application/json' }
  if (token) headers.authorization = `Bearer ${token}`
  return headers
}

function sanitizeError(error) {
  const msg = String(error?.message || error || 'Unknown error')
  const key = env('NINEROUTER_KEY', '')
  const redactedKey = key ? msg.split(key).join('[REDACTED]') : msg
  return redactedKey.replace(/Bearer\s+[A-Za-z0-9._-]+/gi, 'Bearer [REDACTED]')
}

function baseUrl() {
  return env('NINEROUTER_URL', 'https://api.9router.com').replace(/\/$/, '')
}

export async function parseImageResult(result, fetchImpl = fetch) {
  if (result?.b64_json) return { bytes: Buffer.from(result.b64_json, 'base64'), source: 'b64_json' }
  if (result?.url) {
    const response = await fetchImpl(result.url)
    if (!response.ok) throw new Error(`Failed fetch image url: ${response.status}`)
    return { bytes: Buffer.from(await response.arrayBuffer()), source: 'url', url: result.url }
  }
  throw new Error('Unsupported image payload: expected b64_json or url')
}

export async function runBatch(jobs, runOne) {
  const generated = []
  const failed = []
  for (const job of jobs || []) {
    try {
      generated.push(await runOne(job))
    } catch (error) {
      failed.push({ id: job?.id, target_path: job?.target_path, reason: sanitizeError(error) })
    }
  }
  return { status: failed.length ? (generated.length ? 'partial' : 'error') : 'success', generated, failed }
}

function toolText(obj) {
  return [{ type: 'text', text: JSON.stringify(obj, null, 2) }]
}

async function requestJson(endpoint, body, fetchImpl = fetch, token = env('NINEROUTER_KEY', '')) {
  const response = await fetchImpl(`${baseUrl()}${endpoint}`, { method: 'POST', headers: authHeaders(token), body: JSON.stringify(body || {}) })
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

async function requestGet(endpoint, fetchImpl = fetch, token = env('NINEROUTER_KEY', '')) {
  const response = await fetchImpl(`${baseUrl()}${endpoint}`, { method: 'GET', headers: authHeaders(token) })
  if (!response.ok) throw new Error(`HTTP ${response.status}`)
  return response.json()
}

export async function generateImage(input, fetchImpl = fetch) {
  const payload = {
    model: input.model || env('NINEROUTER_IMAGE_MODEL'),
    prompt: input.prompt,
    n: input.n,
    size: input.size || normalizeSize(input.width, input.height),
    quality: input.quality,
    style: input.style,
    response_format: input.response_format,
    output_format: input.output_format,
    background: input.background,
    image: input.image,
    images: input.images,
    providerOptions: input.providerOptions,
  }
  const data = await requestJson('/v1/images/generations', payload, fetchImpl)
  const first = data?.data?.[0] || data?.result || data
  const meta = { model: payload.model, size: payload.size }
  if (first?.url) return { ...meta, source: 'url', url: first.url }
  if (first?.b64_json) return { ...meta, source: 'b64_json', b64_bytes: Buffer.byteLength(first.b64_json, 'base64') }
  return { ...meta, source: 'unknown' }
}

export async function generateImageAsset(input, fetchImpl = fetch) {
  const outputPath = assertInsideRoot(input.project_root, input.target_path)
  await mkdir(path.dirname(outputPath), { recursive: true })

  const format = normalizeOutputFormat(input.output_format || input.format, input.target_path)
  const background = normalizeBackground(input.background, format)
  const quality = normalizeQuality(input.quality)
  const size = normalizeSize(input.width, input.height)
  const model = input.model || env('NINEROUTER_IMAGE_MODEL')
  const maxBytes = Number(env('NINEROUTER_IMAGE_MAX_BYTES', '25000000'))

  const payload = {
    model,
    prompt: input.prompt,
    negative_prompt: input.negative_prompt,
    size,
    output_format: format,
    background,
    quality,
  }

  const res = await fetchImpl(`${baseUrl()}/v1/images/generations`, { method: 'POST', headers: authHeaders(), body: JSON.stringify(payload) })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)

  const contentType = String(res.headers?.get?.('content-type') || '')
  let bytes
  let source = 'binary'
  let sourceUrl = null

  if (contentType.startsWith('image/')) {
    bytes = Buffer.from(await res.arrayBuffer())
  } else {
    const data = await res.json()
    const first = data?.data?.[0] || data?.result || data
    const parsed = await parseImageResult(first, fetchImpl)
    bytes = parsed.bytes
    source = parsed.source
    sourceUrl = parsed.url || null
  }

  if (Number.isFinite(maxBytes) && maxBytes > 0 && bytes.length > maxBytes) {
    throw new Error(`Image exceeds NINEROUTER_IMAGE_MAX_BYTES: ${bytes.length} > ${maxBytes}`)
  }

  await writeFile(outputPath, bytes)
  const warning = background === 'transparent' && format === 'png' && source === 'binary' ? 'Provider may return opaque PNG for transparent request.' : null

  return {
    id: input.id,
    path: input.target_path,
    absolute_path: outputPath,
    format: path.extname(input.target_path).replace('.', '') || input.format || 'png',
    output_format: format,
    background,
    quality,
    alt: input.alt || '',
    model,
    prompt_used: input.prompt,
    legal_note: input.legal_note || 'Generated legal style-equivalent asset; no reference asset copied.',
    bytes: bytes.length,
    source,
    source_url: sourceUrl,
    warning,
  }
}

function modelEndpoint(kind) {
  if (kind === 'image') return '/v1/models/image'
  if (kind === 'web') return '/v1/models/web'
  if (kind === 'tts') return '/v1/models/tts'
  if (kind === 'embedding') return '/v1/models/embedding'
  if (kind === 'stt') return '/v1/models/stt'
  if (kind === 'image-to-text') return '/v1/models/image-to-text'
  return '/v1/models'
}

export function createServer(deps = {}) {
  const runGenerateImageAsset = deps.generateImageAsset || generateImageAsset
  const runGenerateImage = deps.generateImage || generateImage
  const runBatchImpl = deps.runBatch || runBatch
  const requestJsonImpl = deps.requestJson || requestJson
  const requestGetImpl = deps.requestGet || requestGet

  const server = new Server({ name: '9router-mcp', version: '0.1.0' }, { capabilities: { tools: {} } })

  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: [
      { name: 'health_check_9router', description: 'Check 9Router endpoint health.', inputSchema: { type: 'object', properties: {} } },
      { name: 'list_9router_models', description: 'List 9Router models.', inputSchema: { type: 'object', additionalProperties: false, properties: { kind: { type: 'string', enum: ['chat', 'image', 'tts', 'embedding', 'web', 'stt', 'image-to-text'], default: 'chat' } } } },
      { name: 'get_9router_model_info', description: 'Get 9Router model info.', inputSchema: { type: 'object', additionalProperties: false, required: ['id'], properties: { id: { type: 'string' } } } },
      { name: 'web_search', description: 'Web search via 9Router.', inputSchema: { type: 'object', additionalProperties: false, required: ['query'], properties: { query: { type: 'string' }, model: { type: 'string' }, max_results: { type: 'number', default: 5 }, search_type: { type: 'string', enum: ['web', 'news'], default: 'web' }, country: { type: 'string' }, language: { type: 'string' }, time_range: { type: 'string' }, domain_filter: { type: 'array', items: { type: 'string' } }, providerOptions: { type: 'object' } } } },
      { name: 'web_fetch', description: 'Fetch URL via 9Router.', inputSchema: { type: 'object', additionalProperties: false, required: ['url'], properties: { url: { type: 'string' }, model: { type: 'string' }, format: { type: 'string', enum: ['markdown', 'text', 'html'], default: 'markdown' }, max_characters: { type: 'number', default: 5000 } } } },
      { name: 'generate_image', description: 'Generate image via 9Router.', inputSchema: { type: 'object', additionalProperties: false, required: ['prompt'], properties: { prompt: { type: 'string' }, model: { type: 'string' }, n: { type: 'number', default: 1 }, size: { type: 'string', default: '1024x1024' }, quality: { type: 'string' }, style: { type: 'string' }, response_format: { type: 'string', enum: ['url', 'b64_json'], default: 'url' }, output_format: { type: 'string', enum: ['png', 'webp', 'jpeg', 'jpg'] }, background: { type: 'string', enum: ['auto', 'transparent', 'opaque'] }, image: { type: 'string' }, images: { type: 'array', items: { type: 'string' } }, providerOptions: { type: 'object' } } } },
      { name: 'generate_image_asset', description: 'Generate one legal style-equivalent image asset from prompt and save under project_root.', inputSchema: { type: 'object', additionalProperties: false, required: ['project_root', 'target_path', 'prompt'], properties: { project_root: { type: 'string' }, target_path: { type: 'string' }, prompt: { type: 'string', minLength: 1 }, negative_prompt: { type: 'string' }, width: { type: 'number' }, height: { type: 'number' }, format: { type: 'string', enum: ['png', 'webp', 'jpeg', 'jpg'] }, output_format: { type: 'string', enum: ['png', 'webp', 'jpeg', 'jpg'] }, background: { type: 'string', enum: ['auto', 'transparent', 'opaque'] }, quality: { type: 'string', enum: ['low', 'medium', 'high', 'standard', 'hd', 'auto'] }, alt: { type: 'string' }, legal_note: { type: 'string' } } } },
      { name: 'generate_image_assets_batch', description: 'Generate multiple image assets from prepared jobs.', inputSchema: { type: 'object', additionalProperties: false, required: ['jobs'], properties: { jobs: { type: 'array', minItems: 1, items: { type: 'object', required: ['project_root', 'target_path', 'prompt'], properties: { id: { type: 'string' }, project_root: { type: 'string' }, target_path: { type: 'string' }, prompt: { type: 'string' }, negative_prompt: { type: 'string' }, width: { type: 'number' }, height: { type: 'number' }, format: { type: 'string' }, output_format: { type: 'string' }, background: { type: 'string' }, quality: { type: 'string' }, alt: { type: 'string' }, legal_note: { type: 'string' } } } } } } },
    ],
  }))

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args = {} } = request.params
    try {
      if (name === 'health_check_9router') return { content: toolText(await requestGetImpl('/api/health')) }
      if (name === 'list_9router_models') return { content: toolText(await requestGetImpl(modelEndpoint(args.kind === 'chat' ? undefined : args.kind))) }
      if (name === 'get_9router_model_info') return { content: toolText(await requestGetImpl(`/v1/models/info?id=${encodeURIComponent(args.id)}`)) }
      if (name === 'web_search') return { content: toolText(await requestJsonImpl('/v1/search', { query: args.query, model: args.model || env('NINEROUTER_SEARCH_MODEL', 'search-combo'), max_results: args.max_results, search_type: args.search_type, country: args.country, language: args.language, time_range: args.time_range, domain_filter: args.domain_filter, providerOptions: args.providerOptions })) }
      if (name === 'web_fetch') return { content: toolText(await requestJsonImpl('/v1/web/fetch', { url: args.url, model: args.model || env('NINEROUTER_FETCH_MODEL', 'fetch-combo'), format: args.format, max_characters: args.max_characters })) }
      if (name === 'generate_image') return { content: toolText({ status: 'success', generated: await runGenerateImage(args) }) }
      if (name === 'generate_image_asset') return { content: toolText({ status: 'success', generated: await runGenerateImageAsset(args) }) }
      if (name === 'generate_image_assets_batch') return { content: toolText(await runBatchImpl(args.jobs || [], runGenerateImageAsset)) }
      throw new Error(`Unknown tool: ${name}`)
    } catch (error) {
      return { isError: true, content: toolText({ status: 'error', reason: sanitizeError(error) }) }
    }
  })

  return server
}

export async function startServer() {
  const server = createServer()
  const transport = new StdioServerTransport()
  await server.connect(transport)
}

if (import.meta.url === `file://${process.argv[1]}`) {
  await startServer()
}
