import { chmod, copyFile, lstat, mkdir, mkdtemp, readdir, realpath, rm, stat, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { isAbsolute, join, resolve } from "node:path";
const MAX_BYTES = 10 * 1024 * 1024;
const TEMP_PREFIX = "opencode-visual-";
const ATTACHMENT_DIR = ".opencode/visual-attachments";
const MIME_EXTENSIONS = new Map([["image/png", ".png"], ["image/jpeg", ".jpg"], ["image/webp", ".webp"], ["image/gif", ".gif"], ["image/bmp", ".bmp"]]);
const sessions = new Map();
const calls = new Map();

function isImageFilePart(part) {
  return part?.type === "file" && MIME_EXTENSIONS.has(part.mime);
}

function parseImageFilePart(part) {
  if (!isImageFilePart(part) || typeof part.url !== "string") return null;
  const url = part.url;
  if (url.startsWith("data:")) {
    const match = /^data:([^;,]+);base64,([A-Za-z0-9+/]*={0,2})$/.exec(url);
    if (!match || match[1] !== part.mime || match[2].length % 4 !== 0) return null;
    const bytes = Buffer.from(match[2], "base64");
    if (bytes.toString("base64") !== match[2] || bytes.byteLength > MAX_BYTES) return null;
    return { kind: "bytes", bytes, extension: MIME_EXTENSIONS.get(part.mime) };
  }
  if (url.startsWith("http:") || url.startsWith("https:")) return null;
  if (url.startsWith("file:")) {
    let parsed;
    try { parsed = new URL(url); } catch { return null; }
    if (parsed.host) return null;
    let path;
    try { path = fileURLToPath(parsed); } catch { return null; }
    return isAbsolute(path) ? { kind: "path", path: resolve(path), extension: MIME_EXTENSIONS.get(part.mime) } : null;
  }
  return isAbsolute(url) ? { kind: "path", path: resolve(url), extension: MIME_EXTENSIONS.get(part.mime) } : null;
}

async function materializeImagePart(part, worktree) {
  const parsed = parseImageFilePart(part);
  if (!parsed || typeof worktree !== "string") return null;
  const base = join(resolve(worktree), ATTACHMENT_DIR);
  await mkdir(base, { recursive: true, mode: 0o700 });
  await chmod(base, 0o700);
  const root = await mkdtemp(join(base, `${TEMP_PREFIX}`));
  await chmod(root, 0o700);
  const file = join(root, `image${parsed.extension}`);
  try {
    if (parsed.kind === "bytes") {
      await writeFile(file, parsed.bytes, { mode: 0o600 });
    } else {
      const link = await lstat(parsed.path).catch(() => null);
      if (!link || !link.isFile()) return await cleanupMaterialization({ root });
      const safePath = await realpath(parsed.path);
      const info = await stat(safePath).catch(() => null);
      if (!info?.isFile() || info.size > MAX_BYTES) return await cleanupMaterialization({ root });
      await copyFile(safePath, file);
      await chmod(file, 0o600);
    }
    return { root, file, relative: `${ATTACHMENT_DIR}/${root.split("/").pop()}/${file.split("/").pop()}` };
  } catch {
    await cleanupMaterialization({ root });
    return null;
  }
}

async function cleanupMaterialization(materialization) {
  if (materialization?.root) await rm(materialization.root, { recursive: true, force: true });
  return null;
}

async function cleanupStaleMaterializations(worktree, maxAgeMs = 60 * 60 * 1000) {
  if (typeof worktree !== "string") return;
  const base = join(resolve(worktree), ATTACHMENT_DIR);
  const now = Date.now();
  const entries = await readdir(base, { withFileTypes: true }).catch(() => []);
  await Promise.all(entries.filter((entry) => entry.isDirectory()).map(async (entry) => {
    const path = join(base, entry.name);
    const info = await stat(path).catch(() => null);
    if (info && now - info.mtimeMs > maxAgeMs) await rm(path, { recursive: true, force: true });
  }));
}

async function cleanupSession(sessionID) {
  const entry = sessions.get(sessionID);
  sessions.delete(sessionID);
  await Promise.all((entry?.paths || []).map(cleanupMaterialization));
}

function createPlugin() {
  return async ({ worktree }) => {
    await cleanupStaleMaterializations(worktree);
    return {
      "chat.message": async (input, output) => {
        const image = [...(output.parts || [])].reverse().find(isImageFilePart);
        if (image) sessions.set(input.sessionID, { part: image, paths: sessions.get(input.sessionID)?.paths || [] });
      },
      "tool.execute.before": async (input, output) => {
        if (input.tool !== "task" || output.args?.subagent_type !== "visual-context-extractor") return;
        const cached = sessions.get(input.sessionID)?.part;
        const materialization = cached && await materializeImagePart(cached, worktree);
        if (!materialization) return;
        const callID = input.callID;
        calls.set(callID, materialization);
        output.args.prompt = `${output.args.prompt}\n@${materialization.relative}`;
      },
      "tool.execute.after": async (input) => {
        const materialization = calls.get(input.callID);
        calls.delete(input.callID);
        await cleanupMaterialization(materialization);
      },
      event: async ({ event }) => {
        if (event.type === "session.deleted") await cleanupSession(event.properties.sessionID);
      },
      dispose: async () => { await Promise.all([...sessions.keys()].map(cleanupSession)); await Promise.all([...calls.values()].map(cleanupMaterialization)); calls.clear(); }
    };
  };
}

export default createPlugin();
