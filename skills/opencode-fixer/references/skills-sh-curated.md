# skills.sh inspirations for opencode-fixer

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### systematic-debugging — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/systematic-debugging
- Directory description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
- Local adaptation: Use as inspiration for understanding bugs before editing code.

### test-driven-development — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/test-driven-development
- Directory description: Use when implementing any feature or bugfix, before writing implementation code
- Local adaptation: Use as inspiration for Red → Green → Refactor discipline on features and bugfixes.

### diagnose — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/diagnose
- Directory description: Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user…
- Local adaptation: Use as inspiration for hard-bug instrumentation and regression isolation loops.

### verification-before-completion — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/verification-before-completion
- Directory description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output…
- Local adaptation: Use as inspiration for proving fixes with commands and output before claiming success.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
