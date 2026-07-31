import { getTask, claimTask } from "./task-store.mjs";
import { sendMessage } from "./mailbox-store.mjs";
import { prepareWorkerExecution, getWorkerExecution, launchWorkerExecution } from "./executor.mjs";
import { validateImagePath } from "./worker-contracts.mjs";

export function dispatchWorkerTask(projectRoot, runId, payload = {}) {
  const task = getTask(projectRoot, runId, payload.task_id);
  if (!task) throw new Error(`task not found: ${payload.task_id}`);
  const image = validateImagePath(payload.image_path);
  if (!image.ok) throw new Error(image.error);
  const execution = prepareWorkerExecution(projectRoot, runId, {
    execution_id: payload.execution_id,
    task_id: task.task_id,
    worker_name: payload.worker_name,
    lane: payload.lane ?? task.owner_lane,
    prompt: payload.prompt,
    backend: payload.backend,
    image_path: image.path,
    workspace_mode: payload.workspace_mode ?? "worktree",
  });
  const claimedTask = claimTask(projectRoot, runId, task.task_id, payload.worker_name);
  const message = sendMessage(projectRoot, runId, {
    from: payload.from ?? "orchestrator",
    to: payload.worker_name,
    type: payload.message_type ?? "task",
    payload: {
      run_id: runId,
      task_id: task.task_id,
      execution_id: execution.execution_id,
      lane: execution.lane,
      prompt: payload.prompt,
      image_path: image.path,
    },
  });
  return { task: claimedTask, execution, message };
}

export function executeDispatchedTask(projectRoot, runId, executionId, options = {}) {
  return launchWorkerExecution(projectRoot, runId, executionId, options);
}

export { getWorkerExecution };
