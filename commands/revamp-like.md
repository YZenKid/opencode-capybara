---
description: Revamp the current UI to visually match a reference URL or screenshot
agent: orchestrator
model: cliproxyapi/gpt-5.5
---

Revamp the current UI to closely match this reference while preserving the project's real content, framework, routing, accessibility, and local conventions:

```text
$ARGUMENTS
```

Use the standalone `opencode-orchestrator` workflow and delegate visual implementation/review to `@designer` using `opencode-designer` when appropriate.

## Workflow

1. Create or reuse `.opencode/plans/<task-id>.md` plus per-task `.opencode/draft/<task-id>/` and `.opencode/evidence/<task-id>/` artifacts.
2. Capture reference and current screenshots before editing: desktop `1440x1200`, tablet `768x1024`, mobile `390x844`, full page and hero.
3. Use wait → stabilize → scroll → settle → screenshot.
4. Inspect existing project components, styles, assets, icons, animation libraries/APIs, and commands. Reuse before creating.
5. Extract visual spec and asset inventory into the primary plan.
6. Generate or source legal style-equivalent replacements when image assets are required and unavailable.
7. Run a Google Stitch MCP Design System Gate through `@designer` when `stitch` is available: use Stitch to generate/refine the design-system brief and screen/design variants, then adapt them to existing project tokens/components. Record `used`, `unavailable`, `skipped`, or `blocked`.
8. Run an Animation System Gate: choose CSS/native primitives, existing dependency, `motion.dev`, `animejs`, `animate.css`, React Native Reanimated/Gesture Handler, Lottie, Flutter implicit/explicit animation, or Flutter Hero based on platform and reference motion. Do not use web-only libraries for native mobile screens unless target is web/webview.
9. Implement section-by-section: layout shell/background, navbar/hero, content rhythm, cards/icons/decorations, responsive behavior, motion/hover states.
10. Run checks, capture final screenshots at matching viewports, compare section-by-section, and fix largest mismatches first.
11. Summarize artifact paths, captures, Stitch usage status, visual changes, animation library/API choice, generated assets, remaining limitations, and verification.

Rules: do not implement from memory, do not copy restricted assets, and do not claim visual parity without final screenshots.
