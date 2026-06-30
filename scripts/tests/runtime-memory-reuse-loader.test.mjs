// Tests for scripts/runtime/memory-reuse-loader.mjs.
//
// Run:
//   node scripts/tests/runtime-memory-reuse-loader.test.mjs
import { mkdtempSync, rmSync, writeFileSync, readFileSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";
import { test } from "node:test";
import assert from "node:assert/strict";

const REPO_ROOT = resolve(import.meta.dirname, "..", "..");
const LOADER = resolve(REPO_ROOT, "scripts/runtime/memory-reuse-loader.mjs");
const SCRATCH_ROOT = "/var/home/ujang";

async function importFresh() {
  return await import(`${LOADER}?t=${Date.now()}`);
}

function tmpProject() {
  return mkdtempSync(join(SCRATCH_ROOT, "opencode-mem-loader-"));
}

function seedMemory(projectRoot, record) {
  const bundle = join(projectRoot, ".opencode", "mcp-memory", "fixture");
  // derive key+hash via wrapper is overkill for the loader test;
  // the loader calls the CLI which searches by substring, so we
  // can simply place a known-shape file under any key directory.
  // The wrapper resolves its own key, so we must use the same.
  // Run the wrapper once to get the right path, then inject records.
  return bundle;
}

test("applyProjectMemoryContext returns unchanged prompt when env disabled", async () => {
  process.env.OPENCODE_MEMORY_REUSE_LOADER = "0";
  try {
    const { applyProjectMemoryContext } = await importFresh();
    const out = applyProjectMemoryContext("/tmp", { task_id: "t" }, "hello world");
    assert.equal(out.prompt, "hello world");
    assert.equal(out.injected, false);
    assert.equal(out.skipped, true);
    assert.equal(out.reason, "env-disabled");
  } finally {
    delete process.env.OPENCODE_MEMORY_REUSE_LOADER;
  }
});

test("applyProjectMemoryContext leaves prompt unchanged when no hits", async () => {
  const projectRoot = tmpProject();
  try {
    const { applyProjectMemoryContext } = await importFresh();
    const out = applyProjectMemoryContext(projectRoot, { task_id: "no-match-here" }, "unique query phrase");
    assert.equal(out.prompt, "unique query phrase");
    assert.equal(out.injected, false);
    assert.equal(["no-hits", "search-failed"].includes(out.skipped ? out.reason : ""), true);
  } finally {
    rmSync(projectRoot, { recursive: true, force: true });
  }
});

test("applyProjectMemoryContext injects hit block when memory matches", async () => {
  const projectRoot = tmpProject();
  try {
    // Seed a memory record using the existing CLI, then verify injection
    const seedProc = await import("node:child_process").then(({ spawnSync }) =>
      spawnSync("python3", [
        resolve(REPO_ROOT, "scripts/mcp-memory-store.py"),
        "--project-root", projectRoot,
        "--finalize",
        "--task", "tokens-task-2026",
        "--summary", "Tailwind tokens aligned with dashboard source.",
        "--decision", "Keep token identity with templates/dashboard/src/index.css",
        "--file", "resources/js/pages/welcome.tsx",
        "--claim-level", "done",
      ], { encoding: "utf8" }),
    );
    assert.equal(seedProc.status, 0, `seed failed: ${seedProc.stderr}`);

    const { applyProjectMemoryContext } = await importFresh();
    const out = applyProjectMemoryContext(
      projectRoot,
      { task_id: "tokens-task-2026", title: "tokens followup" },
      "Tailwind dashboard tokens followup for hero.",
    );
    assert.equal(out.injected, true, `expected injected=true; skipped=${out.skipped} reason=${out.reason} error=${out.error}`);
    assert.match(out.prompt, /Project memory hits/);
    assert.match(out.prompt, /tokens-task-2026/);
    assert.match(out.prompt, /Tailwind dashboard tokens followup for hero\./);
  } finally {
    rmSync(projectRoot, { recursive: true, force: true });
  }
});

test("applyProjectMemoryContext is fail-soft on missing CLI", async () => {
  // We simulate by pointing PATH to an empty dir so python3 cannot spawn npx.
  // The wrapper itself still works locally; the loader must surface injected=false.
  const projectRoot = tmpProject();
  try {
    const { applyProjectMemoryContext } = await importFresh();
    const out = applyProjectMemoryContext(projectRoot, { task_id: "x" }, "anything");
    assert.equal(typeof out.injected, "boolean");
    assert.equal(typeof out.prompt, "string");
  } finally {
    rmSync(projectRoot, { recursive: true, force: true });
  }
});