# skills.sh inspirations for opencode-mobile

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### systematic-debugging — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/systematic-debugging
- Directory description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
- Local adaptation: Use as inspiration for reproducing and isolating device- or interaction-driven issues before changing code.

### test-driven-development — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/test-driven-development
- Directory description: Use when implementing any feature or bugfix, before writing implementation code
- Local adaptation: Use as inspiration for behavior-first mobile changes with test or reproducibility evidence.

### zoom-out — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/zoom-out
- Directory description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how…
- Local adaptation: Use as inspiration for considering navigation, permissions, offline, and platform context instead of patching one component in isolation.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
