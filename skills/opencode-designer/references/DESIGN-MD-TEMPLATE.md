# DESIGN.md Template

Use this template when creating or updating `DESIGN.md` for a project. This file is the source of truth for design decisions and grammar.

## Structure

```markdown
# [Project Name] Design System

## Overview
- Design philosophy and guiding principles
- Target audience and use cases
- Key design values (e.g., clarity, speed, delight)

## Design Language

### Visual Identity
- **Color palette**: Primary, secondary, accent, neutral, semantic colors
- **Typography**: Font families, sizes, weights, line heights
- **Spacing**: Base unit, scale (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px)
- **Border radius**: Default, small, large, full
- **Shadows**: Elevation levels (e.g., sm, md, lg)

### Component Grammar
- **Button**: Variants (primary, secondary, ghost, danger), sizes, states
- **Input**: Text, textarea, select, checkbox, radio, toggle
- **Card**: Default, interactive, featured
- **Navigation**: Top bar, sidebar, breadcrumbs, tabs
- **Feedback**: Toast, alert, banner, modal, dialog

### Motion Principles
- Duration scale: fast (150ms), normal (250ms), slow (400ms)
- Easing: ease-in, ease-out, ease-in-out
- Purpose: feedback, guidance, delight
- Reduced motion: respect `prefers-reduced-motion`

### Accessibility Requirements
- WCAG 2.1 AA minimum (AAA preferred for critical paths)
- Color contrast: 4.5:1 for text, 3:1 for large text
- Focus indicators: visible, high contrast
- Keyboard navigation: all interactive elements reachable
- Screen reader: semantic HTML, ARIA labels where needed

## Layout System

### Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px
- Wide: > 1440px

### Grid
- Columns: 12 (desktop), 8 (tablet), 4 (mobile)
- Gutter: 16px (mobile), 24px (desktop)
- Max width: 1280px

### Spacing Patterns
- Section padding: 48px (desktop), 32px (mobile)
- Component padding: 16px, 24px
- Gap between elements: 8px, 12px, 16px

## Iconography
- Style: [outline / filled / duotone]
- Size: 16px, 20px, 24px, 32px
- Stroke width: 1.5px or 2px
- Grid: 24px base grid
- Source: [icon library name or custom set]

## Imagery Strategy
- Photography style: [documentary / lifestyle / product / abstract]
- Illustration style: [flat / isometric / 3D / hand-drawn]
- Aspect ratios: [16:9 for hero, 4:3 for cards, 1:1 for avatars]
- Alt text: descriptive, contextual, concise

## Anti-Patterns (Reject If)
- ❌ Card spam: repeated card/grid anatomy across sections
- ❌ Fake metrics: arbitrary KPIs, debug copy, server labels
- ❌ Placeholder imagery: lorem ipsum images, blank frames
- ❌ Generic hero: centered gradient without product composition
- ❌ Debug UI: port numbers, server labels, implementation notes
- ❌ Motion without purpose: decorative animations that don't aid UX

## Reference Pack
- [Link to reference screenshots or URLs]
- [Competitor analysis if applicable]
- [User research insights if available]
```

## Usage

1. **Create**: Copy this template to project root as `DESIGN.md`
2. **Customize**: Fill in project-specific values based on research, references, or existing design
3. **Maintain**: Update when design decisions change
4. **Reference**: All design lanes (@designer, @frontend, @mobile) read this file first

## Integration with Lanes

- **@designer**: Reads DESIGN.md first, produces blueprint aligned with grammar
- **@design-system-engineer**: Translates DESIGN.md tokens/primitives into code
- **@frontend/@mobile**: Implements screens using DESIGN.md component grammar
- **@quality-gate**: Validates output against DESIGN.md requirements

## Example: Minimal DESIGN.md

```markdown
# SaaS Dashboard Design

## Overview
- Clean, professional, data-dense
- Target: Business users, analysts, admins
- Values: Clarity, efficiency, trust

## Color Palette
- Primary: #2563eb (blue)
- Secondary: #64748b (slate)
- Success: #10b981 (green)
- Warning: #f59e0b (amber)
- Error: #ef4444 (red)
- Background: #ffffff, #f8fafc
- Text: #0f172a, #475569, #94a3b8

## Typography
- Font: Inter, system-ui
- Sizes: 12px, 14px, 16px, 20px, 24px, 32px
- Weights: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

## Components
- Button: primary (blue), secondary (outline), ghost (text-only)
- Card: white bg, 8px radius, subtle shadow, 16px padding
- Input: border 1px slate-300, focus ring 2px blue-500
- Table: striped rows, sortable headers, sticky header

## Accessibility
- WCAG 2.1 AA
- Contrast: 4.5:1 minimum
- Focus: 2px blue ring, 2px offset
```
