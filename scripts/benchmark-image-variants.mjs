#!/usr/bin/env node

import { mkdir, writeFile } from 'node:fs/promises'
import path from 'node:path'
import process from 'node:process'
import OpenAI from 'openai'

function env(name, fallback = undefined) {
  const value = process.env[name]
  return value == null || value === '' ? fallback : value
}

const root = path.resolve(import.meta.dirname, '..')
const outDir = path.join(root, 'assets', 'benchmarks')

const defaultPrompt = 'A polished website-ready hero illustration of a lucky maneki-neko cat, friendly and premium, front-facing with one paw raised, clean composition, charming expression, red collar with gold bell, subtle Japanese-inspired decorative accents, soft warm lighting, crisp edges, modern illustrative style suitable for a developer tools website, high visual appeal, no text, isolated subject with gentle scene presence on a clean background.'
const defaultNegativePrompt = 'blurry, distorted anatomy, extra limbs, text, watermark, logo, low detail, creepy face, cluttered background, photorealistic noise, oversaturated, generic stock look'

function parseArgs(argv) {
  const flags = {
    prompt: defaultPrompt,
    negativePrompt: defaultNegativePrompt,
    prefix: 'maneki-neko',
  }

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index]
    if (arg === '--prompt') {
      index += 1
      if (!argv[index]) throw new Error('Missing value for --prompt')
      flags.prompt = argv[index]
      continue
    }
    if (arg === '--negative-prompt') {
      index += 1
      if (!argv[index]) throw new Error('Missing value for --negative-prompt')
      flags.negativePrompt = argv[index]
      continue
    }
    if (arg === '--prefix') {
      index += 1
      if (!argv[index]) throw new Error('Missing value for --prefix')
      flags.prefix = argv[index]
      continue
    }
    throw new Error(`Unknown flag: ${arg}`)
  }

  return flags
}

function buildClient() {
  const apiKey = env('CLIPROXYAPI_API_KEY')
  const baseURL = env('CLIPROXYAPI_BASE_URL')
  if (!apiKey || !baseURL) {
    throw new Error('Missing CLIPROXYAPI_API_KEY or CLIPROXYAPI_BASE_URL')
  }
  return new OpenAI({ apiKey, baseURL })
}

async function generateVariant(client, quality, options) {
  const startedAt = Date.now()
  const response = await client.images.generate({
    model: env('IMAGE_ASSET_MODEL', 'cx/gpt-5.5-image'),
    prompt: `${options.prompt}\n\nNegative prompt: ${options.negativePrompt}`,
    size: '1536x896',
    n: 1,
    quality,
  })
  const elapsedMs = Date.now() - startedAt
  const first = response.data?.[0]
  if (!first?.b64_json) {
    throw new Error(`Image endpoint did not return b64_json for quality=${quality}`)
  }
  const bytes = Buffer.from(first.b64_json, 'base64')
  const targetPath = path.join(outDir, `${options.prefix}-${quality}.png`)
  await writeFile(targetPath, bytes)
  return {
    quality,
    elapsedMs,
    output: targetPath,
    bytes: bytes.length,
    prompt: options.prompt,
    negativePrompt: options.negativePrompt,
  }
}

async function main() {
  const options = parseArgs(process.argv.slice(2))
  await mkdir(outDir, { recursive: true })
  const client = buildClient()
  const results = []
  for (const quality of ['low', 'medium', 'high']) {
    results.push(await generateVariant(client, quality, options))
  }
  process.stdout.write(`${JSON.stringify({ status: 'success', results }, null, 2)}\n`)
}

main().catch((error) => {
  process.stderr.write(`${error?.stack || error?.message || String(error)}\n`)
  process.exit(1)
})
