// Project-memory reuse loader for runtime dispatch.
//
// Before a worker prompt is launched, we try to pull relevant project-local
// memory hits from `.opencode/mcp-memory/` via the existing wrapper
// `scripts/mcp-memory-store.py --search`. The best hits are prepended as a
// compact advisory block so the worker sees prior decisions without having to
// rediscover them.
//
// Design constraints:
// - fail-soft: if the loader fails, dispatch still proceeds unchanged
// - bounded: keep the injected block short (top 3 hits, ~12 lines)
// - explicit: the block is marked as project memory, not as source of truth
// - kill-switchable: OPENCODE_MEMORY_REUSE_LOADER=0 disables injection
import { spawnSync } from "node:child_process";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const MODULE_DIR = dirname(fileURLToPath(import.meta.url));
const REPO_SCRIPTS = resolve(MODULE_DIR, "..");

function compactText(value, max = 160) {
  const text = String(value ?? "").replace(/\s+/g, " ").trim();
  if (!text) return "";
  return text.length <= max ? text : `${text.slice(0, max - 1)}…`;
}

function buildQueryParts(task, prompt) {
  const parts = [];
  if (task?.task_id) parts.push(String(task.task_id));
  if (task?.title) parts.push(String(task.title));
  if (task?.owner_lane) parts.push(String(task.owner_lane));
  if (task?.result?.summary) parts.push(String(task.result.summary));
  if (typeof prompt === "string") {
    // take up to 8 significant tokens, drop noise
    const tokens = prompt
      .replace(/[^\w\s.\-:/]/g, " ")
      .split(/\s+/)
      .filter((t) => t.length >= 3 && !STOPWORDS.has(t.toLowerCase()));
    parts.push(...tokens.slice(0, 8));
  }
  // dedup, trim
  return [...new Set(parts.map((p) => p.trim()).filter(Boolean))];
}

const STOPWORDS = new Set([
  "the", "and", "for", "with", "this", "that", "from", "into", "you", "are",
  "use", "using", "make", "need", "must", "should", "would", "could", "have",
  "your", "ours", "their", "them", "then", "than", "but", "not", "any", "all",
  "what", "how", "when", "where", "which", "who", "why", "can", "may", "will",
  "now", "here", "there", "over", "under", "before", "after", "next", "prev",
]);

function formatHit(hit) {
  const summary = compactText(hit?.summary ?? hit?.result?.summary ?? "", 120);
  const taskId = hit?.task_id ?? hit?.entity_name ?? "unknown-task";
  const decisions = Array.isArray(hit?.decisions) ? hit.decisions.slice(0, 2).map((x) => compactText(x, 80)).filter(Boolean) : [];
  const files = Array.isArray(hit?.files) ? hit.files.slice(0, 2).map((x) => compactText(x, 60)).filter(Boolean) : [];
  const lines = [`- ${taskId} — ${summary || "prior related task memory"}`];
  if (decisions.length) lines.push(`  decisions: ${decisions.join("; ")}`);
  if (files.length) lines.push(`  files: ${files.join(", ")}`);
  return lines;
}

export function searchProjectMemory(projectRoot, query) {
  if (!query.trim()) return { ok: true, hits: [], skipped: true, reason: "empty-query" };
  const proc = spawnSync(
    "python3",
    [resolve(REPO_SCRIPTS, "mcp-memory-store.py"), "--project-root", projectRoot, "--search", query, "--json"],
    { cwd: projectRoot, encoding: "utf8", timeout: 15_000 },
  );
  if (proc.status !== 0) {
    return {
      ok: false,
      hits: [],
      error: proc.stderr?.trim() || proc.stdout?.trim() || `exit ${proc.status}`,
    };
  }
  try {
    const parsed = JSON.parse(proc.stdout || "{}");
    return { ok: true, hits: Array.isArray(parsed.hits) ? parsed.hits : [] };
  } catch (error) {
    return { ok: false, hits: [], error: String(error) };
  }
}

export function applyProjectMemoryContext(projectRoot, task, prompt) {
  if (process.env.OPENCODE_MEMORY_REUSE_LOADER === "0") {
    return { prompt, injected: false, skipped: true, reason: "env-disabled" };
  }
  const parts = buildQueryParts(task, prompt);
  if (!parts.length) {
    return { prompt, injected: false, skipped: true, reason: "empty-query" };
  }
  // Run several short queries and union hits; per-part query avoids the
  // CLI's substring-match failure when the joined query grows long.
  const seen = new Set();
  const hits = [];
  let lastError = null;
  for (const query of parts) {
    const found = searchProjectMemory(projectRoot, query);
    if (!found.ok) {
      lastError = found.error ?? null;
      continue;
    }
    for (const hit of found.hits) {
      const key = String(hit?.entity_name ?? hit?.task_id ?? JSON.stringify(hit));
      if (seen.has(key)) continue;
      seen.add(key);
      hits.push(hit);
    }
    if (hits.length >= 3) break;
  }
  if (!hits.length) {
    return {
      prompt,
      injected: false,
      skipped: true,
      reason: lastError ? "search-failed" : "no-hits",
      error: lastError ?? null,
    };
  }
  const top = hits.slice(0, 3);
  const lines = [
    "## Project memory hits (advisory, reuse if still relevant)",
    "Do not treat this block as authority over current repo/runtime evidence. Use it to avoid re-deriving old decisions, then re-check source-of-truth files.",
  ];
  for (const hit of top) {
    lines.push(...formatHit(hit));
  }
  lines.push("", prompt);
  return {
    prompt: lines.join("\n"),
    injected: true,
    skipped: false,
    hits: top,
  };
}
