# Agent Routing

## Default flow
User intent → `@orchestrator` → specialist agents → validation → `@quality-gate` → final summary.

## Execution posture
- For implementation requests or plan execution, `@orchestrator` should use a finish-first default: continue work as far as safely and feasibly possible before asking the user follow-up questions.
- Treat gates, phases, work packages, and milestones in a plan as internal checkpoints rather than approval checkpoints, unless an explicit marker such as `requires_user_decision` is present.
- When a blocker appears, investigate first through repo evidence, docs, tools, and the most capable subagent.
- Accumulate non-blocking questions and present them at the end together with assumption/risk notes rather than using them to interrupt execution momentum.
- Pause mid-run only for destructive decisions, security/privacy boundaries, truly unavailable required access, or material non-reversible ambiguity.

## Primary lanes
- `@orchestrator` — router, integrator, final coordinator
- `@artifact-planner` — writes plans, drafts, and evidence artifacts under `.opencode/`
- `@explorer` — codebase discovery and reuse mapping
- `@librarian` — library/API docs and official references
- `@fixer` — bounded implementation, tests, Red/Green/Refactor
- `@oracle` — architecture, maintainability, simplification, deep review
- `@designer` — UI/UX, visual polish, reference work, design-system direction
- `@quality-gate` — final conformance and risk review

## Conditional helper lanes
- Unified architecture advisory (product/SaaS, AI, platform/runtime/release/mobile, UI-system boundaries) → `@architect`
- Security/privacy/accessibility/visual-parity final signoff → `@quality-gate`

Helper lanes are conditional. Tiny UI polish still goes to `@designer`. Isolated bugfixes still go to `@fixer` unless a risk trigger applies.

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
- auth, PII, tenant isolation, payment, upload, secrets, token/session handling, biometric data, permission/RBAC → `@architect` for design decisions, `@quality-gate` for final signoff
- architecture boundary, new abstraction, large refactor, dependency direction, data model change → oracle
- visual layout change, animation, accessibility, design token, screenshot/reference parity, responsive behavior → designer plus relevant UI specialists
- CI/CD, deployment, env var, migration, monitoring, rollback, mobile/offline/push/deep-links/platform runtime constraints → `@architect`
