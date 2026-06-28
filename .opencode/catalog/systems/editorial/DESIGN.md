# Design System: Editorial

> Category: Creative & Artistic
> Surface: web | mobile | both
> Vibe: Editorial-grade typography, paper-white ground, ink-black body, single link-blue accent.

> **Source**: https://open-design.ai/plugins/systems/example-editorial
> **License**: Apache-2.0
> **Indexed by**: `python3 ~/.config/opencode/scripts/design-source-importer.py --download editorial`
> **Status**: downloaded (full content). For live refresh: `--refresh --slug editorial`.

---

## 1. Visual Theme & Atmosphere

Editorial restraint is the discipline: serif-led hierarchy, ink-on-paper contrast, and rules that look like a style guide rather than a UI kit.

This system commits to editorial restraint. It is **not** a generic modern-clean aesthetic; the rules below are concrete and rejectable.

## 2. Color Palette & Roles

### Primary
- **Ink** (`#0a0a0a`): Primary text, dark surfaces, structural strokes.
- **Accent** (`#1a3a7a`): Action color, focus, primary CTA, selected state.
- **Surface** (`#fdfcf8`): Light canvas for content blocks; cards, panels, sheets.

### Secondary
- **Muted** (`#d4d0c4`): Secondary text, borders, dividers, low-emphasis fills.
- **Subtle** (`#ebe7da`): Hover, disabled, inactive.

### Semantic
- **Success** (`#0a6b3a`): Confirmations, positive deltas.
- **Warning** (`#a86b00`): Caution, recoverable errors.
- **Danger** (`#9a1f1f`): Destructive actions, errors, critical alerts.
- **Info** (`#1a3a7a`): Tips, non-blocking notices.

### Dark variants (when applicable)
- **Dark ground** (`#0a0a0a`): For optional inverted hero surfaces.
- **Dark ink** (`#fdfcf8`): Primary text on dark ground.

## 3. Typography Scale

| Role | Family | Size | Weight | Line-height | Letter-spacing |
|---|---|---|---|---|---|
| Display | Playfair Display | 56/64 | 700 | 1.05 | -0.02em |
| H1 | LMR Roman / Source Serif | 40/48 | 700 | 1.1 | -0.015em |
| H2 | LMR Roman / Source Serif | 32/40 | 700 | 1.15 | -0.01em |
| H3 | LMR Roman / Source Serif | 24/32 | 600 | 1.2 | -0.005em |
| H4 | LMR Roman / Source Serif | 20/28 | 600 | 1.25 | 0 |
| Body Large | LMR Roman / Source Serif | 18/28 | 400 | 1.55 | 0 |
| Body | LMR Roman / Source Serif | 16/24 | 400 | 1.5 | 0 |
| Small | LMR Roman / Source Serif | 14/20 | 400 | 1.45 | 0.01em |
| Caption | LMR Roman / Source Serif | 12/16 | 500 | 1.35 | 0.02em |
| Mono | JetBrains Mono | 14/20 | 400 | 1.5 | 0 |

## 4. Spacing & Layout

- **Base unit**: 4px
- **Scale**: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128
- **Container max-width**: 1280px (content), 1440px (full bleed)
- **Grid**: 12 columns (desktop), 8 (tablet), 4 (mobile)
- **Gutter**: 24px (desktop), 16px (mobile)
- **Section padding**: 96px (desktop), 64px (tablet), 48px (mobile)
- **Component padding**: 12px, 16px, 24px
- **Border radius**: 6px (sharp), 10px (default), 16px (chunky), 9999px (pill)

## 5. Motion Language

- **Duration**: fast 150ms, normal 250ms, slow 400ms, theatrical 800ms
- **Easing**: standard (cubic-bezier(0.2, 0, 0, 1)), decel (cubic-bezier(0, 0, 0, 1)), accel (cubic-bezier(0.3, 0, 1, 1))
- **Intent**: feedback (hover/focus/press), guidance (page transitions), delight (only when earned)
- **Reduced motion**: respect `prefers-reduced-motion: reduce`. Replace transforms with opacity, halve durations.

## 6. Voice & Copy

### Tone rules
1. Be direct. Lead with the action or answer, not preamble.
2. Use present tense. Avoid future-tense promises ("akan bisa").
3. Show specifics. Numbers, names, paths. Not "some users" — "12 teams".
4. Match the system's vibe: editorial restraint means serif-led hierarchy, ink-on-paper.

### Anti-tone rules
1. No "ayo", "pasti bisa", "solusi terbaik", vague mission filler.
2. No "foto menyusul", "dokumentasi menyusul", placeholder/trust-breaking text.
3. No internal jargon, server labels, port numbers, framework names in user-facing copy.
4. No emoji unless the system explicitly calls for them.

## 7. Imagery Strategy

- **Photo style**: editorial photojournalism, B&W option
- **Illustration style**: line illustration
- **Aspect ratios**: 16:9 (hero), 4:3 (cards), 1:1 (avatars), 21:9 (banner)
- **Alt text**: descriptive, contextual, concise (≤140 chars). Start with the subject.
- **When real photography is required** (org/community/craft/food/agriculture): hero and product sections MUST use real photography or generated domain-specific imagery, not abstract illustrations.

## 8. Component Variants

### Button
- Variants: primary, secondary, ghost, danger, link
- Sizes: sm (32), md (40), lg (48)
- States: default, hover, focus (visible ring), active, disabled, loading
- Icon-only: square variants, 16/20/24 icons

### Input
- Types: text, textarea, select, checkbox, radio, toggle, slider, combobox
- States: default, focused (ring + label lift), filled, error, disabled
- Sizes: sm (32), md (40), lg (48)

### Card
- Variants: default (elevated), flat (bordered), interactive (hover lift), featured (accent border)
- Anatomy: media slot (top), body (title + description + meta), footer (actions)

### Navigation
- Top bar: logo + nav + actions. Height 56 (compact) or 64 (default).
- Sidebar: 240 (expanded) / 64 (collapsed). Persistent or hover-trigger.
- Tabs: underline (default), pill (filled), segment (bordered).
- Breadcrumbs: chevron-separated, current page non-link.

### Feedback
- Toast: top-right (web), bottom (mobile). Auto-dismiss 4s, action optional.
- Alert: inline, contextual. Variants: info, success, warning, danger.
- Modal: centered, scrim, trap focus, ESC to close, return focus on close.

## 9. Anti-Patterns (Reject If)

1. Centered gradient hero without product/domain composition.
2. Card-spam section anatomy repeated 3+ times with identical grid.
3. Fake metrics (e.g. "10k+ users") without meaningful source.
4. "Foto menyusul" or placeholder imagery in production-facing UI.
5. Decorative stats (5, 10, 100) without context.
6. Generic "modern clean" copy without source-backed specifics.
7. Three-tier pricing with one tier obviously featured without business justification.
8. Emoji icons used as decorative filler.
9. Debug copy, port numbers, framework names in user-facing strings.
10. Abstract blobs or CSS glass panels as hero when domain requires real photography.

## 10. Source & Provenance

- **Catalog source**: https://open-design.ai/plugins/systems/example-editorial
- **License**: Apache-2.0
- **Adapted by**: OpenCode harness (designer lane), 2026-06-28
- **Deviations**: token values adapted for high-contrast printing on dark grounds; H4 weight raised from 500 to 600 for accessibility; reduced-motion handling explicit.
- **Project extensions**: add per-project overrides under `## Project Overrides` below; do not edit sections 1-9 in place.

## 11. Project Overrides (fork only)

> Only present in forks via `python3 ~/.config/opencode/scripts/design-system-fork.py --base editorial`.
> List deviations here with reason + risk per deviation.
