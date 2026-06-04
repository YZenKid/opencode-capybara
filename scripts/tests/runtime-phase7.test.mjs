#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { createRun } from "../runtime/run-store.mjs";
import { createTask, failTask, getTask } from "../runtime/task-store.mjs";
import { sendMessage } from "../runtime/mailbox-store.mjs";
import { prepareWorkerExecution, updateWorkerExecution } from "../runtime/executor.mjs";
import { runRuntimeCli } from "../runtime/cli.mjs";
import { consumeWorkerMailboxWithLease, computeRetryDelayMs, tailExecutionLog } from "../runtime/ops-loop.mjs";
import { supervisorTick } from "../runtime/supervisor.mjs";
import { workerLeaseLockFile } from "../runtime/state-paths.mjs";
import { acquireLock } from "../runtime/locks.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-phase7-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "generic repo\n");
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });

createRun(repoRoot, { run_id: "run-phase7", goal: "Phase 7", status: "executing" });
createTask(repoRoot, "run-phase7", { task_id: "task-lock", title: "Lock me", owner_lane: "@backend" });
sendMessage(repoRoot, "run-phase7", { from: "orchestrator", to: "backend-1", type: "task", payload: { task_id: "task-lock" } });

const lockPath = workerLeaseLockFile(repoRoot, "run-phase7", "backend-1");
const lock = acquireLock(lockPath, { owner: "other-consumer", stale_ms: 1000 });
assert.equal(lock.acquired, true);
const leasedBlocked = consumeWorkerMailboxWithLease(repoRoot, "run-phase7", "backend-1", { owner: "local-consumer", lease_ms: 1000 });
assert.equal(leasedBlocked.consumed, false);
assert.equal(leasedBlocked.reason, "lease-held");

createTask(repoRoot, "run-phase7", { task_id: "task-backoff", title: "Backoff me", owner_lane: "@backend" });
failTask(repoRoot, "run-phase7", "task-backoff", { reason: "boom" });
prepareWorkerExecution(repoRoot, "run-phase7", {
  execution_id: "exec-backoff",
  task_id: "task-backoff",
  worker_name: "backend-2",
  lane: "@backend",
  prompt: "Backoff retry",
  workspace_mode: "single"
});
updateWorkerExecution(repoRoot, "run-phase7", "exec-backoff", (record) => ({ ...record, status: "failed", retry_count: 1, last_retry_at: new Date().toISOString() }));
const delay = computeRetryDelayMs(1, { base_ms: 10, multiplier: 2, max_ms: 100 });
assert.equal(delay, 20);
const skipped = supervisorTick(repoRoot, "run-phase7", { max_retries: 3, auto_consume: false, auto_retry: true, poll_executions: false, retry_base_ms: 1000, retry_multiplier: 2 });
assert.equal(skipped.retried.length, 0);
assert.equal(getTask(repoRoot, "run-phase7", "task-backoff").status, "failed");
updateWorkerExecution(repoRoot, "run-phase7", "exec-backoff", (record) => ({ ...record, last_retry_at: new Date(Date.now() - 5000).toISOString() }));
const retried = supervisorTick(repoRoot, "run-phase7", { max_retries: 3, auto_consume: false, auto_retry: true, poll_executions: false, retry_base_ms: 10, retry_multiplier: 2 });
assert.equal(retried.retried.length, 1);
assert.equal(getTask(repoRoot, "run-phase7", "task-backoff").status, "pending");

prepareWorkerExecution(repoRoot, "run-phase7", {
  execution_id: "exec-logtail",
  task_id: "task-lock",
  worker_name: "backend-3",
  lane: "@backend",
  prompt: "Tail log",
  workspace_mode: "single"
});
updateWorkerExecution(repoRoot, "run-phase7", "exec-logtail", (record) => ({
  ...record,
  logs: { ...record.logs, stdout: record.logs.stdout, stderr: record.logs.stderr }
}));
writeFileSync((await import('../runtime/state-paths.mjs')).executionStdoutLogFile(repoRoot, 'run-phase7', 'exec-logtail'), 'line1\nline2\nline3\n');
const tail = tailExecutionLog(repoRoot, 'run-phase7', 'exec-logtail', { stream: 'stdout', lines: 2 });
assert.equal(tail.lines.length, 2);
assert.deepEqual(tail.lines, ['line2', 'line3']);

const boardWatch = await runRuntimeCli(repoRoot, ['board', '--run-id', 'run-phase7', '--watch', '--ticks', '2', '--interval-ms', '1']);
assert.equal(boardWatch.snapshots.length, 2);
const tailCli = await runRuntimeCli(repoRoot, ['tail', '--run-id', 'run-phase7', '--execution-id', 'exec-logtail', '--lines', '1']);
assert.deepEqual(tailCli.tail.lines, ['line3']);
console.log('runtime-phase7.test.mjs: PASS');
