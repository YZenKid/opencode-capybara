#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { createRun } from "../runtime/run-store.mjs";
import { createTask, failTask } from "../runtime/task-store.mjs";
import { sendMessage } from "../runtime/mailbox-store.mjs";
import { prepareWorkerExecution, updateWorkerExecution } from "../runtime/executor.mjs";
import { runRuntimeCli } from "../runtime/cli.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-cli-ops-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "cli ops\n");
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });

createRun(repoRoot, { run_id: "run-cli-ops", goal: "CLI ops", status: "executing" });
createTask(repoRoot, "run-cli-ops", { task_id: "task-1", title: "Retry from cli", owner_lane: "@backend" });
failTask(repoRoot, "run-cli-ops", "task-1", { reason: "boom" });
prepareWorkerExecution(repoRoot, "run-cli-ops", {
  execution_id: "exec-1",
  task_id: "task-1",
  worker_name: "backend-1",
  lane: "@backend",
  prompt: "Retry from CLI",
  workspace_mode: "single",
});
updateWorkerExecution(repoRoot, "run-cli-ops", "exec-1", (record) => ({ ...record, status: "failed", retry_count: 0 }));
sendMessage(repoRoot, "run-cli-ops", {
  from: "orchestrator",
  to: "backend-1",
  type: "task",
  payload: { task_id: "task-1", execution_id: "exec-1" },
});

const retryResult = await runRuntimeCli(repoRoot, [
  "retry",
  "--run-id", "run-cli-ops",
  "--task-id", "task-1",
  "--worker-name", "backend-1",
  "--execution-id", "exec-1",
  "--max-attempts", "2",
]);
assert.equal(retryResult.retry.execution.retry_count, 1);

const consumeResult = await runRuntimeCli(repoRoot, [
  "consume",
  "--run-id", "run-cli-ops",
  "--worker-name", "backend-1",
]);
assert.equal(consumeResult.consume.message.status, "acked");

const pollResult = await runRuntimeCli(repoRoot, ["poll", "--run-id", "run-cli-ops"]);
assert.ok(Array.isArray(pollResult.executions));

const boardResult = await runRuntimeCli(repoRoot, ["board", "--run-id", "run-cli-ops"]);
assert.match(boardResult.board.board, /RUN run-cli-ops/);
assert.match(boardResult.board.board, /actionable tasks:/);

const superviseResult = await runRuntimeCli(repoRoot, ["supervise", "--run-id", "run-cli-ops", "--max-retries", "2"]);
assert.ok(superviseResult.tick);
console.log("runtime-cli-ops.test.mjs: PASS");
