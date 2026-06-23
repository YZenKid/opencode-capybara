## Start Here
- Routing rules: `.opencode/docs/AGENT_ROUTING.md`
- Architecture: `.opencode/docs/ARCHITECTURE.md`
- Quality and evidence: `.opencode/docs/QUALITY.md`
- Harness evals and replayability: `.opencode/docs/EVALS.md`
- Project stack and tool detection: `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present
- Project framework commands/playbook: `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md` when present
- Security policy: `.opencode/docs/SECURITY.md`
- Prompt gates: `.opencode/docs/PROMPT_GATES.md`
- Skills index: `.opencode/docs/SKILLS.md`
- MCP overview: `.opencode/docs/MCP.md`
- Golden principles: `.opencode/docs/GOLDEN_PRINCIPLES.md`
- Agent legibility: `.opencode/docs/AGENT_LEGIBILITY.md`
- Decisions log: `.opencode/docs/DECISIONS.md`
- Release and operational readiness: `.opencode/docs/RELEASE.md`
- Quality score and GC workflow: `.opencode/docs/QUALITY_SCORE.md`, `.opencode/docs/GC_WORKFLOW.md`

## Notes
- Keep this file short and map-like.
- `.opencode/docs/` is the system of record.
- Plans are first-class artifacts under `.opencode/plans/`.
- Runtime state lives under `.opencode/state/`.
- Non-trivial work should route through `@artifact-planner` and `@orchestrator` before execution.
- Use `@quality-gate` for material changes.
- Use project stack/playbook docs before manual framework edits when present.
- If harness guidance is missing or stale, run `/init-harness` first.
- Prefer evidence over assertion and references over assumptions.
- Keep this file short and map-like.
