# Architecture

`opencode-capybara` is a local harness for agent-first engineering in OpenCode.

## Core architecture
User Intent
→ `@orchestrator`
→ task classification
→ `@artifact-planner` for non-trivial work
→ execution-ready plan artifact
→ specialist implementation lanes / worker tasks
→ mechanical gates + evidence collection
→ `@quality-gate`
→ final summary / local commit / follow-up plan

## Brain vs worker model
- **Brain lanes**: `@orchestrator` + `@artifact-planner`
  - `@orchestrator` routes, decomposes, integrates, tracks execution, and runs remediation loops.
  - `@artifact-planner` writes durable plans and execution handoff contracts before non-trivial implementation.
- **Worker lanes**: `@fixer`, `@designer`, `@explorer`, `@librarian`, `@oracle`, `@quality-gate`, `@architect`, and `@visual-context-extractor`. Domain capabilities remain on-demand skills.
  - Workers execute scoped tasks only.
  - Workers do not reroute or delegate on their own.
  - Workers report back to `@orchestrator`.

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

## Optional support guidance
- Caveman guidance is optional support when it helps readability or concise communication.
- It is not required for OpenCode or OpenChamber operation.

## Mechanical enforcement targets
- prompt/config/docs invariants,
- docs integrity and cross-linking,
- agent and skill boundary contracts,
- evidence contract compliance,
- environment and repo health via `doctor`.

## OMP adoption posture (local)
- Canonical runtime lanes remain local capybara lanes.
- Built-in OpenCode `build`/`plan`/`explore`/`general` are comparator/experiment opt-in only, not default routing.
- Contract baseline requires typed outputs + validation ladder + LSP-first execution policy across active lanes.
