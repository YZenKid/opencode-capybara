# skills.sh inspirations for opencode-project-manager

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### writing-plans — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/writing-plans
- Directory description: Use when you have a spec or requirements for a multi-step task, before touching code
- Local adaptation: Use as inspiration for multi-step task decomposition before execution begins.

### to-prd — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/to-prd
- Directory description: Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context.
- Local adaptation: Use as inspiration for turning stakeholder context into implementation-ready planning artifacts.

### handoff — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/handoff
- Directory description: Compact the current conversation into a handoff document for another agent to pick up.
- Local adaptation: Use as inspiration for concise status and ownership handoffs.

### verification-before-completion — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/verification-before-completion
- Directory description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output…
- Local adaptation: Use as inspiration for exit criteria that require real validation, not optimistic status updates.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
