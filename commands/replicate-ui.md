---
description: Replicate a target UI from a reference URL or screenshot with measured visual parity
agent: orchestrator
model: cliproxyapi/gpt-5.5
---

Replicate the target UI from the reference with measurable visual similarity while preserving the project's real content, framework, routing, accessibility, and conventions.

```text
$ARGUMENTS
```

Use the standalone `opencode-orchestrator` workflow for routing. Route visual planning, implementation, or review to `@designer` using `opencode-designer` when available. Use `@explorer` for broad codebase discovery and `@fixer` only for bounded implementation/test edits.

## Required workflow

1. Create or reuse SDD/TDD artifacts with stable task id `YYYYMMDD-HHMM-<slug>`:
   - `.opencode/plans/<task-id>.md` as the only primary plan file.
   - `.opencode/draft/<task-id>/visual-notes.md` when expanded visual notes are needed.
   - `.opencode/draft/<task-id>/asset-manifest.md` when detailed image generation jobs are needed.
   - `.opencode/evidence/<task-id>/discovery.md`, `reference-captures.md`, `current-captures.md`, `visual-comparison.md`, `verification.md`.
2. Capture reference evidence before editing at desktop `1440x1200`, tablet `768x1024`, and mobile `390x844`; capture full page and hero/above-fold.
3. Use wait → stabilize → scroll → settle → screenshot. Record paths and notes.
4. Capture current target evidence at matching viewports when runnable.
5. Extract visual spec and asset inventory into the primary plan; put expanded details under per-task draft folder when needed.
6. Classify assets as project-owned/provided, licensed, or third-party requiring legal replacement. Do not copy restricted assets.
7. Run a Google Stitch MCP Design System Gate through `@designer` when `stitch` is available: translate reference traits into a project-adapted design-system brief, component anatomy, responsive rules, states, and implementation handoff. Record `used`, `unavailable`, `skipped`, or `blocked` with the reason.
8. Run an Animation System Gate: inspect existing animation libraries/APIs, then choose CSS/native primitives, existing dependency, `motion.dev`, `animejs`, `animate.css`, React Native Reanimated/Gesture Handler, Lottie, Flutter implicit/explicit animation, or Flutter Hero based on platform and reference motion. Do not use web-only libraries for native mobile screens unless target is web/webview.
9. Implement section-by-section for parity while preserving real content.
10. After implementation, run checks, capture final screenshots with the same workflow, compare section-by-section, and fix largest mismatches first. Include Stitch usage status plus animation library/API choice and rationale in the summary.

Do not claim close visual parity without final screenshots and comparison notes.
