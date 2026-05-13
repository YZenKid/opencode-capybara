---
description: Initialize or update the current project's DESIGN.md
agent: orchestrator
model: cliproxyapi/gpt-5.3-codex
---

Initialize a project-local `DESIGN.md` for the current target project.

Arguments from user, if any:

```text
$ARGUMENTS
```

Workflow:

1. Inspect the current target project root and identify existing design guidance.
2. Look first for `DESIGN.md` at the project root.
3. If the project documents a local equivalent such as `design-system/DESIGN.md`, read it too and treat it as project-specific guidance.
4. Inspect existing project tokens, components, styles, and docs when available so the file matches the project instead of generic taste.
5. If `DESIGN.md` already exists at the project root, ask before overwriting or replacing it.
6. If no root `DESIGN.md` exists, create one in the current project root.
7. Use the user's brand/style hints from `$ARGUMENTS` together with the project's current patterns.
8. Keep the file in English and use exactly these 9 sections, in this order:
   - Visual Theme & Atmosphere
   - Color Palette & Roles
   - Typography Rules
   - Component Stylings
   - Layout Principles
   - Depth & Elevation
   - Do's and Don'ts
   - Responsive Behavior
   - Agent Prompt Guide
9. Make the guidance concrete, specific, and aligned to the target project's own UI language.
10. Prefer rules that map to existing tokens, components, breakpoints, and interaction patterns; add new guidance only when the project actually needs it.
11. Include explicit instructions that project-local `DESIGN.md` wins over generic preferences, and that UI/design work should read it first, then `design-system/DESIGN.md` or any documented project-specific equivalent.
12. If the project is missing design guidance and the work is substantial UI/design work, suggest `/init-design` and ask targeted follow-up questions before inventing a new visual direction.
13. Do not overwrite project design guidance silently.
14. In the generated guide, make the downstream ownership chain explicit enough that future operators know `@designer` owns UI direction first, while accessibility/motion/UI-system review lanes and final `@quality-gate` signoff are conditional follow-up lanes rather than replacements.

Write `DESIGN.md` as a concrete project guide, not a generic checklist. Use this structure:

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

The `Agent Prompt Guide` should also state the downstream ownership chain for substantial UI work: `@designer` owns direction, motion/reduced-motion review, and implementation guidance first; `@architect` is a conditional specialist lane; `@quality-gate` remains the final cross-cutting signoff lane when the work is non-trivial.
```

After writing the file, summarize:

- where `DESIGN.md` was created or updated,
- which project files informed it,
- any assumptions made,
- how future agents should apply it,
- whether follow-up screenshots or design review are recommended.
