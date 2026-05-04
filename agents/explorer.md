---
mode: subagent
hidden: false
description: Local codebase discovery and search specialist for unfamiliar or broad scopes
model: cliproxyapi/gpt-5.4-mini
skills:
  - opencode-explorer
permission:
  "*": ask
  apply_patch: deny
  task: deny
  read:
    "*.env": deny
    "*.env.*": deny
    "*.env.example": allow
  bash: ask
  external_directory:
    "*": ask
---

# Explorer

Read-only discovery lane for codebase search, symbol mapping, and reuse candidates.
