# Agent Routing

## Default flow
User intent → `@orchestrator` → specialist agents → validation → `@quality-gate` → final summary.

## Execution posture
- For implementation requests or plan execution, `@orchestrator` should use a finish-first default: continue work as far as safely and feasibly possible before asking the user follow-up questions.
- Treat gates, phases, work packages, and milestones in a plan as internal checkpoints rather than approval checkpoints, unless an explicit marker such as `requires_user_decision` is present.
- When a blocker appears, investigate first through repo evidence, docs, tools, and the most capable subagent.
- Accumulate non-blocking questions and present them at the end together with assumption/risk notes rather than using them to interrupt execution momentum.
- Pause mid-run only for destructive decisions, security/privacy boundaries, truly unavailable required access, or material non-reversible ambiguity.

Planner invocation expectation:
- Non-trivial tasks should route through `@artifact-planner` first so implementation is plan-bound with explicit evidence paths.
- Trivial, single-step, and easily reversible tasks may execute directly without planner.

## Direct-work thresholds for `@orchestrator`
`@orchestrator` is a router/integrator first, not the default worker. Direct execution is allowed only for tiny tasks.

`@orchestrator` may act directly only when **all** conditions are true:
- scope is trivial, single-step, and easily reversible,
- at most 1 file is edited,
- at most 3 files are read for local confirmation,
- no unknown-scope discovery is required,
- no risk trigger/domain specialist lane is required.

`@orchestrator` must delegate by default when one of these is true:
- discovery is unknown-scope, cross-area, or read-heavy (>3 files) → `@explorer`,
- implementation is bounded but touches 2+ files (including code+test/docs pair) → `@fixer`,
- work is non-trivial or has material ambiguity/risk → `@artifact-planner` first,
- change is material and needs completion claim → final pass through `@quality-gate`.

Permitted fallback: if a specialist is unavailable, use the next safest lane and record the limitation explicitly in final evidence.

## Routing anti-patterns (and remediation)
- Anti-pattern: delegate discovery to `@explorer`, then `@orchestrator` still reads many files and redoes discovery.
  - Remediation: consume explorer output; only perform minimal spot-check reads.
- Anti-pattern: `@orchestrator` performs multi-file implementation directly because "it is faster".
  - Remediation: route bounded implementation to `@fixer`.
- Anti-pattern: non-trivial implementation starts without plan/evidence path.
  - Remediation: route to `@artifact-planner` first, then implement plan-bound.
- Anti-pattern: completion claim on material change without `@quality-gate`.
  - Remediation: run final conformance gate before claiming done.

## Compact routing quality checklist
Use this quick rubric for real workflow audits:

- [ ] **Lane fit**: discovery/implementation/review went to the expected primary lanes.
- [ ] **Threshold compliance**: orchestrator direct work stayed within tiny-task limits.
- [ ] **Planner-first**: non-trivial work is plan-bound before implementation.
- [ ] **Evidence legibility**: delegation choices and fallback reasons are explicitly recorded.
- [ ] **Final gate**: material changes include `@quality-gate` pass/verdict.

Score guidance: 5/5 = strong routing discipline; 3–4/5 = acceptable with minor drift; ≤2/5 = routing failure requiring remediation.

## Primary lanes
- `@orchestrator` — router, integrator, final coordinator
- `@artifact-planner` — writes plans, drafts, and evidence artifacts under `.opencode/`
- `@explorer` — codebase discovery and reuse mapping
- `@librarian` — library/API docs and official references
- `@fixer` — bounded implementation, tests, Red/Green/Refactor
- `@oracle` — architecture, maintainability, simplification, deep review
- `@designer` — UI/UX, visual polish, reference work, design-system direction
- `@quality-gate` — final conformance and risk review

## Conditional domain specialists
- PRD/product blueprint work → `@product-architect`
- SaaS architecture → `@saas-architect`
- AI system design → `@ai-systems-architect`
- Security/privacy review → `@security-privacy-reviewer`
- Release/ops readiness → `@release-engineer`
- Mobile/hybrid architecture → `@mobile-architect`

Domain specialists are conditional. Tiny UI polish still goes to `@designer`. Isolated bugfixes still go to `@fixer` unless a risk trigger applies.

## UI and reference policy
- First inspect the target project's `DESIGN.md`.
- If missing, inspect `design-system/DESIGN.md` or equivalent.
- Suggest `/init-design` for substantial UI work without project-local guidance.
- Avoid generic UI, numeric-only service icons, and blank image frames.
- Require visual density, production-like screenshots, designer signoff, and reference/current/final evidence for substantial UI/reference work.
- Generic hover-only motion is not enough for substantial reference work.
- Treat image-heavy work explicitly with an image generation decision and legal style-equivalent generation when needed.
- Do not leave final sections as CSS placeholders when imagery materially affects quality.

## General Design Readiness Gate
For substantial UI/UX work, high-level visual direction is not enough. Require a UI/UX Design Blueprint with:
- Experience direction
- Page-by-page UX blueprint
- Section-level visual specification
- Component system plan
- Visual system
- Asset and image decision
- Motion system
- Interaction and state design
- Responsive plan
- Accessibility gate
- Validation evidence

If the blueprint is incomplete, status must be `blocked`, `needs-polish`, or `draft`, not `done`.

## Risk triggers
- auth, PII, tenant isolation, payment, upload, secrets, token/session handling, biometric data, permission/RBAC → security review
- architecture boundary, new abstraction, large refactor, dependency direction, data model change → oracle
- visual layout change, animation, accessibility, design token, screenshot/reference parity, responsive behavior → designer plus relevant UI specialists
- CI/CD, deployment, env var, migration, monitoring, rollback → release engineer
