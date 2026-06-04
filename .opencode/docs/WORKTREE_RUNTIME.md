
# Worktree Runtime

Runtime worktrees are the safe default for parallel or isolated implementation helpers.

## Goal
Prevent cross-worker file collisions while preserving replayability and dirty-state safety.

## Layout
- Base directory: `../<repo>.opencode-worktrees/<run-id>/<worker-name>`
- Branch naming: sanitized `opencode/<run-id>/<worker-name>`
- Runtime metadata must record:
  - `worktree_path`
  - `worktree_branch`
  - `worktree_created`
  - `worktree_repo_root`
  - `workspace_mode`

## Safety rules
- Refuse fresh provisioning when the root repo is dirty.
- Reuse a compatible clean worktree when possible.
- Preserve dirty worker worktrees on cleanup.
- Reject mismatched path/branch reuse.
- Cleanup never force-removes a dirty worktree by default.

## Verification expectations
- prove clean-root detection,
- prove dirty worker preservation,
- prove branch/path metadata is inspectable,
- prove dispatcher/executor records preserve workspace metadata,
- record cleanup result in evidence for material runs.
