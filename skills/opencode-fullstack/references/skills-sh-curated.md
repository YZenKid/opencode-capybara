# skills.sh inspirations for opencode-fullstack

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### frontend-design — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/frontend-design
- Directory description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts,…
- Local adaptation: Use as inspiration for stronger UI quality on vertical slices, without delegating visual taste to generic defaults.

### webapp-testing — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/webapp-testing
- Directory description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing…
- Local adaptation: Use as inspiration for end-to-end browser verification across FE/BE flows.

### systematic-debugging — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/systematic-debugging
- Directory description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
- Local adaptation: Use as inspiration for isolating multi-layer bugs across client, server, and data boundaries.

### test-driven-development — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/test-driven-development
- Directory description: Use when implementing any feature or bugfix, before writing implementation code
- Local adaptation: Use as inspiration for regression-safe vertical-slice implementation.

### improve-codebase-architecture — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/improve-codebase-architecture
- Directory description: Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve…
- Local adaptation: Use as inspiration for discovering deeper cross-layer structural improvements when requested.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
