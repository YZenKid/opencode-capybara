import { getRun, updateRun } from "./run-store.mjs";
import { listTasks } from "./task-store.mjs";
import { summarizeMailbox } from "./mailbox-store.mjs";
import { renderRunBoard } from "./board.mjs";

function dependencyMap(tasks) {
  return new Map(tasks.map((task) => [task.task_id, task]));
}

function isActionable(task, byId) {
  if (!["pending", "failed"].includes(task.status)) return false;
  const dependsOn = task.depends_on ?? [];
  return dependsOn.every((depId) => byId.get(depId)?.status === "completed");
}

export function computeNextTasks(projectRoot, runId) {
  const tasks = listTasks(projectRoot, runId);
  const byId = dependencyMap(tasks);
  return tasks.filter((task) => isActionable(task, byId));
}

export function getRunStatusView(projectRoot, runId) {
  const run = getRun(projectRoot, runId);
  if (!run) throw new Error(`run not found: ${runId}`);
  const tasks = listTasks(projectRoot, runId);
  const mailbox = summarizeMailbox(projectRoot, runId);
  return {
    run,
    tasks,
    mailbox,
    next_tasks: computeNextTasks(projectRoot, runId),
    board: renderRunBoard({ run, tasks, mailbox_summary: mailbox }),
  };
}

export function continueRun(projectRoot, runId) {
  const view = getRunStatusView(projectRoot, runId);
  const first = view.next_tasks[0] ?? null;
  const run = updateRun(projectRoot, runId, (current) => ({
    ...current,
    status: current.status === "planning" ? "executing" : current.status,
    next_step: first ? `dispatch ${first.task_id}` : current.next_step ?? null,
  }));
  return {
    ...view,
    run,
    board: renderRunBoard({ run, tasks: view.tasks, mailbox_summary: view.mailbox }),
  };
}
