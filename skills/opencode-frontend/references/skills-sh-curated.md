# skills.sh inspirations for opencode-frontend

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### frontend-design — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/frontend-design
- Directory description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts,…
- Local adaptation: Use as inspiration for distinctive, production-grade UI implementation once design direction exists.

### webapp-testing — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/webapp-testing
- Directory description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing…
- Local adaptation: Use as inspiration for Playwright-based browser validation, screenshots, and UI debugging.

### design-taste-frontend — leonxlnx/taste-skill
- URL: https://www.skills.sh/leonxlnx/taste-skill/design-taste-frontend
- Directory description: Senior UI/UX Engineer. Architect digital interfaces overriding default LLM biases. Enforces metric-based rules, strict component architecture, CSS hardware…
- Local adaptation: Use as inspiration for stricter component, spacing, and anti-generic-UI discipline.

### emil-design-eng — emilkowalski/skill
- URL: https://www.skills.sh/emilkowalski/skill/emil-design-eng
- Directory description: This skill encodes Emil Kowalski's philosophy on UI polish, component design, animation decisions, and the invisible details that make software feel great.
- Local adaptation: Use as inspiration for invisible polish, motion restraint, and refined component detail.

### full-output-enforcement — leonxlnx/taste-skill
- URL: https://www.skills.sh/leonxlnx/taste-skill/full-output-enforcement
- Directory description: Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. Apply to any…
- Local adaptation: Use as inspiration for complete deliverables: avoid placeholder code, TODO-only fragments, and half-finished UI outputs.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
