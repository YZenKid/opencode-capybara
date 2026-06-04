# skills.sh inspirations for opencode-oracle

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### improve-codebase-architecture — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/improve-codebase-architecture
- Directory description: Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve…
- Local adaptation: Use as inspiration for deep architecture improvement reviews tied to domain language and ADRs.

### zoom-out — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/zoom-out
- Directory description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how…
- Local adaptation: Use as inspiration for stepping back from local diffs into system-level reasoning.

### critique — pbakaus/impeccable
- URL: https://www.skills.sh/pbakaus/impeccable/critique
- Directory description: Evaluate design from a UX perspective, assessing visual hierarchy, information architecture, emotional resonance, cognitive load, and overall quality with…
- Local adaptation: Use as inspiration for structured design and product critique when UX quality intersects architecture.

### audit — pbakaus/impeccable
- URL: https://www.skills.sh/pbakaus/impeccable/audit
- Directory description: Run technical quality checks across accessibility, performance, theming, responsive design, and anti-patterns. Generates a scored report with P0-P3 severity…
- Local adaptation: Use as inspiration for scored technical quality reviews across cross-cutting concerns.

### requesting-code-review — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/requesting-code-review
- Directory description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
- Local adaptation: Use as inspiration for pre-merge review posture and standards.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
