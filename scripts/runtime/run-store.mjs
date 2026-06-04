
import { readdirSync } from "node:fs";
import { resolve } from "node:path";
import { runDir, runEventsFile, runFile, runsRoot } from "./state-paths.mjs";
import { appendNdjson, ensureDir, readJson, writeJsonAtomic } from "./state-io.mjs";

function timestamp() {
  return new Date().toISOString();
}

export function createRun(projectRoot, payload) {
  const now = timestamp();
  const run = {
    run_id: payload.run_id,
    goal: payload.goal,
    mode: payload.mode ?? "maintenance",
    status: payload.status ?? "planning",
    next_step: payload.next_step ?? null,
    evidence_paths: payload.evidence_paths ?? [],
    notes: payload.notes ?? [],
    created_at: now,
    updated_at: now,
  };
  ensureDir(runDir(projectRoot, run.run_id));
  writeJsonAtomic(runFile(projectRoot, run.run_id), run);
  appendNdjson(runEventsFile(projectRoot, run.run_id), { timestamp: now, type: "run-created", run_id: run.run_id, status: run.status });
  return run;
}

export function getRun(projectRoot, runId) {
  return readJson(runFile(projectRoot, runId), null);
}

export function updateRun(projectRoot, runId, updater) {
  const current = getRun(projectRoot, runId);
  if (!current) throw new Error(`run not found: ${runId}`);
  const updated = { ...updater(current), updated_at: timestamp() };
  writeJsonAtomic(runFile(projectRoot, runId), updated);
  appendNdjson(runEventsFile(projectRoot, runId), { timestamp: updated.updated_at, type: "run-updated", run_id: runId, status: updated.status, next_step: updated.next_step ?? null });
  return updated;
}

export function listRuns(projectRoot) {
  const base = runsRoot(projectRoot);
  try {
    return readdirSync(base, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => readJson(resolve(base, entry.name, "run.json"), null))
      .filter(Boolean)
      .sort((a, b) => String(a.run_id).localeCompare(String(b.run_id)));
  } catch {
    return [];
  }
}
