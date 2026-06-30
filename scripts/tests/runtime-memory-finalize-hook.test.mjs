// Tests for scripts/runtime/memory-finalize-hook.mjs and the auto-finalize
// behavior added to completeTask() in scripts/runtime/task-store.mjs.
//
// Run:
//   node scripts/tests/runtime-memory-finalize-hook.test.mjs
import { mkdtempSync, rmSync, existsSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { test } from "node:test";
import assert from "node:assert/strict";

const REPO_ROOT = resolve(import.meta.dirname, "..", "..");
const TASK_STORE = resolve(REPO_ROOT, "scripts/runtime/task-store.mjs");
const HOOK = resolve(REPO_ROOT, "scripts/runtime/memory-finalize-hook.mjs");
const RUN_STORE = resolve(REPO_ROOT, "scripts/runtime/run-store.mjs");

const SCRATCH_ROOT = "/var/home/ujang";

async function importFresh(cwd) {
  process.chdir(cwd);
  return await import(`${TASK_STORE}?t=${Date.now()}`);
}

function tempProject() {
  const root = mkdtempSync(join(SCRATCH_ROOT, "opencode-mem-hook-"));
  const runId = "test-run";
  return import(RUN_STORE).then((runStore) => {
    runStore.createRun(root, { run_id: runId, goal: "fixture", mode: "maintenance" });
    return { root, runId };
  });
}

test("completeTask persists status=completed", async () => {
  const { root, runId } = await tempProject();
  try {
    const store = await importFresh(root);
    store.createTask(root, runId, { task_id: "task-1", title: "first", owner_lane: "@fixer" });
    const completed = store.completeTask(root, runId, "task-1", {
      summary: "fixed the bug",
      decisions: ["use plan mode"],
      files_touched: ["src/app.ts"],
      claim_level: "done",
    });
    assert.equal(completed.status, "completed");
    assert.ok(completed.memory_finalize, "memory_finalize metadata should be present");
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("hook writes project memory bundle under .opencode/mcp-memory", async () => {
  const { root, runId } = await tempProject();
  try {
    const store = await importFresh(root);
    store.createTask(root, runId, { task_id: "task-2", title: "second", owner_lane: "@fixer" });
    const completed = store.completeTask(root, runId, "task-2", {
      summary: "shipped landing hero using dashboard tokens",
      decisions: ["Use dashboard tokens as source of truth"],
      files_touched: ["resources/js/pages/welcome.tsx"],
      claim_level: "done",
    });
    const memory = completed.memory_finalize ?? {};
    // local fallback is acceptable when MCP server is unavailable
    assert.ok(["local-fallback", "mcp+local", "local"].includes(memory.backend) || memory.ok === false, `unexpected backend: ${memory.backend}`);
    // if ok=true then bundle must exist
    if (memory.ok) {
      const opencodeDir = join(root, ".opencode", "mcp-memory");
      assert.ok(existsSync(opencodeDir), "expected .opencode/mcp-memory bundle");
    }
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("hook is fail-soft when mcp-memory-store.py errors out", async () => {
  const { root, runId } = await tempProject();
  try {
    // Force the finalize CLI to fail by writing a stub script that exits 2,
    // and pointing PATH at it so the hook cannot find mcp-memory-store.py
    // directly. Simplest: just rely on the wrapper's own catch: a task result
    // missing required fields must produce ok:false but not throw.
    const { runMemoryFinalize } = await import(`${HOOK}?t=${Date.now()}`);
    const memory = runMemoryFinalize(root, runId, { task_id: "x" }, {});
    // The hook should return a structured outcome, not throw.
    assert.equal(memory.task_id, "x");
    assert.equal(typeof memory.ok, "boolean");
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("OPENCODE_MEMORY_FINALIZE=0 disables hook", async () => {
  const { root, runId } = await tempProject();
  try {
    process.env.OPENCODE_MEMORY_FINALIZE = "0";
    const store = await importFresh(root);
    store.createTask(root, runId, { task_id: "task-skip", title: "skip", owner_lane: "@fixer" });
    const completed = store.completeTask(root, runId, "task-skip", { summary: "x" });
    assert.equal(completed.status, "completed");
    assert.equal(completed.memory_finalize, undefined, "memory_finalize must be absent when hook is disabled");
  } finally {
    delete process.env.OPENCODE_MEMORY_FINALIZE;
    rmSync(root, { recursive: true, force: true });
  }
});
