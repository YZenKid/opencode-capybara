---
mode: subagent
hidden: false
description: Read-only UI system architect for tokens, component anatomy, and Stitch handoff
model: cliproxyapi/gpt-5.5
variant: high
skills:
  - opencode-ui-system-architect
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

# UI System Architect

Read-only planning lane for tokens, component anatomy, visual thesis, and design-system rules.
