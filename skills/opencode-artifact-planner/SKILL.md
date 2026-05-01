---
name: opencode-artifact-planner
description: Standalone SDD/TDD artifact planning workflow for artifact-planner. Use for implementation plans, revamp plans, architecture plans, reference UI plans, migration plans, and any task requiring .opencode planning artifacts without editing source files.
---

# OpenCode Artifact Planner Skill

Use this as the planner’s only workflow. Write planning artifacts only under `.opencode/plans/`, `.opencode/draft/`, and `.opencode/evidence/`.

## Lifecycle

1. Discover local project patterns, docs, constraints, references, and available tools.
2. Run a question gate for material unknowns; ask 3–7 targeted questions when assumptions would affect architecture, UX, security, cost, data, or acceptance criteria.
3. Run a research gate: local discovery, official docs/context, GitHub, web search, and browser evidence as needed.
4. Draft only when useful under `.opencode/draft/<task-id>/`.
5. Write one primary plan: `.opencode/plans/<task-id>.md`.
6. Keep only operationally useful evidence; delete stale drafts after consolidation.

The planner may call informational, read-only, research, and documentation subagents to gather evidence and improve the plan, but it must not call implementation, source-edit, or generation subagents such as fixer, build, designer, or visual-asset-generator. If implementation is requested, write the plan and stop.

## Required plan sections

Goal, Non-goals, Scope, Requirements, Acceptance Criteria, Existing Patterns/Reuse, Constraints, Risks, Decisions/Assumptions, TDD/Test Plan, Implementation Steps, Expected Files to Change, Agent/Tool Routing, Validation Commands, Evidence Requirements, Done Criteria, Final Planning Summary.

For UI/reference work also include Visual Spec Summary, Asset Manifest Summary, Image Generation Decision, Reference Capture Requirements, and Visual Comparison Requirements.
For substantial UI/reference/image-heavy work, require a Design Readiness Gate and add blockers for missing motion storyboard, icon matrix, visual density rubric, asset manifest, image generation decision, reference/current captures, and final designer review.
For portfolio/reference/template work with hero art, portraits, project cards, thumbnails, testimonial/avatar clusters, blog cards, icon badges, or rich backgrounds, assume image-heavy until proven otherwise. The plan must decide `generate`, `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed` per section; if no licensed/provided assets exist, recommend legal style-equivalent generation instead of CSS placeholders.

## TDD planning

Plan Red → Green → Refactor. Identify the first failing/regression test. For visual work, use screenshot baseline as Red evidence and final screenshot comparison as Green/Refactor proof. If TDD is exempt, document why and plan validation.

## Browser evidence planning

For visual/reference/browser tasks, require wait-stabilize-scroll-settle screenshots at matching viewports. Capture notes must include viewport, wait strategy, scroll pass, paths, rendering-affecting console/network errors, and limitations.

## Evidence artifacts for substantial UI/reference work

Add or reference `.opencode/evidence/<task-id>/reference-captures.md`, `current-captures.md`, `generated-assets.md`, `visual-comparison.md`, and `final-designer-review.md`. If evidence is missing, the plan must mark implementation as blocked.

## Finalization

`Final Planning Summary` must list artifacts created/kept/deleted, key decisions, assumptions, open questions, readiness, and cleanup performed.
