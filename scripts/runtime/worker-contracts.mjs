import { statSync } from "node:fs";
import { extname, resolve } from "node:path";

const BACKENDS = new Set([
  "opencode-subagent",
  "opencode-session",
  "external-cli-codex",
  "external-cli-claude",
  "external-cli-gemini",
]);
const IMAGE_EXTENSIONS = new Set([".bmp", ".gif", ".jpeg", ".jpg", ".png", ".webp"]);

export function validateImagePath(imagePath) {
  if (imagePath === undefined || imagePath === null) return { ok: true, path: null };
  if (typeof imagePath !== "string" || !imagePath.trim()) return { ok: false, error: "image_path must be a non-empty string" };
  const normalizedPath = resolve(imagePath);
  if (!IMAGE_EXTENSIONS.has(extname(normalizedPath).toLowerCase())) return { ok: false, error: "image_path must reference an image file" };
  try {
    if (!statSync(normalizedPath).isFile()) return { ok: false, error: "image_path must reference an image file" };
  } catch {
    return { ok: false, error: "image_path must reference an existing image file" };
  }
  return { ok: true, path: normalizedPath };
}

export function normalizeWorkerSpec(spec = {}) {
  const image = validateImagePath(spec.image_path);
  return image.ok ? { ...spec, image_path: image.path } : spec;
}

export function validateWorkerSpec(spec = {}) {
  const errors = [];
  if (!spec.worker_name) errors.push("worker_name required");
  if (!spec.lane) errors.push("lane required");
  if (!spec.run_id) errors.push("run_id required");
  if (!spec.project_root) errors.push("project_root required");
  if (!spec.prompt) errors.push("prompt required");
  if (spec.backend && !BACKENDS.has(spec.backend)) errors.push(`unsupported backend: ${spec.backend}`);
  const image = validateImagePath(spec.image_path);
  if (!image.ok) errors.push(image.error);
  return { ok: errors.length === 0, errors, image_path: image.path ?? null };
}

export function pickDefaultBackend(lane = "@fixer") {
  if (["@designer", "@oracle", "@architect", "@quality-gate"].includes(lane)) return "external-cli-claude";
  if (["@fixer"].includes(lane)) return "opencode-subagent";
  return "opencode-session";
}

export function listSupportedBackends() {
  return [...BACKENDS].sort();
}
