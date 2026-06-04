#!/usr/bin/env node
import assert from "node:assert/strict";
import { validateWorkerSpec, pickDefaultBackend } from "../runtime/worker-contracts.mjs";
import { buildWorkerLaunchPlan } from "../runtime/worker-launch.mjs";

const spec = {
  worker_name: "backend-1",
  lane: "@backend",
  backend: "opencode-subagent",
  prompt: "Implement endpoint",
  run_id: "run-workers",
  project_root: "/tmp/project",
};
assert.equal(validateWorkerSpec(spec).ok, true);
assert.equal(pickDefaultBackend("@designer"), "external-cli-claude");
const plan = buildWorkerLaunchPlan(spec);
assert.equal(plan.backend, "opencode-subagent");
assert.match(plan.command_preview, /opencode/);
console.log("runtime-worker-adapters.test.mjs: PASS");
