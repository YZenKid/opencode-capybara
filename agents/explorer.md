---
mode: subagent
hidden: false
description: Local codebase discovery and search specialist for unfamiliar or broad scopes
model: cliproxyapi/gpt-5.4-mini
skills:
  - opencode-explorer
permission:
  "*": allow
  apply_patch: deny
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

# Explorer

Read-only discovery lane for codebase search, symbol mapping, and reuse candidates.
