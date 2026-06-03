# Agent Routing

Capability registry: `.opencode/capabilities/registry.json`. Generated advisory view: `docs/generated/capability-matrix.md`.

## Default flow
User intent → `@orchestrator` → specialist agents → validation → `@quality-gate` → final summary.

## Execution posture
- For implementation requests or plan execution, `@orchestrator` should use a finish-first default: continue work as far as safely and feasibly possible before asking the user follow-up questions.
- Treat gates, phases, work packages, and milestones in a plan as internal checkpoints rather than approval checkpoints, unless an explicit marker such as `requires_user_decision` is present.
- When a blocker appears, investigate first through repo evidence, docs, tools, and the most capable subagent.
- Use blocker taxonomy:
  - `hard_stop`: destructive/irreversible approval boundary, security/privacy/secrets decision boundary, truly unavailable required access/dependency, contradictory requirements, or material non-reversible decision with no safe subset.
  - `soft_blocker`: continue safe subset and record risk.
  - `deferred_question`: queue to final summary.
  - `follow_up`: non-blocking continuation item.
- Advisory lanes are non-veto by default. Advisory labels (`needs-architect-decisions`, `blocked`, `Material block exists`) must be reclassified via taxonomy + repo evidence before stopping.
- Accumulate non-blocking questions and present them at the end together with assumption/risk notes rather than using them to interrupt execution momentum.
- Pause mid-run only for `hard_stop`.

Planner invocation expectation:
- `@artifact-planner` is a **triggered lane**, not default-first.
- Invoke it for multi-phase, spec-heavy, materially ambiguous, or evidence-heavy work.
- Trivial, single-step, and easily reversible tasks may execute directly without planner.
- Non-trivial tasks should route through `@artifact-planner` first when planning depth/evidence is required.
- Planner handoff quality bar: non-trivial plans must include an explicit `Execution-ready Worklist / Handoff Contract` with ordered atomic tasks, dependencies, owner/lane, validation, exit criteria, blocking status, and a `start_with` first action for orchestrator.

## Plan-bound execution contract (orchestrator)
- If a primary plan includes `Execution-ready Worklist / Handoff Contract`, treat it as execution source of truth.
- Start from `start_with` and run all non-blocked tasks in order using declared dependencies/lanes.
- Treat milestones/phases as internal progress markers, not stop points.
- Stop only for `hard_stop` conditions or explicit `requires_user_decision` boundaries.
- Advisory/worklist labels using `blocked` must be normalized into the blocker taxonomy before orchestrator decides to stop.
- Completion claim requires finishing every non-blocked task and satisfying plan done criteria.

## Mode-aware execution contracts

Before non-trivial routing, classify the request into one mode and record the mode in evidence or handoff notes.

### Greenfield App Accelerator
Use for new apps, blank repos, MVPs, SaaS/product builds, or major product revamps.

- Always route new app/MVP/SaaS/product builds to `@artifact-planner` before implementation except explicitly tiny prototype-only work labeled `draft`/`prototype`.
- Optimize for the first usable vertical slice, not whole-app perfection.
- Explore 2-3 credible product/UX/architecture options, compare tradeoffs, then converge.
- Allow `PASS_FOR_SLICE` execution when whole-product decisions remain open but the selected slice avoids locking those decisions.
- Allow `@fullstack` to own one bounded greenfield vertical slice when FE/BE coupling is high and contracts are clear enough.
- Allow `@fixer` to scaffold or implement only from a ready slice plan, not from a vague product idea.
- Require enough design direction for MVP usefulness; require the full visual/reference gate only when the work is substantial UI, image-heavy, or parity-driven.
- Final claim should be `MVP slice complete` unless the whole app is actually finished and validated.

### Maintenance Stability Mode
Use for bugfixes, regressions, refactors, dependency updates, small features in existing apps, and incident follow-up.

- Maintenance work should not be forced through greenfield product thesis, 2-3 creative alternatives, or whole-app planning by default.
- Do not require product thesis, 2-3 creative alternatives, or greenfield gates by default.
- Start with repro, regression test, targeted evidence, or clear failing behavior.
- Prefer the smallest safe diff and preserve existing architecture/UX unless the bug proves they are broken.
- Use `@explorer` for local facts, `@fixer` or the domain lane for implementation, and `@quality-gate` for material/risky changes.
- Ask only for material behavior, security, privacy, product, or irreversible decisions.

## Best Practice Readiness Contract
Non-trivial work is not ready to implement until the handoff identifies the mode, goal, non-goals, constraints, acceptance criteria, owner/lane, validation path, evidence path, and blocker class. Fresh app/product work must also identify material product, data, auth, payment, privacy, RBAC, platform, UI, and release decisions as answered, deferred, slice-safe, or blocked.

## Creative Depth Contract
For Greenfield App Accelerator work, plans must include: product thesis and target pain; 2-3 viable product/UX approaches before choosing one; architecture options with tradeoff scoring; first vertical slice options and chosen-slice rationale; `user journey → data model → API/contracts → UI screens → tests` mapping; design readiness summary; differentiation ideas bounded by MVP scope; and readiness status (`draft`, `blocked`, `ready-for-slice`, or `ready-for-implementation`). Plans missing this contract are not execution-ready.

## Plan Quality Gate
Before `@orchestrator` executes a non-trivial plan, classify readiness:

- `PASS`: plan has material decisions, creative alternatives where required, tradeoffs, TDD, validation, and worklist ready.
- `PASS_FOR_SLICE`: whole product has open questions, but the first slice is safe, explicit, and does not lock unresolved decisions.
- `NEEDS_DEPTH`: plan has sections but lacks substance, alternatives, mapping, evidence, or validation detail.
- `BLOCKED`: material decision missing and no safe slice exists.

Only `PASS` and `PASS_FOR_SLICE` may proceed to implementation. `NEEDS_DEPTH` goes back to planner/advisory lanes. `BLOCKED` asks the user or waits for required access/decision.

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
- work is multi-phase, spec-heavy, materially ambiguous, or evidence-heavy → `@artifact-planner`,
- change is material and needs completion claim → final pass through `@quality-gate`.

Permitted fallback: if a specialist is unavailable, use the next safest lane and record the limitation explicitly in final evidence.

## Routing anti-patterns (and remediation)
- Anti-pattern: delegate discovery to `@explorer`, then `@orchestrator` still reads many files and redoes discovery.
  - Remediation: consume explorer output; only perform minimal spot-check reads.
- Anti-pattern: `@orchestrator` performs multi-file implementation directly because "it is faster".
  - Remediation: route bounded implementation to `@fixer`.
- Anti-pattern: complex/ambiguous work starts without a plan/evidence path.
  - Remediation: route to `@artifact-planner`, then implement plan-bound.
- Anti-pattern: completion claim on material change without `@quality-gate`.
  - Remediation: run final conformance gate before claiming done.

## Compact routing quality checklist
Use this quick rubric for real workflow audits:

- [ ] **Lane fit**: discovery/implementation/review went to the expected primary lanes.
- [ ] **Threshold compliance**: orchestrator direct work stayed within tiny-task limits.
- [ ] **Planner triggered correctly**: complex/ambiguous/evidence-heavy work is plan-bound before implementation.
- [ ] **Evidence legibility**: delegation choices and fallback reasons are explicitly recorded.
- [ ] **Final gate**: material changes include `@quality-gate` pass/verdict.

Score guidance: 5/5 = strong routing discipline; 3–4/5 = acceptable with minor drift; ≤2/5 = routing failure requiring remediation.

## Core agents (default operating model)

Cross-lane contract baseline (non-trivial work):
- Typed output schema fields: `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`.
- Typed schema is internal coordination contract and non-user-facing.
- Orchestrator must normalize internal outputs before user-facing final response; never pass raw internal labels directly.
- Validation ladder: plan/handoff check → discovery/research evidence → implementation/docs change → diff review → targeted validation commands → `@quality-gate` for non-trivial/risky completion claims.
- LSP-first for rename/refactor/navigation/diagnostic-driven edits where available; fallback to `glob`/`grep`/`read` + minimal edits must be recorded in evidence when confidence drops.
- `@orchestrator` — router, integrator, final coordinator
- `@explorer` — codebase discovery and reuse mapping
- `@fixer` — bounded implementation, tests, Red/Green/Refactor
- `@designer` — UI/UX, visual polish, reference work, design-system direction
- `@oracle` — architecture, maintainability, simplification, deep review
- `@quality-gate` — final conformance and risk review

## Triggered planning lane
- `@artifact-planner` — planning artifacts and evidence paths under `.opencode/`.
- Trigger only when scope/ambiguity/evidence needs justify planning overhead.

## Helper lanes (triggered)
- `@architect` — unified read-only advisory lane for product/SaaS, platform/runtime/release/mobile, AI/LLM/RAG/evals, and UI-system architecture boundaries.
- `@artifact-planner` — planning artifacts and evidence paths under `.opencode/`.
- `@librarian` — supporting docs/API research helper and document-centric read-only extraction/research/transformation support.
- `@skill-improver` — prompt/skill/routing improvements after repeated failure or evidence.

## Domain subagents (triggered only)

These agents are `mode: subagent`. `@orchestrator` remains default. `@artifact-planner` remains triggered, not default-first.

| Agent | Owns | Route when | Do not route when |
|---|---|---|---|
| `@frontend` | Web UI implementation | React/Next/Vue/Svelte components, pages, forms, state, routing, API integration, component tests, accessibility implementation | Visual direction or design-system choices are missing -> `@designer`; backend contract unclear -> `@backend`/`@system-analyst` |
| `@mobile` | Mobile implementation | React Native, Expo, Flutter, navigation, native permissions, offline, push, camera, deep links, mobile performance | Mobile architecture/privacy/store boundary needs decision -> `@architect`/`@quality-gate` |
| `@backend` | API/server/data implementation | Endpoints, services, validation, auth integration, DB queries, migrations, jobs, queues, backend tests | Requirements/API contract unclear -> `@system-analyst`; major data/security architecture -> `@architect`/`@quality-gate` |
| `@devops` | CI/CD, Docker, env, deploy, monitoring | GitHub Actions, Dockerfile, compose, release scripts, observability config, rollback plans | Deploy/destructive/credential action lacks explicit approval; architecture/release boundary -> `@architect`/`@quality-gate` |
| `@system-analyst` | Read-only requirements/contracts | PRD, user flows, API contracts, data flows, edge cases, NFRs, acceptance criteria | Source edits or tests are requested -> implementation lane |
| `@project-manager` | Read-only delivery planning | Milestones, backlog, issue breakdown, dependency/risk register, release checklist, handoff | Requirements unclear -> `@system-analyst`; source edits requested -> implementation lane |
| `@fullstack` | Small vertical slice | Tight, clear FE/BE change with small scope and known contract | Broad scope, unknown contracts, or multi-subsystem work -> split `@frontend` + `@backend` or plan first |

Domain anti-overlap rules:
- UI/UX direction stays with `@designer`; `@frontend` implements from direction.
- `@fullstack` is never catch-all/default. Split once scope grows or contracts are unclear.
- Read-only agents (`@system-analyst`, `@project-manager`) must not edit source.
- `@devops` must ask before deploy, destructive infra, credential, or production mutation commands.

Document fallback rule:
- If a user asks to read, summarize, compare, or transform PDF/DOCX/XLSX/PPT/Office input and the active model reports no direct attachment support (for example `input.pdf:false`), do not stop at the model capability check. Treat it as a direct-attachment limitation, check whether the file is available in the workspace, then route to `@librarian` for document-centric extraction. Ask the user to convert the file only after the `@librarian` lane or local extraction tools are unavailable or fail.

Helper lanes are conditional. Tiny UI polish still routes to `@designer`; isolated bugfixes still route to `@fixer` unless a risk trigger applies.

Global conditional specialist framing:
- PRD/product blueprint work, SaaS architecture, AI system design, Security/privacy review, Release/ops readiness, and Mobile/hybrid architecture can trigger `@architect`.
- Tiny UI polish still goes to `@designer`.
- Isolated bugfixes still go to `@fixer`.
- Web implementation with existing design direction can route to `@frontend`.
- Backend/API/data implementation can route to `@backend`.
- Mobile app implementation can route to `@mobile`.
- CI/CD/Docker/env/deploy work can route to `@devops` with approval gates.
- Requirements/contract clarification can route to `@system-analyst`.
- Milestone/backlog/release planning can route to `@project-manager`.
- Small FE/BE vertical slices can route to `@fullstack`; split when scope grows.

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
- auth, PII, tenant isolation, payment, upload, secrets, token/session handling, biometric data, permission/RBAC → final security/privacy assessment in `@quality-gate`; use `@architect` for upstream architecture decisions
- architecture boundary, new abstraction, large refactor, dependency direction, data model change → oracle
- visual layout change, animation/motion direction, design token, screenshot/reference parity, responsive behavior → `@designer` for design direction (including reduced-motion review) and `@quality-gate` for final accessibility/visual-parity signoff when material
- CI/CD, deployment, env var, migration, monitoring, rollback, mobile/offline/push/deep-links/platform runtime constraints → `@architect`
