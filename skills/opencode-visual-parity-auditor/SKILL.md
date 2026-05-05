---
name: opencode-visual-parity-auditor
description: Standalone read-only skill for screenshot-based visual parity audits, section comparison, and claim-level assessment.
---

# Visual Parity Auditor

- Audit reference/current/final screenshots.
- Capture with wait-stabilize-scroll-settle: wait for load/preloaders, settle animations, scroll to trigger lazy content, then capture stable frames.
- Compare section order, spacing, density, typography, color, imagery, icon style, motion/state, and responsive behavior.
- Use claim levels: `draft`, `inspired by`, `style-equivalent`, or `close parity`.
- Block close-parity claims without final screenshots and designer signoff.
- Stay read-only; do not edit files.

## Evidence requirements

For reference or clone-like work, require reference/current/final captures at matching viewports unless the user explicitly narrows scope. Default viewports: desktop `1440x1200`, tablet `768x1024`, mobile `390x844`.

Use the same capture method for all sides:

1. Set exact viewport.
2. Navigate with network-idle best effort.
3. Wait for known preloaders/loading overlays.
4. Let entrance animations settle.
5. Scroll in increments to trigger lazy images and reveal animations.
6. Wait after each scroll step.
7. Return to the intended hero/top position.
8. Capture stable hero and full-page screenshots.

## Comparison matrix

Compare section order, hero composition, CTA placement, grid, spacing, density, typography scale/weight/tracking, palette, backgrounds, card/list/table/form treatment, image crop/treatment, icon style, motion/state behavior, responsive adaptation, and rendering-affecting console/network errors.

Return: claim level, matched strengths, section-by-section deltas, blockers before higher claim, and evidence paths. Never call `close parity` without final screenshots and designer pass/fail review.
