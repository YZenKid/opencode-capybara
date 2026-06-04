import { computeRunProgress } from "./verification-loop.mjs";
import { getRun } from "./run-store.mjs";
import { listTasks } from "./task-store.mjs";
import { summarizeMailbox } from "./mailbox-store.mjs";
import { listWorkerExecutions } from "./executor.mjs";
import { listRunLeases } from "./locks.mjs";

function computeNextTasks(tasks = []) {
  const byId = new Map(tasks.map((task) => [task.task_id, task]));
  return tasks.filter((task) => ["pending", "failed"].includes(task.status) && (task.depends_on ?? []).every((depId) => byId.get(depId)?.status === "completed"));
}

function executionCounts(executions = []) {
  const counts = {};
  for (const execution of executions) {
    const key = execution?.status ?? "unknown";
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return counts;
}

export function renderRunBoard({ run, tasks = [], mailbox_summary = { pending: 0, acked: 0, workers: [] }, execution_counts = {}, next_tasks = [] }) {
  const progress = computeRunProgress(tasks);
  const executionSummary = Object.entries(execution_counts).sort(([a], [b]) => a.localeCompare(b)).map(([status, count]) => `${status}:${count}`).join(", ") || "none";
  const nextSummary = next_tasks.length > 0 ? next_tasks.map((task) => task.task_id).join(", ") : "none";
  const lines = [
    `RUN ${run?.run_id ?? "unknown"}`,
    `status: ${run?.status ?? "unknown"}`,
    `goal: ${run?.goal ?? "(missing)"}`,
    `tasks: ${progress.completed}/${progress.total} completed`,
    `failed tasks: ${progress.failed}`,
    `blocked tasks: ${progress.blocked}`,
    `pending mailbox: ${mailbox_summary?.pending ?? 0}`,
    `acked mailbox: ${mailbox_summary?.acked ?? 0}`,
    `executions: ${executionSummary}`,
    `actionable tasks: ${nextSummary}`,
  ];

  if (Array.isArray(mailbox_summary?.workers) && mailbox_summary.workers.length > 0) {
    lines.push(`workers: ${mailbox_summary.workers.join(", ")}`);
  }

  if (tasks.length > 0) {
    lines.push("", "task board:", ...tasks.map((task) => `- ${task?.task_id ?? "unknown"}: ${task?.status ?? "pending"}`));
  }

  return lines.join("\n");
}

export function buildRuntimeBoardSummary(projectRoot, runId) {
  const run = getRun(projectRoot, runId);
  if (!run) throw new Error(`run not found: ${runId}`);
  const tasks = listTasks(projectRoot, runId);
  const mailbox = summarizeMailbox(projectRoot, runId);
  const executions = listWorkerExecutions(projectRoot, runId);
  const counts = executionCounts(executions);
  const nextTasks = computeNextTasks(tasks);
  return {
    run,
    tasks,
    mailbox,
    executions,
    execution_counts: counts,
    next_tasks: nextTasks,
    board: renderRunBoard({ run, tasks, mailbox_summary: mailbox, execution_counts: counts, next_tasks: nextTasks }),
  };
}

export function buildRuntimeDiagnosticsReport(projectRoot, runId) {
  const board = buildRuntimeBoardSummary(projectRoot, runId);
  const leases = listRunLeases(projectRoot, runId);
  const leaseLines = leases.length === 0
    ? ['lease summary: none']
    : [
        'lease summary:',
        ...leases.map((lease) => `- ${lease.worker}: owner=${lease.lock?.owner ?? 'unknown'} expires=${lease.lock?.expires_at_ms ?? 'unknown'} heartbeat=${lease.lock?.heartbeat_count ?? 0}`),
      ];
  return {
    ...board,
    leases,
    text: `${board.board}\n\n${leaseLines.join('\n')}`,
  };
}
