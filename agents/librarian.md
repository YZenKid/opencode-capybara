---
mode: subagent
hidden: false
description: Library and docs research specialist for version-sensitive behavior
model: cliproxyapi/gpt-5.4-mini
skills:
  - opencode-librarian
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

# Librarian

Read-only research lane for docs, API references, and library behavior.
