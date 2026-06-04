
import { execFileSync } from "node:child_process";
import { existsSync, rmSync } from "node:fs";
import { basename, resolve } from "node:path";
import { worktreeBaseRoot } from "./state-paths.mjs";

function runGit(repoRoot, args) {
  return execFileSync("git", args, { cwd: repoRoot, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] }).trim();
}

function sanitize(value) {
  return value.replace(/[^a-zA-Z0-9._-]+/g, "-").replace(/^-+|-+$/g, "").toLowerCase();
}

export function rootRepoDirty(repoRoot) {
  const status = runGit(repoRoot, ["status", "--porcelain", "--untracked-files=all"]);
  if (!status) return false;
  const meaningful = status
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .filter((line) => !line.includes(".opencode/state/"));
  return meaningful.length > 0;
}

export function planWorkerWorktree(repoRoot, runId, workerName) {
  const worktree_path = resolve(worktreeBaseRoot(repoRoot, runId), workerName);
  const worktree_branch = `opencode/${sanitize(runId)}/${sanitize(workerName)}`;
  return {
    repo_root: resolve(repoRoot),
    worktree_path,
    worktree_branch,
    workspace_mode: "worktree",
  };
}

export function inspectWorktree(worktreePath) {
  if (!existsSync(worktreePath)) return { exists: false, dirty: false, branch: null };
  const branch = runGit(worktreePath, ["rev-parse", "--abbrev-ref", "HEAD"]);
  const dirty = runGit(worktreePath, ["status", "--porcelain"]) !== "";
  return { exists: true, dirty, branch, path: worktreePath };
}

export function createWorkerWorktree(repoRoot, runId, workerName) {
  if (rootRepoDirty(repoRoot)) {
    throw new Error("root repo is dirty; refuse worktree provisioning");
  }
  const plan = planWorkerWorktree(repoRoot, runId, workerName);
  const current = inspectWorktree(plan.worktree_path);
  if (current.exists) {
    if (current.branch !== basename(plan.worktree_branch)) {
      throw new Error(`existing worktree branch mismatch: ${current.branch}`);
    }
    return { ...plan, worktree_created: false };
  }
  runGit(repoRoot, ["worktree", "add", "-b", plan.worktree_branch, plan.worktree_path, "HEAD"]);
  return { ...plan, worktree_created: true };
}

export function cleanupWorkerWorktree(worktreePath) {
  const current = inspectWorktree(worktreePath);
  if (!current.exists) return { removed: false, preserved_dirty: false, reason: "missing" };
  if (current.dirty) return { removed: false, preserved_dirty: true, reason: "dirty" };
  execFileSync("git", ["worktree", "remove", worktreePath], { cwd: worktreePath, stdio: ["ignore", "pipe", "pipe"] });
  if (existsSync(worktreePath)) rmSync(worktreePath, { recursive: true, force: true });
  return { removed: true, preserved_dirty: false, reason: "clean" };
}
