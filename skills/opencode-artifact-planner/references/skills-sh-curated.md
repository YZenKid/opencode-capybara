# skills.sh inspirations for opencode-artifact-planner

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### writing-plans — obra/superpowers
- URL: https://www.skills.sh/obra/superpowers/writing-plans
- Directory description: Use when you have a spec or requirements for a multi-step task, before touching code
- Local adaptation: Use as inspiration for turning specs into multi-step implementation plans before touching code.

### to-prd — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/to-prd
- Directory description: Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context.
- Local adaptation: Use as inspiration for converting vague asks or conversation context into concrete product/requirements artifacts.

### zoom-out — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/zoom-out
- Directory description: Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how…
- Local adaptation: Use as inspiration for lifting from ticket-level details into product, architecture, and slice strategy.

### handoff — mattpocock/skills
- URL: https://www.skills.sh/mattpocock/skills/handoff
- Directory description: Compact the current conversation into a handoff document for another agent to pick up.
- Local adaptation: Use as inspiration for concise planner-to-implementer handoff contracts.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
