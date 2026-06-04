#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { createRun } from "../runtime/run-store.mjs";
import { createTask, getTask } from "../runtime/task-store.mjs";
import { listMessages } from "../runtime/mailbox-store.mjs";
import { dispatchWorkerTask, getWorkerExecution } from "../runtime/dispatcher.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-dispatch-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "dispatch\n");
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });

createRun(repoRoot, { run_id: "run-dispatch", goal: "Dispatch work", status: "executing" });
createTask(repoRoot, "run-dispatch", {
  task_id: "task-1",
  title: "Implement backend change",
  owner_lane: "@backend",
});
const dispatched = dispatchWorkerTask(repoRoot, "run-dispatch", {
  task_id: "task-1",
  worker_name: "backend-1",
  prompt: "Implement backend change",
});
assert.equal(dispatched.task.status, "claimed");
assert.equal(dispatched.execution.status, "planned");
assert.equal(dispatched.execution.launch_plan.backend, "opencode-subagent");
assert.equal(dispatched.execution.launch_plan.metadata.workspace_mode, "worktree");
assert.equal(getTask(repoRoot, "run-dispatch", "task-1").claimed_by, "backend-1");
assert.equal(listMessages(repoRoot, "run-dispatch", "backend-1").length, 1);
const execution = getWorkerExecution(repoRoot, "run-dispatch", dispatched.execution.execution_id);
assert.equal(execution.worker_name, "backend-1");
assert.match(execution.launch_plan.command_preview, /opencode/);
console.log("runtime-dispatcher.test.mjs: PASS");
