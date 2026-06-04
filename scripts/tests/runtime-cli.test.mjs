#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createRun } from "../runtime/run-store.mjs";
import { createTask } from "../runtime/task-store.mjs";
import { runRuntimeCli } from "../runtime/cli.mjs";

const projectRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-cli-"));
const created = await runRuntimeCli(projectRoot, ["create", "--run-id", "run-cli", "--goal", "Fix regression", "--mode", "maintenance", "--json"]);
assert.equal(created.run.run_id, "run-cli");
assert.equal(created.run.status, "planning");

const status = await runRuntimeCli(projectRoot, ["status", "--run-id", "run-cli", "--json"]);
assert.equal(status.run.run_id, "run-cli");
assert.equal(status.tasks.length, 0);

createTask(projectRoot, "run-cli", {
  task_id: "task-1",
  title: "Investigate issue",
  owner_lane: "@fixer",
});
createTask(projectRoot, "run-cli", {
  task_id: "task-2",
  title: "Patch issue",
  owner_lane: "@fixer",
  depends_on: ["task-1"],
});
createRun(projectRoot, { run_id: "run-continue", goal: "Continue test", status: "executing" });
createTask(projectRoot, "run-continue", {
  task_id: "task-a",
  title: "First actionable",
  owner_lane: "@fixer",
});
createTask(projectRoot, "run-continue", {
  task_id: "task-b",
  title: "Blocked until a completes",
  owner_lane: "@backend",
  depends_on: ["task-a"],
});
const continued = await runRuntimeCli(projectRoot, ["continue", "--run-id", "run-continue", "--json"]);
assert.equal(continued.run.run_id, "run-continue");
assert.deepEqual(continued.next_tasks.map((task) => task.task_id), ["task-a"]);
assert.equal(continued.mailbox.pending, 0);
console.log("runtime-cli.test.mjs: PASS");
