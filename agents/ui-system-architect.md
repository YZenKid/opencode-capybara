---
mode: subagent
hidden: false
description: Read-only UI system architect for tokens, component anatomy, and Stitch handoff
model: cliproxyapi/gpt-5.5
variant: high
skills:
  - opencode-ui-system-architect
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

# UI System Architect

Read-only planning lane for tokens, component anatomy, visual thesis, and design-system rules.
