---
mode: subagent
hidden: false
description: Read-only accessibility reviewer for semantics, keyboard, focus, contrast, and motion
model: cliproxyapi/gpt-5.4-mini
skills:
  - opencode-accessibility-reviewer
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

# Accessibility Reviewer

Read-only review lane for semantic roles, labels, focus, contrast, touch targets, and reduced motion.
