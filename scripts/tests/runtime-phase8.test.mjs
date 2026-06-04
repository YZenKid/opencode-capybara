#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, appendFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { createRun } from "../runtime/run-store.mjs";
import { prepareWorkerExecution } from "../runtime/executor.mjs";
import { runRuntimeCli } from "../runtime/cli.mjs";
import { computeRetryDelayMs, followExecutionLog } from "../runtime/ops-loop.mjs";
import { acquireLock, renewLockHeartbeat } from "../runtime/locks.mjs";
import { executionStdoutLogFile, workerLeaseLockFile } from "../runtime/state-paths.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-phase8-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "generic repo\n");
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });

createRun(repoRoot, { run_id: "run-phase8", goal: "Phase 8", status: "executing" });
prepareWorkerExecution(repoRoot, "run-phase8", {
  execution_id: "exec-follow",
  task_id: "task-1",
  worker_name: "backend-1",
  lane: "@backend",
  prompt: "follow",
  workspace_mode: "single"
});
const stdoutLog = executionStdoutLogFile(repoRoot, "run-phase8", "exec-follow");
writeFileSync(stdoutLog, "line1\n");
const followed = await followExecutionLog(repoRoot, "run-phase8", "exec-follow", {
  lines: 5,
  ticks: 2,
  interval_ms: 1,
  on_tick: (index) => {
    if (index === 0) appendFileSync(stdoutLog, "line2\n");
  }
});
assert.equal(followed.snapshots.length, 2);
assert.deepEqual(followed.snapshots.at(-1).lines.slice(-2), ["line1", "line2"]);

const jittered = computeRetryDelayMs(2, { base_ms: 100, multiplier: 2, max_ms: 1000, jitter_ratio: 0.25, jitter_seed: "alpha" });
assert.equal(jittered, computeRetryDelayMs(2, { base_ms: 100, multiplier: 2, max_ms: 1000, jitter_ratio: 0.25, jitter_seed: "alpha" }));
assert.notEqual(jittered, computeRetryDelayMs(2, { base_ms: 100, multiplier: 2, max_ms: 1000 }));

const leasePath = workerLeaseLockFile(repoRoot, "run-phase8", "backend-1");
const acquired = acquireLock(leasePath, { owner: "worker-1", stale_ms: 50, now_ms: 1000 });
assert.equal(acquired.acquired, true);
const renewed = renewLockHeartbeat(leasePath, "worker-1", { stale_ms: 50, now_ms: 1050 });
assert.equal(renewed.renewed, true);
assert.equal(renewed.lock.expires_at_ms, 1100);

const cliTail = await runRuntimeCli(repoRoot, ["tail", "--run-id", "run-phase8", "--execution-id", "exec-follow", "--follow", "--ticks", "2", "--interval-ms", "1"]);
assert.equal(cliTail.tail.snapshots.length, 2);
const cliHeartbeat = await runRuntimeCli(repoRoot, ["heartbeat", "--run-id", "run-phase8", "--worker-name", "backend-1", "--owner", "worker-1", "--lease-ms", "50"]);
assert.equal(cliHeartbeat.heartbeat.renewed, true);
console.log("runtime-phase8.test.mjs: PASS");
