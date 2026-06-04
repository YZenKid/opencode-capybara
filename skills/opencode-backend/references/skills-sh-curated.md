# skills.sh inspirations for opencode-backend

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### systematic-debugging — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/systematic-debugging
- Directory description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
- Local adaptation: Use as inspiration for backend failure analysis before patching services or data flows.

### test-driven-development — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/test-driven-development
- Directory description: Use when implementing any feature or bugfix, before writing implementation code
- Local adaptation: Use as inspiration for contract-first, regression-safe backend implementation.

### improve-codebase-architecture — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/improve-codebase-architecture
- Directory description: Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve…
- Local adaptation: Use as inspiration for deeper architectural cleanup and modularity work when the user asks for improvement, not only bugfixing.

### mcp-builder — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/mcp-builder
- Directory description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when…
- Local adaptation: Use as inspiration when backend work crosses into tool/server interfaces and protocol design.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
