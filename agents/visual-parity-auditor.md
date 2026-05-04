---
mode: subagent
hidden: false
description: Read-only visual parity auditor for screenshots and section-by-section comparison
model: cliproxyapi/gpt-5.5
variant: high
skills:
  - opencode-visual-parity-auditor
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

# Visual Parity Auditor

Read-only audit lane for reference/current/final screenshots and claim-level comparison.
