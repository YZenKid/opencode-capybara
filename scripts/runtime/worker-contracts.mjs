const BACKENDS = new Set([
  "opencode-subagent",
  "opencode-session",
  "external-cli-codex",
  "external-cli-claude",
  "external-cli-gemini",
]);

export function validateWorkerSpec(spec = {}) {
  const errors = [];
  if (!spec.worker_name) errors.push("worker_name required");
  if (!spec.lane) errors.push("lane required");
  if (!spec.run_id) errors.push("run_id required");
  if (!spec.project_root) errors.push("project_root required");
  if (!spec.prompt) errors.push("prompt required");
  if (spec.backend && !BACKENDS.has(spec.backend)) errors.push(`unsupported backend: ${spec.backend}`);
  return { ok: errors.length === 0, errors };
}

export function pickDefaultBackend(lane = "@fixer") {
  if (["@designer", "@oracle", "@architect", "@quality-gate"].includes(lane)) return "external-cli-claude";
  if (["@frontend", "@backend", "@mobile", "@devops", "@fullstack", "@fixer"].includes(lane)) return "opencode-subagent";
  return "opencode-session";
}

export function listSupportedBackends() {
  return [...BACKENDS].sort();
}
