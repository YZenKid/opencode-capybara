---
name: reference-ui-replication
description: Replicate a website or screenshot reference into an existing frontend with high visual parity using Playwright screenshots, section mapping, design-token extraction, implementation, and iterative visual review.
---

# Reference UI Replication

Use this skill when the user asks to make an existing page look like a reference URL, screenshot, template, landing page, portfolio, dashboard, or visual style. The goal is not merely inspiration; the goal is measurable visual similarity while preserving the project's real content, framework, routing, accessibility, and conventions.

## Core Principle

Do not implement from memory or a vague impression. First capture the reference, extract its design system, implement section-by-section, then visually compare the result and iterate.

## Required Workflow

### 1. Capture the Reference

Use Playwright before editing code.

- Open the reference URL.
- Capture full-page screenshots at minimum:
  - desktop: `1440x1200` or project default desktop viewport
  - tablet: `768x1024`
  - mobile: `390x844`
- Capture above-the-fold viewport screenshots for hero comparison.
- Record console errors only if they affect rendering.
- If the page has animation, wait for initial load animations to settle before final capture, but note what animations exist.

### 2. Extract a Visual Spec

Create a concise visual spec before implementation:

- Section order and purpose.
- Hero composition: copy placement, visual asset placement, CTA placement, stats/badges.
- Layout grid: container width, columns, alignment, section spacing.
- Color system: background, surface, border, text, muted text, accent, gradients.
- Typography: display/body font style, scale, weight, line height, letter spacing.
- Components: navbar, buttons, cards, tabs, timeline rows, carousel cards, pricing/testimonial/news/CTA/footer if present.
- Background details: glows, radial gradients, patterns, dotted lines, overlays, noise, decorative shapes.
- Iconography and assets: exact icon family if known; otherwise match style, size, stroke/fill, and placement.
- Motion: initial reveal, hover, carousel, tab, scroll effects, transitions.
- Responsive behavior: what stacks, hides, resizes, or reorders.

### 3. Inspect Existing Project Patterns

Before creating new code, inspect the local project for:

- Framework and routing.
- Styling approach: CSS modules, global CSS, Tailwind, styled components, shadcn/ui, design tokens.
- Existing components, utility functions, icons, image handling, animation libraries.
- Existing tests or visual/e2e setup.

Prefer reuse over recreation. Extend existing components where possible.

### 4. Implement for Parity

Implement section-by-section in this order:

1. Layout shell and global background.
2. Navbar and hero.
3. Primary content sections in reference order.
4. Decorative layers, icon treatments, and card polish.
5. Responsive refinements.
6. Motion and interactive states.

Rules:

- Preserve the user's real content unless explicitly asked to clone reference text.
- Match reference structure, rhythm, and visual hierarchy.
- Avoid generic AI UI patterns that are not present in the reference.
- Do not replace the whole app architecture unless the user explicitly asks.
- Do not add new icon or animation dependencies if an existing project dependency can achieve the result.
- If an exact asset cannot be legally or technically reused, create a style-equivalent substitute and state the limitation.

### 5. Visual Validation Loop

After implementation:

- Run the app if needed.
- Capture screenshots of the resulting page at the same viewports as the reference.
- Compare against the reference screenshots.
- Identify mismatches by section:
  - composition
  - spacing
  - typography
  - color/contrast
  - asset/icon style
  - background/decorative details
  - animation/interaction
  - responsive behavior
- Fix the largest visible mismatches first.
- Repeat at least one visual review pass for high-fidelity tasks.

Do not claim a close match if screenshots were not captured after implementation.

## When the Prompt Is Minimal

If the user says only something like:

```text
buat jadi mirip seperti ini https://example.com
```

Assume they want:

- same section rhythm and visual hierarchy,
- same overall color mood,
- same style of hero, cards, background, buttons, and footer,
- real project content preserved,
- no copyrighted asset copying unless assets are already available or explicitly licensed,
- responsive desktop/tablet/mobile parity.

Ask only if a decision materially changes content, branding, legality, architecture, or UX direction.

## Output Expectations

For implementation summaries, include:

- Reference captures used.
- Main visual changes made.
- Remaining intentional differences or asset limitations.
- Verification commands/screenshots/checks.

Keep summaries concise.
