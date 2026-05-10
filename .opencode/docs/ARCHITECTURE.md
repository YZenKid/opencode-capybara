# Architecture

`opencode-capybara` is a local harness for agent-first engineering in OpenCode.

## Core architecture
User Intent
→ `@orchestrator`
→ task classification
→ specialist lane
→ mechanical gates
→ evidence collection
→ `@quality-gate`
→ final summary / local commit / follow-up plan

## Primary repository layers
- **Root config** — `opencode.json`, `tui.json`, `AGENTS.md`
- **Agent contracts** — `agents/*.md`
- **Skill contracts** — `skills/opencode-*/SKILL.md`
- **Commands** — `commands/*.md`
- **Scripts / gates** — `scripts/*.mjs`
- **Docs system of record** — `.opencode/docs/`
- **Plans and evidence** — `.opencode/plans/`, `.opencode/evidence/`, `.opencode/draft/`

## System-of-record policy
- `AGENTS.md` is the short entrypoint.
- `.opencode/docs/` is the durable policy/reference layer.
- `scripts/*` are the enforceable controls.
- `.opencode/` contains task-local plans and evidence.

## Mechanical enforcement targets
- prompt/config/docs invariants,
- docs integrity and cross-linking,
- agent and skill boundary contracts,
- evidence contract compliance,
- environment and repo health via `doctor`.
