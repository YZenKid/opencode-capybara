
import { randomUUID } from "node:crypto";
import { existsSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import { mailboxMessageFile, mailboxWorkerRoot, runEventsFile } from "./state-paths.mjs";
import { appendNdjson, ensureDir, listJson, readJson, writeJsonAtomic } from "./state-io.mjs";

function timestamp() {
  return new Date().toISOString();
}

export function sendMessage(projectRoot, runId, payload) {
  const now = timestamp();
  const message = {
    message_id: payload.message_id ?? randomUUID(),
    from: payload.from,
    to: payload.to,
    type: payload.type ?? "task",
    payload: payload.payload ?? {},
    status: "pending",
    created_at: now,
    updated_at: now,
  };
  ensureDir(mailboxWorkerRoot(projectRoot, runId, message.to));
  writeJsonAtomic(mailboxMessageFile(projectRoot, runId, message.to, message.message_id), message);
  appendNdjson(runEventsFile(projectRoot, runId), { timestamp: now, type: "mailbox-sent", run_id: runId, message_id: message.message_id, to: message.to, message_type: message.type });
  return message;
}

export function listMessages(projectRoot, runId, worker, { includeAcked = false } = {}) {
  return listJson(mailboxWorkerRoot(projectRoot, runId, worker))
    .map((item) => item.data)
    .filter((item) => includeAcked || item.status !== "acked");
}

export function ackMessage(projectRoot, runId, worker, messageId, actor) {
  const path = mailboxMessageFile(projectRoot, runId, worker, messageId);
  const current = readJson(path, null);
  if (!current) throw new Error(`message not found: ${messageId}`);
  const updated = { ...current, status: "acked", acked_by: actor, updated_at: timestamp() };
  writeJsonAtomic(path, updated);
  appendNdjson(runEventsFile(projectRoot, runId), { timestamp: updated.updated_at, type: "mailbox-acked", run_id: runId, message_id: messageId, by: actor });
  return updated;
}

export function requeueMessage(projectRoot, runId, worker, messageId, actor) {
  const path = mailboxMessageFile(projectRoot, runId, worker, messageId);
  const current = readJson(path, null);
  if (!current) throw new Error(`message not found: ${messageId}`);
  const updated = { ...current, status: "pending", requeued_by: actor, updated_at: timestamp() };
  writeJsonAtomic(path, updated);
  appendNdjson(runEventsFile(projectRoot, runId), { timestamp: updated.updated_at, type: "mailbox-requeued", run_id: runId, message_id: messageId, by: actor });
  return updated;
}

export function summarizeMailbox(projectRoot, runId) {
  const base = resolve(mailboxWorkerRoot(projectRoot, runId, "."));
  if (!existsSync(base)) return { pending: 0, acked: 0, workers: [] };
  const workers = readdirSync(base, { withFileTypes: true }).filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();
  let pending = 0;
  let acked = 0;
  for (const worker of workers) {
    for (const message of listMessages(projectRoot, runId, worker, { includeAcked: true })) {
      if (message.status === "acked") acked += 1;
      else pending += 1;
    }
  }
  return { pending, acked, workers };
}
