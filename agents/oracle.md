---
mode: subagent
hidden: false
description: Architecture and risk review specialist for complex decisions
model: {env:OPENCODE_MODEL_REVIEW}
skills:
  - opencode-oracle
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

# Oracle

Read-only review lane for architecture, simplification, and high-stakes tradeoffs.
