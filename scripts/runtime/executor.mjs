import { randomUUID } from "node:crypto";
import { spawn } from "node:child_process";
import { closeSync, openSync } from "node:fs";
import { dirname } from "node:path";
import { appendNdjson, ensureDir, listJson, readJson, writeJsonAtomic } from "./state-io.mjs";
import { createWorkerWorktree } from "./worktree-plan.mjs";
import { buildWorkerLaunchPlan } from "./worker-launch.mjs";
import {
  executionLogDir,
  executionStderrLogFile,
  executionStdoutLogFile,
  runEventsFile,
  workerExecutionFile,
  workerExecutionsRoot,
} from "./state-paths.mjs";

function timestamp() {
  return new Date().toISOString();
}

export function getWorkerExecution(projectRoot, runId, executionId) {
  return readJson(workerExecutionFile(projectRoot, runId, executionId), null);
}

export function listWorkerExecutions(projectRoot, runId) {
  return listJson(workerExecutionsRoot(projectRoot, runId)).map((item) => item.data);
}

export function updateWorkerExecution(projectRoot, runId, executionId, updater) {
  const current = getWorkerExecution(projectRoot, runId, executionId);
  if (!current) throw new Error(`worker execution not found: ${executionId}`);
  const updated = { ...updater(current), updated_at: timestamp() };
  writeJsonAtomic(workerExecutionFile(projectRoot, runId, executionId), updated);
  appendNdjson(runEventsFile(projectRoot, runId), {
    timestamp: updated.updated_at,
    type: "worker-execution-updated",
    run_id: runId,
    execution_id: executionId,
    status: updated.status,
  });
  return updated;
}

export function prepareWorkerExecution(projectRoot, runId, spec = {}) {
  const workspaceMode = spec.workspace_mode ?? "worktree";
  const workspace = workspaceMode === "worktree"
    ? createWorkerWorktree(projectRoot, runId, spec.worker_name)
    : { repo_root: projectRoot, worktree_path: null, worktree_branch: null, workspace_mode: "single", worktree_created: false };

  const executionId = spec.execution_id ?? randomUUID();
  const launchPlan = buildWorkerLaunchPlan({
    ...spec,
    run_id: runId,
    project_root: projectRoot,
    worktree_path: workspace.worktree_path ?? undefined,
    worktree_branch: workspace.worktree_branch ?? undefined,
    workspace_mode: workspace.workspace_mode,
  });

  const now = timestamp();
  const stdoutLog = executionStdoutLogFile(projectRoot, runId, executionId);
  const stderrLog = executionStderrLogFile(projectRoot, runId, executionId);
  ensureDir(executionLogDir(projectRoot, runId, executionId));
  const record = {
    execution_id: executionId,
    run_id: runId,
    worker_name: spec.worker_name,
    lane: spec.lane,
    task_id: spec.task_id ?? null,
    prompt: spec.prompt,
    status: "planned",
    backend: launchPlan.backend,
    launch_plan: launchPlan,
    workspace,
    logs: {
      dir: executionLogDir(projectRoot, runId, executionId),
      stdout: stdoutLog,
      stderr: stderrLog,
    },
    spawned_pid: null,
    created_at: now,
    updated_at: now,
  };

  ensureDir(workerExecutionsRoot(projectRoot, runId));
  writeJsonAtomic(workerExecutionFile(projectRoot, runId, executionId), record);
  appendNdjson(runEventsFile(projectRoot, runId), {
    timestamp: now,
    type: "worker-execution-created",
    run_id: runId,
    execution_id: executionId,
    task_id: record.task_id,
    worker_name: record.worker_name,
    backend: record.backend,
  });
  return record;
}

export function launchWorkerExecution(projectRoot, runId, executionId, { spawn_process = false } = {}) {
  const current = getWorkerExecution(projectRoot, runId, executionId);
  if (!current) throw new Error(`worker execution not found: ${executionId}`);

  if (!spawn_process) {
    return updateWorkerExecution(projectRoot, runId, executionId, (record) => ({
      ...record,
      status: "ready",
    }));
  }

  ensureDir(dirname(current.logs.stdout));
  ensureDir(dirname(current.logs.stderr));
  const stdoutFd = openSync(current.logs.stdout, "a");
  const stderrFd = openSync(current.logs.stderr, "a");

  try {
    const child = spawn(current.launch_plan.command, current.launch_plan.args, {
      cwd: current.launch_plan.cwd,
      stdio: ["ignore", stdoutFd, stderrFd],
      detached: true,
    });
    child.unref();
    return updateWorkerExecution(projectRoot, runId, executionId, (record) => ({
      ...record,
      status: "spawned",
      spawned_pid: child.pid ?? null,
      spawned_at: timestamp(),
    }));
  } finally {
    closeSync(stdoutFd);
    closeSync(stderrFd);
  }
}
