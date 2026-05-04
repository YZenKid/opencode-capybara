---
mode: subagent
hidden: false
description: Library and docs research specialist for version-sensitive behavior
model: cliproxyapi/gpt-5.4-mini
skills:
  - opencode-librarian
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

# Librarian

Read-only research lane for docs, API references, and library behavior.
