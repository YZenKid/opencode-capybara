#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function run(command, args) {
  return spawnSync(command, args, {
    cwd: root,
    encoding: "utf8",
    stdio: "inherit",
  });
}

function log(message = "") {
  process.stdout.write(`${message}\n`);
}

function main() {
  log("opencode-capybara post-update refresh");
  log("Refreshing agent model sync, generated docs, OpenChamber sync, and doctor checks.");

  const agentSyncResult = run("node", ["scripts/sync-agent-models.mjs"]);
  if (agentSyncResult.status !== 0) {
    process.exitCode = agentSyncResult.status || 1;
    return;
  }

  const generatedDocsResult = run("node", ["scripts/generate-generated-docs.mjs"]);
  if (generatedDocsResult.status !== 0) {
    process.exitCode = generatedDocsResult.status || 1;
    return;
  }

  const syncResult = run("node", ["scripts/sync-openchamber-settings.mjs", "--seed-approved-directories"]);
  if (syncResult.status !== 0) {
    process.exitCode = syncResult.status || 1;
    return;
  }

  const doctorResult = run("node", ["scripts/doctor.mjs"]);
  if (doctorResult.status !== 0) {
    process.exitCode = doctorResult.status || 1;
    return;
  }

  log("Done.");
}

main();
