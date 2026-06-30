
import { taskFile, tasksRoot, runEventsFile } from "./state-paths.mjs";
import { appendNdjson, ensureDir, listJson, readJson, writeJsonAtomic } from "./state-io.mjs";
import { runMemoryFinalize } from "./memory-finalize-hook.mjs";

function timestamp() {
  return new Date().toISOString();
}

function withTask(projectRoot, runId, taskId, updater) {
  const path = taskFile(projectRoot, runId, taskId);
  const current = readJson(path, null);
  if (!current) throw new Error(`task not found: ${taskId}`);
  const updated = { ...updater(current), updated_at: timestamp() };
  writeJsonAtomic(path, updated);
  appendNdjson(runEventsFile(projectRoot, runId), { timestamp: updated.updated_at, type: "task-updated", run_id: runId, task_id: taskId, status: updated.status, claimed_by: updated.claimed_by ?? null });
  return updated;
}

export function createTask(projectRoot, runId, payload) {
  const now = timestamp();
  ensureDir(tasksRoot(projectRoot, runId));
  const task = {
    task_id: payload.task_id,
    title: payload.title,
    owner_lane: payload.owner_lane ?? "@fixer",
    status: payload.status ?? "pending",
    depends_on: payload.depends_on ?? [],
    validation: payload.validation ?? null,
    exit_criteria: payload.exit_criteria ?? null,
    claimed_by: null,
    result: null,
    created_at: now,
    updated_at: now,
  };
  writeJsonAtomic(taskFile(projectRoot, runId, task.task_id), task);
  appendNdjson(runEventsFile(projectRoot, runId), { timestamp: now, type: "task-created", run_id: runId, task_id: task.task_id, status: task.status });
  return task;
}

export function getTask(projectRoot, runId, taskId) {
  return readJson(taskFile(projectRoot, runId, taskId), null);
}

export function listTasks(projectRoot, runId) {
  return listJson(tasksRoot(projectRoot, runId)).map((item) => item.data);
}

export function claimTask(projectRoot, runId, taskId, worker) {
  return withTask(projectRoot, runId, taskId, (current) => {
    if (!["pending", "failed"].includes(current.status)) throw new Error(`task not claimable: ${current.status}`);
    return { ...current, status: "claimed", claimed_by: worker };
  });
}

export function completeTask(projectRoot, runId, taskId, result = {}) {
  const finished = withTask(projectRoot, runId, taskId, (current) => ({ ...current, status: "completed", result }));
  // ponytail: project memory auto-finalize. The hook is fail-soft: a missing
  // MCP server or a malformed payload must not block task completion. To
  // disable globally, set OPENCODE_MEMORY_FINALIZE=0 in the environment.
  if (process.env.OPENCODE_MEMORY_FINALIZE === "0") {
    return finished;
  }
  const memory = runMemoryFinalize(projectRoot, runId, finished, result);
  return { ...finished, memory_finalize: memory };
}

export function failTask(projectRoot, runId, taskId, result = {}) {
  return withTask(projectRoot, runId, taskId, (current) => ({ ...current, status: "failed", result }));
}

export function blockTask(projectRoot, runId, taskId, result = {}) {
  return withTask(projectRoot, runId, taskId, (current) => ({ ...current, status: "blocked", result }));
}
