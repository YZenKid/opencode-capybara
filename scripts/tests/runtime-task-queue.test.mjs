#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createRun } from "../runtime/run-store.mjs";
import { createTask, claimTask, completeTask, failTask, listTasks, getTask } from "../runtime/task-store.mjs";

const projectRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-tasks-"));
createRun(projectRoot, { run_id: "run-beta", goal: "queue test", mode: "maintenance", status: "planning" });
createTask(projectRoot, "run-beta", { task_id: "task-1", title: "discover", owner_lane: "@explorer" });
claimTask(projectRoot, "run-beta", "task-1", "explorer-1");
completeTask(projectRoot, "run-beta", "task-1", { summary: "done" });
createTask(projectRoot, "run-beta", { task_id: "task-2", title: "patch", owner_lane: "@fixer" });
claimTask(projectRoot, "run-beta", "task-2", "fixer-1");
failTask(projectRoot, "run-beta", "task-2", { error: "lint failed" });
assert.equal(getTask(projectRoot, "run-beta", "task-1").status, "completed");
assert.equal(getTask(projectRoot, "run-beta", "task-2").status, "failed");
assert.deepEqual(listTasks(projectRoot, "run-beta").map((item) => item.task_id), ["task-1", "task-2"]);
console.log("runtime-task-queue.test.mjs: PASS");
