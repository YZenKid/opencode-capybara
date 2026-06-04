# skills.sh inspirations for opencode-explorer

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### diagnose — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/diagnose
- Directory description: Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user…
- Local adaptation: Use as inspiration for disciplined discovery loops: reproduce, minimise, instrument, then report evidence instead of guessing.

### zoom-out — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/zoom-out
- Directory description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how…
- Local adaptation: Use as inspiration for situating local findings in wider codebase context.

### browser-use — browser-use/browser-use
- URL: https://www.skills.sh/browser-use/browser-use/browser-use
- Directory description: Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web…
- Local adaptation: Use as inspiration for browser-grounded exploration when web behavior matters and local code alone is not enough.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
