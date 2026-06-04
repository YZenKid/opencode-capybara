#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, appendFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { createRun } from "../runtime/run-store.mjs";
import { prepareWorkerExecution } from "../runtime/executor.mjs";
import { runRuntimeCli } from "../runtime/cli.mjs";
import { acquireLock, readLeaseLock, cleanupStaleLease } from "../runtime/locks.mjs";
import { followExecutionLogLive } from "../runtime/ops-loop.mjs";
import { supervisorTick } from "../runtime/supervisor.mjs";
import { executionStdoutLogFile, workerLeaseLockFile } from "../runtime/state-paths.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-phase9-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "generic repo\n");
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });

createRun(repoRoot, { run_id: "run-phase9", goal: "Phase 9", status: "executing" });
prepareWorkerExecution(repoRoot, "run-phase9", {
  execution_id: "exec-live",
  task_id: "task-1",
  worker_name: "backend-1",
  lane: "@backend",
  prompt: "live",
  workspace_mode: "single"
});
const logPath = executionStdoutLogFile(repoRoot, "run-phase9", "exec-live");
writeFileSync(logPath, "line1\n");
const live = await followExecutionLogLive(repoRoot, "run-phase9", "exec-live", {
  lines: 10,
  poll_ms: 5,
  timeout_ms: 40,
  on_poll: (index) => {
    if (index === 0) appendFileSync(logPath, "line2\n");
  }
});
assert.ok(live.events.length >= 2);
assert.deepEqual(live.events.at(-1).lines.slice(-2), ["line1", "line2"]);

const leasePath = workerLeaseLockFile(repoRoot, "run-phase9", "backend-1");
acquireLock(leasePath, { owner: "supervisor:backend-1", stale_ms: 20, now_ms: 1000 });
const before = readLeaseLock(leasePath);
supervisorTick(repoRoot, "run-phase9", { auto_consume: false, auto_retry: false, poll_executions: false, renew_heartbeats: true, consume_owner: "supervisor", consume_lease_ms: 50 });
const after = readLeaseLock(leasePath);
assert.ok(after.expires_at_ms >= before.expires_at_ms);
assert.ok(after.heartbeat_count >= 1);

const status = await runRuntimeCli(repoRoot, ["lease-status", "--run-id", "run-phase9", "--worker-name", "backend-1"]);
assert.equal(status.lease.lock.owner, "supervisor:backend-1");
const cleanup = cleanupStaleLease(leasePath, { now_ms: after.expires_at_ms + 1 });
assert.equal(cleanup.cleaned, true);
const cliCleanup = await runRuntimeCli(repoRoot, ["lease-cleanup", "--run-id", "run-phase9", "--worker-name", "backend-1", "--force"]);
assert.equal(cliCleanup.cleanup.cleaned || cliCleanup.cleanup.reason === 'missing', true);
const tailCli = await runRuntimeCli(repoRoot, ["tail", "--run-id", "run-phase9", "--execution-id", "exec-live", "--follow", "--timeout-ms", "20", "--poll-ms", "5"]);
assert.ok(tailCli.tail.events.length >= 1);
console.log("runtime-phase9.test.mjs: PASS");
