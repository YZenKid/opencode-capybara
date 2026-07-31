# AGENTS.md

## Start Here
- Routing rules: `.opencode/docs/AGENT_ROUTING.md`
- Architecture: `.opencode/docs/ARCHITECTURE.md`
- Quality and evidence: `.opencode/docs/QUALITY.md`
- Harness evals and replayability: `.opencode/docs/EVALS.md`
- Runtime execution state: `.opencode/docs/STATE_RUNTIME.md`, `.opencode/docs/DURABLE_EXECUTION.md`, `.opencode/docs/WORKTREE_RUNTIME.md`, `.opencode/docs/VERIFY_FIX_LOOP.md`, `.opencode/docs/WORKER_BACKENDS.md`, `.opencode/docs/DETERMINISTIC_EDIT_RUNTIME.md`
- Project stack and tool detection: `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present
- Project framework commands/playbook: `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md` when present
- Security policy: `.opencode/docs/SECURITY.md`
- Prompt gates: `.opencode/docs/PROMPT_GATES.md`
- Skills index: `.opencode/docs/SKILLS.md`
- MCP overview: `.opencode/docs/MCP.md`
- Golden principles: `.opencode/docs/GOLDEN_PRINCIPLES.md`
- Execution conduct (finish-first, question batching, internet-reference default): `.opencode/docs/EXECUTION_CONDUCT.md`
- Agent legibility: `.opencode/docs/AGENT_LEGIBILITY.md`
- Decisions log: `.opencode/docs/DECISIONS.md`
- Release and operational readiness: `.opencode/docs/RELEASE.md`
- Quality score and GC workflow: `.opencode/docs/QUALITY_SCORE.md`, `.opencode/docs/GC_WORKFLOW.md`

## Non-negotiable Rules
- Keep shell command usage explicit and reviewable in OpenCode sessions and OpenChamber sessions that invoke OpenCode.
- Use Caveman guidance as an optional support utility when it helps readability or concise communication; do not treat it as required.
- Never commit secrets, tokens, or `.env` files.
- Use `@orchestrator` for routing and integration.
- Use `@quality-gate` for material changes, including non-trivial/risky work, prompt/config changes, and security-sensitive changes.
- Harness Preflight Gate: before non-trivial work, `@orchestrator` must verify the target project has a current root `AGENTS.md`, canonical `.opencode/docs/`, and root `DESIGN.md` when UI/design work is involved.
- For framework-managed artifacts, follow project-local `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` before manual edits when those docs are present.
- If harness guidance is missing/stale, run `/init-harness` first, or ask the user to run `/init-harness` when command execution is unavailable. Skip only for tiny, read-only, or emergency tasks and record the skip reason in the final summary.
- Prefer evidence over assertion.
- For broad architecture/dependency discovery, query Graphify first when `.opencode/graphify-out/graph.json` exists and is fresh. Use narrow `query`, `path`, or `explain` requests; treat `INFERRED` and `AMBIGUOUS` edges as leads only.
- Graphify is optional, local, code-only, read-only discovery context. It never replaces direct source reading, tests, or runtime checks. If graph is missing or stale, use normal repo discovery or refresh graph when permitted.
- Prefer references over assumptions. If repo files, official docs, upstream source, screenshots/reference URLs, or runtime evidence are reasonably available, use them before inventing details.
- Creativity must stay grounded. For greenfield/product/UI work, generate 2-3 bounded options from evidence or explicit first principles when that materially improves quality, then choose and explain.
- Do not let checklist compliance override stronger evidence, better references, or clear runtime feedback.
- Prefer repo-local docs over chat memory.
- Do not modify files from read-only reviewer agents.
- Keep `AGENTS.md` short; detailed policy belongs in `.opencode/docs/` and mechanical checks.
- Visual understanding from screenshots/images/mockups/diagrams must route to `@visual-context-extractor` first. No agent except the extractor may self-infer from visual input. Downstream decisions remain with designer/fixer/etc.
- **UI/UX catalog source of truth**: substantial UI work anchors to the **Open Design catalog** at `open-design.ai` (150 design systems, 290 templates) — see `.opencode/plans/ui-ux-open-design-upgrade.md` and `.opencode/catalog/INDEX.md`. Project `DESIGN.md` must use the v2 schema with `catalog_citation` block. `@designer` selects, `@frontend`/`@mobile` implement from the cited catalog, `@quality-gate` enforces.

## Default Flow
User intent → `@orchestrator` → specialist agents → validation → `@quality-gate` → final summary.

`@artifact-planner` is a **triggered planning lane** (not default tax). Use it only when planning complexity, unresolved architecture/security/data/product decisions, multi-phase scope, or evidence-heavy work require durable planning artifacts.
Bounded Maintenance Direct Fix may skip planner when work is bounded, existing-code, and decision-complete; trivial single-step and easily reversible tasks may skip planner.

Default operating model:
- **6 core agents**: `@orchestrator`, `@explorer`, `@fixer`, `@designer`, `@oracle`, `@quality-gate`
- **Helper lanes (triggered as needed)**: `@architect`, `@artifact-planner`, `@librarian`, `@skill-improver`

`AGENT_ROUTING.md` is the source of truth for routing and ownership.

## Harness Posture
- `.opencode/docs/` is the repository knowledge system of record.
- `AGENTS.md` is the map, not the encyclopedia.
- Plans are first-class artifacts under `.opencode/plans/`.
- Runtime state lives under `.opencode/state/` for durable runs, task queues, mailbox, memory, and worktree metadata.
- Evidence is required for material changes.
- Repeated failures should produce docs, gate, script, or skill improvements.
- `@orchestrator` routes, decomposes, and integrates; do not let all implementation collapse into direct orchestrator execution.
- Specialists and subagents should own bounded work according to their documented capabilities in `.opencode/docs/AGENT_ROUTING.md` and `.opencode/docs/SKILLS.md`.
- Core ownership shorthand: `@orchestrator` routes/integrates, `@fixer` implements bounded changes/tests, `@oracle` handles architecture/review, `@designer` owns UI/UX, `@explorer` handles discovery, and `@quality-gate` does final signoff.

## Risk Triggers
- Product ambiguity and SaaS/multi-tenant/RBAC/billing boundaries → `@architect`
- AI/LLM/RAG/evals architecture boundaries → `@architect`
- CI/CD/env/deploy/migration/monitoring and Native mobile/hybrid/PWA/offline/push/deep links/camera/QR constraints → `@architect`
- Product/SaaS/platform/AI/UI-system architecture boundaries → `@architect`
- Security/privacy/accessibility/visual-parity final signoff → `@quality-gate`
- PII/auth/payments/uploads/biometric/privacy final signoff → `@quality-gate`
- Document/file-centric read-only extraction/research/transformation support (PDF/sheets/Office) → supporting `@librarian` lane
- Prompt/skill/routing improvement after repeated failure/evidence → `@skill-improver`
- Current library/API docs lookup when local context is insufficient → supporting `@librarian` research lane
- User-facing UI/reference/animation/accessibility/design-system work → `@designer`

## Notes
- For substantial UI work, inspect the target project's `DESIGN.md` first, then `design-system/DESIGN.md` or a documented equivalent.
- For framework-managed artifacts in existing apps or greenfield work, inspect `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` first when present; follow project framework playbook/commands before manual edits.
- For image-heavy or reference UI work, require evidence, asset decisions, direct reuse inventory, and style-equivalent fallback handling.
- Asset reuse is globally loosened (Option B, see `.opencode/docs/DECISIONS.md`): user-directed direct reuse is allowed, but users/projects own license/trademark/production-use risk and direct reuse must never be silent.
- If the project has many agents/subagents, document the role and primary skill ownership clearly enough that future work does not default back to `@orchestrator` for planning, implementation, review, or research.
- If many agents are available, read `.opencode/docs/AGENT_ROUTING.md` and `.opencode/docs/SKILLS.md` first to understand who owns discovery, implementation, review, design, and domain-specific risk.
- For full operational details, follow the linked docs rather than expanding this file.
