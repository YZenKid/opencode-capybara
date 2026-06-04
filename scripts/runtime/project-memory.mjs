
import { projectMemoryFile, sharedRunMemoryFile, sharedRunMemoryRoot } from "./state-paths.mjs";
import { ensureDir, listJson, readJson, writeJsonAtomic } from "./state-io.mjs";

export function readProjectMemory(projectRoot) {
  return readJson(projectMemoryFile(projectRoot), { conventions: [], notes: [], active_decisions: [] });
}

export function writeProjectMemory(projectRoot, memory, { merge = false } = {}) {
  const current = readProjectMemory(projectRoot);
  const next = merge ? { ...current, ...memory } : memory;
  return writeJsonAtomic(projectMemoryFile(projectRoot), next);
}

export function putRunMemory(projectRoot, runId, key, value) {
  ensureDir(sharedRunMemoryRoot(projectRoot, runId));
  return writeJsonAtomic(sharedRunMemoryFile(projectRoot, runId, key), { key, value, updated_at: new Date().toISOString() });
}

export function getRunMemory(projectRoot, runId, key, fallback = null) {
  return readJson(sharedRunMemoryFile(projectRoot, runId, key), fallback);
}

export function listRunMemory(projectRoot, runId) {
  return listJson(sharedRunMemoryRoot(projectRoot, runId)).map((item) => item.data);
}
