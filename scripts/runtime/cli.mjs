#!/usr/bin/env node
import { buildRuntimeBoardSummary, buildRuntimeDiagnosticsReport } from "./board.mjs";
import { continueRun, getRunStatusView } from "./continue-run.mjs";
import { dispatchWorkerTask, executeDispatchedTask } from "./dispatcher.mjs";
import { prepareWorkerExecution } from "./executor.mjs";
import { cleanupStaleLease, readLeaseLock, renewLockHeartbeat, sweepRunLeases } from "./locks.mjs";
import { consumeWorkerMailbox, followExecutionLog, followExecutionLogLive, pollRunExecutions, retryFailedTask, tailExecutionLog } from "./ops-loop.mjs";
import { createRun } from "./run-store.mjs";
import { tailSessionFile, workerLeaseLockFile } from "./state-paths.mjs";
import { supervisorLoop, supervisorTick, watchBoard } from "./supervisor.mjs";
import { createTailSession, getTailSession, pollTailSession, stopTailSession } from "./tail-sessions.mjs";

function parseArgs(argv) {
  const flags = {};
  const positionals = [];
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value.startsWith("--")) {
      const key = value.slice(2).replace(/-/g, "_");
      const next = argv[index + 1];
      if (!next || next.startsWith("--")) {
        flags[key] = true;
      } else {
        flags[key] = next;
        index += 1;
      }
    } else {
      positionals.push(value);
    }
  }
  return { command: positionals[0], flags };
}

function requireFlag(flags, key) {
  if (!flags[key]) throw new Error(`missing required flag --${key.replace(/_/g, "-")}`);
  return flags[key];
}

function asInt(value, fallback) {
  if (value === undefined || value === null || value === true) return fallback;
  const parsed = Number.parseInt(String(value), 10);
  return Number.isNaN(parsed) ? fallback : parsed;
}

async function resultFor(command, projectRoot, flags) {
  switch (command) {
    case "create": {
      const run = createRun(projectRoot, {
        run_id: requireFlag(flags, "run_id"),
        goal: requireFlag(flags, "goal"),
        mode: flags.mode ?? "maintenance",
        status: flags.status ?? "planning",
        next_step: flags.next_step ?? null,
      });
      return { ok: true, command, run };
    }
    case "status":
      return { ok: true, command, ...getRunStatusView(projectRoot, requireFlag(flags, "run_id")) };
    case "continue":
      return { ok: true, command, ...continueRun(projectRoot, requireFlag(flags, "run_id")) };
    case "dispatch":
      return {
        ok: true,
        command,
        ...dispatchWorkerTask(projectRoot, requireFlag(flags, "run_id"), {
          task_id: requireFlag(flags, "task_id"),
          worker_name: requireFlag(flags, "worker_name"),
          prompt: requireFlag(flags, "prompt"),
          lane: flags.lane,
          backend: flags.backend,
          workspace_mode: flags.workspace_mode ?? "worktree",
        }),
      };
    case "execute": {
      if (flags.execution_id) {
        return {
          ok: true,
          command,
          execution: executeDispatchedTask(projectRoot, requireFlag(flags, "run_id"), flags.execution_id, {
            spawn_process: flags.spawn === true,
          }),
        };
      }
      return {
        ok: true,
        command,
        execution: prepareWorkerExecution(projectRoot, requireFlag(flags, "run_id"), {
          task_id: flags.task_id ?? null,
          worker_name: requireFlag(flags, "worker_name"),
          lane: requireFlag(flags, "lane"),
          prompt: requireFlag(flags, "prompt"),
          backend: flags.backend,
          workspace_mode: flags.workspace_mode ?? "worktree",
        }),
      };
    }
    case "board": {
      const runId = requireFlag(flags, "run_id");
      if (flags.watch === true || flags.ticks) {
        const snapshots = await watchBoard(projectRoot, runId, {
          ticks: asInt(flags.ticks, 2),
          interval_ms: asInt(flags.interval_ms, 250),
        });
        return { ok: true, command, snapshots };
      }
      return { ok: true, command, board: buildRuntimeBoardSummary(projectRoot, runId) };
    }
    case "poll":
      return { ok: true, command, executions: pollRunExecutions(projectRoot, requireFlag(flags, "run_id")) };
    case "retry":
      return {
        ok: true,
        command,
        retry: retryFailedTask(projectRoot, requireFlag(flags, "run_id"), requireFlag(flags, "task_id"), {
          worker_name: flags.worker_name,
          execution_id: requireFlag(flags, "execution_id"),
          max_attempts: asInt(flags.max_attempts, 1),
        }),
      };
    case "consume":
      return {
        ok: true,
        command,
        consume: consumeWorkerMailbox(projectRoot, requireFlag(flags, "run_id"), requireFlag(flags, "worker_name")),
      };
    case "heartbeat": {
      const runId = requireFlag(flags, "run_id");
      const worker = requireFlag(flags, "worker_name");
      const owner = requireFlag(flags, "owner");
      return {
        ok: true,
        command,
        heartbeat: renewLockHeartbeat(workerLeaseLockFile(projectRoot, runId, worker), owner, {
          stale_ms: asInt(flags.lease_ms, 30000),
        }),
      };
    }
    case "lease-status": {
      const runId = requireFlag(flags, "run_id");
      const worker = requireFlag(flags, "worker_name");
      return {
        ok: true,
        command,
        lease: {
          path: workerLeaseLockFile(projectRoot, runId, worker),
          lock: readLeaseLock(workerLeaseLockFile(projectRoot, runId, worker)),
        },
      };
    }
    case "lease-cleanup": {
      const runId = requireFlag(flags, "run_id");
      const worker = requireFlag(flags, "worker_name");
      return {
        ok: true,
        command,
        cleanup: cleanupStaleLease(workerLeaseLockFile(projectRoot, runId, worker), {
          force: flags.force === true,
        }),
      };
    }
    case "lease-sweep": {
      const runId = requireFlag(flags, "run_id");
      return {
        ok: true,
        command,
        sweep: sweepRunLeases(projectRoot, runId, { force: flags.force === true }),
      };
    }
    case "diagnostics": {
      return {
        ok: true,
        command,
        diagnostics: buildRuntimeDiagnosticsReport(projectRoot, requireFlag(flags, "run_id")),
      };
    }
    case "tail-session-start": {
      const runId = requireFlag(flags, "run_id");
      return {
        ok: true,
        command,
        session: createTailSession(projectRoot, runId, requireFlag(flags, "execution_id"), {
          session_id: flags.session_id,
          stream: flags.stream ?? "stdout",
          lines: asInt(flags.lines, 20),
        }),
      };
    }
    case "tail-session-status": {
      const runId = requireFlag(flags, "run_id");
      return {
        ok: true,
        command,
        session: await pollTailSession(projectRoot, runId, requireFlag(flags, "session_id")),
      };
    }
    case "tail-session-stop": {
      const runId = requireFlag(flags, "run_id");
      return {
        ok: true,
        command,
        session: stopTailSession(projectRoot, runId, requireFlag(flags, "session_id")),
      };
    }
    case "tail": {
      const runId = requireFlag(flags, "run_id");
      const executionId = requireFlag(flags, "execution_id");
      if (flags.follow === true && (flags.timeout_ms || flags.poll_ms) && !flags.ticks) {
        return {
          ok: true,
          command,
          tail: await followExecutionLogLive(projectRoot, runId, executionId, {
            stream: flags.stream ?? "stdout",
            lines: asInt(flags.lines, 20),
            poll_ms: asInt(flags.poll_ms, 250),
            timeout_ms: asInt(flags.timeout_ms, 2000),
          }),
        };
      }
      if (flags.follow === true || flags.ticks) {
        return {
          ok: true,
          command,
          tail: await followExecutionLog(projectRoot, runId, executionId, {
            stream: flags.stream ?? "stdout",
            lines: asInt(flags.lines, 20),
            ticks: asInt(flags.ticks, 2),
            interval_ms: asInt(flags.interval_ms, 250),
          }),
        };
      }
      return {
        ok: true,
        command,
        tail: tailExecutionLog(projectRoot, runId, executionId, {
          stream: flags.stream ?? "stdout",
          lines: asInt(flags.lines, 20),
        }),
      };
    }
    case "supervise": {
      const runId = requireFlag(flags, "run_id");
      const options = {
        ticks: asInt(flags.ticks, 1),
        interval_ms: asInt(flags.interval_ms, 250),
        max_retries: asInt(flags.max_retries, 1),
        auto_consume: flags.auto_consume !== false,
        auto_retry: flags.auto_retry !== false,
        poll_executions: flags.poll_executions !== false,
        retry_base_ms: asInt(flags.retry_base_ms, 1000),
        retry_multiplier: asInt(flags.retry_multiplier, 2),
        retry_max_ms: asInt(flags.retry_max_ms, 60000),
        retry_jitter_ratio: Number(flags.retry_jitter_ratio ?? 0),
        consume_lease_ms: asInt(flags.consume_lease_ms, 30000),
        renew_heartbeats: flags.renew_heartbeats === true,
      };
      if (flags.loop === true || flags.ticks) {
        return { ok: true, command, results: await supervisorLoop(projectRoot, runId, options) };
      }
      return { ok: true, command, tick: supervisorTick(projectRoot, runId, options) };
    }
    default:
      throw new Error(`unsupported command: ${command ?? "(missing)"}`);
  }
}

export async function runRuntimeCli(projectRoot, argv) {
  const { command, flags } = parseArgs(argv);
  return resultFor(command, projectRoot, flags);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try {
    const { flags } = parseArgs(process.argv.slice(2));
    const projectRoot = flags.project_root ? String(flags.project_root) : process.cwd();
    const output = await runRuntimeCli(projectRoot, process.argv.slice(2));
    console.log(JSON.stringify(output, null, 2));
  } catch (error) {
    console.error(error.message);
    process.exit(1);
  }
}
