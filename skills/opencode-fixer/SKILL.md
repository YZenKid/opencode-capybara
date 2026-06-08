---
name: opencode-fixer
description: Standalone bounded implementation workflow for fixer. Use for code edits, tests, fixtures, UI/runtime fixes, Red-Green-Refactor execution, Playwright checks, accessibility fixes, and small maintainability refactors.
---

# OpenCode Fixer Skill

Use this for scoped execution after requirements or a plan are clear.

For canonical tool policy and boundaries, refer to:
- `.opencode/docs/TOOL_USAGE.md`
- `.opencode/docs/AGENT_TOOL_ACCESS.md`

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Principles

- Follow the provided plan/evidence.
- When a durable run/worktree/task assignment exists, preserve runtime metadata and report task/result updates in evidence rather than inventing side channels.
- Select mode from handoff: Greenfield App Accelerator can implement a planned `PASS`/`PASS_FOR_SLICE` slice; Maintenance Stability Mode stays regression-first and minimal.
- Reuse project patterns before creating new abstractions.
- Preserve generator-first policy: for new framework artifacts, use detected official CLI/scaffold/generator/MCP before manual file creation when usable.
- Manual artifact fallback must record evidence: attempted/unavailable/failed tool, repo convention, explicit project/user reason, or existing generated-file customization.
- Make minimal safe changes.
- Escalate architecture/unclear decisions instead of guessing.
- Do not add new animation dependencies unless an explicit plan/designer handoff names the dependency and rationale, or the user directly approves it after existing options are checked.

## Boundary table

| Work | Route |
| --- | --- |
| Bounded edits, tests, fixtures, small refactors | `@fixer` |
| Web UI implementation with design already clear | `@frontend` or `@fixer` for tiny changes |
| Backend/API/data implementation | `@backend` |
| Native/hybrid mobile implementation | `@mobile` |
| Cross-stack vertical slice, small and clear | `@fullstack` |
| Missing UX/visual/motion direction | `@designer` first |
| Architecture/product/security tradeoff | `@architect`/`@oracle` |
| Final conformance/risk decision | `@quality-gate` |

## Red → Green → Refactor

- TDD is default for behavior changes when a practical test, fixture, or reproducible check exists.
- Red: failing test/regression evidence or visual baseline.
- Green: minimal implementation that passes.
- Refactor: simplify after checks pass; avoid unrelated churn.
- Validation: run relevant lint/build/test/browser checks.
- For maintenance, do not require product thesis or creative alternatives unless the bug requires a product/UX decision.

## UI/browser validation

Use wait-stabilize-scroll-settle screenshots for visual/browser tasks. Check desktop/tablet/mobile when responsive behavior changes. Record console/network issues only when they affect rendering.
For substantial UI/reference/image-heavy work, do not close on screenshots alone; require production-like evidence, icon audit, motion audit, and draft vs reference-ready status.
For substantial UI/UX, web, mobile, dashboard, landing page, reference, revamp, or design-system work, implement only from the provided `@designer` handoff. If the spec is missing or conflicts with project patterns, stop and ask instead of creating a new visual direction.

Before implementing UI-related changes, inspect the target project's `DESIGN.md` at the project root, then `design-system/DESIGN.md` or any documented project-specific equivalent. Treat project-local design guidance as higher priority than generic preferences, and do not silently override it.

Follow the smart UI handoff contract: implement from blueprint/plan, respect the active design system and tokens, avoid generic AI UI fallback, and stop on missing asset, motion, state, accessibility, or evidence detail for substantial work.

## Animation implementation gate

For website, frontend, or mobile app animation work, follow the plan/designer motion spec. If no spec exists and the motion is non-trivial, pause or route back for design direction instead of guessing.

- Check existing animation dependencies and patterns first (`package.json`, lockfiles, `pubspec.yaml`, components, tokens, utilities). Prefer reuse over new dependencies.
- Hard rule: no new animation package for bounded fixer work by default. Reuse existing system or platform primitives; if a new package is still needed, stop and route/ask unless explicit approved handoff already exists.
- Web: use CSS native for simple hover/focus/opacity/transform; consider `motion.dev` for non-trivial React/Next/Vue layout/state/gesture/scroll motion, `animejs` for timeline/SVG choreography, and `animate.css` only for quick ready-made effects.
- React Native/Expo: prefer existing patterns; use built-in `Animated`/`LayoutAnimation` for simple motion, Reanimated + Gesture Handler for non-trivial UI-thread/gesture/layout motion, and Lottie only for valid motion assets like onboarding/loading/brand illustrations.
- Flutter: prefer implicit animations for simple property changes, explicit `AnimationController` for complex choreography, and Hero for shared-element route transitions.
- Do not use web-only libraries (`motion.dev`, `animejs`, `animate.css`) for native mobile screens unless the target is web/webview.
- Support `prefers-reduced-motion` or platform reduced-motion/accessibility behavior where relevant; document limitations if not testable.
- Avoid `transition: all`, layout-janky animation, interaction-blocking overlays, and unbounded loops.
- Pause if designer spec, motion storyboard, icon system, asset manifest, or image generation decision is missing on a substantial UI/reference/image-heavy task; do not invent numeric-only icons, fake controls, blank image frames, generic gradients, or generic hover-only motion.
- Tiny reversible UI fixes can proceed with bounded assumptions; substantial work cannot.
- Validate browser runtime for web and simulator/device behavior for mobile when runnable.

## Local resources

- `references/playwright/` for Playwright patterns.
- `scripts/with_server.py` for local web app checks.
- `references/senior-frontend/`, `scripts/senior-frontend/` for frontend implementation helpers.
- `scripts/senior-backend/` for backend/API helpers.
- `references/senior-qa/`, `scripts/senior-qa/` for test scaffolding/coverage.
- `references/simplify-README.md` for behavior-preserving simplification.

## Accessibility/code checklist

Semantic links/buttons, labels, alt text, explicit image dimensions, visible focus, reduced motion, no `transition: all`, no mobile overflow, project style consistency.

## Final response

Report files changed plus Red, Green, Refactor, Verification. For UI animation work, include the animation library/API choice and why it was chosen or avoided.
## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
