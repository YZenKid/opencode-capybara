# skills.sh inspirations for opencode-devops

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### verification-before-completion — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/verification-before-completion
- Directory description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output…
- Local adaptation: Use as inspiration for no-deploy-success claims without logs, checks, or rollback evidence.

### diagnose — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/diagnose
- Directory description: Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user…
- Local adaptation: Use as inspiration for root-cause analysis on CI/CD, runtime, or performance regressions.

### handoff — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/handoff
- Directory description: Compact the current conversation into a handoff document for another agent to pick up.
- Local adaptation: Use as inspiration for concise release, incident, and rollback handoffs.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
