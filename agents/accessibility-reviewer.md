---
mode: subagent
hidden: false
description: Read-only accessibility reviewer for semantics, keyboard, focus, contrast, and motion
model: cliproxyapi/gpt-5.4-mini
skills:
  - opencode-accessibility-reviewer
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

# Accessibility Reviewer

Read-only review lane for semantic roles, labels, focus, contrast, touch targets, and reduced motion.
