#!/usr/bin/env node

import assert from 'node:assert/strict'
import { rm, readFile } from 'node:fs/promises'
import path from 'node:path'
import {
  assertInsideRoot,
  normalizeSize,
  normalizeQuality,
  normalizeOutputFormat,
  normalizeBackground,
  authHeaders,
  parseImageResult,
  runBatch,
  generateImageAsset,
  parsePngInfo,
} from '../../bin/9router-mcp.mjs'

const root = path.resolve(import.meta.dirname, '..', '..')
const testTmpDir = path.resolve(root, 'scripts/tests/fixtures/9router-tmp')

process.env.NINEROUTER_IMAGE_DEFAULT_SIZE = '1024x1024'
process.env.NINEROUTER_IMAGE_DEFAULT_QUALITY = 'medium'
process.env.NINEROUTER_IMAGE_DEFAULT_BACKGROUND = 'auto'
process.env.NINEROUTER_IMAGE_MAX_BYTES = '1024'

assert.throws(() => assertInsideRoot(root, '../etc/passwd'), /target_path must stay inside project_root/)
assert.throws(() => assertInsideRoot(root, '/etc/passwd'), /target_path must stay inside project_root/)
assert.equal(assertInsideRoot(root, 'scripts/tests/9router-mcp.test.mjs'), path.resolve(root, 'scripts/tests/9router-mcp.test.mjs'))

assert.equal(normalizeSize(512, 512), '512x512')
assert.equal(normalizeSize('512.4', '512.8'), '512x513')
assert.equal(normalizeSize(null, undefined), '1024x1024')

assert.equal(normalizeQuality('bad'), 'medium')
assert.equal(normalizeOutputFormat('jpg', ''), 'jpeg')
assert.equal(normalizeBackground('auto', 'png'), 'auto')
assert.throws(() => normalizeBackground('transparent', 'jpeg'), /alpha-capable format/)

const headers = authHeaders('my-key-123')
assert.equal(headers.authorization, 'Bearer my-key-123')
assert.equal(headers['content-type'], 'application/json')

const sampleBase64 = 'SGVsbG8gV29ybGQ='
const expectedBuf = Buffer.from('Hello World')
const pngAlpha1x1 = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC', 'base64')
const pngOpaque1x1 = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAC0lEQVR4nGNgQAAAAAMAASsJTYQAAAAASUVORK5CYII=', 'base64')

const parsedB64 = await parseImageResult({ b64_json: sampleBase64 })
assert.deepEqual(parsedB64.bytes, expectedBuf)
assert.equal(parsedB64.source, 'b64_json')

const mockFetchUrl = async (url) => {
  assert.equal(url, 'https://mock.com/img.png')
  return {
    ok: true,
    arrayBuffer: async () => expectedBuf.buffer.slice(expectedBuf.byteOffset, expectedBuf.byteOffset + expectedBuf.byteLength),
  }
}
const parsedUrl = await parseImageResult({ url: 'https://mock.com/img.png' }, mockFetchUrl)
assert.deepEqual(parsedUrl.bytes, expectedBuf)
assert.equal(parsedUrl.source, 'url')

const mockFetchFail = async () => ({ ok: false, status: 500 })
await assert.rejects(() => parseImageResult({ url: 'https://mock.com/img.png' }, mockFetchFail), /Failed fetch image url: 500/)

assert.equal(parsePngInfo(pngAlpha1x1)?.has_alpha, true)
assert.equal(parsePngInfo(pngOpaque1x1)?.has_alpha, false)
assert.equal(parsePngInfo(expectedBuf), null)

const jobs = [{ id: '1', target_path: 'a.png' }, { id: '2', target_path: 'b.png' }]
const batchRes = await runBatch(jobs, async (job) => {
  if (job.id === '2') throw new Error('Failed to generate b')
  return { id: job.id, path: job.target_path }
})
assert.equal(batchRes.status, 'partial')
assert.equal(batchRes.generated.length, 1)
assert.equal(batchRes.failed.length, 1)

const targetRel = 'scripts/tests/fixtures/9router-tmp/test-out.png'
const targetAbs = path.resolve(root, targetRel)

const mockFetchGenerate = async (url, options) => {
  assert.equal(url, 'https://api.9router.com/v1/images/generations')
  assert.equal(options.method, 'POST')
  return {
    ok: true,
    headers: { get: () => 'application/json' },
    json: async () => ({ data: [{ b64_json: sampleBase64 }] }),
  }
}

let transparentCalls = 0
const mockFetchGenerateTransparentFallback = async (url, options) => {
  assert.equal(url, 'https://api.9router.com/v1/images/generations')
  transparentCalls += 1
  const body = JSON.parse(options.body)
  if (transparentCalls === 1) {
    assert.equal(body.background, 'transparent')
    return {
      ok: false,
      status: 400,
      text: async () => 'transparent background is not supported',
    }
  }
  assert.equal(body.background, 'opaque')
  return {
    ok: true,
    headers: { get: () => 'application/json' },
    json: async () => ({ data: [{ b64_json: pngOpaque1x1.toString('base64') }] }),
  }
}

try {
  const result = await generateImageAsset({
    project_root: root,
    target_path: targetRel,
    prompt: 'Test prompt',
    width: 256,
    height: 256,
  }, mockFetchGenerate)

  assert.equal(result.absolute_path, targetAbs)
  assert.equal(result.bytes, expectedBuf.length)
  assert.equal(result.background, 'auto')
  assert.equal(result.quality, 'medium')
  const saved = await readFile(targetAbs)
  assert.deepEqual(saved, expectedBuf)

  const transparentResult = await generateImageAsset({
    project_root: root,
    target_path: targetRel,
    prompt: 'Test transparent',
    width: 1,
    height: 1,
    output_format: 'png',
    background: 'transparent',
  }, mockFetchGenerateTransparentFallback)

  assert.equal(transparentCalls, 2)
  assert.equal(transparentResult.background, 'transparent')
  assert.equal(transparentResult.transparency_verified, true)
  assert.match(String(transparentResult.transparency_warning), /retried opaque/)
  assert.match(String(transparentResult.transparency_warning), /repaired opaque PNG via sharp/)
  assert.equal(transparentResult.png_info?.has_alpha, true)

  const repairedSaved = await readFile(targetAbs)
  assert.equal(parsePngInfo(repairedSaved)?.has_alpha, true)
} finally {
  await rm(testTmpDir, { recursive: true, force: true })
}

console.log('OK 9router-mcp tests passed')
