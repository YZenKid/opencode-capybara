// Project memory finalization hook for the runtime task completion boundary.
//
// This module wraps the single-task `completeTask` write so that, when a task
// transitions to `status: "completed"`, the project-local MCP memory store is
// automatically finalized for that task before the next downstream step
// (verification loop, summary, user-facing reply) is computed.
//
// Why:
// - The agent prompt layer already says "finalize memory before final summary",
//   but the runtime execution engine can ship a task without the agent
//   re-emitting the finalizer. Wiring the hook here makes the gate mechanical.
// - The hook is fail-soft: if the memory store is unavailable, the task still
//   completes, and the failure is recorded on the run events stream.
//
// This is intentionally a small module: it reads task result metadata,
// spawns the existing `mcp-memory-store.py --finalize` CLI, and records the
// outcome. No new storage path, no new format, no new dependency.
import { spawnSync } from "node:child_process";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { appendNdjson } from "./state-io.mjs";
import { runEventsFile } from "./state-paths.mjs";

const MODULE_DIR = dirname(fileURLToPath(import.meta.url));
const REPO_SCRIPTS = resolve(MODULE_DIR, "..");

function nowIso() {
  return new Date().toISOString();
}

function deriveSummary(task, result) {
  const candidate = String(
    result?.summary ?? result?.final_summary ?? result?.outcome ?? task?.title ?? ""
  ).trim();
  if (candidate) return candidate;
  return `Task ${task?.task_id ?? "unknown"} completed.`;
}

function deriveDecisions(result) {
  if (Array.isArray(result?.decisions)) {
    return result.decisions.filter((d) => typeof d === "string" && d.trim().length > 0);
  }
  if (typeof result?.decisions === "string" && result.decisions.trim().length > 0) {
    return [result.decisions.trim()];
  }
  if (Array.isArray(result?.key_findings)) {
    return result.key_findings.filter((d) => typeof d === "string" && d.trim().length > 0);
  }
  return [];
}

function deriveFiles(result, task) {
  const sources = [];
  if (Array.isArray(result?.files_touched)) sources.push(...result.files_touched);
  if (Array.isArray(result?.changed_files)) sources.push(...result.changed_files);
  if (Array.isArray(task?.handoff?.files_touched)) sources.push(...task.handoff.files_touched);
  return [...new Set(sources.map((s) => String(s).trim()).filter((s) => s && !s.includes("..")))];
}

function deriveClaimLevel(task, result) {
  const fromResult = String(result?.claim_level ?? "").trim();
  if (fromResult) return fromResult;
  const fromTask = String(task?.claim_level ?? "").trim();
  if (fromTask) return fromTask;
  return task?.status === "completed" ? "done" : "partial";
}

export function findProjectRoot(cwd) {
  // The runtime is typically invoked with projectRoot=process.cwd(). The
  // wrapper script uses `.opencode/mcp-memory/<key>/`; if the cwd has no
  // .opencode directory we still allow the call (the wrapper will create
  // the bundle lazily).
  return cwd;
}

function buildFinalizeArgs(task, result, projectRoot) {
  const summary = deriveSummary(task, result);
  const decisions = deriveDecisions(result);
  const files = deriveFiles(result, task);
  const claimLevel = deriveClaimLevel(task, result);
  const args = [
    resolve(REPO_SCRIPTS, "mcp-memory-store.py"),
    "--project-root",
    projectRoot,
    "--finalize",
    "--task",
    task.task_id,
    "--summary",
    summary,
    "--claim-level",
    claimLevel,
    "--json",
  ];
  for (const decision of decisions) {
    args.push("--decision", decision);
  }
  for (const file of files) {
    args.push("--file", file);
  }
  return { args, summary, decisions, files, claimLevel };
}

export function runMemoryFinalize(projectRoot, runId, task, result) {
  if (!task || !task.task_id) {
    return { ok: false, skipped: true, reason: "no task" };
  }
  const { args, summary, decisions, files, claimLevel } = buildFinalizeArgs(
    task,
    result,
    projectRoot,
  );
  let proc;
  try {
    proc = spawnSync("python3", args, {
      cwd: projectRoot,
      encoding: "utf8",
      timeout: 30_000,
    });
  } catch (e) {
    return { ok: false, error: String(e), task_id: task.task_id };
  }
  let parsed = null;
  if (proc.stdout) {
    try {
      parsed = JSON.parse(proc.stdout);
    } catch {
      parsed = null;
    }
  }
  const ok = proc.status === 0 && parsed && parsed.ok !== false;
  const outcome = {
    ok,
    exit_code: proc.status,
    task_id: task.task_id,
    summary,
    decisions,
    files,
    claim_level: claimLevel,
    backend: parsed?.backend ?? null,
    active_count: parsed?.active_count ?? null,
    archived_count: parsed?.archived_count ?? null,
    stderr_tail: proc.stderr ? proc.stderr.split(/\r?\n/).slice(-5).join("\n") : "",
  };
  if (runId) {
    appendNdjson(runEventsFile(projectRoot, runId), {
      timestamp: nowIso(),
      type: "task-memory-finalized",
      run_id: runId,
      task_id: task.task_id,
      ok,
      backend: outcome.backend,
      active_count: outcome.active_count,
      archived_count: outcome.archived_count,
    });
  }
  return outcome;
}

export function wrapTaskCompletion(completeTaskFn) {
  if (typeof completeTaskFn !== "function") {
    throw new TypeError("wrapTaskCompletion requires the original completeTask function");
  }
  return function completedTaskWithMemoryHook(projectRoot, runId, taskId, result = {}) {
    const finished = completeTaskFn(projectRoot, runId, taskId, result);
    const memory = runMemoryFinalize(projectRoot, runId, finished, result);
    return { ...finished, memory_finalize: memory };
  };
}
