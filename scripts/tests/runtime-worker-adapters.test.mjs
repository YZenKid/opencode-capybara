#!/usr/bin/env node
import assert from "node:assert/strict";
import { writeFileSync, rmSync } from "node:fs";
import { validateWorkerSpec, pickDefaultBackend } from "../runtime/worker-contracts.mjs";
import { buildWorkerLaunchPlan } from "../runtime/worker-launch.mjs";

const imagePath = "/tmp/runtime-worker-adapter.png";
writeFileSync(imagePath, "image");

const spec = {
  worker_name: "backend-1",
  lane: "@fixer",
  backend: "opencode-subagent",
  prompt: "Implement endpoint",
  run_id: "run-workers",
  project_root: "/tmp/project",
  image_path: imagePath,
};
assert.equal(validateWorkerSpec(spec).ok, true);
assert.equal(validateWorkerSpec({ ...spec, image_path: "/tmp/missing.png" }).ok, false);
assert.equal(validateWorkerSpec({ ...spec, image_path: "/tmp/runtime-worker-adapter.txt" }).ok, false);
assert.equal(pickDefaultBackend("@designer"), "external-cli-claude");

const prevWrapper = process.env.OPENCHAMBER_OPENCODE_PATH;
const prevAttach = process.env.OPENCODE_ATTACH_URL;
process.env.OPENCHAMBER_OPENCODE_PATH = "/tmp/opencode-with-env";
process.env.OPENCODE_ATTACH_URL = "http://127.0.0.1:51777";

const plan = buildWorkerLaunchPlan(spec);
assert.equal(plan.backend, "opencode-subagent");
assert.equal(plan.command, "/tmp/opencode-with-env");
assert.deepEqual(plan.args.slice(0, 8), [
  "run",
  "--attach",
  "http://127.0.0.1:51777",
  "--dir",
  "/tmp/project",
  "--file",
  imagePath,
  "--agent",
]);
assert.match(plan.command_preview, /--attach/);
const sessionPlan = buildWorkerLaunchPlan({ ...spec, backend: "opencode-session" });
assert.equal(sessionPlan.args.includes("--file"), false);
rmSync(imagePath, { force: true });

if (prevWrapper === undefined) delete process.env.OPENCHAMBER_OPENCODE_PATH;
else process.env.OPENCHAMBER_OPENCODE_PATH = prevWrapper;
if (prevAttach === undefined) delete process.env.OPENCODE_ATTACH_URL;
else process.env.OPENCODE_ATTACH_URL = prevAttach;

console.log("runtime-worker-adapters.test.mjs: PASS");
