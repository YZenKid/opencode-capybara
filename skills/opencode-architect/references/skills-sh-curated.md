# skills.sh inspirations for opencode-architect

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### improve-codebase-architecture — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/improve-codebase-architecture
- Directory description: Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve…
- Local adaptation: Use as inspiration for finding deeper architectural improvement opportunities beyond the immediate ticket.

### to-prd — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/to-prd
- Directory description: Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context.
- Local adaptation: Use as inspiration when architecture framing must grow out of product/problem statements, not isolated tech choices.

### zoom-out — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/zoom-out
- Directory description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how…
- Local adaptation: Use as inspiration for big-picture system reasoning and tradeoff framing.

### mcp-builder — anthropics/skills
- URL: https://www.skills.sh/anthropics/skills/mcp-builder
- Directory description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when…
- Local adaptation: Use as inspiration when architecture work includes MCP/tooling interface design.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
