import { randomUUID } from "node:crypto";
import { listJson, readJson, removeFile, writeJsonAtomic } from "./state-io.mjs";
import { tailExecutionLog } from "./ops-loop.mjs";
import { tailSessionFile, tailSessionsRoot } from "./state-paths.mjs";

function nowIso() {
  return new Date().toISOString();
}

function nowMs() {
  return Date.now();
}

export function createTailSession(projectRoot, runId, executionId, { session_id = randomUUID(), stream = "stdout", lines = 20 } = {}) {
  const createdAt = nowIso();
  const session = {
    session_id,
    run_id: runId,
    execution_id: executionId,
    stream,
    lines,
    status: "active",
    created_at: createdAt,
    updated_at: createdAt,
    created_at_ms: nowMs(),
    updated_at_ms: nowMs(),
    last_event: null,
  };
  writeJsonAtomic(tailSessionFile(projectRoot, runId, session_id), session);
  return session;
}

export function getTailSession(projectRoot, runId, sessionId) {
  return readJson(tailSessionFile(projectRoot, runId, sessionId), null);
}

export function listTailSessions(projectRoot, runId) {
  return listJson(tailSessionsRoot(projectRoot, runId)).map(({ data }) => data).filter(Boolean);
}

export async function pollTailSession(projectRoot, runId, sessionId) {
  const session = getTailSession(projectRoot, runId, sessionId);
  if (!session) throw new Error(`tail session not found: ${sessionId}`);
  const latest = tailExecutionLog(projectRoot, runId, session.execution_id, { stream: session.stream, lines: session.lines });
  const updated = {
    ...session,
    updated_at: nowIso(),
    updated_at_ms: nowMs(),
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
    updated_at_ms: nowMs(),
  };
  writeJsonAtomic(tailSessionFile(projectRoot, runId, sessionId), updated);
  return { session: updated };
}

export function collectTailSessions(projectRoot, runId, { now_ms = Date.now(), max_age_ms = 3600000, include_stopped = false } = {}) {
  const removed = [];
  const kept = [];
  for (const session of listTailSessions(projectRoot, runId)) {
    const age = now_ms - (session.updated_at_ms ?? session.created_at_ms ?? now_ms);
    const stale = age >= max_age_ms;
    const removable = stale || (include_stopped && session.status === "stopped");
    if (removable) {
      removeFile(tailSessionFile(projectRoot, runId, session.session_id));
      removed.push({ session_id: session.session_id, status: session.status, stale, age_ms: age });
    } else {
      kept.push({ session_id: session.session_id, status: session.status, age_ms: age });
    }
  }
  return { removed, kept };
}
