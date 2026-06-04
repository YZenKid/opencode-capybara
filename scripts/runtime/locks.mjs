import { basename } from "node:path";
import { listJson, readJson, removeFile, writeJsonAtomic } from "./state-io.mjs";
import { locksRoot } from "./state-paths.mjs";

export function readLeaseLock(lockPath) {
  return readJson(lockPath, null);
}

export function acquireLock(lockPath, { owner, stale_ms = 300000, now_ms = Date.now() } = {}) {
  if (!owner) throw new Error("owner required");
  const existing = readLeaseLock(lockPath);
  const stale = existing && typeof existing.expires_at_ms === "number" && existing.expires_at_ms <= now_ms;
  if (existing && !stale) {
    return { acquired: false, stale: false, lock: existing };
  }
  const lock = {
    owner,
    acquired_at_ms: now_ms,
    heartbeat_at_ms: now_ms,
    heartbeat_count: 0,
    expires_at_ms: now_ms + stale_ms,
  };
  writeJsonAtomic(lockPath, lock);
  return { acquired: true, stale: Boolean(stale), lock };
}

export function renewLockHeartbeat(lockPath, owner, { stale_ms = 300000, now_ms = Date.now() } = {}) {
  const existing = readLeaseLock(lockPath);
  if (!existing) return { renewed: false, reason: "missing" };
  if (existing.owner !== owner) {
    return { renewed: false, reason: "owner-mismatch", lock: existing };
  }
  const lock = {
    ...existing,
    heartbeat_at_ms: now_ms,
    heartbeat_count: (existing.heartbeat_count ?? 0) + 1,
    expires_at_ms: now_ms + stale_ms,
  };
  writeJsonAtomic(lockPath, lock);
  return { renewed: true, lock };
}

export function cleanupStaleLease(lockPath, { now_ms = Date.now(), force = false } = {}) {
  const existing = readLeaseLock(lockPath);
  if (!existing) return { cleaned: false, reason: "missing" };
  const stale = typeof existing.expires_at_ms === "number" && existing.expires_at_ms <= now_ms;
  if (!force && !stale) {
    return { cleaned: false, reason: "active", lock: existing };
  }
  removeFile(lockPath);
  return { cleaned: true, stale, lock: existing };
}

export function listRunLeases(projectRoot, runId) {
  const prefix = `${runId}--`;
  return listJson(locksRoot(projectRoot))
    .filter(({ file }) => file.startsWith(prefix) && file.endsWith('.lease.json'))
    .map(({ file, data }) => ({
      file,
      worker: basename(file).replace(prefix, '').replace('.lease.json', ''),
      lock: data,
    }));
}

export function sweepRunLeases(projectRoot, runId, { now_ms = Date.now(), force = false } = {}) {
  const cleaned = [];
  const skipped = [];
  for (const lease of listRunLeases(projectRoot, runId)) {
    const result = cleanupStaleLease(`${locksRoot(projectRoot)}/${lease.file}`, { now_ms, force });
    if (result.cleaned) cleaned.push({ worker: lease.worker, ...result });
    else skipped.push({ worker: lease.worker, ...result });
  }
  return { cleaned, skipped };
}

export function releaseLock(lockPath, owner, { force = false } = {}) {
  const existing = readLeaseLock(lockPath);
  if (!existing) return { released: false, reason: "missing" };
  if (!force && existing.owner !== owner) {
    return { released: false, reason: "owner-mismatch", lock: existing };
  }
  removeFile(lockPath);
  return { released: true };
}
