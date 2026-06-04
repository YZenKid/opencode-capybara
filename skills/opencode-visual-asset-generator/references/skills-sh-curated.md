# skills.sh inspirations for opencode-visual-asset-generator

Curated external references from https://www.skills.sh for this agent lane.
These are reference inputs only. This repo still keeps one skill folder per agent; absorb useful practices here instead of creating separate local skill folders.

## Selected references

### ai-image-generation — doany-ai/skills
- URL: https://www.skills.sh/doany-ai/skills/ai-image-generation
- Directory description: Generate and edit images on RunComfy via the `runcomfy` CLI — a smart router across the full image-model catalog: FLUX 2 (Klein 9B/4B, Pro, Dev, Flash, Turbo,…
- Local adaptation: Use as inspiration for model-routing awareness, generation task selection, and image output discipline.

### image-edit — doany-ai/skills
- URL: https://www.skills.sh/doany-ai/skills/image-edit
- Directory description: Edit images on RunComfy — this skill is a smart router that matches the user's intent to the right edit model in the RunComfy catalog. Picks Nano Banana Edit…
- Local adaptation: Use as inspiration for edit-first workflows when a base image exists and pure generation is not enough.

### gpt-image-2 — agentspace-so/agent-skills
- URL: https://www.skills.sh/agentspace-so/agent-skills/gpt-image-2
- Directory description: Generate images with GPT Image 2 (ChatGPT Images 2.0) inside Claude Code, using your existing ChatGPT Plus or Pro subscription — no separate OpenAI access, no…
- Local adaptation: Use as inspiration for agent-mediated image generation workflows and provider constraint awareness.

## Adaptation rules

- Prefer exact repo-local evidence and official docs over imported taste or workflow defaults.
- Treat these references as inspiration, not as authority to bypass this agent's local boundaries.
- If a referenced pattern conflicts with local `AGENTS.md`, `.opencode/docs/`, project `DESIGN.md`, or this skill's own contracts, local rules win.
