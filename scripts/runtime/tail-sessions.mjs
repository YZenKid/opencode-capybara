import { randomUUID } from "node:crypto";
import { readJson, writeJsonAtomic } from "./state-io.mjs";
import { tailExecutionLog } from "./ops-loop.mjs";
import { tailSessionFile } from "./state-paths.mjs";

function nowIso() {
  return new Date().toISOString();
}

export function createTailSession(projectRoot, runId, executionId, { session_id = randomUUID(), stream = "stdout", lines = 20 } = {}) {
  const session = {
    session_id,
    run_id: runId,
    execution_id: executionId,
    stream,
    lines,
    status: "active",
    created_at: nowIso(),
    updated_at: nowIso(),
    last_event: null,
  };
  writeJsonAtomic(tailSessionFile(projectRoot, runId, session_id), session);
  return session;
}

export function getTailSession(projectRoot, runId, sessionId) {
  return readJson(tailSessionFile(projectRoot, runId, sessionId), null);
}

export async function pollTailSession(projectRoot, runId, sessionId) {
  const session = getTailSession(projectRoot, runId, sessionId);
  if (!session) throw new Error(`tail session not found: ${sessionId}`);
  const latest = tailExecutionLog(projectRoot, runId, session.execution_id, { stream: session.stream, lines: session.lines });
  const updated = {
    ...session,
    updated_at: nowIso(),
    last_event: latest,
  };
  writeJsonAtomic(tailSessionFile(projectRoot, runId, sessionId), updated);
  return { session: updated, latest };
}

export function stopTailSession(projectRoot, runId, sessionId) {
  const session = getTailSession(projectRoot, runId, sessionId);
  if (!session) throw new Error(`tail session not found: ${sessionId}`);
  const updated = {
    ...session,
    status: "stopped",
    updated_at: nowIso(),
  };
  writeJsonAtomic(tailSessionFile(projectRoot, runId, sessionId), updated);
  return { session: updated };
}
