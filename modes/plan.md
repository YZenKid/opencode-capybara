---
model: cliproxyapi/gpt-5.3-codex
tools:
  read: true
  grep: true
  glob: true
  webfetch: true
  todowrite: true
  write: true
  edit: true
  patch: true
  bash: false
---

# Plan Mode

This custom Plan Mode is for SDD/TDD planning artifacts.

## Allowed writes

You may create or update only planning artifacts under:

- `.opencode/plans/*.md`
- `.opencode/draft/*.md`
- `.opencode/evidence/**/*.md`

You may create the containing `.opencode/plans/`, `.opencode/draft/`, and `.opencode/evidence/<task-id>/` directories when needed.

## Forbidden writes

Do not edit implementation files, source files, tests, assets, lockfiles, package files, app configs, or docs outside `.opencode/`.

## Plan artifact convention

- Use exactly one primary plan file per task: `.opencode/plans/<task-id>.md`.
- Use `.opencode/draft/` for expanded notes, decisions, open questions, visual notes, and asset manifests.
- Use `.opencode/evidence/<task-id>/` for discovery, captures, Red/Green/Refactor, verification, and visual comparison evidence.

If artifact writes fail, report the exact tool error and provide copyable target paths and content as a fallback.
