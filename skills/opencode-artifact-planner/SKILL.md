---
name: opencode-artifact-planner
description: Standalone SDD/TDD artifact planning workflow for artifact-planner. Use for implementation plans, revamp plans, architecture plans, reference UI plans, migration plans, and any task requiring .opencode planning artifacts without editing source files.
---

# OpenCode Artifact Planner Skill

Use this as the planner’s only workflow. Write planning artifacts only under `.opencode/plans/`, `.opencode/draft/`, and `.opencode/evidence/`.
`@artifact-planner` is a triggered/conditional planning lane, not a default-first lane for every task.

Canonical tool references:
- `.opencode/docs/TOOL_USAGE.md` (operational tool selection)
- `.opencode/docs/AGENT_TOOL_ACCESS.md` (role boundaries and fallback)

## Language

- Use Indonesian for all user-facing communication, including chat, operational explanations, assumptions, question gates, planning summaries, and planning artifacts produced by this skill.
- Do not mix Indonesian and English in the same prose block except for exact technical names, paths, commands, APIs, quoted text, or errors.

## Lifecycle

1. Discover local project patterns, docs, constraints, references, and available tools.
2. Run a question gate for material unknowns; ask 3–7 targeted questions when assumptions would affect architecture, UX, security, cost, data, or acceptance criteria.
3. Run a research gate: local discovery, official docs/context, GitHub, web search, and browser evidence as needed.
4. Draft only when useful under `.opencode/draft/<task-id>/`.
5. Write one primary plan: `.opencode/plans/<task-id>.md`.
6. Keep only operationally useful evidence; delete stale drafts after consolidation.

The planner may call informational/read-only/research/documentation helpers to improve plan confidence. `@librarian` remains a supporting research helper (not a core/specialist routing lane). Domain advisory is conditional via:
- `@architect`

This planner may call informational, read-only, research, and documentation subagents only. Do not call implementation/source-edit/generation subagents such as fixer, designer, or visual-asset-generator.

Do not call implementation/source-edit/generation subagents (e.g., `@fixer`, `@designer`, `@visual-asset-generator`). If implementation is requested, write the plan and stop.

## Required plan sections

Goal, Non-goals, Scope, Requirements, Acceptance Criteria, Existing Patterns/Reuse, Constraints, Risks, Decisions/Assumptions, TDD/Test Plan, Implementation Steps, Expected Files to Change, Agent/Tool Routing, Execution-ready Worklist / Handoff Contract, Validation Commands, Evidence Requirements, Done Criteria, Final Planning Summary.

Execution-ready Worklist / Handoff Contract is mandatory for non-trivial plans and must allow `@orchestrator` to execute to completion without replanning. For each atomic ordered task include: dependencies (`depends_on`), owner/lane, validation, task exit criteria, blocking status (`ready`/`blocked`) with reason, `requires_user_decision` (`yes`/`no`), and a `start_with` pointer for the first non-blocked task.

For UI/reference work also include Visual Spec Summary, Asset Manifest Summary, Image Generation Decision, Reference Capture Requirements, and Visual Comparison Requirements.
Keep one primary plan file as the durable source of truth; any visual artifacts or extra notes belong in draft/evidence only when operationally useful and should not compete as alternate primary plans.
For substantial UI/reference/image-heavy work, require a Design Readiness Gate and add blockers for missing motion storyboard, icon matrix, visual density rubric, asset manifest, image generation decision, reference/current captures, and final designer review.
For portfolio/reference/template work with hero art, portraits, project cards, thumbnails, testimonial/avatar clusters, blog cards, icon badges, or rich backgrounds, assume image-heavy until proven otherwise. The plan must decide `generate`, `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed` per section; if no licensed/provided assets exist, recommend legal style-equivalent generation instead of CSS placeholders.

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
