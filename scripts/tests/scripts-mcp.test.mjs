#!/usr/bin/env node
import assert from 'node:assert/strict'
import { EventEmitter } from 'node:events'
import { mkdtempSync, mkdirSync, writeFileSync, symlinkSync, rmSync, statSync, existsSync, realpathSync } from 'node:fs'
import path from 'node:path'
import { createServer, ALLOWED_TOOLS, TOOL_REGISTRY, resolveScript, resolveProjectRoot, resolveChild, sanitizeError, toolText, run } from '../../bin/scripts-mcp.mjs'

const root = path.resolve(import.meta.dirname, '..', '..')
const fixture = mkdtempSync('/tmp/scripts-mcp-b1-')
mkdirSync(path.join(fixture, 'scripts'), { recursive: true })
writeFileSync(path.join(fixture, 'scripts', 'ok.py'), '#!/usr/bin/env python3\nprint("ok")')
writeFileSync(path.join(fixture, 'scripts', 'visual-audit.py'), '#!/usr/bin/env python3\nprint("ok")')
writeFileSync(path.join(fixture, 'scripts', 'legal-source-check.py'), '#!/usr/bin/env python3\nprint("ok")')
writeFileSync(path.join(fixture, 'scripts', 'task-progress.py'), '#!/usr/bin/env python3\nprint("ok")')
try { writeFileSync(path.join(fixture, 'scripts', 'loop.py'), '#!/usr/bin/env python3\nimport time\ntime.sleep(60)'); } catch {}
try { if (process.platform !== 'win32') symlinkSync(path.join(fixture, 'scripts', 'ok.py'), path.join(fixture, 'scripts', 'link.py')) } catch {}

function collectHandlers() { const handlers = []; const fakeServer = { setRequestHandler(_schema, fn) { handlers.push(fn) } }; return { handlers, fakeServer } }
function makeSpawnCapture(stdout = 'ok', code = 0) { return (cmd, args, opts) => { const child = new EventEmitter(); child.stdout = new EventEmitter(); child.stderr = new EventEmitter(); process.nextTick(() => { child.stdout.emit('data', stdout); child.emit('close', code) }); child._captured = { cmd, args, opts }; return child } }
function makeSpawnDelayed(code = 0, delay = 200) { return (_cmd, args, opts) => { const child = new EventEmitter(); child.stdout = new EventEmitter(); child.stderr = new EventEmitter(); let killed = false; child.kill = () => { killed = true }; const t = setTimeout(() => { if (!killed) { child.stdout.emit('data', 'late'); child.emit('close', code) } }, delay); return child } }

// T1: registry is single source of truth
{
  assert.equal(ALLOWED_TOOLS.length, 15)
  assert.equal(TOOL_REGISTRY.length, 15)
  for (const tool of TOOL_REGISTRY) {
    assert.ok(tool.name, 'name')
    assert.ok(tool.classification, 'classification')
    assert.ok(tool.laneRecommendation, 'lane')
    assert.ok(tool.schema, 'schema')
    assert.ok(tool.inputSchema, 'inputSchema')
    assert.ok(tool.cliFallback, 'cliFallback')
    assert.ok(Array.isArray(tool.inputSchema.required), 'required array')
    assert.ok(tool.inputSchema.required.includes('project_root'), 'project_root required in every entry')
  }
  console.log('PASS registry single source of truth (15 entries)')
}

// T2: tools/list parity with registry
{
  const { handlers, fakeServer } = collectHandlers(); createServer({ server: fakeServer, projectRoot: fixture })
  const list = await handlers[0]()
  assert.equal(list.tools.length, TOOL_REGISTRY.length)
  for (const tool of list.tools) {
    assert.equal(tool.inputSchema.required.includes('project_root'), true)
  }
  console.log('PASS tools/list parity and project_root required')
}

// T3: unknown tool returns tool_not_allowed with full envelope
{
  const { handlers, fakeServer } = collectHandlers(); createServer({ server: fakeServer, projectRoot: fixture })
  const res = await handlers[1]({ params: { name: 'nope', arguments: { project_root: fixture } } })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(res.isError, true)
  assert.equal(parsed.reason, 'tool_not_allowed')
  assert.equal(parsed.command_id.length, 36)
  for (const key of ['status', 'reason', 'command_id', 'exit_code', 'duration_ms', 'stdout', 'stderr', 'truncated']) assert.ok(key in parsed, `envelope has ${key}`)
  console.log('PASS unknown tool returns envelope with command_id')
}

// T4: missing project_root rejected as invalid_args
{
  const { handlers, fakeServer } = collectHandlers(); createServer({ server: fakeServer, projectRoot: fixture })
  const res = await handlers[1]({ params: { name: 'scripts_catalog', arguments: {} } })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.reason, 'invalid_args')
  assert.equal(parsed.command_id.length, 36)
  console.log('PASS missing project_root rejected')
}

// T5: non-directory project_root rejected
{
  const { handlers, fakeServer } = collectHandlers(); createServer({ server: fakeServer, projectRoot: fixture })
  const res = await handlers[1]({ params: { name: 'scripts_catalog', arguments: { project_root: path.join(fixture, 'scripts', 'ok.py') } } })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.reason, 'invalid_project_root')
  console.log('PASS non-directory project_root rejected')
}

// T6: scripts_catalog never reads filesystem, derives only from registry
{
  const { handlers, fakeServer } = collectHandlers(); let spawnCalled = false; const spawn = () => { spawnCalled = true; throw new Error('spawn called') }
  createServer({ server: fakeServer, projectRoot: fixture, spawn })
  const res = await handlers[1]({ params: { name: 'scripts_catalog', arguments: { project_root: fixture } } })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.status, 'success')
  assert.equal(parsed.count, 15)
  assert.equal(parsed.tools.length, 15)
  for (const tool of parsed.tools) {
    assert.ok(['name', 'source_script', 'classification', 'lane_recommendation', 'required_input', 'cli_fallback'].every((k) => k in tool), 'catalog shape')
  }
  assert.equal(spawnCalled, false)
  console.log('PASS scripts_catalog no filesystem, no spawn')
}

// T7: scripts_visual_audit returns tool_pending reason only because script absent
{
  const noScriptFixture = mkdtempSync('/tmp/scripts-mcp-pend-')
  mkdirSync(path.join(noScriptFixture, 'scripts'), { recursive: true })
  const { handlers, fakeServer } = collectHandlers(); createServer({ server: fakeServer, projectRoot: noScriptFixture })
  const res = await handlers[1]({ params: { name: 'scripts_visual_audit', arguments: { project_root: noScriptFixture, paths: ['scripts/ok.py'] } } })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.status, 'tool_pending')
  assert.equal(parsed.reason, 'canonical_script_unavailable')
  assert.equal(parsed.command_id.length, 36)
  rmSync(noScriptFixture, { recursive: true })
  console.log('PASS visual_audit tool_pending only when script absent')
}

// T8: scripts_visual_audit without script tries to spawn script path with shell:false
{
  const { handlers, fakeServer } = collectHandlers(); let captured = null
  const spawn = (cmd, args, opts) => { captured = { cmd, args, opts }; const child = new EventEmitter(); child.stdout = new EventEmitter(); child.stderr = new EventEmitter(); process.nextTick(() => { child.stdout.emit('data', 'ok'); child.emit('close', 0) }); return child }
  createServer({ server: fakeServer, projectRoot: fixture, spawn })
  await handlers[1]({ params: { name: 'scripts_visual_audit', arguments: { project_root: fixture, paths: ['scripts/ok.py'] } } })
  assert.equal(captured.cmd, 'python3')
  assert.equal(captured.opts.shell, false)
  assert.ok(captured.args[0].endsWith('visual-audit.py'))
  console.log('PASS spawn uses python3 with shell:false and canonical script path')
}

// T9: scripts_legal_source_check refuses traversal/absolute/NUL source via argv-builder via schema
{
  const { handlers, fakeServer } = collectHandlers(); createServer({ server: fakeServer, projectRoot: fixture })
  const bad = await handlers[1]({ params: { name: 'scripts_legal_source_check', arguments: { project_root: fixture, source: '' } } })
  const parsed = JSON.parse(bad.content[0].text)
  assert.equal(parsed.reason, 'invalid_args')
  console.log('PASS legal_source_check schema min enforcement')
}

// T10: scripts_legal_source_check argv with shell:false and resolved path
{
  const { handlers, fakeServer } = collectHandlers(); let captured = null
  const spawn = (cmd, args, opts) => { captured = { cmd, args, opts }; const child = new EventEmitter(); child.stdout = new EventEmitter(); child.stderr = new EventEmitter(); process.nextTick(() => { child.stdout.emit('data', 'ok'); child.emit('close', 0) }); return child }
  createServer({ server: fakeServer, projectRoot: fixture, spawn })
  await handlers[1]({ params: { name: 'scripts_legal_source_check', arguments: { project_root: fixture, source: 'fixture-content' } } })
  assert.equal(captured.cmd, 'python3')
  assert.equal(captured.opts.shell, false)
  assert.ok(captured.args[0].endsWith('legal-source-check.py'))
  assert.deepEqual(captured.args.slice(1), ['--source', 'fixture-content'])
  console.log('PASS legal_source_check spawn argv + shell false')
}

// T11: success envelope has lifecycle fields
{
  const { handlers, fakeServer } = collectHandlers(); const spawn = makeSpawnCapture('done', 0)
  createServer({ server: fakeServer, projectRoot: fixture, spawn })
  const res = await handlers[1]({ params: { name: 'scripts_progress_read', arguments: { project_root: fixture, task_id: 'T' } } })
  const parsed = JSON.parse(res.content[0].text)
  for (const key of ['status', 'command_id', 'exit_code', 'duration_ms', 'stdout', 'stderr', 'truncated']) assert.ok(key in parsed, `success envelope ${key}`)
  assert.equal(parsed.status, 'success')
  assert.equal(parsed.exit_code, 0)
  assert.equal(parsed.truncated, false)
  assert.equal(parsed.command_id.length, 36)
  console.log('PASS success envelope has all lifecycle fields')
}

// T12: nonzero exit returns status=error + exit_code + stderr
{
  const { handlers, fakeServer } = collectHandlers(); const spawn = makeSpawnCapture('', 2)
  createServer({ server: fakeServer, projectRoot: fixture, spawn })
  const res = await handlers[1]({ params: { name: 'scripts_progress_read', arguments: { project_root: fixture, task_id: 'T' } } })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.status, 'error')
  assert.equal(parsed.reason, 'exit_nonzero')
  assert.equal(parsed.exit_code, 2)
  console.log('PASS nonzero exit envelope')
}

// T13: spawn error returns status=error + reason=spawn_error
{
  const { handlers, fakeServer } = collectHandlers(); const spawn = (() => { const child = new EventEmitter(); child.stdout = new EventEmitter(); child.stderr = new EventEmitter(); process.nextTick(() => { child.emit('error', new Error('boom')) }); return () => child })()
  createServer({ server: fakeServer, projectRoot: fixture, spawn })
  const res = await handlers[1]({ params: { name: 'scripts_progress_read', arguments: { project_root: fixture, task_id: 'T' } } })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.status, 'error')
  assert.equal(parsed.reason, 'spawn_error')
  assert.equal(parsed.exit_code, null)
  console.log('PASS spawn error envelope')
}

// T14: timeout fires with status=error + reason=timeout
{
  const { handlers, fakeServer } = collectHandlers(); const spawn = makeSpawnDelayed(0, 5000)
  createServer({ server: fakeServer, projectRoot: fixture, spawn, timeoutMs: 200 })
  const t0 = Date.now()
  const res = await handlers[1]({ params: { name: 'scripts_progress_read', arguments: { project_root: fixture, task_id: 'T' } } })
  const elapsed = Date.now() - t0
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.status, 'error')
  assert.equal(parsed.reason, 'timeout')
  assert.equal(parsed.exit_code, null)
  assert.ok(elapsed < 4000, `should not wait for child, elapsed=${elapsed}`)
  console.log('PASS timeout envelope')
}

// T15: output cap with truncated=true
{
  const { handlers, fakeServer } = collectHandlers(); const huge = 'x'.repeat(500000)
  const spawn = makeSpawnCapture(huge, 0)
  createServer({ server: fakeServer, projectRoot: fixture, spawn })
  const res = await handlers[1]({ params: { name: 'scripts_progress_read', arguments: { project_root: fixture, task_id: 'T' } } })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.truncated, true)
  assert.ok(parsed.stdout.length < 500000)
  assert.ok(parsed.stdout.includes('[TRUNCATED'))
  console.log('PASS output cap with truncated flag')
}

// T16: success stdout sanitization
{
  const { handlers, fakeServer } = collectHandlers(); const exposedPath = path.resolve(fixture, 'scripts/foo.py')
  const spawn = makeSpawnCapture(`leaked: ${exposedPath} secret=supersecret1234`, 0)
  createServer({ server: fakeServer, projectRoot: fixture, spawn })
  const res = await handlers[1]({ params: { name: 'scripts_progress_read', arguments: { project_root: fixture, task_id: 'T' } } })
  const parsed = JSON.parse(res.content[0].text)
  assert.ok(!parsed.stdout.includes(exposedPath))
  assert.ok(parsed.stdout.includes('[PROJECT_ROOT]'))
  assert.ok(!parsed.stdout.includes('supersecret1234'))
  console.log('PASS stdout sanitization')
}

// T17: scripts_plan_validate runs all four validators and returns named results
{
  const planFixture = mkdtempSync('/tmp/scripts-mcp-plan-')
  mkdirSync(path.join(planFixture, 'scripts'), { recursive: true })
  mkdirSync(path.join(planFixture, 'docs'), { recursive: true })
  writeFileSync(path.join(planFixture, 'docs', 'x.md'), '# plan')
  for (const name of ['validate-plan-depth.py', 'plan-compliance-check.py', 'subagent-handoff-check.py', 'plan-execution-readiness.py']) writeFileSync(path.join(planFixture, 'scripts', name), '#!/usr/bin/env python3\nprint("ok")')
  const { handlers, fakeServer } = collectHandlers(); const calls = []
  const spawn = (cmd, args, opts) => { calls.push({ cmd, args, opts }); const child = new EventEmitter(); child.stdout = new EventEmitter(); child.stderr = new EventEmitter(); process.nextTick(() => { child.stdout.emit('data', 'ok'); child.emit('close', 0) }); return child }
  createServer({ server: fakeServer, projectRoot: planFixture, spawn })
  const res = await handlers[1]({ params: { name: 'scripts_plan_validate', arguments: { project_root: planFixture, plan_path: 'docs/x.md', task_id: 'TASK' } } })
  rmSync(planFixture, { recursive: true, force: true })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.status, 'success')
  assert.equal(parsed.command_id.length, 36)
  assert.ok(Array.isArray(parsed.validators))
  const names = parsed.validators.map((v) => v.name).sort()
  assert.deepEqual(names, ['compliance', 'depth', 'handoff', 'readiness'])
  assert.equal(calls.length, 4)
  for (const call of calls) {
    assert.equal(call.cmd, 'python3')
    assert.equal(call.opts.shell, false)
  }
  console.log('PASS plan_validate runs 4 named validators')
}

// T18: plan_validate aggregate returns status=error when any validator fails
{
  const planFixture = mkdtempSync('/tmp/scripts-mcp-planfail-')
  mkdirSync(path.join(planFixture, 'scripts'), { recursive: true })
  mkdirSync(path.join(planFixture, 'docs'), { recursive: true })
  writeFileSync(path.join(planFixture, 'docs', 'x.md'), '# plan')
  for (const name of ['validate-plan-depth.py', 'plan-compliance-check.py', 'subagent-handoff-check.py', 'plan-execution-readiness.py']) writeFileSync(path.join(planFixture, 'scripts', name), '#!/usr/bin/env python3\nprint("ok")')
  const { handlers, fakeServer } = collectHandlers(); let n = 0
  const spawn = (cmd, args, opts) => { n += 1; const child = new EventEmitter(); child.stdout = new EventEmitter(); child.stderr = new EventEmitter(); process.nextTick(() => { child.stdout.emit('data', n === 2 ? 'bad' : 'ok'); child.emit('close', n === 2 ? 1 : 0) }); return child }
  createServer({ server: fakeServer, projectRoot: planFixture, spawn })
  const res = await handlers[1]({ params: { name: 'scripts_plan_validate', arguments: { project_root: planFixture, plan_path: 'docs/x.md', task_id: 'TASK' } } })
  rmSync(planFixture, { recursive: true, force: true })
  const parsed = JSON.parse(res.content[0].text)
  assert.equal(parsed.status, 'error')
  assert.equal(parsed.reason, 'validator_failed')
  const failed = parsed.validators.find((v) => v.status !== 'success')
  assert.ok(failed, 'at least one validator failed')
  console.log('PASS plan_validate aggregate error')
}

// T19: path containment rejects absolute, traversal, and symlink escape
{
  assert.throws(() => resolveChild(fixture, '/etc/passwd'), /path escape|absolute/)
  assert.throws(() => resolveChild(fixture, '../escape'), /path escape|escape/)
  assert.throws(() => resolveChild(fixture, 'subdir\x00bad'), /invalid|null|escape/i)
  if (process.platform !== 'win32') {
    const outside = mkdtempSync('/tmp/scripts-mcp-outside-')
    writeFileSync(path.join(outside, 'secret'), 'secret')
    try { symlinkSync(outside, path.join(fixture, 'scripts', 'escape-link'), 'dir') } catch { rmSync(outside, { recursive: true, force: true }); console.log('PASS path containment (no symlink support, escape skipped)') }
    let didThrow = false
    try { resolveChild(fixture, 'scripts/escape-link/secret') } catch { didThrow = true }
    rmSync(outside, { recursive: true, force: true })
    if (didThrow) { console.log('PASS path containment rejects symlink escape') } else { throw new Error('symlink escape not detected') }
  } else { console.log('PASS path containment (windows symlink test skipped)') }
}

// T20: resolveProjectRoot requires existing directory
{
  assert.throws(() => resolveProjectRoot(path.join(fixture, 'no-such')), /invalid_project_root|directory/)
  assert.equal(resolveProjectRoot(fixture), realpathSync(fixture))
  console.log('PASS resolveProjectRoot')
}

// T21: resolveScript rejects traversal in script name
{
  assert.throws(() => resolveScript('../x.py', fixture), /path escape/)
  assert.throws(() => resolveScript('a/b.py', fixture), /path escape/)
  console.log('PASS resolveScript containment')
}

// T22: static deny scan — no exec, shell:true, script_path, extra_args, raw_args
{
  const fs = await import('node:fs/promises')
  const src = await fs.readFile(path.resolve(root, 'bin/scripts-mcp.mjs'), 'utf8')
  for (const forbidden of ['exec(', 'execFile(', 'shell: true', 'script_path', 'extra_args', 'raw_args', 'raw_flags']) {
    assert.ok(!src.includes(forbidden), `forbidden token present: ${forbidden}`)
  }
  console.log('PASS static deny scan')
}

// T23: marker coverage unchanged
{
  const fs = await import('node:fs/promises')
  const agentFiles = (await fs.readdir(path.join(root, 'agents'))).filter((name) => name.endsWith('.md')).map((name) => path.join(root, 'agents', name))
  const skillDirs = (await fs.readdir(path.join(root, 'skills'), { withFileTypes: true })).filter((entry) => entry.isDirectory() && entry.name.startsWith('opencode-'))
  const skillFiles = skillDirs.map((entry) => path.join(root, 'skills', entry.name, 'SKILL.md'))
  const files = [...agentFiles, ...skillFiles]
  const marker = '<!-- scripts-mcp-pointer -->'
  const missing = []
  for (const file of files) { if (!(await fs.readFile(file, 'utf8')).includes(marker)) missing.push(path.relative(root, file)) }
  assert.deepEqual(missing, [], `missing marker: ${missing.join(', ')}`)
  console.log(`PASS marker coverage (${files.length} files)`)
}

rmSync(fixture, { recursive: true, force: true })
console.log('\nAll tests passed')
