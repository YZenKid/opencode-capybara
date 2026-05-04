---
name: opencode-build
description: Standalone primary build-agent workflow for everyday coding. Use for implementation, TDD, tests, UI runtime checks, package/build/test commands, validation, and concise delivery.
---

# OpenCode Build Skill

Use this for direct coding sessions.

## Workflow

1. Understand request and inspect local patterns.
2. Ask only for material ambiguity.
3. Reuse existing components/utilities/tests.
4. Red → Green → Refactor.
5. Run relevant validation.
6. Summarize briefly.

## Local resources

- `references/playwright/` and `scripts/with_server.py` for browser/app validation.
- `references/senior-frontend/`, `scripts/senior-frontend/` for frontend.
- `scripts/senior-backend/` for backend.
- `references/senior-devops/`, `scripts/senior-devops/` for deployment/CI.
- `references/senior-fullstack/`, `scripts/senior-fullstack/` for fullstack.
- `references/senior-qa/`, `scripts/senior-qa/` for tests.
- `references/simplify-README.md` for refactor clarity.

## UI/browser

For substantial UI/reference/image-heavy work, require production-like screenshots, visual comparison notes, and clear draft vs reference-ready status before closing the task.
For substantial UI/UX, web, mobile, dashboard, landing page, reference, revamp, or design-system work, follow the `@designer` handoff and any Google Stitch MCP design-system brief before implementing. Stitch output is an input to adapt, not a final UI to copy; preserve project components/tokens, accessibility, responsive behavior, content, routing, and validation gates. If the design-system brief or visual spec is missing, pause instead of inventing generic UI.

## Animation System Gate

For website/UI/mobile app work, do not default to generic/simple animation without checking fit. Inspect existing dependencies/patterns first and choose the smallest platform-appropriate motion system.

- Web: CSS native for small interactions; `motion.dev` for non-trivial React/Next/Vue layout/state/gesture/scroll motion; `animejs` for timeline/SVG/hero choreography; `animate.css` for quick ready-made effects only.
- React Native/Expo: built-in `Animated`/`LayoutAnimation` for simple motion; Reanimated + Gesture Handler for non-trivial UI-thread/gesture/layout motion; Lottie for valid illustration/loading/brand motion assets.
- Flutter: implicit animations for simple state/property changes; explicit `AnimationController` for complex choreography; Hero for shared-element route transitions.
- Do not apply web-only animation libraries to native mobile screens unless target is web/webview.
- Support reduced-motion/accessibility behavior, avoid `transition: all` and janky layout animation, and validate via browser or simulator/device when runnable.
- If the motion storyboard, icon strategy, asset manifest, or image generation decision is missing on a substantial UI/reference/image-heavy task, pause and ask for design direction instead of inventing placeholders, generic gradients, blank frames, or generic hover-only effects.

## Final

Include files changed, commands, and Red/Green/Refactor/Verification. For UI animation work, state the animation library/API choice and rationale.
