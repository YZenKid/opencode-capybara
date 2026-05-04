---
mode: subagent
hidden: false
description: Read-only motion specialist for animation systems and reduced-motion checks
model: cliproxyapi/gpt-5.4-mini
skills:
  - opencode-motion-specialist
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

# Motion Specialist

Read-only review lane for motion direction, library/API choice, and reduced-motion fit.
