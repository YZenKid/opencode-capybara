import { basename, join, resolve } from "node:path";

export function normalizeProjectRoot(projectRoot = process.cwd()) {
  return resolve(projectRoot);
}

export function repoSlug(projectRoot = process.cwd()) {
  return basename(normalizeProjectRoot(projectRoot));
}

export function runtimeRoot(projectRoot = process.cwd()) {
  return join(normalizeProjectRoot(projectRoot), ".opencode", "state");
}

export function runsRoot(projectRoot = process.cwd()) {
  return join(runtimeRoot(projectRoot), "runs");
}

export function runDir(projectRoot, runId) {
  return join(runsRoot(projectRoot), runId);
}

export function runFile(projectRoot, runId) {
  return join(runDir(projectRoot, runId), "run.json");
}

export function runEventsFile(projectRoot, runId) {
  return join(runDir(projectRoot, runId), "events.ndjson");
}

export function boardSnapshotFile(projectRoot, runId) {
  return join(runDir(projectRoot, runId), "board.txt");
}

export function boardSnapshotJsonFile(projectRoot, runId) {
  return join(runDir(projectRoot, runId), "board.json");
}

export function tasksRoot(projectRoot, runId) {
  return join(runtimeRoot(projectRoot), "tasks", runId);
}

export function taskFile(projectRoot, runId, taskId) {
  return join(tasksRoot(projectRoot, runId), `${taskId}.json`);
}

export function mailboxRoot(projectRoot, runId) {
  return join(runtimeRoot(projectRoot), "mailbox", runId);
}

export function mailboxWorkerRoot(projectRoot, runId, worker) {
  return join(mailboxRoot(projectRoot, runId), worker);
}

export function mailboxMessageFile(projectRoot, runId, worker, messageId) {
  return join(mailboxWorkerRoot(projectRoot, runId, worker), `${messageId}.json`);
}

export function locksRoot(projectRoot = process.cwd()) {
  return join(runtimeRoot(projectRoot), "locks");
}

export function workerLeaseLockFile(projectRoot, runId, worker) {
  return join(locksRoot(projectRoot), `${runId}--${worker}.lease.json`);
}

export function memoryRoot(projectRoot = process.cwd()) {
  return join(runtimeRoot(projectRoot), "memory");
}

export function projectMemoryFile(projectRoot = process.cwd()) {
  return join(memoryRoot(projectRoot), "project-memory.json");
}

export function sharedRunMemoryRoot(projectRoot, runId) {
  return join(memoryRoot(projectRoot), "runs", runId);
}

export function sharedRunMemoryFile(projectRoot, runId, key) {
  return join(sharedRunMemoryRoot(projectRoot, runId), `${key}.json`);
}

export function worktreeBaseRoot(projectRoot, runId) {
  const root = normalizeProjectRoot(projectRoot);
  return resolve(root, "..", `${repoSlug(root)}.opencode-worktrees`, runId);
}

export function workerExecutionsRoot(projectRoot, runId) {
  return join(runDir(projectRoot, runId), "workers");
}

export function workerExecutionFile(projectRoot, runId, executionId) {
  return join(workerExecutionsRoot(projectRoot, runId), `${executionId}.json`);
}

export function executionLogsRoot(projectRoot, runId) {
  return join(runDir(projectRoot, runId), "logs");
}

export function executionLogDir(projectRoot, runId, executionId) {
  return join(executionLogsRoot(projectRoot, runId), executionId);
}

export function executionStdoutLogFile(projectRoot, runId, executionId) {
  return join(executionLogDir(projectRoot, runId, executionId), "stdout.log");
}

export function executionStderrLogFile(projectRoot, runId, executionId) {
  return join(executionLogDir(projectRoot, runId, executionId), "stderr.log");
}

export function tailSessionsRoot(projectRoot, runId) {
  return join(runDir(projectRoot, runId), "tail-sessions");
}

export function tailSessionFile(projectRoot, runId, sessionId) {
  return join(tailSessionsRoot(projectRoot, runId), `${sessionId}.json`);
}

export function diagnosticsHistoryRoot(projectRoot, runId) {
  return join(runDir(projectRoot, runId), "diagnostics-history");
}

export function diagnosticsSnapshotFile(projectRoot, runId, snapshotId) {
  return join(diagnosticsHistoryRoot(projectRoot, runId), `${snapshotId}.json`);
}

export function dashboardRoot(projectRoot, runId) {
  return join(runDir(projectRoot, runId), "dashboard");
}

export function dashboardTextFile(projectRoot, runId) {
  return join(dashboardRoot(projectRoot, runId), "dashboard.txt");
}

export function dashboardHtmlFile(projectRoot, runId) {
  return join(dashboardRoot(projectRoot, runId), "dashboard.html");
}
