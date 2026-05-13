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
3. Inspect `.opencode/docs/index.md` first when present, then review the full canonical doc set when it exists: `.opencode/docs/AGENT_ROUTING.md`, `.opencode/docs/AGENT_LEGIBILITY.md`, `.opencode/docs/QUALITY.md`, `.opencode/docs/EVALS.md`, `.opencode/docs/SECURITY.md`, `.opencode/docs/PROMPT_GATES.md`, `.opencode/docs/SKILLS.md`, `.opencode/docs/MCP.md`, `.opencode/docs/GOLDEN_PRINCIPLES.md`, `.opencode/docs/DECISIONS.md`, `.opencode/docs/RELEASE.md`, `.opencode/docs/QUALITY_SCORE.md`, and `.opencode/docs/GC_WORKFLOW.md`.
4. Inspect the project README, package manager files, and validation scripts so the file reflects the real workflow instead of generic advice.
5. If `AGENTS.md` already exists at the project root, ask before overwriting or replacing it.
6. If no root `AGENTS.md` exists, create one in the current project root.
7. Keep the file in English and keep it short: target under 60 lines, never exceed 100.
8. Treat `AGENTS.md` as a map, not an encyclopedia. Detailed policy belongs in `.opencode/docs/` and mechanical checks.
9. Prefer repo-local docs over embedded long-form instructions. Point to canonical docs instead of duplicating policy.
10. If the project already uses a docs-as-system-of-record workflow, reflect it explicitly.
11. If the project does not yet have canonical docs under `.opencode/docs/`, ask whether to scaffold the docs system of record before inventing placeholder links.
12. Include the current routing and validation posture that future agents must follow.
13. Make the division of labor legible: future readers should understand that `@orchestrator` routes/integrates, while specialists and subagents own bounded execution, design, research, review, and domain-risk work.
14. Make agent/subagent capabilities explicit enough that work does not collapse back into `@orchestrator` by default. Mention where to look for the full role/capability matrix when the project uses many specialists.
15. In `AGENTS.md`, include a short role-and-skill ownership note that explains what the most important agents are for: routing/integration, planning, bounded implementation, architecture/review, UI/design, discovery/docs research, and final quality signoff.
16. Use merged specialist lane names directly (`@product-systems-architect`, `@platform-architect`, `@security-risk-reviewer`) so a future operator can route quickly without reading every agent file.
17. When the project also uses project-local design guidance, mention the downstream UI ownership chain clearly: `@designer` first, then UI specialist review lanes and `@quality-gate` when relevant.
18. Use the user's hints from `$ARGUMENTS` only to specialize the file; do not discard the harness baseline.
19. Do not silently overwrite existing project-specific rules.

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
- Product ambiguity/SaaS boundaries (MVP, flows, tenancy, RBAC, billing) → `@product-systems-architect`
- AI/LLM/RAG/evals → `@ai-systems-architect`
- PII/auth/payments/uploads/biometric/privacy → `@security-risk-reviewer`
- CI/CD/env/deploy/migration/monitoring + native mobile/hybrid/offline/push/deep-links constraints → `@platform-architect`
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
