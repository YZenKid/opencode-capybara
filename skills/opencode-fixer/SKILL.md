---
name: opencode-fixer
description: Standalone bounded implementation workflow for fixer. Use for code edits, tests, fixtures, UI/runtime fixes, Red-Green-Refactor execution, Playwright checks, accessibility fixes, and small maintainability refactors.
---

# OpenCode Fixer Skill

Use this for scoped execution after requirements or a plan are clear.

## Principles

- Follow the provided plan/evidence.
- Reuse project patterns before creating new abstractions.
- Make minimal safe changes.
- Escalate architecture/unclear decisions instead of guessing.

## Red → Green → Refactor

- Red: failing test/regression evidence or visual baseline.
- Green: minimal implementation that passes.
- Refactor: simplify after checks pass; avoid unrelated churn.
- Verification: run relevant lint/build/test/browser checks.

## UI/browser validation

Use wait-stabilize-scroll-settle screenshots for visual/browser tasks. Check desktop/tablet/mobile when responsive behavior changes. Record console/network issues only when they affect rendering.
For substantial UI/reference/image-heavy work, do not close on screenshots alone; require production-like evidence, icon audit, motion audit, and draft vs reference-ready status.
For substantial UI/UX, web, mobile, dashboard, landing page, reference, revamp, or design-system work, implement only from the provided `@designer` handoff and any Google Stitch MCP design-system brief. Treat Stitch output as structured design input that must be adapted to existing project components/tokens, accessibility, responsive behavior, and content. If the spec is missing or conflicts with project patterns, stop and ask instead of creating a new visual direction.

Follow the Open Design-inspired handoff contract: implement from blueprint/plan, respect the active design system and tokens, avoid generic AI UI fallback, and stop on missing asset, motion, state, accessibility, or evidence detail for substantial work.

## Animation implementation gate

For website, frontend, or mobile app animation work, follow the plan/designer motion spec. If no spec exists and the motion is non-trivial, pause or route back for design direction instead of guessing.

- Check existing animation dependencies and patterns first (`package.json`, lockfiles, `pubspec.yaml`, components, tokens, utilities). Prefer reuse over new dependencies.
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
