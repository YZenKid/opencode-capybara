# skills.sh inspirations for opencode-orchestrator

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### subagent-driven-development — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/subagent-driven-development
- Directory description: Use when executing implementation plans with independent tasks in the current session
- Local adaptation: Use as inspiration for plan-bound delegation, dependency-aware work splitting, and lane ownership without collapsing everything back into one worker.

### verification-before-completion — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/verification-before-completion
- Directory description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output…
- Local adaptation: Use as inspiration for completion discipline: no success claims before validation output and evidence are in hand.

### handoff — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/handoff
- Directory description: Compact the current conversation into a handoff document for another agent to pick up.
- Local adaptation: Use as inspiration for concise, execution-ready handoff summaries between lanes and sessions.

### zoom-out — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/zoom-out
- Directory description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how…
- Local adaptation: Use as inspiration for stepping back when route choice, scope, or architecture context is still fuzzy.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
