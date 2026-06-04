#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, appendFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { createRun } from "../runtime/run-store.mjs";
import { prepareWorkerExecution } from "../runtime/executor.mjs";
import { runRuntimeCli } from "../runtime/cli.mjs";
import { acquireLock, sweepRunLeases } from "../runtime/locks.mjs";
import { buildRuntimeDiagnosticsReport } from "../runtime/board.mjs";
import { createTailSession, pollTailSession, stopTailSession } from "../runtime/tail-sessions.mjs";
import { executionStdoutLogFile, tailSessionFile, workerLeaseLockFile } from "../runtime/state-paths.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-phase10-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "generic repo\n");
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });

createRun(repoRoot, { run_id: "run-phase10", goal: "Phase 10", status: "executing" });
prepareWorkerExecution(repoRoot, "run-phase10", {
  execution_id: "exec-1",
  task_id: "task-1",
  worker_name: "backend-1",
  lane: "@backend",
  prompt: "tail",
  workspace_mode: "single"
});
const stdoutLog = executionStdoutLogFile(repoRoot, "run-phase10", "exec-1");
writeFileSync(stdoutLog, "line1\n");
const session = createTailSession(repoRoot, "run-phase10", "exec-1", { session_id: "session-1", lines: 10 });
appendFileSync(stdoutLog, "line2\n");
const poll = await pollTailSession(repoRoot, "run-phase10", "session-1");
assert.equal(poll.session.session_id, "session-1");
assert.deepEqual(poll.latest.lines.slice(-2), ["line1", "line2"]);
assert.equal(stopTailSession(repoRoot, "run-phase10", "session-1").session.status, "stopped");

acquireLock(workerLeaseLockFile(repoRoot, "run-phase10", "backend-1"), { owner: "worker-1", stale_ms: 1, now_ms: 1000 });
acquireLock(workerLeaseLockFile(repoRoot, "run-phase10", "backend-2"), { owner: "worker-2", stale_ms: 5000, now_ms: 1000 });
const sweep = sweepRunLeases(repoRoot, "run-phase10", { now_ms: 2000 });
assert.equal(sweep.cleaned.length, 1);
assert.equal(sweep.cleaned[0].worker, "backend-1");

const report = buildRuntimeDiagnosticsReport(repoRoot, "run-phase10");
assert.ok(report.text.includes("lease summary"));
assert.ok(report.text.includes("RUN run-phase10"));

const cliStart = await runRuntimeCli(repoRoot, ["tail-session-start", "--run-id", "run-phase10", "--execution-id", "exec-1", "--session-id", "cli-session", "--lines", "5"]);
assert.equal(cliStart.session.session_id, "cli-session");
const cliStatus = await runRuntimeCli(repoRoot, ["tail-session-status", "--run-id", "run-phase10", "--session-id", "cli-session"]);
assert.equal(cliStatus.session.session.session_id, "cli-session");
const cliSweep = await runRuntimeCli(repoRoot, ["lease-sweep", "--run-id", "run-phase10", "--force"]);
assert.ok(Array.isArray(cliSweep.sweep.cleaned));
const cliDiag = await runRuntimeCli(repoRoot, ["diagnostics", "--run-id", "run-phase10"]);
assert.ok(cliDiag.diagnostics.text.includes("lease summary"));
console.log("runtime-phase10.test.mjs: PASS");
