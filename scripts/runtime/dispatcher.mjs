import { getTask, claimTask } from "./task-store.mjs";
import { sendMessage } from "./mailbox-store.mjs";
import { prepareWorkerExecution, getWorkerExecution, launchWorkerExecution } from "./executor.mjs";
import { applyProjectMemoryContext } from "./memory-reuse-loader.mjs";

export function dispatchWorkerTask(projectRoot, runId, payload = {}) {
  const task = getTask(projectRoot, runId, payload.task_id);
  if (!task) throw new Error(`task not found: ${payload.task_id}`);
  const memoryContext = applyProjectMemoryContext(projectRoot, task, payload.prompt ?? "");
  const execution = prepareWorkerExecution(projectRoot, runId, {
    execution_id: payload.execution_id,
    task_id: task.task_id,
    worker_name: payload.worker_name,
    lane: payload.lane ?? task.owner_lane,
    prompt: memoryContext.prompt,
    backend: payload.backend,
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
    },
  });
  return { task: claimedTask, execution, message, memory_context: memoryContext };
}

export function executeDispatchedTask(projectRoot, runId, executionId, options = {}) {
  return launchWorkerExecution(projectRoot, runId, executionId, options);
}

export { getWorkerExecution };
