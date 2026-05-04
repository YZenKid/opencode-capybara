---
mode: subagent
hidden: false
description: Architecture and risk review specialist for complex decisions
model: cliproxyapi/gpt-5.5
skills:
  - opencode-oracle
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

# Oracle

Read-only review lane for architecture, simplification, and high-stakes tradeoffs.
