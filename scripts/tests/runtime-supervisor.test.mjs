#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, readFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { createRun } from "../runtime/run-store.mjs";
import { createTask, failTask, getTask } from "../runtime/task-store.mjs";
import { sendMessage } from "../runtime/mailbox-store.mjs";
import { prepareWorkerExecution, updateWorkerExecution, launchWorkerExecution, getWorkerExecution } from "../runtime/executor.mjs";
import { supervisorTick } from "../runtime/supervisor.mjs";
import { boardSnapshotFile, executionStdoutLogFile } from "../runtime/state-paths.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-supervisor-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "supervisor\n");
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });

createRun(repoRoot, { run_id: "run-supervisor", goal: "Supervisor loop", status: "executing" });
createTask(repoRoot, "run-supervisor", { task_id: "task-retry", title: "Retry me", owner_lane: "@backend" });
failTask(repoRoot, "run-supervisor", "task-retry", { reason: "boom" });
prepareWorkerExecution(repoRoot, "run-supervisor", {
  execution_id: "exec-retry",
  task_id: "task-retry",
  worker_name: "backend-1",
  lane: "@backend",
  prompt: "Retry task",
  workspace_mode: "single"
});
updateWorkerExecution(repoRoot, "run-supervisor", "exec-retry", (record) => ({ ...record, status: "failed", retry_count: 0 }));
sendMessage(repoRoot, "run-supervisor", { from: "orchestrator", to: "backend-1", type: "task", payload: { task_id: "task-retry" } });

createTask(repoRoot, "run-supervisor", { task_id: "task-log", title: "Log me", owner_lane: "@backend" });
prepareWorkerExecution(repoRoot, "run-supervisor", {
  execution_id: "exec-log",
  task_id: "task-log",
  worker_name: "backend-2",
  lane: "@backend",
  prompt: "Log task",
  workspace_mode: "single"
});
updateWorkerExecution(repoRoot, "run-supervisor", "exec-log", (record) => ({
  ...record,
  launch_plan: {
    ...record.launch_plan,
    command: process.execPath,
    args: ["-e", "process.stdout.write('SUPERVISOR_LOG_OK\\n'); setTimeout(() => process.exit(0), 50)"]
  }
}));
launchWorkerExecution(repoRoot, "run-supervisor", "exec-log", { spawn_process: true });
await new Promise((resolve) => setTimeout(resolve, 120));

const tick = supervisorTick(repoRoot, "run-supervisor", { max_retries: 2, auto_consume: true, auto_retry: true, poll_executions: true });
assert.equal(getTask(repoRoot, "run-supervisor", "task-retry").status, "pending");
assert.equal(getWorkerExecution(repoRoot, "run-supervisor", "exec-retry").status, "retrying");
assert.ok(tick.retried.length >= 1);
assert.ok(tick.consumed.length >= 1);
assert.ok(tick.polled.length >= 1);
assert.ok(existsSync(boardSnapshotFile(repoRoot, "run-supervisor")));
assert.match(readFileSync(boardSnapshotFile(repoRoot, "run-supervisor"), "utf8"), /executions:/);
const stdoutPath = executionStdoutLogFile(repoRoot, "run-supervisor", "exec-log");
assert.ok(existsSync(stdoutPath));
let stdout = "";
for (let attempt = 0; attempt < 10; attempt += 1) {
  stdout = readFileSync(stdoutPath, "utf8");
  if (stdout.includes("SUPERVISOR_LOG_OK")) break;
  await new Promise((resolve) => setTimeout(resolve, 50));
}
assert.match(stdout, /SUPERVISOR_LOG_OK/);
console.log("runtime-supervisor.test.mjs: PASS");
