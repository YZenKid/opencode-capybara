#!/usr/bin/env node
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import path from 'node:path'
import process from 'node:process'
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js'
import OpenAI from 'openai'

const server = new Server(
  {
    name: 'image-asset-generator',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  },
)

function env(name, fallback = undefined) {
  const value = process.env[name]
  return value == null || value === '' ? fallback : value
}

function errorText(error) {
  const parts = [
    error?.message,
    error?.error?.message,
    error?.response?.data?.error?.message,
    error?.response?.data?.message,
    typeof error === 'string' ? error : undefined,
  ].filter(Boolean)
  try {
    parts.push(JSON.stringify(error))
  } catch {}
  return parts.join('\n')
}

function isTransparentUnsupportedError(error) {
  return /transparent background is not supported|background.*transparent.*not supported|unsupported.*transparent|transparent.*unsupported/i.test(errorText(error))
}

function assertInsideRoot(projectRoot, targetPath) {
  const root = path.resolve(projectRoot)
  const out = path.resolve(root, targetPath)
  const relative = path.relative(root, out)
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    throw new Error(`target_path must stay inside project_root: ${targetPath}`)
  }
  return out
}

function normalizeSize(width, height) {
  const w = Number(width)
  const h = Number(height)
  if (!Number.isFinite(w) || !Number.isFinite(h) || w <= 0 || h <= 0) {
    return env('IMAGE_ASSET_DEFAULT_SIZE', '1024x1024')
  }
  return `${Math.round(w)}x${Math.round(h)}`
}

function normalizeModel() {
  return env('IMAGE_ASSET_MODEL', 'cx/gpt-5.5-image')
}

function normalizeQuality(value) {
  const next = (value || env('IMAGE_ASSET_QUALITY', 'medium')).toLowerCase()
  if (!['low', 'medium', 'high', 'auto'].includes(next)) return 'medium'
  return next
}

function normalizeBackground(background, format) {
  const value = background || env('IMAGE_ASSET_DEFAULT_BACKGROUND', 'auto')
  if (!['auto', 'transparent', 'opaque'].includes(value)) return 'auto'
  const requestedFormat = (format || '').toLowerCase()
  if (value === 'transparent' && ['jpg', 'jpeg'].includes(requestedFormat)) {
    throw new Error('background=transparent requires an alpha-capable format such as png or webp, not jpeg/jpg')
  }
  return value
}

function normalizeOutputFormat(format, targetPath) {
  const ext = path.extname(targetPath || '').replace('.', '').toLowerCase()
  const value = (format || ext || 'png').toLowerCase()
  if (value === 'jpg') return 'jpeg'
  if (!['png', 'webp', 'jpeg'].includes(value)) return 'png'
  return value
}

function pngHasAlpha(bytes) {
  return bytes.length > 25 && bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])) && [4, 6].includes(bytes[25])
}

function parsePngInfo(bytes) {
  if (!bytes.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]))) return null
  return { color_type: bytes[25], has_alpha: [4, 6].includes(bytes[25]) }
}

async function ensureTransparentPng(outputPath, bytes, background) {
  if (background !== 'transparent') return { bytes, transparency_verified: null, transparency_warning: null }
  if (pngHasAlpha(bytes)) return { bytes, transparency_verified: true, transparency_warning: null }

  const warning = 'Image endpoint accepted background=transparent but returned a PNG without alpha channel. Install `sharp` for automatic white-background removal fallback, or use a provider/model that returns alpha.'
  try {
    const sharp = (await import('sharp')).default
    const fallback = await sharp(bytes).ensureAlpha().raw().toBuffer({ resolveWithObject: true })
    const data = fallback.data
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i]
      const g = data[i + 1]
      const b = data[i + 2]
      const whiteness = Math.min(r, g, b)
      const spread = Math.max(r, g, b) - whiteness
      if (whiteness > 235 && spread < 24) data[i + 3] = 0
    }
    const out = await sharp(data, { raw: fallback.info }).png({ colorType: 6 }).toBuffer()
    await writeFile(outputPath, out)
    return { bytes: out, transparency_verified: pngHasAlpha(out), transparency_warning: 'Endpoint returned opaque PNG; applied near-white background removal fallback with sharp.' }
  } catch {
    return { bytes, transparency_verified: false, transparency_warning: warning }
  }
}

async function makeWhiteBackgroundTransparent(inputPath, outputPath = inputPath) {
  const sharp = (await import('sharp')).default
  const original = await sharp(inputPath).ensureAlpha().raw().toBuffer({ resolveWithObject: true })
  const { data, info } = original
  const width = info.width
  const height = info.height
  const visited = new Uint8Array(width * height)
  const queue = []
  const pushIfBackground = (x, y) => {
    if (x < 0 || y < 0 || x >= width || y >= height) return
    const idx = y * width + x
    if (visited[idx]) return
    const offset = idx * 4
    const r = data[offset]
    const g = data[offset + 1]
    const b = data[offset + 2]
    const min = Math.min(r, g, b)
    const max = Math.max(r, g, b)
    const isBg = min > 220 && max - min < 38
    if (!isBg) return
    visited[idx] = 1
    queue.push(idx)
  }

  for (let x = 0; x < width; x += 1) {
    pushIfBackground(x, 0)
    pushIfBackground(x, height - 1)
  }
  for (let y = 0; y < height; y += 1) {
    pushIfBackground(0, y)
    pushIfBackground(width - 1, y)
  }

  for (let cursor = 0; cursor < queue.length; cursor += 1) {
    const idx = queue[cursor]
    const x = idx % width
    const y = Math.floor(idx / width)
    const offset = idx * 4
    data[offset + 3] = 0
    pushIfBackground(x + 1, y)
    pushIfBackground(x - 1, y)
    pushIfBackground(x, y + 1)
    pushIfBackground(x, y - 1)
  }

  // Feather near-background pixels adjacent to removed edge for less jagged cutouts.
  const alpha = new Uint8Array(width * height)
  for (let i = 0; i < width * height; i += 1) alpha[i] = data[i * 4 + 3]
  for (let y = 1; y < height - 1; y += 1) {
    for (let x = 1; x < width - 1; x += 1) {
      const idx = y * width + x
      if (alpha[idx] === 0) continue
      const touchesTransparent = alpha[idx - 1] === 0 || alpha[idx + 1] === 0 || alpha[idx - width] === 0 || alpha[idx + width] === 0
      if (!touchesTransparent) continue
      const offset = idx * 4
      const r = data[offset]
      const g = data[offset + 1]
      const b = data[offset + 2]
      const min = Math.min(r, g, b)
      if (min > 225) data[offset + 3] = Math.min(data[offset + 3], 80)
    }
  }

  const out = await sharp(data, { raw: info }).png({ colorType: 6 }).toBuffer()
  await writeFile(outputPath, out)
  return { bytes: out, removed_pixels: queue.length, png_info: parsePngInfo(out) }
}

function buildClient() {
  const apiKey = env('IMAGE_ASSET_API_KEY', env('CLIPROXYAPI_API_KEY'))
  const baseURL = env('IMAGE_ASSET_BASE_URL', env('CLIPROXYAPI_BASE_URL'))
  if (!apiKey) throw new Error('Missing IMAGE_ASSET_API_KEY or CLIPROXYAPI_API_KEY')
  return new OpenAI({ apiKey, baseURL })
}

function toolText(obj) {
  return [{ type: 'text', text: JSON.stringify(obj, null, 2) }]
}

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'generate_image_asset',
      description:
        'Generate one legal style-equivalent image asset from a prompt and save it under project_root. Uses the configured image endpoint/model via IMAGE_ASSET_* or CLIPROXYAPI_* environment variables.',
      inputSchema: {
        type: 'object',
        additionalProperties: false,
        required: ['project_root', 'target_path', 'prompt'],
        properties: {
          project_root: { type: 'string', description: 'Absolute project root directory.' },
          target_path: {
            type: 'string',
            description: 'Output path relative to project_root, e.g. public/assets/generated/hero.png.',
          },
          prompt: { type: 'string', minLength: 1 },
          negative_prompt: { type: 'string' },
          width: { type: 'number', description: 'Requested output width in pixels.' },
          height: { type: 'number', description: 'Requested output height in pixels.' },
          format: {
            type: 'string',
            enum: ['png', 'webp', 'jpeg', 'jpg'],
            description: 'Preferred output extension. The endpoint may return PNG bytes regardless; file extension follows target_path.',
          },
          output_format: {
            type: 'string',
            enum: ['png', 'webp', 'jpeg', 'jpg'],
            description: 'Preferred image endpoint output format. Defaults to format or target_path extension.',
          },
          background: {
            type: 'string',
            enum: ['auto', 'transparent', 'opaque'],
            description: 'Use transparent for PNG/WebP assets that need alpha channel, such as cutouts, icons, badges, and overlays.',
          },
          quality: {
            type: 'string',
            enum: ['low', 'medium', 'high', 'auto'],
            description: 'Image generation quality preset for the configured image model.',
          },
          alt: { type: 'string' },
          legal_note: { type: 'string' },
        },
      },
    },
    {
      name: 'generate_image_assets_batch',
      description:
        'Generate multiple image assets from prepared jobs. Each job uses the same contract as generate_image_asset. Stops only failed jobs and returns per-asset metadata.',
      inputSchema: {
        type: 'object',
        additionalProperties: false,
        required: ['jobs'],
        properties: {
          jobs: {
            type: 'array',
            minItems: 1,
            items: {
              type: 'object',
              required: ['project_root', 'target_path', 'prompt'],
              properties: {
                id: { type: 'string' },
                project_root: { type: 'string' },
                target_path: { type: 'string' },
                prompt: { type: 'string' },
                negative_prompt: { type: 'string' },
                width: { type: 'number' },
                height: { type: 'number' },
                format: { type: 'string' },
                output_format: { type: 'string' },
                background: { type: 'string' },
                quality: { type: 'string' },
                alt: { type: 'string' },
                legal_note: { type: 'string' },
              },
            },
          },
        },
      },
    },
  ],
}))

async function generateOne(input) {
  const client = buildClient()
  const projectRoot = input.project_root
  const targetPath = input.target_path
  const outputPath = assertInsideRoot(projectRoot, targetPath)
  const prompt = [input.prompt, input.negative_prompt ? `Negative prompt: ${input.negative_prompt}` : '']
    .filter(Boolean)
    .join('\n\n')
  const size = normalizeSize(input.width, input.height)
  const model = normalizeModel()
  const outputFormat = normalizeOutputFormat(input.output_format || input.format, targetPath)
  const background = normalizeBackground(input.background, outputFormat)
  const quality = normalizeQuality(input.quality)

  const request = { model, prompt, size, n: 1 }
  if (background !== 'auto') request.background = background
  if (outputFormat && outputFormat !== 'png') request.output_format = outputFormat
  if (quality !== 'auto') request.quality = quality

  let response
  let transparentFallbackMode = null
  try {
    response = await client.images.generate(request)
  } catch (error) {
    if (background === 'transparent' && isTransparentUnsupportedError(error)) {
      transparentFallbackMode = 'endpoint_rejected_transparent_background; retried opaque then applied CV background removal'
      delete request.background
      response = await client.images.generate(request)
    } else {
      throw error
    }
  }
  const first = response.data?.[0]
  if (!first?.b64_json) {
    throw new Error('Image endpoint did not return b64_json. Configure endpoint/model to return base64 image data.')
  }
  await mkdir(path.dirname(outputPath), { recursive: true })
  const initialBytes = Buffer.from(first.b64_json, 'base64')
  await writeFile(outputPath, initialBytes)
  let transparentResult = await ensureTransparentPng(outputPath, initialBytes, background)
  if (background === 'transparent' && transparentFallbackMode) {
    const cvResult = await makeWhiteBackgroundTransparent(outputPath)
    transparentResult = {
      bytes: cvResult.bytes,
      transparency_verified: cvResult.png_info?.has_alpha || false,
      transparency_warning: `${transparentFallbackMode}; removed ${cvResult.removed_pixels} edge-connected near-white pixels.`,
    }
  }
  const bytes = transparentResult.bytes
  return {
    id: input.id,
    path: targetPath,
    absolute_path: outputPath,
    width: Number(input.width) || null,
    height: Number(input.height) || null,
    format: path.extname(targetPath).replace('.', '') || input.format || outputFormat || 'png',
    output_format: outputFormat,
    background,
    quality,
    transparency_verified: transparentResult.transparency_verified,
    transparency_warning: transparentResult.transparency_warning,
    png_info: parsePngInfo(bytes),
    alt: input.alt || '',
    model,
    prompt_used: prompt,
    legal_note: input.legal_note || 'Generated legal style-equivalent asset; no reference asset copied.',
    bytes: bytes.length,
  }
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params
  try {
    if (name === 'generate_image_asset') {
      const generated = await generateOne(args)
      return { content: toolText({ status: 'success', generated }) }
    }
    if (name === 'generate_image_assets_batch') {
      const generated = []
      const failed = []
      for (const job of args.jobs || []) {
        try {
          generated.push(await generateOne(job))
        } catch (error) {
          failed.push({ id: job.id, target_path: job.target_path, reason: error.message })
        }
      }
      return {
        content: toolText({
          status: failed.length ? (generated.length ? 'partial' : 'error') : 'success',
          generated,
          failed,
        }),
      }
    }
    throw new Error(`Unknown tool: ${name}`)
  } catch (error) {
    return {
      isError: true,
      content: toolText({ status: 'error', reason: error.message }),
    }
  }
})

const transport = new StdioServerTransport()
await server.connect(transport)
