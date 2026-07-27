#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const root = resolve(import.meta.dirname, "..", "..");
const fixtureRoot = mkdtempSync(join(tmpdir(), "opencode-openchamber-sync-"));
const settingsPath = join(fixtureRoot, "settings.json");
const opencodeRoot = join(fixtureRoot, "opencode");

spawnSync("mkdir", ["-p", opencodeRoot], { check: true });
writeFileSync(
  join(opencodeRoot, "opencode.json"),
  JSON.stringify({ model: "{env:OPENCODE_MODEL_DEFAULT}", default_agent: "orchestrator" }),
);
writeFileSync(
  join(opencodeRoot, ".env"),
  [
    "OPENCODE_MODEL_DEFAULT=9router/medium",
    "OPENCODE_MODEL_ORCHESTRATOR=9router/high",
    "OPENCODE_MODEL_DISCOVERY=9router/low",
    "OPENCODE_MODEL_PLANNER=9router/high",
    "OPENCODE_MODEL_DESIGN=9router/high",
    "OPENCODE_MODEL_VISUAL_ASSET=9router/high",
    "OPENCODE_MODEL_REVIEW=9router/high",
    "OPENCODE_MODEL_QUALITY_GATE=9router/high",
    "OPENCODE_MODEL_ADVISORY=9router/high",
    "OPENCODE_MODEL_EXECUTION=9router/high",
    "OPENCODE_MODEL_FAST=9router/low",
  ].join("\n"),
);
writeFileSync(
  settingsPath,
  JSON.stringify({ homeDirectory: "/Users/tester", defaultModel: "old/model", defaultAgent: "build" }),
);

const args = [
  "scripts/sync-openchamber-settings.mjs",
  "--opencode-root",
  opencodeRoot,
  "--openchamber-settings",
  settingsPath,
  "--seed-approved-directories",
];
let result = spawnSync("node", args, { cwd: root, encoding: "utf8" });
assert.equal(result.status, 0, result.stderr || result.stdout);

const settings = JSON.parse(readFileSync(settingsPath, "utf8"));
assert.equal(settings.homeDirectory, "/Users/tester");
assert.equal(settings.defaultModel, "9router/high");
assert.equal(settings.defaultAgent, "orchestrator");
assert.equal(settings.zenModel, "9router/low");
assert.deepEqual(settings.approvedDirectories, [opencodeRoot]);

result = spawnSync("node", [...args, "--check"], { cwd: root, encoding: "utf8" });
assert.equal(result.status, 0, result.stderr || result.stdout);

console.log("sync-openchamber-settings.test: PASS");
