---
description: Initialize or update the current project's harness docs: AGENTS.md, canonical .opencode/docs, and DESIGN.md
agent: orchestrator
model: 9router/high
---

Initialize or update the current project's harness docs so the repository has an up-to-date `AGENTS.md`, canonical `.opencode/docs`, project-local framework command/playbook docs, and project-local `DESIGN.md` guidance.

This consolidated command is the single entrypoint for both harness and design initialization. Do not refer users to any separate design initialization command.

Arguments from user, if any:

```text
$ARGUMENTS
```

Workflow:

1. Inspect the current target project root before writing anything.
2. Read the existing root `AGENTS.md` if it exists.
3. Read the existing root `DESIGN.md` if it exists.
4. If the project documents a local equivalent such as `design-system/DESIGN.md`, read it too and treat it as project-specific guidance.
5. Inspect `.opencode/docs/index.md` first when present, then review the full canonical doc set when it exists: `.opencode/docs/AGENT_ROUTING.md`, `.opencode/docs/ARCHITECTURE.md`, `.opencode/docs/AGENT_LEGIBILITY.md`, `.opencode/docs/QUALITY.md`, `.opencode/docs/EVALS.md`, `.opencode/docs/SECURITY.md`, `.opencode/docs/PROMPT_GATES.md`, `.opencode/docs/SKILLS.md`, `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`, `.opencode/docs/GOLDEN_PRINCIPLES.md`, `.opencode/docs/DECISIONS.md`, `.opencode/docs/RELEASE.md`, `.opencode/docs/QUALITY_SCORE.md`, and `.opencode/docs/GC_WORKFLOW.md`.
6. Run an explicit project tech-stack discovery workflow before drafting: inspect README plus package/lock/build/runtime manifests and validation scripts (for example `package.json`, `pnpm-lock.yaml`, `requirements*.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`, Docker/compose files, CI workflows, and test/lint scripts) so routing and validation guidance is project-specific.
7. Detect framework/library/tooling surfaces relevant to generator-first work in existing apps and greenfield repos: package managers, CLIs, code generators, migration tools, framework scaffolds, dev servers, test/build/lint tools, and repo scripts. Examples to check when relevant include `artisan`, `composer`, `pnpm`/`npm`/`bun`, shadcn, Prisma, Drizzle, goose, `sqlc`, `buf`, `oapi-codegen`, Rails, Nest, Nx, Expo, Flutter, Docker, and CI helpers.
8. Read existing `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when they already exist.
9. Do not silently overwrite project-specific framework guidance. If those project docs exist, update them conservatively: merge with current evidence, preserve project-specific notes, and ask before replacing guidance whose intent is unclear.
10. Write or update these project-local docs under `.opencode/docs/` by default:
   - `PROJECT_STACK.md` — detected frameworks/libraries/runtimes/versions, package managers, test/build/lint tools, docs source strategy, and staleness notes.
   - `PROJECT_COMMANDS.md` — safe/default commands, generator/scaffold commands, validation commands, commands requiring approval, destructive/prod-risk commands, and env/test DB notes.
   - `FRAMEWORK_PLAYBOOK.md` — framework/library-specific best practices: official CLI/generator-first rules, migration rules, routing/file placement, testing/validation, manual fallback conditions, and repo-specific conventions.
   - `PROJECT_DETECTED_TOOLS.md` — discovered tools/generators and the repo evidence for each detection.
11. `FRAMEWORK_PLAYBOOK.md` must make generator/CLI-first the default for existing app development too, not only from scratch. Name concrete examples when they fit the detected stack, such as Laravel `php artisan make:*` / `php artisan test` / `php artisan route:list`, goose `goose create <name> sql` / `status` / `up` / `down`, shadcn CLI/MCP, Prisma/Drizzle migrate/generate, Rails/Nest/Expo/Flutter generators, and `sqlc`/`buf`/`oapi-codegen`.
12. Manual fallback guidance must be explicit: manual artifact edits are allowed only when the command/tool is unavailable or not permitted, the command failed with evidence, the project intentionally avoids the generator, the task customizes existing generated files, or the user explicitly asks for manual edits. Require evidence naming the attempted or skipped command and reason.
13. If framework/library behavior or command best practice is version-sensitive and local project docs do not already settle it, use external references per `.opencode/docs/TOOL_USAGE.md` and prefer official docs via `context7`/`@librarian` before broader sources.
14. Inspect existing project tokens, components, styles, breakpoints, UI docs, screenshots, and related guidance when available so `DESIGN.md` matches the project instead of generic taste.
15. Capture concise stack-and-tooling findings (languages, frameworks, package managers, test runners, linters, build/deploy surfaces) and reflect them in `AGENTS.md` instead of generic advice.
16. Keep repo-local-docs-first posture. Use external references only when local evidence is insufficient or version-sensitive, following `.opencode/docs/TOOL_USAGE.md` (prefer official docs via `context7`, then source/examples via GitHub, then broad web search).
17. If external references are needed, state what was checked and why in the final summary.
18. If `AGENTS.md` already exists at the project root, ask before overwriting or replacing it. Do not silently overwrite project-specific rules.
19. If `DESIGN.md` already exists at the project root, ask before overwriting or replacing it. Do not silently overwrite project design guidance.
20. If no root `AGENTS.md` exists, create one in the current project root.
21. If no root `DESIGN.md` exists, create one in the current project root.
22. Keep both files in English.
23. Keep `AGENTS.md` short: target under 60 lines, never exceed 100.
24. Treat `AGENTS.md` as a map, not an encyclopedia. Detailed policy belongs in `.opencode/docs/` and mechanical checks.
25. Prefer repo-local docs over embedded long-form instructions. Point to canonical docs instead of duplicating policy.
26. If the project already uses a docs-as-system-of-record workflow, reflect it explicitly.
27. If canonical docs are missing under `.opencode/docs/`, scaffold the full canonical system-of-record first (create `.opencode/docs/index.md` plus the current canonical corpus files), then write `AGENTS.md`; do not produce placeholder or missing-doc links.
28. The scaffolded canonical docs must contain comparable operational detail (not placeholders) across concerns: routing thresholds and delegation boundaries, tool/MCP state boundaries, quality and evidence expectations, evals/replayability posture, prompt gates and mechanical checks, security constraints, skills ownership and division of labor, decisions/release/GC workflow, and architecture context.
29. Make `DESIGN.md` concrete, specific, and aligned to the target project's own UI language.
30. Prefer design rules that map to existing tokens, components, breakpoints, and interaction patterns; add new guidance only when the project actually needs it.
31. Explicitly state that project-local `DESIGN.md` wins over generic preferences, and that UI/design work should read it first, then `design-system/DESIGN.md` or any documented project-specific equivalent.
32. In both docs, keep the downstream ownership chain legible: `@orchestrator` routes/integrates, `@designer` owns UI direction/review first, bounded implementation/tests go to `@fixer` or domain lanes, evidence-heavy/spec-heavy planning goes to `@artifact-planner`, and final non-trivial UI/prompt/config/docs/security-sensitive changes go to `@quality-gate`.
33. Add the Harness Preflight Gate concisely: before non-trivial work, `@orchestrator` must verify the target project has a current root `AGENTS.md`, canonical `.opencode/docs/`, root `DESIGN.md` when UI/design work is involved, and the project stack/command/playbook docs when framework-managed artifacts are in scope.
34. State that if harness guidance is missing or stale, future operators should run `/init-harness` first, or ask the user to run `/init-harness` when command execution is unavailable. Do not start broad implementation until harness guidance is available, except for tiny, read-only, or emergency tasks; if skipped, record the reason in the final summary.
35. State that agents should follow project framework playbook/commands before manual framework artifact edits.
36. State that `@designer` may implement only when directly routed/requested.
37. State that `@artifact-planner` may use designer only as read-only advisory input.
38. State that `@visual-asset-generator` is invoked by `@orchestrator`/`@designer` from an asset manifest/image-heavy plan, not by planner.
39. State that substantial UI requires evidence/screenshots/reduced-motion/accessibility checks and `@quality-gate` before completion claim.
40. Use the user's hints from `$ARGUMENTS` only to specialize the files; do not discard the harness baseline or invent a broad new visual direction without evidence.
41. Explicitly state which agent should be used first for default execution (`@orchestrator`).
42. After command/config edits, remind the user to restart OpenCode because command/config-time files are loaded at startup.

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

## Non-negotiable Rules
- Do not prefix shell commands with `rtk` in OpenCode sessions or OpenChamber sessions that invoke OpenCode.
- RTK may be installed by explicit setup, but OpenCode auto-rewrite/prefix remains opt-in unless user explicitly asks; OpenChamber should follow that OpenCode posture rather than redefine it.
- Token compression/context packing should use RTK and Caveman together when that capability is needed; do not invent a parallel local compression flow or treat them as either/or alternatives.
- Never commit secrets, tokens, or `.env` files.
- Use `@orchestrator` for routing and integration.
- Use `@quality-gate` for material changes, including non-trivial/risky work, prompt/config changes, and security-sensitive changes.
- Harness Preflight Gate: before non-trivial work, `@orchestrator` must verify the target project has a current root `AGENTS.md`, canonical `.opencode/docs/`, and root `DESIGN.md` when UI/design work is involved.
- For framework-managed artifacts, read project-local `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` before manual edits when those docs are present.
- If harness guidance is missing/stale, run `/init-harness` first, or ask the user to run `/init-harness` when command execution is unavailable. Skip only for tiny, read-only, or emergency tasks and record the skip reason in the final summary.
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
- 6 core agents: `@orchestrator` routes/integrates, `@explorer` discovers, `@fixer` implements bounded changes/tests, `@designer` owns UI/UX direction and review, `@oracle` handles architecture/review, and `@quality-gate` does final signoff.
- Triggered helper/domain lanes: `@artifact-planner`, `@architect`, `@librarian`, `@skill-improver`, `@frontend`, `@backend`, `@mobile`, `@devops`, `@fullstack`, `@system-analyst`, `@project-manager`, `@council`, and `@visual-asset-generator`.
- Active skills: 19 `opencode-*` skills listed in `.opencode/docs/SKILLS.md`; legacy merged-away reviewer variants are not active routing lanes.

## Risk Triggers
- Product/SaaS/platform/runtime/mobile/AI/UI-system architecture ambiguity → `@architect`
- Requirements, user flows, API contracts, data flows, NFRs, or acceptance criteria unclear → `@system-analyst`
- Docs/API research or document extraction/summary needed → `@librarian`
- Release/deploy/ops, CI/CD, Docker, env, monitoring, or rollback work → `@devops` with approval gates
- PII/auth/payments/uploads/biometric/privacy, prompt/config/security-sensitive changes, or material completion claims → `@quality-gate`
- User-facing UI/reference/animation/accessibility/design-system work → `@designer`
- Repeated failure or post-task prompt/routing improvement → `@skill-improver`

## Notes
- For substantial UI work, inspect the target project's `DESIGN.md` first, then `design-system/DESIGN.md` or a documented equivalent.
- For framework-managed artifacts in existing apps or greenfield work, inspect `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` first when present; follow project framework playbook/commands before manual edits.
- `@designer` owns UI direction/review and may implement only when directly routed/requested; `@artifact-planner` may use designer only as read-only advisory input.
- For image-heavy or reference UI work, require evidence, asset decisions, and direct reuse / style-equivalent fallback handling; `@visual-asset-generator` is invoked by `@orchestrator`/`@designer` from an asset manifest/image-heavy plan, not by planner.
- Substantial UI requires screenshots/evidence/reduced-motion/accessibility checks and `@quality-gate` before completion claim.
- If the project has many agents/subagents, document the role and primary skill ownership clearly enough that future work does not default back to `@orchestrator` for planning, implementation, review, or research.
- If many agents are available, future operators should read `.opencode/docs/AGENT_ROUTING.md` and `.opencode/docs/SKILLS.md` first to understand who owns discovery, implementation, review, design, and domain-specific risk.
- For full operational details, follow the linked docs rather than expanding this file.
```

Write `DESIGN.md` using exactly these 9 sections, in this order:

- Visual Theme & Atmosphere
- Color Palette & Roles
- Typography Rules
- Component Stylings
- Layout Principles
- Depth & Elevation
- Do's and Don'ts
- Responsive Behavior
- Agent Prompt Guide

Use this structure:

```markdown
# <Project or Product Name> Design System

> Category: <Product category, audience, and platform>
> Source: Generated from the current project structure, existing UI patterns, and user-provided hints.

## Visual Theme & Atmosphere
Describe the product personality, visual mood, density, tone, and what the UI should feel like in use.

## Color Palette & Roles
Define semantic roles for background, surface, text, muted text, border, primary accent, secondary accent, success, warning, destructive, focus, and data visualization colors. Prefer existing tokens/classes/variables when found.

## Typography Rules
Define heading, body, label, caption, numeric, and code/mono usage. Include scale, weight, line-height, tracking, and when display type is appropriate.

## Component Stylings
Define buttons, inputs, cards, navigation, tables/lists, dialogs/drawers, feedback surfaces, empty states, icons, imagery, and chart treatments with important variants and states.

## Layout Principles
Define grid, max widths, spacing rhythm, section density, responsive breakpoints, sticky/fixed behavior, and how content hierarchy should adapt across mobile/tablet/desktop.

## Depth & Elevation
Define border, shadow, layering, overlays, focus rings, hover/active depth, and when flat vs elevated surfaces should be used.

## Do's and Don'ts
List concrete project-specific rules, including anti-generic UI rules, icon/image rules, copy/metric rules, and what must never be introduced without approval.

## Responsive Behavior
Define mobile-first rules, navigation changes, CTA placement, data display adaptation, form behavior, image crops, touch target expectations, and reduced-motion expectations.

## Agent Prompt Guide
Give direct instructions for future coding/design agents: which files/tokens/components to read first, how to apply this design system, when to reuse/extend/create, when to ask questions, when to run visual validation, and how to report deviations.

The `Agent Prompt Guide` should also state the downstream ownership chain for substantial UI work: `@orchestrator` routes/integrates; `@designer` owns direction, motion/reduced-motion review, and implementation guidance first; `@designer` may implement only when directly routed/requested; bounded implementation/tests go to `@fixer` or domain lanes; `@artifact-planner` handles evidence-heavy/spec-heavy planning and may use designer only as read-only advisory input; `@visual-asset-generator` is invoked by `@orchestrator`/`@designer` from an asset manifest/image-heavy plan; `@quality-gate` remains final signoff for non-trivial UI/prompt/config/docs/security-sensitive changes.
```

After writing the files, summarize:

- whether `AGENTS.md` was created, updated, skipped, or left unchanged,
- whether `DESIGN.md` was created, updated, skipped, or left unchanged,
- whether `PROJECT_STACK.md`, `PROJECT_COMMANDS.md`, `FRAMEWORK_PLAYBOOK.md`, and `PROJECT_DETECTED_TOOLS.md` were created, updated, skipped, or left unchanged,
- which repo-local docs, project files, and scripts informed the result,
- any assumptions made,
- whether a `.opencode/docs/` system-of-record scaffold is still missing,
- how future agents should apply the docs,
- whether follow-up screenshots or design review are recommended,
- and that the user should restart OpenCode for command/config changes to take effect.
