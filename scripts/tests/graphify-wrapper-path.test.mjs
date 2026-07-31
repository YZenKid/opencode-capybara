import assert from "node:assert/strict";
import { chmod, mkdir, mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";

const repoRoot = fileURLToPath(new URL("../..", import.meta.url));
const wrapper = join(repoRoot, "scripts/graphify-mcp-wrapper");
const root = await mkdtemp(join(tmpdir(), "graphify-wrapper-"));
const bin = join(root, "bin");
const log = join(root, "calls.log");
await mkdir(join(root, ".opencode", "graphify-out"), { recursive: true });
await mkdir(bin);
const stub = String.raw`#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$0 $*" >> "$CALL_LOG"
if [[ "$1" == extract ]]; then
  out="$6"
  mkdir -p "$out/graphify-out"
  printf '{}' > "$out/graphify-out/graph.json"
fi
`;
await writeFile(join(bin, "graphify"), stub);
await writeFile(join(bin, "graphify-mcp"), stub);
await chmod(join(bin, "graphify"), 0o755);
await chmod(join(bin, "graphify-mcp"), 0o755);

const run = () => new Promise((resolve, reject) => {
  const child = spawn(wrapper, [root], { env: { ...process.env, PATH: `${bin}:${process.env.PATH}`, CALL_LOG: log } });
  let stderr = "";
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  child.on("error", reject);
  child.on("close", (code) => code === 0 ? resolve(stderr) : reject(new Error(stderr)));
});

await run();
const first = await (await import("node:fs/promises")).readFile(log, "utf8");
assert.match(first, /graphify extract .*--out .*\.opencode/);
assert.match(first, /graphify-mcp .*\.opencode\/graphify-out\/graph\.json/);
assert.doesNotMatch(first, /graphify-out\/graph\.json[^\n]*--out/);
await run();
const second = await (await import("node:fs/promises")).readFile(log, "utf8");
assert.equal((second.match(/graphify extract/g) ?? []).length, 1);
console.log("graphify wrapper behavioral canonical path and reuse: PASS");
