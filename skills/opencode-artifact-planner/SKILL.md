---
name: opencode-artifact-planner
description: Standalone SDD/TDD artifact planning workflow for artifact-planner. Use for implementation plans, revamp plans, architecture plans, reference UI plans, migration plans, and any task requiring .opencode planning artifacts without editing source files.
---

# OpenCode Artifact Planner Skill

Use this as the planner’s only workflow. Write planning artifacts only under `.opencode/plans/`, `.opencode/draft/`, and `.opencode/evidence/`.
Inside `.opencode/evidence/<task-id>/`, include `index.json` when repo evidence checks require a task-scoped evidence manifest.
`@artifact-planner` is a triggered/conditional planning lane, not a default-first lane for every task.

Canonical tool references:
- `.opencode/docs/TOOL_USAGE.md` (operational tool selection)
- `.opencode/docs/AGENT_TOOL_ACCESS.md` (role boundaries and fallback)

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Reference Depth Gate
- Tiny maintenance, local bugfixes, and prompt/config plans may rely on repo-local evidence when enough; do not force internet research or make external claims for low-risk local work.
- For greenfield, substantial UI/UX, unfamiliar or version-sensitive library/API behavior, current external facts, reference UI, product/market-sensitive, or upstream-dependent work, define source strategy before convergence: repo evidence, official/library docs via `@librarian`/context when available, upstream source/examples or GitHub/web search when needed, and browser/reference screenshots for visual work.
- Do not finalize substantial plans until reasonable references were checked or explicitly skipped with rationale. Missing current docs/API/source facts route to `@librarian`; do not invent library/API behavior, package capabilities, pricing, market facts, or upstream behavior from memory.
- If a relevant source path is skipped, record why and lower the claim level (`draft`, `assumption`, `repo-local only`, or `first-principles`).
- Greenfield plans must use `.opencode/docs/GREENFIELD_STARTER.md` or a repo-local equivalent as starter input unless explicitly prototype-only; if skipped, record why.

## Anti-AI-slop quality bar
- No generic UI/product plans. Require reference pack or explicit first-principles rationale plus distinctive direction and concrete page/component/state/motion/accessibility details for substantial UI.
- Substantial UI needs page-by-page flows, section composition, component inventory, responsive behavior, empty/loading/error/success states, motion intent with reduced-motion handling, accessibility checks, and visual evidence plan.
- Avoid bland defaults: centered gradient hero, fake metrics, vague dashboards, emoji/icon placeholders, unexplained cards, generic SaaS copy, and “modern clean” without source-backed or first-principles specifics.

## Material Grammar Translation
- Substantial UI plans with explicit aesthetic requests must include Material Grammar Translation before final readiness: user phrase -> tokens -> surfaces -> layout rules -> reject_if.
- Example: `claymorphism + glassmorphism` -> soft warm/pastel tokens, rounded tactile clay surfaces, frosted translucent glass overlays, layered shadows/highlights, airy product/domain hero composition; reject_if: generic neon SaaS, repeated card/grid anatomy, unreadable blur, fake metrics, debug copy, abstract CSS filler where imagery matters.
- Do not finalize `ready-for-implementation`, `PASS`, or `PASS_FOR_SLICE` if style grammar is missing; mark `blocked`/`NEEDS_DEPTH` and route to `@designer` advisory.

## Language

- Use Indonesian for all user-facing communication, including chat, operational explanations, assumptions, question gates, planning summaries, and planning artifacts produced by this skill.
- Do not mix Indonesian and English in the same prose block except for exact technical names, paths, commands, APIs, quoted text, or errors.

## Lifecycle

1. Discover local project patterns, docs, constraints, references, and available tools.
2. Run a question gate for material unknowns; ask 3–7 targeted questions when assumptions would affect architecture, UX, security, cost, data, or acceptance criteria.
3. Run a research gate: local discovery, official docs/context, GitHub, web search, design advisory, and browser evidence as needed.
4. Draft only when useful under `.opencode/draft/<task-id>/`.
5. Write one primary plan: `.opencode/plans/<task-id>.md`.
6. Keep only operationally useful evidence; delete stale drafts after consolidation.

Before convergence, explicitly choose source strategy for the task: local repo evidence, official docs, upstream source/examples, screenshots/reference URLs, and current web research. If a reasonable source is skipped, state why.

The planner may call informational/read-only/research/documentation helpers to improve plan confidence. `@librarian` remains a supporting research helper. Domain advisory is conditional and should be used only when material.

This planner may call informational, read-only, research, and documentation subagents only; design-advisory is read-only only. Do not call implementation/source-edit/generation subagents such as fixer or visual-asset-generator. `@designer` is allowed only for read-only UX/product creativity advisory input; never for implementation, source edits, or generation.

Do not call implementation/source-edit/generation subagents (for example `@fixer` or `@visual-asset-generator`). If implementation is requested, write the plan and stop.

## Planning lane boundaries

| Need | Route |
| --- | --- |
| Requirements, flows, contracts, acceptance criteria | `@system-analyst` as read-only input |
| Milestones, tickets, dependency sequencing | `@project-manager` as read-only input |
| Durable `.opencode/plans/**` artifact | `@artifact-planner` owns write |
| Implementation/source edits | `@fixer` or domain agent after plan |
| Architecture option/risk framing | `@architect`/`@oracle` as advisory input |
| UX/product creativity options | `@designer` as read-only advisory input |
| Final completion gate | `@quality-gate` after implementation |

## Mode-aware planning

- Greenfield App Accelerator: for new apps, MVPs, SaaS/product builds, blank repos, and major revamps. Include Creative Depth Contract: product thesis, 2-3 product/UX/architecture options, tradeoff scoring, first-slice rationale, `user journey → data model → API/contracts → UI screens → tests` mapping, design readiness, and readiness status.
- Maintenance Stability Mode: for bugfix, regression, refactor, dependency update, small feature, and incident follow-up. Keep plans regression-first and minimal; do not require product thesis or 2-3 creative alternatives unless the bug needs product/UX decisions.
- Creativity Fast Path: planner is not the default tax. For explicit draft/prototype/exploration asks that remain reversible, `@artifact-planner` may be skipped entirely or produce only a lightweight draft-only artifact when that helps. Full planning becomes required again once the scope turns multi-phase, materially ambiguous, implementation-bound, or promotion-ready.
- Plan readiness values: `draft`, `blocked`, `ready-for-slice`, `ready-for-implementation`.
- Plan Quality Gate values: `PASS`, `PASS_FOR_SLICE`, `NEEDS_DEPTH`, `BLOCKED`. Only `PASS` and `PASS_FOR_SLICE` are execution-ready.

## Required plan sections

Goal, Non-goals, Scope, Requirements, Acceptance Criteria, Existing Patterns/Reuse, Constraints, Risks, Decisions/Assumptions, Execution Source of Truth, Non-negotiable Implementation Invariants, Do Not / Reject If, Diff Boundary, TDD/Test Plan, Implementation Steps, Expected Files to Change, Agent/Tool Routing, Executor Handoff Prompt, Execution-ready Worklist / Handoff Contract, Validation Commands, Evidence Requirements, Done Criteria, Final Planning Summary.

For **Source-approved 1:1 Porting / Literal Porting Contract** tasks, also require: Upstream/Source File Map, Local Target Map, Copy/Adapt/Prune/Create Decision per source file/component/asset, License/Attribution Note, Forbidden Deviations, and Remaining Parity Debt for every non-copied or intentionally diverged section. Do not accept vague grammar/style parity as the only success condition.

For non-trivial plans, Execution Source of Truth must define precedence for implementation: latest explicit user instruction; safety/security/permission rules; Non-negotiable Implementation Invariants; Execution-ready Worklist / Handoff Contract; Acceptance Criteria and Done Criteria; Implementation Steps; follow-ups/recommendations. Conflicts must be recorded in verification evidence.

Non-negotiable Implementation Invariants are required when plan semantics can be implemented incorrectly despite checklist compliance. Capture artifact-only planner posture, conditional planner use, tiny fast path lightweight behavior, owner/lane boundaries, evidence requirements, and claim scope when relevant.

Do Not / Reject If must name concrete scope-creep, overclaiming, generated-weirdness, and risky-shortcut failures that should stop, revert, or remediate implementation before final claim.

Diff Boundary must list allowed file groups, generated-report exceptions, and evidence paths. Any out-of-boundary change must be reverted or justified in verification evidence before final quality gate.

Executor Handoff Prompt must be copyable for `@orchestrator` and implementation lanes with minimal translation. Include scope, must_preserve, do_not_touch, validation, return/evidence expectations, and plan-specific claim limits.

For non-trivial plans, include a concise source-strategy note or equivalent under `Evidence Requirements`, `Decisions/Assumptions`, or `Final Planning Summary`: what sources were used, what was skipped, which major choices are repo-backed/reference-backed/docs-backed/first-principles-driven, and which assumptions remain.

Execution-ready Worklist / Handoff Contract is mandatory for non-trivial plans and must allow `@orchestrator` to execute to completion without replanning. For each atomic ordered task include: dependencies (`depends_on`), owner/lane, validation, task exit criteria, blocking status (`ready`/`blocked`) with reason, `requires_user_decision` (`yes`/`no`), `must_preserve`, `do_not_touch`, `evidence_update`, `exit_verification`, and a `start_with` pointer for the first non-blocked task.

For UI/reference work also include Visual Spec Summary, Asset Manifest Summary, Image Generation Decision, Reference Capture Requirements, and Visual Comparison Requirements.
For source-approved 1:1 UI/reference work, the visual spec must distinguish `copy`, `adapt`, `prune`, and `create` per section/component/asset and record `remaining parity debt` for every non-copied section.
For substantial UI, require page, component, state, motion, responsive, and accessibility specifics plus reference pack or first-principles rationale; generic “modern dashboard/landing page” prose is not execution-ready.
For explicit aesthetics, require Material Grammar Translation: user phrase -> tokens -> surfaces -> layout rules -> reject_if; no final plan readiness if missing.
Keep one primary plan file as the durable source of truth; any visual artifacts or extra notes belong in draft/evidence only when operationally useful and should not compete as alternate primary plans.
For substantial UI/reference/image-heavy work, require a Design Readiness Gate and add blockers for missing motion storyboard, icon matrix, visual density rubric, asset manifest, image generation decision, reference/current captures, and final designer review.
For portfolio/reference/template work with hero art, portraits, project cards, thumbnails, testimonial/avatar clusters, blog cards, icon badges, or rich backgrounds, assume image-heavy until proven otherwise. The plan must decide `generate`, `use-provided-assets`, `licensed-existing-assets`, `no-generation-needed`, or `direct-reuse-user-approved` per section; if the user explicitly approved direct reuse and it is safe/allowed, prefer direct reuse over fallback generation. If no licensed/provided/direct-reuse-safe assets exist, recommend style-equivalent generation fallback instead of CSS placeholders.

## TDD planning

Plan Red → Green → Refactor. Identify the first failing/regression test. For visual work, use screenshot baseline as Red evidence and final screenshot comparison as Green/Refactor proof. If TDD is exempt, document why and plan validation.

## PRD to Production Blueprint

Use this mode when the user provides PRD/product docs or asks to turn product documentation into an implementation-ready plan. The planner remains the artifact writer; domain specialists are conditional advisors only.

- If the source is PDF, DOCX, spreadsheet, presentation, or mixed document input, use `@librarian` first for document-centric read-only extraction/research/transformation support.
- Use `@architect` when product/SaaS/platform/runtime/AI/UI-system architecture boundaries are material (MVP slicing, flows, tenancy/RBAC/billing, runtime/release constraints, AI eval/reliability/safety decisions, design-system architecture boundaries).
- Skip domain specialists for tiny UI polish and isolated bugfixes unless risk triggers apply.
- Add a Production Blueprint Summary when applicable: MVP slice, epics/user flows, data/API outline, SaaS/RBAC considerations, UI/design readiness, AI boundaries, mobile constraints, security/privacy checklist, release/ops checklist, and validation plan.

## Browser evidence planning

For visual/reference/browser tasks, require wait-stabilize-scroll-settle screenshots at matching viewports. Capture notes must include viewport, wait strategy, scroll pass, paths, rendering-affecting console/network errors, and limitations.

## Evidence artifacts for substantial UI/reference work

Add or reference `.opencode/evidence/<task-id>/reference-captures.md`, `current-captures.md`, `generated-assets.md`, `visual-comparison.md`, and `final-designer-review.md`. If evidence is missing, the plan must mark implementation as blocked.

## Finalization

`Final Planning Summary` must list artifacts created/kept/deleted, key decisions, assumptions, open questions, readiness, and cleanup performed.
## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
