# Generic UI Plan

## Design Read
Reading this as: modern clean SaaS.
- DESIGN_VARIANCE: low
- MOTION_INTENSITY: subtle
- VISUAL_DENSITY: balanced

## Reference Pack
- first-principles rationale: generic modern clean is fine.

## Goal
- Create landing page with centered gradient hero, fake dashboard metrics, emoji icons, placeholder copy, abstract blobs, floating UI cards, CSS glass panels, and default purple blue glow.

## Non-goals
- Avoid extra work.

## Requirements
1. Use centered gradient hero.
2. Add fake KPI 99% improvement.
3. Add emoji icons.
4. Add placeholder imagery.
5. Use abstract blobs.
6. Use glass panels.
7. Keep it modern clean.
8. Add hero.
9. Add CTA.
10. Ship fast.

## Acceptance Criteria
1. Page looks modern clean.
2. Hero has fake dashboard metrics.
3. Emoji icons visible.
4. Placeholder copy present.
5. Purple blue glow visible.
6. Abstract blobs present.
7. CSS glass panel used.
8. CTA works.

## Design Depth Specification
### Page-by-page UX Blueprint
- Landing only
### Section-level Visual Specification
- Hero only
### Asset/Image Decision
- no-generation-needed
### Motion System
- basic fade
### Accessibility Gate
- maybe later
### Validation Evidence Plan
- screenshot

## Component Inventory
1. **HeroCard**
   - States: empty, loading, error, success
2. **CTAButton**
   - States: empty, loading, error, success

## Implementation Steps
1. Build hero.
2. Add metrics.
3. Add icons.
4. Add copy.
5. Test.

## Validation Commands
1. npm test
2. npm run lint
