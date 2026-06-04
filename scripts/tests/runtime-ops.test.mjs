#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync, spawn } from "node:child_process";
import { createRun } from "../runtime/run-store.mjs";
import { createTask, failTask, getTask } from "../runtime/task-store.mjs";
import { sendMessage, listMessages } from "../runtime/mailbox-store.mjs";
import { prepareWorkerExecution, updateWorkerExecution, getWorkerExecution } from "../runtime/executor.mjs";
import { retryFailedTask, consumeWorkerMailbox, pollWorkerExecution } from "../runtime/ops-loop.mjs";
import { buildRuntimeBoardSummary } from "../runtime/board.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-ops-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "ops\n");
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });

createRun(repoRoot, { run_id: "run-ops", goal: "Ops loop", status: "executing" });
createTask(repoRoot, "run-ops", { task_id: "task-failed", title: "Retry me", owner_lane: "@backend" });
failTask(repoRoot, "run-ops", "task-failed", { reason: "boom" });
sendMessage(repoRoot, "run-ops", { from: "orchestrator", to: "backend-1", type: "task", payload: { task_id: "task-failed" } });
const prepared = prepareWorkerExecution(repoRoot, "run-ops", {
  execution_id: "exec-failed",
  task_id: "task-failed",
  worker_name: "backend-1",
  lane: "@backend",
  prompt: "Retry backend task",
});
updateWorkerExecution(repoRoot, "run-ops", "exec-failed", (record) => ({ ...record, status: "failed", retry_count: 0 }));
const retried = retryFailedTask(repoRoot, "run-ops", "task-failed", { worker_name: "backend-1", execution_id: "exec-failed", max_attempts: 2 });
assert.equal(retried.task.status, "pending");
assert.equal(retried.execution.status, "retrying");
assert.equal(retried.execution.retry_count, 1);
assert.ok(listMessages(repoRoot, "run-ops", "backend-1").length >= 2);

const consumed = consumeWorkerMailbox(repoRoot, "run-ops", "backend-1");
assert.equal(consumed.message.status, "acked");
assert.equal(consumed.execution.execution_id, "exec-failed");

const child = spawn(process.execPath, ["-e", "setTimeout(() => {}, 2000)"], { detached: true, stdio: "ignore" });
child.unref();
const live = prepareWorkerExecution(repoRoot, "run-ops", {
  execution_id: "exec-live",
  task_id: "task-failed",
  worker_name: "backend-2",
  lane: "@backend",
  prompt: "Long running task",
  workspace_mode: "single",
});
updateWorkerExecution(repoRoot, "run-ops", "exec-live", (record) => ({ ...record, status: "spawned", spawned_pid: child.pid }));
const polledLive = pollWorkerExecution(repoRoot, "run-ops", "exec-live");
assert.equal(polledLive.status, "running");
process.kill(child.pid, "SIGTERM");
await new Promise((resolve) => setTimeout(resolve, 150));
const polledExited = pollWorkerExecution(repoRoot, "run-ops", "exec-live");
assert.equal(polledExited.status, "exited");

const summary = buildRuntimeBoardSummary(repoRoot, "run-ops");
assert.equal(summary.execution_counts.retrying, 1);
assert.ok(summary.board.includes("executions: "));
assert.ok(summary.board.includes("actionable tasks:"));
console.log("runtime-ops.test.mjs: PASS");
