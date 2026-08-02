#!/usr/bin/env node
import { realpathSync, statSync } from 'node:fs'
import { spawn as nodeSpawn } from 'node:child_process'
import { randomUUID } from 'node:crypto'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import process from 'node:process'
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod'

const MAX_OUTPUT_BYTES = 200000
const DEFAULT_TIMEOUT_MS = 30000
const rootSchema = { project_root: { type: 'string' } }
const strict = (shape) => z.object(shape).strict()
const jsonSchema = (properties, required) => ({ type: 'object', properties: { ...rootSchema, ...properties }, required: ['project_root', ...required], additionalProperties: false })
const withRoot = (shape) => strict({ project_root: z.string(), ...shape })

export const TOOL_REGISTRY = Object.freeze([
  { name: 'scripts_catalog', sourceScript: null, classification: 'catalog', laneRecommendation: '@orchestrator', schema: withRoot({}), inputSchema: jsonSchema({}, []), cliFallback: 'python3 ~/.config/opencode/scripts/<script>.py <fixed args>' },
  { name: 'scripts_plan_validate', sourceScript: null, classification: 'validation', laneRecommendation: '@artifact-planner', schema: withRoot({ plan_path: z.string(), task_id: z.string() }), inputSchema: jsonSchema({ plan_path: { type: 'string' }, task_id: { type: 'string' } }, ['plan_path', 'task_id']), cliFallback: 'python3 ~/.config/opencode/scripts/validate-plan-depth.py <plan>; python3 ~/.config/opencode/scripts/plan-compliance-check.py --project-root <root> --plan <plan> --task-id <task>; python3 ~/.config/opencode/scripts/subagent-handoff-check.py --plan <plan>; python3 ~/.config/opencode/scripts/plan-execution-readiness.py <plan> --project-root <root>' },
  { name: 'scripts_runtime_verify', sourceScript: 'runtime-verify.py', classification: 'runtime-check', laneRecommendation: '@fixer', schema: withRoot({ route: z.string().optional(), asset: z.string().optional(), env: z.string().optional() }), inputSchema: jsonSchema({ route: { type: 'string' }, asset: { type: 'string' }, env: { type: 'string' } }, []), cliFallback: 'python3 ~/.config/opencode/scripts/runtime-verify.py --project-root <root> [--route <route>] [--asset <asset>] [--env <env>]' },
  { name: 'scripts_pre_gate_smoke', sourceScript: 'pre-gate-smoke-check.py', classification: 'static-check', laneRecommendation: '@fixer', schema: withRoot({}), inputSchema: jsonSchema({}, []), cliFallback: 'python3 ~/.config/opencode/scripts/pre-gate-smoke-check.py --project-root <root>' },
  { name: 'scripts_template_discover', sourceScript: 'template-source-discovery.py', classification: 'source-discovery', laneRecommendation: '@explorer', schema: withRoot({}), inputSchema: jsonSchema({}, []), cliFallback: 'python3 ~/.config/opencode/scripts/template-source-discovery.py --project-root <root> --json' },
  { name: 'scripts_visual_audit', sourceScript: 'visual-audit.py', classification: 'visual-review', laneRecommendation: '@designer', schema: withRoot({ paths: z.array(z.string()).min(1) }), inputSchema: jsonSchema({ paths: { type: 'array', items: { type: 'string' } } }, ['paths']), cliFallback: 'python3 ~/.config/opencode/scripts/visual-audit.py <relative paths>' },
  { name: 'scripts_legal_source_check', sourceScript: 'legal-source-check.py', classification: 'source-review', laneRecommendation: '@librarian', schema: withRoot({ source: z.string().min(1) }), inputSchema: jsonSchema({ source: { type: 'string' } }, ['source']), cliFallback: 'python3 ~/.config/opencode/scripts/legal-source-check.py --source <source>' },
  { name: 'scripts_design_audit', sourceScript: 'design-audit.py', classification: 'design-review', laneRecommendation: '@designer', schema: withRoot({}), inputSchema: jsonSchema({}, []), cliFallback: 'python3 ~/.config/opencode/scripts/design-audit.py --project-root <root>' },
  { name: 'scripts_progress_read', sourceScript: 'task-progress.py', classification: 'state-read', laneRecommendation: '@orchestrator', schema: withRoot({ task_id: z.string().min(1) }), inputSchema: jsonSchema({ task_id: { type: 'string' } }, ['task_id']), cliFallback: 'python3 ~/.config/opencode/scripts/task-progress.py <task> --summary' },
  { name: 'scripts_delegation_read', sourceScript: 'delegation-log.py', classification: 'state-read', laneRecommendation: '@orchestrator', schema: withRoot({ task_id: z.string().min(1) }), inputSchema: jsonSchema({ task_id: { type: 'string' } }, ['task_id']), cliFallback: 'python3 ~/.config/opencode/scripts/delegation-log.py --task <task> --summary' },
  { name: 'scripts_session_trace_audit', sourceScript: 'session-trace-audit.py', classification: 'trace-review', laneRecommendation: '@quality-gate', schema: withRoot({ path: z.string().optional() }), inputSchema: jsonSchema({ path: { type: 'string' } }, []), cliFallback: 'python3 ~/.config/opencode/scripts/session-trace-audit.py [<relative path>]' },
  { name: 'scripts_backup_scan', sourceScript: 'backup-cleanup.py', classification: 'safety-scan', laneRecommendation: '@quality-gate', schema: withRoot({}), inputSchema: jsonSchema({}, []), cliFallback: 'python3 ~/.config/opencode/scripts/backup-cleanup.py --scan' },
  { name: 'scripts_rules_dry_run', sourceScript: 'rules-harmonizer.py', classification: 'policy-check', laneRecommendation: '@quality-gate', schema: withRoot({}), inputSchema: jsonSchema({}, []), cliFallback: 'python3 ~/.config/opencode/scripts/rules-harmonizer.py --dry-run' },
])

export const ALLOWED_TOOLS = Object.freeze(TOOL_REGISTRY.map(({ name }) => name))
const byName = new Map(TOOL_REGISTRY.map((tool) => [tool.name, tool]))

function failure(reason, commandId = randomUUID(), extra = {}) {
  return { status: 'error', reason, command_id: commandId, exit_code: null, duration_ms: 0, stdout: '', stderr: '', truncated: false, ...extra }
}

export function resolveProjectRoot(input, baseRoot = process.cwd()) {
  if (typeof input !== 'string' || input.includes('\0')) throw Object.assign(new Error('invalid project_root'), { reason: 'invalid_project_root' })
  const candidate = path.resolve(baseRoot, input)
  try {
    const resolved = realpathSync(candidate)
    if (!statSync(resolved).isDirectory()) throw new Error('not directory')
    return resolved
  } catch {
    throw Object.assign(new Error('project_root must be an existing directory'), { reason: 'invalid_project_root' })
  }
}

export function resolveChild(root, input) {
  if (typeof input !== 'string' || input.includes('\0') || path.isAbsolute(input) || input.split(/[\\/]/).includes('..')) throw Object.assign(new Error('path escape'), { reason: 'path_escape' })
  const candidate = path.resolve(root, input)
  let resolved
  try { resolved = realpathSync(candidate) } catch { throw Object.assign(new Error('path not found'), { reason: 'path_not_found' }) }
  const relative = path.relative(root, resolved)
  if (relative.startsWith('..') || path.isAbsolute(relative)) throw Object.assign(new Error('path escape'), { reason: 'path_escape' })
  return resolved
}

export function resolveScript(name, projectRoot = process.cwd()) {
  if (typeof name !== 'string' || name.includes('..') || name.includes('/') || name.includes('\\') || name.includes('\0')) throw Object.assign(new Error('path escape'), { reason: 'path_escape' })
  return resolveChild(projectRoot, path.join('scripts', name))
}

export function sanitizeError(error, projectRoot = process.cwd()) {
  let text = String(error?.message || error || '')
  for (const projectPath of new Set([path.resolve(projectRoot), realpathSync(projectRoot)])) text = text.split(projectPath).join('[PROJECT_ROOT]')
  const projectName = path.basename(path.resolve(projectRoot)).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  text = text.replace(new RegExp(`/(?:private/)?tmp/${projectName}(?:/[^\\s"']*)?`, 'g'), '[PROJECT_ROOT]')
  for (const value of Object.values(process.env)) if (value && value.length > 3) text = text.split(value).join('[REDACTED]')
  return text.replace(/Bearer\s+\S+/gi, 'Bearer [REDACTED]').replace(/(token|secret|key)[=:]\s*\S+/gi, '$1=[REDACTED]')
}

export function toolText(obj) { return { content: [{ type: 'text', text: JSON.stringify(obj) }] } }

function appendOutput(current, chunk) {
  const value = Buffer.isBuffer(chunk) ? chunk.toString('utf8') : String(chunk)
  const room = MAX_OUTPUT_BYTES - Buffer.byteLength(current)
  if (room <= 0) return { text: current, truncated: true }
  const bytes = Buffer.from(value)
  if (bytes.length <= room) return { text: current + value, truncated: false }
  return { text: current + bytes.subarray(0, room).toString('utf8'), truncated: true }
}

export function run(spawn, args, cwd, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const commandId = randomUUID(); const started = process.hrtime.bigint()
  return new Promise((resolve) => {
    let child; let stdout = ''; let stderr = ''; let truncated = false; let settled = false
    const done = (result) => { if (settled) return; settled = true; clearTimeout(timer); const marker = truncated ? `\n[TRUNCATED: output exceeded ${MAX_OUTPUT_BYTES} bytes]` : ''; resolve({ command_id: commandId, duration_ms: Number((process.hrtime.bigint() - started) / 1000000n), stdout: sanitizeError(stdout + marker, cwd), stderr: sanitizeError(stderr + marker, cwd), truncated, ...result }) }
    let timer
    try {
      child = spawn('python3', args, { cwd, shell: false })
      child.stdout?.on('data', (chunk) => { const next = appendOutput(stdout, chunk); stdout = next.text; truncated ||= next.truncated })
      child.stderr?.on('data', (chunk) => { const next = appendOutput(stderr, chunk); stderr = next.text; truncated ||= next.truncated })
      child.once('error', (error) => done({ status: 'error', reason: 'spawn_error', exit_code: null, stderr: sanitizeError(error, cwd) }))
      child.once('close', (code) => done(code === 0 ? { status: 'success', exit_code: 0 } : { status: 'error', reason: 'exit_nonzero', exit_code: code ?? null }))
      timer = setTimeout(() => { try { child.kill('SIGTERM') } catch {} ; done({ status: 'error', reason: 'timeout', exit_code: null }) }, timeoutMs)
    } catch (error) { done({ status: 'error', reason: 'spawn_error', exit_code: null, stderr: sanitizeError(error, cwd) }) }
  })
}

function catalog() {
  return { status: 'success', count: TOOL_REGISTRY.length, tools: TOOL_REGISTRY.map((tool) => ({ name: tool.name, source_script: tool.sourceScript, classification: tool.classification, lane_recommendation: tool.laneRecommendation, required_input: tool.inputSchema.required, cli_fallback: tool.cliFallback, pending_reason: tool.name === 'scripts_visual_audit' ? 'canonical script unavailable' : undefined })) }
}

function fixedArgs(name, args, root) {
  const plan = (value) => resolveChild(root, value)
  switch (name) {
    case 'scripts_runtime_verify': return ['runtime-verify.py', '--project-root', root, ...(['route', 'asset', 'env'].flatMap((key) => args[key] ? [`--${key}`, args[key]] : []))]
    case 'scripts_pre_gate_smoke': return ['pre-gate-smoke-check.py', '--project-root', root]
    case 'scripts_template_discover': return ['template-source-discovery.py', '--project-root', root, '--json']
    case 'scripts_visual_audit': return ['visual-audit.py', ...args.paths.map(plan)]
    case 'scripts_legal_source_check': return ['legal-source-check.py', '--source', args.source]
    case 'scripts_design_audit': return ['design-audit.py', '--project-root', root]
    case 'scripts_progress_read': return ['task-progress.py', args.task_id, '--summary']
    case 'scripts_delegation_read': return ['delegation-log.py', '--task', args.task_id, '--summary']
    case 'scripts_session_trace_audit': return ['session-trace-audit.py', ...(args.path ? [plan(args.path)] : [])]
    case 'scripts_backup_scan': return ['backup-cleanup.py', '--scan']
    case 'scripts_rules_dry_run': return ['rules-harmonizer.py', '--dry-run']
    default: throw Object.assign(new Error('tool not implemented'), { reason: 'tool_not_allowed' })
  }
}

async function runNamed(spawn, root, script, argv, timeoutMs = DEFAULT_TIMEOUT_MS) {
  let scriptPath
  try { scriptPath = resolveScript(script, root) } catch (error) { return failure(error.reason || 'script_missing', undefined, { stderr: sanitizeError(error, root) }) }
  return run(spawn, [scriptPath, ...argv], root, timeoutMs)
}

async function planValidate(spawn, root, args, timeoutMs = DEFAULT_TIMEOUT_MS) {
  const plan = resolveChild(root, args.plan_path)
  const checks = [
    ['depth', 'validate-plan-depth.py', [plan]],
    ['compliance', 'plan-compliance-check.py', ['--project-root', root, '--plan', plan, '--task-id', args.task_id]],
    ['handoff', 'subagent-handoff-check.py', ['--plan', plan]],
    ['readiness', 'plan-execution-readiness.py', [plan, '--project-root', root]],
  ]
  const started = process.hrtime.bigint(); const validators = []
  for (const [name, script, argv] of checks) validators.push({ name, ...(await runNamed(spawn, root, script, argv, timeoutMs)) })
  const bad = validators.find((result) => result.status !== 'success')
  return { status: bad ? 'error' : 'success', reason: bad ? 'validator_failed' : undefined, command_id: randomUUID(), exit_code: bad ? 1 : 0, duration_ms: Number((process.hrtime.bigint() - started) / 1000000n), stdout: '', stderr: '', truncated: validators.some((result) => result.truncated), validators }
}

export function createServer(deps = {}) {
  const baseRoot = path.resolve(deps.projectRoot || process.cwd()); const spawn = deps.spawn || nodeSpawn; const timeoutMs = deps.timeoutMs || DEFAULT_TIMEOUT_MS
  const server = deps.server || new Server({ name: 'scripts-mcp', version: '0.2.0' }, { capabilities: { tools: {} } })
  server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOL_REGISTRY.map(({ name, inputSchema, classification }) => ({ name, description: `Read-only governance ${classification}`, inputSchema })) }))
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const name = request.params?.name; const commandId = randomUUID(); const tool = byName.get(name)
    if (!tool) return { isError: true, reason: 'tool_not_allowed', ...toolText(failure('tool_not_allowed', commandId)) }
    try {
      const args = tool.schema.parse(request.params?.arguments || {})
      const root = resolveProjectRoot(args.project_root, baseRoot)
      if (name === 'scripts_catalog') return toolText(catalog())
      if (name === 'scripts_visual_audit') {
        try { resolveScript('visual-audit.py', root) } catch { return toolText({ status: 'tool_pending', reason: 'canonical_script_unavailable', command_id: commandId, exit_code: null, duration_ms: 0, stdout: '', stderr: '', truncated: false }) }
      }
      if (name === 'scripts_plan_validate') return toolText(await planValidate(spawn, root, args, timeoutMs))
      const [script, ...argv] = fixedArgs(name, args, root)
      return toolText(await runNamed(spawn, root, script, argv, timeoutMs))
    } catch (error) {
      const reason = error.reason || (error?.name === 'ZodError' ? 'invalid_args' : 'error')
      return { isError: true, ...toolText(failure(reason, commandId, { stderr: sanitizeError(error, baseRoot) })) }
    }
  })
  return server
}

export async function startServer() { const server = createServer(); await server.connect(new StdioServerTransport()) }
if (process.argv[1] && process.argv[1] !== '-' && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) await startServer()
