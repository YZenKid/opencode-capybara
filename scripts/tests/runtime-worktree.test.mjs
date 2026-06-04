#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync, writeFileSync, mkdirSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { execFileSync } from "node:child_process";
import { planWorkerWorktree, createWorkerWorktree, cleanupWorkerWorktree, inspectWorktree } from "../runtime/worktree-plan.mjs";

const repoRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-worktree-"));
execFileSync("git", ["init"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.email", "runtime@example.com"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["config", "user.name", "Runtime Test"], { cwd: repoRoot, stdio: "pipe" });
writeFileSync(join(repoRoot, "README.md"), "hello\n");
execFileSync("git", ["add", "README.md"], { cwd: repoRoot, stdio: "pipe" });
execFileSync("git", ["commit", "-m", "init"], { cwd: repoRoot, stdio: "pipe" });
const plan = planWorkerWorktree(repoRoot, "run-worktree", "backend-1");
assert.match(plan.worktree_path, /backend-1$/);
const created = createWorkerWorktree(repoRoot, "run-worktree", "backend-1");
assert.equal(inspectWorktree(created.worktree_path).exists, true);
writeFileSync(join(created.worktree_path, "README.md"), readFileSync(join(created.worktree_path, "README.md"), "utf8") + "dirty\n");
const preserved = cleanupWorkerWorktree(created.worktree_path);
assert.equal(preserved.removed, false);
assert.equal(preserved.preserved_dirty, true);
console.log("runtime-worktree.test.mjs: PASS");
