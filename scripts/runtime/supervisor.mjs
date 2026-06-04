import { writeFileSync } from "node:fs";
import { buildRuntimeBoardSummary } from "./board.mjs";
import { listWorkerExecutions } from "./executor.mjs";
import { readLeaseLock, renewLockHeartbeat } from "./locks.mjs";
import { summarizeMailbox } from "./mailbox-store.mjs";
import { consumeWorkerMailboxWithLease, pollRunExecutions, retryFailedTask, retryReady } from "./ops-loop.mjs";
import { boardSnapshotFile, boardSnapshotJsonFile, workerLeaseLockFile } from "./state-paths.mjs";
import { listTasks } from "./task-store.mjs";

function latestExecutionByTask(executions = []) {
  const map = new Map();
  for (const execution of executions) {
    if (!execution.task_id) continue;
    const current = map.get(execution.task_id);
    const left = String(execution.updated_at ?? execution.created_at ?? "");
    const right = String(current?.updated_at ?? current?.created_at ?? "");
    if (!current || left.localeCompare(right) >= 0) {
      map.set(execution.task_id, execution);
    }
  }
  return map;
}

export function persistBoardSnapshot(projectRoot, runId) {
  const summary = buildRuntimeBoardSummary(projectRoot, runId);
  writeFileSync(boardSnapshotFile(projectRoot, runId), `${summary.board}\n`, "utf8");
  writeFileSync(boardSnapshotJsonFile(projectRoot, runId), `${JSON.stringify(summary, null, 2)}\n`, "utf8");
  return summary;
}

export function watchBoard(projectRoot, runId, { ticks = 2, interval_ms = 250 } = {}) {
  return supervisorLoop(projectRoot, runId, {
    ticks,
    interval_ms,
    auto_consume: false,
    auto_retry: false,
    poll_executions: false,
  }).then((results) => results.map((entry) => entry.board));
}

export function supervisorTick(projectRoot, runId, {
  max_retries = 1,
  auto_consume = true,
  auto_retry = true,
  poll_executions = true,
  consume_owner = `consumer:${process.pid}`,
  consume_lease_ms = 30000,
  renew_heartbeats = false,
  retry_base_ms = 1000,
  retry_multiplier = 2,
  retry_max_ms = 60000,
  retry_jitter_ratio = 0,
} = {}) {
  const polled = poll_executions ? pollRunExecutions(projectRoot, runId) : [];

  const consumed = [];
  const workers = Array.from(new Set([
    ...summarizeMailbox(projectRoot, runId).workers,
    ...listWorkerExecutions(projectRoot, runId).map((execution) => execution.worker_name).filter(Boolean),
  ]));
  if (auto_consume) {
    for (const worker of workers) {
      const result = consumeWorkerMailboxWithLease(projectRoot, runId, worker, {
        owner: `${consume_owner}:${worker}`,
        lease_ms: consume_lease_ms,
      });
      if (result?.consumed) consumed.push(result);
    }
  }

  const heartbeats = [];
  if (renew_heartbeats) {
    for (const worker of workers) {
      const owner = `${consume_owner}:${worker}`;
      const lockPath = workerLeaseLockFile(projectRoot, runId, worker);
      const existing = readLeaseLock(lockPath);
      if (!existing || existing.owner !== owner) continue;
      const renewed = renewLockHeartbeat(lockPath, owner, { stale_ms: consume_lease_ms });
      if (renewed?.renewed) heartbeats.push(renewed);
    }
  }

  const retried = [];
  if (auto_retry) {
    const tasks = listTasks(projectRoot, runId).filter((task) => task.status === "failed");
    const executionsByTask = latestExecutionByTask(listWorkerExecutions(projectRoot, runId));
    for (const task of tasks) {
      const execution = executionsByTask.get(task.task_id);
      if (!execution) continue;
      if (execution.status !== "failed") continue;
      if ((execution.retry_count ?? 0) >= max_retries) continue;
      if (!retryReady(execution, {
        base_ms: retry_base_ms,
        multiplier: retry_multiplier,
        max_ms: retry_max_ms,
        jitter_ratio: retry_jitter_ratio,
      })) continue;
      retried.push(retryFailedTask(projectRoot, runId, task.task_id, {
        worker_name: execution.worker_name,
        execution_id: execution.execution_id,
        max_attempts: max_retries,
      }));
    }
  }

  const board = persistBoardSnapshot(projectRoot, runId);
  return { polled, consumed, heartbeats, retried, board };
}

export async function supervisorLoop(projectRoot, runId, {
  ticks = 1,
  interval_ms = 250,
  ...options
} = {}) {
  const results = [];
  for (let index = 0; index < ticks; index += 1) {
    results.push(supervisorTick(projectRoot, runId, options));
    if (index < ticks - 1) {
      await new Promise((resolve) => setTimeout(resolve, interval_ms));
    }
  }
  return results;
}
