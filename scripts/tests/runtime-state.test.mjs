#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { acquireLock, releaseLock } from "../runtime/locks.mjs";
import { createRun, getRun, updateRun, listRuns } from "../runtime/run-store.mjs";
import { readJson } from "../runtime/state-io.mjs";

const projectRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-state-"));
const run = createRun(projectRoot, {
  run_id: "run-alpha",
  goal: "stabilize runtime foundation",
  mode: "maintenance",
  status: "planning",
});
assert.equal(run.run_id, "run-alpha");
assert.equal(getRun(projectRoot, "run-alpha").goal, "stabilize runtime foundation");
updateRun(projectRoot, "run-alpha", (current) => ({ ...current, status: "executing", next_step: "task-1" }));
const updated = getRun(projectRoot, "run-alpha");
assert.equal(updated.status, "executing");
assert.equal(updated.next_step, "task-1");
assert.deepEqual(listRuns(projectRoot).map((item) => item.run_id), ["run-alpha"]);
const lockPath = join(projectRoot, ".opencode", "state", "locks", "runtime.lock.json");
const first = acquireLock(lockPath, { owner: "test-owner", stale_ms: 10 });
assert.equal(first.acquired, true);
const second = acquireLock(lockPath, { owner: "other-owner", stale_ms: 10 });
assert.equal(second.acquired, false);
releaseLock(lockPath, "test-owner");
assert.equal(readJson(lockPath, null), null);
console.log("runtime-state.test.mjs: PASS");
