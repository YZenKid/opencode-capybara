import { readFileSync } from "node:fs";
import { ackMessage, listMessages, sendMessage, summarizeMailbox } from "./mailbox-store.mjs";
import { getWorkerExecution, listWorkerExecutions, updateWorkerExecution } from "./executor.mjs";
import { acquireLock, releaseLock } from "./locks.mjs";
import { getRun } from "./run-store.mjs";
import { buildRuntimeBoardSummary } from "./board.mjs";
import { executionStderrLogFile, executionStdoutLogFile, taskFile, workerLeaseLockFile } from "./state-paths.mjs";
import { getTask, listTasks } from "./task-store.mjs";
import { writeJsonAtomic } from "./state-io.mjs";

function nowIso() {
  return new Date().toISOString();
}

function nowMs() {
  return Date.now();
}

function isPidAlive(pid) {
  if (!pid || typeof pid !== "number") return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function stableJitterUnit(seed = "") {
  let hash = 2166136261;
  for (const char of String(seed)) {
    hash ^= char.charCodeAt(0);
    hash = Math.imul(hash, 16777619);
  }
  return ((hash >>> 0) % 10000) / 10000;
}

export function computeRetryDelayMs(retryCount = 0, { base_ms = 1000, multiplier = 2, max_ms = 60000, jitter_ratio = 0, jitter_seed = "" } = {}) {
  const safeRetry = Math.max(0, Number(retryCount ?? 0));
  const baseValue = base_ms * (multiplier ** safeRetry);
  const capped = Math.min(baseValue, max_ms);
  if (!jitter_ratio) return capped;
  const unit = stableJitterUnit(`${jitter_seed}:${safeRetry}:${base_ms}:${multiplier}:${max_ms}`);
  const jitterWindow = capped * Math.max(0, jitter_ratio);
  const jittered = capped + Math.round(unit * jitterWindow);
  return Math.min(jittered, max_ms);
}

export function retryReady(execution, policy = {}, current_ms = nowMs()) {
  if (!execution) return false;
  const delayMs = computeRetryDelayMs(execution.retry_count ?? 0, {
    ...policy,
    jitter_seed: policy.jitter_seed ?? execution.execution_id ?? execution.task_id ?? "",
  });
  if (!execution.last_retry_at) return true;
  const lastMs = Date.parse(execution.last_retry_at);
  if (Number.isNaN(lastMs)) return true;
  return (current_ms - lastMs) >= delayMs;
}

export function retryFailedTask(projectRoot, runId, taskId, { worker_name, execution_id, max_attempts = 1 } = {}) {
  const task = getTask(projectRoot, runId, taskId);
  if (!task) throw new Error(`task not found: ${taskId}`);
  if (task.status !== "failed") throw new Error(`task not retryable: ${task.status}`);

  const execution = getWorkerExecution(projectRoot, runId, execution_id);
  if (!execution) throw new Error(`worker execution not found: ${execution_id}`);

  const retryCount = execution.retry_count ?? 0;
  if (retryCount >= max_attempts) throw new Error(`retry limit reached: ${retryCount}/${max_attempts}`);

  writeJsonAtomic(taskFile(projectRoot, runId, taskId), {
    ...task,
    status: "pending",
    claimed_by: null,
    result: { ...(task.result ?? {}), retry_requested: true, retry_count: retryCount + 1 },
    updated_at: nowIso(),
  });

  const updatedExecution = updateWorkerExecution(projectRoot, runId, execution_id, (record) => ({
    ...record,
    status: "retrying",
    retry_count: retryCount + 1,
    last_retry_at: nowIso(),
  }));

  const message = sendMessage(projectRoot, runId, {
    from: "runtime-retry-loop",
    to: worker_name ?? execution.worker_name,
    type: "retry",
    payload: {
      run_id: runId,
      task_id: taskId,
      execution_id,
      retry_count: retryCount + 1,
      prompt: execution.prompt,
    },
  });

  return { task: getTask(projectRoot, runId, taskId), execution: updatedExecution, message };
}

export function consumeWorkerMailbox(projectRoot, runId, workerName) {
  const pending = listMessages(projectRoot, runId, workerName).sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)));
  const message = pending[0];
  if (!message) return { consumed: false, reason: "empty" };

  const acked = ackMessage(projectRoot, runId, workerName, message.message_id, `consumer:${workerName}`);
  const executionId = acked.payload?.execution_id ?? null;
  return {
    consumed: true,
    message: acked,
    task: acked.payload?.task_id ? getTask(projectRoot, runId, acked.payload.task_id) : null,
    execution: executionId ? getWorkerExecution(projectRoot, runId, executionId) : null,
  };
}

export function consumeWorkerMailboxWithLease(projectRoot, runId, workerName, { owner = `consumer:${process.pid}`, lease_ms = 30000 } = {}) {
  const leasePath = workerLeaseLockFile(projectRoot, runId, workerName);
  const lease = acquireLock(leasePath, { owner, stale_ms: lease_ms });
  if (!lease.acquired) {
    return { consumed: false, reason: "lease-held", lease: lease.lock };
  }

  try {
    const result = consumeWorkerMailbox(projectRoot, runId, workerName);
    return { ...result, lease: lease.lock };
  } finally {
    releaseLock(leasePath, owner, { force: true });
  }
}

export function pollWorkerExecution(projectRoot, runId, executionId) {
  const execution = getWorkerExecution(projectRoot, runId, executionId);
  if (!execution) throw new Error(`worker execution not found: ${executionId}`);
  if (!["spawned", "running"].includes(execution.status)) return execution;

  const alive = isPidAlive(execution.spawned_pid);
  return updateWorkerExecution(projectRoot, runId, executionId, (record) => ({
    ...record,
    status: alive ? "running" : "exited",
    exit_reason: alive ? record.exit_reason ?? null : "pid-missing",
  }));
}

export function pollRunExecutions(projectRoot, runId) {
  return listWorkerExecutions(projectRoot, runId).map((execution) => pollWorkerExecution(projectRoot, runId, execution.execution_id));
}

function tailLines(content, lines) {
  const trimmed = content.split(/\r?\n/).filter((line, index, arr) => !(index === arr.length - 1 && line === ""));
  return trimmed.slice(-Math.max(1, lines));
}

export function tailExecutionLog(projectRoot, runId, executionId, { stream = "stdout", lines = 20 } = {}) {
  const execution = getWorkerExecution(projectRoot, runId, executionId);
  if (!execution) throw new Error(`worker execution not found: ${executionId}`);
  const path = stream === "stderr"
    ? executionStderrLogFile(projectRoot, runId, executionId)
    : executionStdoutLogFile(projectRoot, runId, executionId);
  const content = readFileSync(path, "utf8");
  return {
    execution_id: executionId,
    stream,
    path,
    lines: tailLines(content, lines),
  };
}

export async function followExecutionLog(projectRoot, runId, executionId, {
  stream = "stdout",
  lines = 20,
  ticks = 2,
  interval_ms = 250,
  on_tick,
} = {}) {
  const snapshots = [];
  for (let index = 0; index < ticks; index += 1) {
    snapshots.push(tailExecutionLog(projectRoot, runId, executionId, { stream, lines }));
    if (typeof on_tick === "function") {
      await on_tick(index, snapshots.at(-1));
    }
    if (index < ticks - 1) {
      await new Promise((resolve) => setTimeout(resolve, interval_ms));
    }
  }
  return { execution_id: executionId, stream, snapshots };
}

export async function followExecutionLogLive(projectRoot, runId, executionId, {
  stream = "stdout",
  lines = 20,
  poll_ms = 250,
  timeout_ms = 2000,
  on_poll,
} = {}) {
  const events = [];
  const startedAt = Date.now();
  let index = 0;
  while (Date.now() - startedAt <= timeout_ms) {
    const tail = tailExecutionLog(projectRoot, runId, executionId, { stream, lines });
    const previous = events.at(-1);
    const changed = !previous || JSON.stringify(previous.lines) !== JSON.stringify(tail.lines);
    const event = { ...tail, tick: index, at_ms: Date.now(), changed };
    events.push(event);
    if (typeof on_poll === "function") {
      await on_poll(index, event);
    }
    index += 1;
    await new Promise((resolve) => setTimeout(resolve, poll_ms));
  }
  return { execution_id: executionId, stream, events, timed_out: true };
}

export function getRuntimeOpsSnapshot(projectRoot, runId) {
  return {
    run: getRun(projectRoot, runId),
    tasks: listTasks(projectRoot, runId),
    mailbox: summarizeMailbox(projectRoot, runId),
    executions: listWorkerExecutions(projectRoot, runId),
    board: buildRuntimeBoardSummary(projectRoot, runId),
  };
}
