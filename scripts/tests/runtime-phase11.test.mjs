#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { createRun } from "../runtime/run-store.mjs";
import { prepareWorkerExecution } from "../runtime/executor.mjs";
import { runRuntimeCli } from "../runtime/cli.mjs";
import { createTailSession, collectTailSessions } from "../runtime/tail-sessions.mjs";
import { buildRuntimeDiagnosticsReport, exportRuntimeDashboard, writeDiagnosticsSnapshot } from "../runtime/board.mjs";
import { dashboardHtmlFile, dashboardTextFile, diagnosticsSnapshotFile, executionStdoutLogFile } from "../runtime/state-paths.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-phase11-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "generic repo\n");
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });

createRun(repoRoot, { run_id: "run-phase11", goal: "Phase 11", status: "executing" });
prepareWorkerExecution(repoRoot, "run-phase11", {
  execution_id: "exec-1",
  task_id: "task-1",
  worker_name: "backend-1",
  lane: "@backend",
  prompt: "tail",
  workspace_mode: "single"
});
writeFileSync(executionStdoutLogFile(repoRoot, "run-phase11", "exec-1"), "line1\n");
createTailSession(repoRoot, "run-phase11", "exec-1", { session_id: "old-session" });
const gc = collectTailSessions(repoRoot, "run-phase11", { now_ms: Date.now() + 10_000, max_age_ms: 1, include_stopped: true });
assert.equal(gc.removed.length, 1);

const snapshot = writeDiagnosticsSnapshot(repoRoot, "run-phase11", { snapshot_id: "snap-1" });
assert.equal(snapshot.snapshot_id, "snap-1");
const report = buildRuntimeDiagnosticsReport(repoRoot, "run-phase11");
assert.ok(report.text.includes("RUN run-phase11"));
const dashboard = exportRuntimeDashboard(repoRoot, "run-phase11", { snapshot_id: "dash-1" });
assert.ok(dashboard.text_path.endsWith("dashboard.txt"));
assert.ok(dashboard.html_path.endsWith("dashboard.html"));

const cliSnap = await runRuntimeCli(repoRoot, ["diagnostics-snapshot", "--run-id", "run-phase11", "--snapshot-id", "snap-cli"]);
assert.equal(cliSnap.snapshot.snapshot_id, "snap-cli");
const cliDash = await runRuntimeCli(repoRoot, ["dashboard-export", "--run-id", "run-phase11", "--snapshot-id", "dash-cli"]);
assert.ok(cliDash.dashboard.text_path.endsWith("dashboard.txt"));
const cliGc = await runRuntimeCli(repoRoot, ["tail-session-gc", "--run-id", "run-phase11", "--max-age-ms", "0", "--include-stopped"]);
assert.ok(Array.isArray(cliGc.gc.removed));
console.log("runtime-phase11.test.mjs: PASS");
