---
mode: subagent
description: General-purpose agent for researching complex questions and executing multi-step tasks. Use this agent to execute multiple units of work in parallel.
model: omniroute/cx/gpt-5.4
skills:
  - opencode-general
permission:
  "*": allow
  bash: ask
  doom_loop: ask
  external_directory:
    "*": ask
    "{env:HOME}/.local/share/opencode/tool-output/*": allow
    "{env:HOME}/.config/opencode/skills/opencode-general/*": allow
  question: deny
  plan_enter: deny
  plan_exit: deny
  read:
    "*.env": ask
    "*.env.*": ask
    "*.env.example": allow
  todowrite: deny
  task: deny
---

# General Agent Rules

Use the standalone `opencode-general` workflow. Do not load archived legacy skills.
