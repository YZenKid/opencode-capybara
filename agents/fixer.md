---
mode: subagent
hidden: false
description: Bounded implementation and testing specialist for Red/Green/Refactor work
model: cliproxyapi/gpt-5.3-codex
skills:
  - opencode-fixer
permission:
  "*": allow
  apply_patch: allow
  task: deny
  read:
    "*.env": ask
    "*.env.*": allow
    "*.env.example": allow
  bash: ask
  external_directory:
    "*": allow
    write: ask
    update: ask
    delete: ask
---

# Fixer

Implementation lane for bounded changes, tests, fixtures, and TDD work.
