---
description: Revamp the current UI to visually match a reference URL or screenshot
agent: orchestrator
model: cliproxyapi/gpt-5.5
---

Revamp the current UI to closely match this reference while preserving the project's real content, framework, routing, accessibility, and local conventions:

```text
$ARGUMENTS
```

Use this workflow strictly:

1. Load the `reference-ui-replication` skill.
2. If the task is user-facing UI, delegate visual implementation/review to `@designer`.
3. Use Playwright before editing code:
   - capture reference desktop, tablet, mobile, and full-page screenshots,
   - capture the current implementation at matching viewports,
   - note section order, visual tokens, background treatments, icon style, animation, and responsive behavior.
4. Inspect existing project components, styles, assets, icons, animation libraries, and commands. Reuse before creating.
5. Implement section-by-section for visual parity:
   - layout shell/background,
   - navbar and hero,
   - content sections in reference rhythm,
   - cards, icons, decorative layers,
   - responsive behavior,
   - motion and hover states.
6. After implementation, run the app/checks and capture result screenshots at the same viewports.
7. Compare against the reference and fix the largest mismatches first.
8. Summarize:
   - reference captures used,
   - visual changes made,
   - remaining intentional differences or asset limitations,
   - verification performed.

Rules:

- Do not implement from memory.
- Do not claim close visual parity without post-implementation screenshots.
- Preserve real content unless the user explicitly asks to clone reference text.
- Do not copy copyrighted assets directly unless they are already available, licensed, or explicitly provided.
- Ask only before decisions that materially affect branding, legality, architecture, content, or UX direction.
