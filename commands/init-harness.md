---
description: Initialize or update the current project's AGENTS.md for the harness workflow
agent: orchestrator
model: cliproxyapi/gpt-5.4
---

Initialize a project-local `AGENTS.md` for the current target project so it matches the current harness workflow and rules.

Arguments from user, if any:

```text
$ARGUMENTS
```

Workflow:

1. Inspect the current target project root before writing anything.
2. Read the existing root `AGENTS.md` if it exists.
3. Inspect `.opencode/docs/index.md` first when present, then review the full canonical doc set when it exists: `.opencode/docs/AGENT_ROUTING.md`, `.opencode/docs/ARCHITECTURE.md`, `.opencode/docs/AGENT_LEGIBILITY.md`, `.opencode/docs/QUALITY.md`, `.opencode/docs/EVALS.md`, `.opencode/docs/SECURITY.md`, `.opencode/docs/PROMPT_GATES.md`, `.opencode/docs/SKILLS.md`, `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`, `.opencode/docs/GOLDEN_PRINCIPLES.md`, `.opencode/docs/DECISIONS.md`, `.opencode/docs/RELEASE.md`, `.opencode/docs/QUALITY_SCORE.md`, and `.opencode/docs/GC_WORKFLOW.md`.
4. Run an explicit project tech-stack discovery workflow before drafting: inspect README plus package/lock/build/runtime manifests and validation scripts (for example `package.json`, `pnpm-lock.yaml`, `requirements*.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`, Docker/compose files, CI workflows, and test/lint scripts) so routing and validation guidance is project-specific.
5. Capture concise stack-and-tooling findings (languages, frameworks, package managers, test runners, linters, build/deploy surfaces) and reflect them in `AGENTS.md` instead of generic advice.
6. Keep repo-local-docs-first posture. Use external references only when local evidence is insufficient or version-sensitive, following `.opencode/docs/TOOL_USAGE.md` (prefer official docs via `context7`, then source/examples via GitHub, then broad web search).
7. If external references are needed, state what was checked and why in the final summary.
8. If `AGENTS.md` already exists at the project root, ask before overwriting or replacing it.
9. If no root `AGENTS.md` exists, create one in the current project root.
10. Keep the file in English and keep it short: target under 60 lines, never exceed 100.
11. Treat `AGENTS.md` as a map, not an encyclopedia. Detailed policy belongs in `.opencode/docs/` and mechanical checks.
12. Prefer repo-local docs over embedded long-form instructions. Point to canonical docs instead of duplicating policy.
13. If the project already uses a docs-as-system-of-record workflow, reflect it explicitly.
14. If canonical docs are missing under `.opencode/docs/`, scaffold the full canonical system-of-record first (create `.opencode/docs/index.md` plus the current canonical corpus files), then write `AGENTS.md`; do not produce placeholder or missing-doc links.
15. The scaffolded canonical docs must contain comparable operational detail (not placeholders) across concerns: routing thresholds and delegation boundaries, tool/MCP state boundaries, quality and evidence expectations, evals/replayability posture, prompt gates and mechanical checks, security constraints, skills ownership and division of labor, decisions/release/GC workflow, and architecture context.
16. Keep `AGENTS.md` short and map-like by linking to canonical docs instead of embedding long policy text.
17. Include the current routing and validation posture that future agents must follow.
18. Make the division of labor legible: future readers should understand that `@orchestrator` routes/integrates, while specialists and subagents own bounded execution, design, research, review, and domain-risk work.
19. Make agent/subagent capabilities explicit enough that work does not collapse back into `@orchestrator` by default. Mention where to look for the full role/capability matrix when the project uses many specialists.
20. In `AGENTS.md`, include a short role-and-skill ownership note that explains what the most important agents are for: routing/integration, planning, bounded implementation, architecture/review, UI/design, discovery/docs research, and final quality signoff.
21. Use the unified helper lane names directly (`@architect`, `@quality-gate`) so a future operator can route quickly without reading every agent file.
22. When the project also uses project-local design guidance, mention the downstream UI ownership chain clearly: `@designer` first, then UI specialist review lanes and `@quality-gate` when relevant.
23. Use the user's hints from `$ARGUMENTS` only to specialize the file; do not discard the harness baseline.
24. Do not silently overwrite existing project-specific rules.
25. Explicitly state which agent should be used first for default execution (`@orchestrator`).

Write `AGENTS.md` using exactly these sections, in this order:

- Start Here
- Non-negotiable Rules
- Default Flow
- Harness Posture
- Risk Triggers
- Notes

Use this structure:

```markdown
# AGENTS.md

## Start Here
- Routing rules: `.opencode/docs/AGENT_ROUTING.md`
- Architecture: `.opencode/docs/ARCHITECTURE.md`
- Quality and evidence: `.opencode/docs/QUALITY.md`
- Harness evals and replayability: `.opencode/docs/EVALS.md`
- Security policy: `.opencode/docs/SECURITY.md`
- Prompt gates: `.opencode/docs/PROMPT_GATES.md`
- Skills index: `.opencode/docs/SKILLS.md`
- MCP overview: `.opencode/docs/MCP.md`
- Golden principles: `.opencode/docs/GOLDEN_PRINCIPLES.md`
- Agent legibility: `.opencode/docs/AGENT_LEGIBILITY.md`
- Decisions log: `.opencode/docs/DECISIONS.md`
- Release and operational readiness: `.opencode/docs/RELEASE.md`
- Quality score and GC workflow: `.opencode/docs/QUALITY_SCORE.md`, `.opencode/docs/GC_WORKFLOW.md`

## Non-negotiable Rules
- Do not prefix shell commands with `rtk` in OpenCode sessions or OpenChamber sessions that invoke OpenCode.
- RTK may be installed by explicit setup, but OpenCode auto-rewrite/prefix remains opt-in unless user explicitly asks; OpenChamber should follow that OpenCode posture rather than redefine it.
- Token compression/context packing should use RTK and Caveman together when that capability is needed; do not invent a parallel local compression flow or treat them as either/or alternatives.
- Never commit secrets, tokens, or `.env` files.
- Use `@orchestrator` for routing and integration.
- Use `@quality-gate` for material changes, including non-trivial/risky work, prompt/config changes, and security-sensitive changes.
- Prefer evidence over assertion.
- Prefer repo-local docs over chat memory.
- Do not modify files from read-only reviewer agents.
- Keep `AGENTS.md` short; detailed policy belongs in `.opencode/docs/` and mechanical checks.

## Default Flow
User intent → `@orchestrator` → specialist agents → validation → `@quality-gate` → final summary.

## Harness Posture
- `.opencode/docs/` is the repository knowledge system of record.
- `AGENTS.md` is the map, not the encyclopedia.
- Plans are first-class artifacts under `.opencode/plans/`.
- Evidence is required for material changes.
- Repeated failures should produce docs, gate, script, or skill improvements.
- `@orchestrator` routes, decomposes, and integrates; do not let all implementation collapse into direct orchestrator execution.
- Specialists and subagents should own bounded work according to their documented capabilities in `.opencode/docs/AGENT_ROUTING.md` and `.opencode/docs/SKILLS.md`.
- Core ownership shorthand: `@orchestrator` routes/integrates, `@artifact-planner` writes plans, `@fixer` implements bounded changes/tests, `@oracle` handles architecture/review, `@designer` owns UI/UX, `@explorer`/`@librarian` handle discovery/docs, and `@quality-gate` does final signoff.

## Risk Triggers
- Product/SaaS/platform/AI/UI-system architecture ambiguity → `@architect`
- PII/auth/payments/uploads/biometric/privacy + accessibility/visual-parity final signoff → `@quality-gate`
- User-facing UI/reference/animation/accessibility/design-system work → `@designer` plus UI specialists as needed

## Notes
- For substantial UI work, inspect the target project's `DESIGN.md` first, then `design-system/DESIGN.md` or a documented equivalent.
- For image-heavy or reference UI work, require evidence, asset decisions, and legal style-equivalent handling.
- If the project has many agents/subagents, document the role and primary skill ownership clearly enough that future work does not default back to `@orchestrator` for planning, implementation, review, or research.
- If many agents are available, future operators should read `.opencode/docs/AGENT_ROUTING.md` and `.opencode/docs/SKILLS.md` first to understand who owns discovery, implementation, review, design, and domain-specific risk.
- For full operational details, follow the linked docs rather than expanding this file.
```

After writing the file, summarize:

- where `AGENTS.md` was created or updated,
- which repo-local docs and scripts informed it,
- any assumptions made,
- whether a `.opencode/docs/` system-of-record scaffold is still missing,
- what future agents should read first.
