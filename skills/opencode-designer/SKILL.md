---
name: opencode-designer
description: Standalone UI/UX and visual parity workflow for designer. Use for frontend design, design systems, responsive layouts, reference replication, accessibility review, visual polish, asset planning, and browser-validated UI quality.
---

# OpenCode Designer Skill

Use this as the designer’s self-contained UI/UX manual.

## Quality bar

- Pick a clear visual direction before coding or reviewing.
- Avoid generic AI UI: default purple gradients, bland centered cards, emoji icons, numeric-only service icons, placeholder imagery, blank image frames, and accidental system-font sameness.
- Design typography, hierarchy, color, spacing, surfaces, motion, visual density, responsive behavior, and accessibility deliberately.
- Prefer existing components/tokens; create small tokens only when missing.

## Build/review workflow

1. Inspect framework, styling, tokens, assets, components, and tests.
2. Define visual direction and interaction model.
3. Implement/review section-by-section.
4. Check accessibility: semantics, labels, focus-visible, alt text, touch targets, reduced motion.
5. Validate with browser screenshots when runnable; for substantial UI/reference work, require reference/current/final captures and section-by-section comparison.

## Google Stitch MCP Design System Gate

For substantial UI/UX, web, mobile, app design, design-system, dashboard, landing page, reference replication, or revamp work, use Google Stitch MCP as a design-system ideation and generation assistant when the `stitch` MCP is available. Stitch is a remote MCP server at `https://stitch.googleapis.com/mcp`; it can connect AI tools to Stitch projects and provide project/screen, AI generation, and design-system workflows. Treat Stitch output as design input, not final implementation.

Decision order:

1. Inspect existing project UI, tokens, component library, assets, routing, accessibility conventions, responsive breakpoints, and animation patterns.
2. Decide whether Stitch adds value. Use Stitch for new visual direction, substantial redesign, mobile/web app screen generation, design-system extraction, variants, or reference-to-system translation. Skip Stitch for tiny visual fixes, backend-only tasks, or projects with a strict existing design system where generation would add noise.
3. If Stitch is available, provide a focused design brief instead of a generic prompt: target platform, target users, primary flows, existing tokens/components, brand constraints, content constraints, accessibility requirements, responsive breakpoints, motion direction, asset/image decisions, and legal/reference limitations.
4. Ask Stitch for a structured handoff: visual thesis, design-system principles, token recommendations, typography scale, color roles, spacing/radius/elevation, component anatomy, screen layout rules, responsive behavior, interaction states, accessibility notes, and implementation guidance.
5. Adapt Stitch output to project patterns using Reuse > Extend > Create. Do not copy generated UI blindly, introduce unrelated libraries, override established tokens without reason, or bypass accessibility and browser validation.
6. Record Stitch usage in the design output: `used`, `unavailable`, `skipped`, or `blocked`, with the MCP/tool status and reason. If unavailable, continue with local design-system reasoning and mark the limitation.

Stitch must not replace these gates: anti-AI-slop quality bar, Animation System Gate, asset inventory/legal replacement handling, image generation decision, Playwright/browser evidence, and final designer signoff. `impeccable` from `skills.sh` may be used as an optional design-quality checklist reference; the deprecated `frontend-design` skill must not be used for new work.

## Designer signoff contract

For substantial UI/reference/image-heavy work, return one of these statuses: `ready`, `blocked`, or `needs-polish`.

- `ready`: the plan/spec is sufficient for implementation and the visual direction is coherent.
- `blocked`: missing reference evidence, motion storyboard, icon strategy, asset manifest, image generation decision, or other required visual spec.
- `needs-polish`: the structure is sound but the design still needs targeted refinement before implementation is called complete.

Required deliverables for substantial work: reference capture report, section anatomy table, visual spec matrix, motion storyboard, icon system matrix, visual density checklist, asset manifest, image generation decision, and final pass/fail comparison.

## Animation System Gate

For website, frontend, mobile app, React/Next, React Native/Expo, Flutter, landing page, dashboard, or reference UI work, define motion direction before implementation/review. Do not default to generic CSS fades/slides when the experience needs richer motion, and do not add animation dependencies when CSS or existing project patterns are enough.

Decision order: reuse existing project animation system → CSS/native platform primitives → existing dependency → justified new dependency. Always inspect `package.json`, `pubspec.yaml`, lockfiles, existing components, tokens, and animation utilities before recommending a library.

### Web animation choices

- CSS native: small hover/focus/active states, simple opacity/transform, skeletons, and minor `@keyframes`; prefer transform/opacity, avoid `transition: all`, and support `prefers-reduced-motion` for non-trivial motion.
- `motion.dev`: recommended default for non-trivial React/Next/Vue component, state, layout, gesture, scroll, route, modal/drawer, shared-layout, spring, and staggered motion when no existing standard conflicts.
- `animejs`: choose for choreographed timelines, SVG path/line/morphing, hero logo/brand motion, advanced staggering, animated counters/graphs, or DOM/canvas-like decorative motion.
- `animate.css`: use only for quick ready-made entrance/attention effects, prototypes, or simple landing-page hints; avoid overuse when it would look template/generic.

### Mobile animation choices

- React Native built-in `Animated` / `LayoutAnimation`: simple opacity/translate/scale or light feedback when already used and sufficient.
- React Native Reanimated: recommended default for non-trivial React Native/Expo UI-thread motion, shared values, springs, layout entering/exiting, keyboard/sensor motion, bottom sheets, swipe actions, carousels, drawers, and gesture-driven transitions.
- React Native Gesture Handler: pair with Reanimated for native-feeling pan/swipe/drag, drawer/swipeable rows, press/long-press, and interactive cards/sheets.
- Lottie / `lottie-react-native`: use for valid bodymovin JSON assets such as onboarding illustrations, empty states, loading, brand/motion identity, and celebration moments; not for ordinary layout/gesture transitions.
- Flutter implicit animations: prefer for simple property/state changes like `AnimatedContainer`, `AnimatedOpacity`, and `AnimatedAlign`.
- Flutter explicit animations / `AnimationController`: use for complex timelines, coordinated multi-widget motion, repeated/controlled animations, physics/spring simulations, and advanced transitions.
- Flutter Hero: use for shared-element route transitions such as thumbnail-to-detail or card-to-detail continuity.

For native mobile screens, do not recommend web-only animation libraries (`motion.dev`, `animejs`, `animate.css`) unless the target is web/webview or the project explicitly uses a web context.

Designer output for non-trivial motion should state the chosen animation level/library/API, why it fits the UX/brand, reduced-motion/accessibility expectations, and validation needs.

## Reference replication

Capture reference/current, extract visual spec, inventory assets, classify licensing, preserve user content, implement for section density/composition, then compare final screenshots. Do not copy restricted assets; use legal icon libraries, existing assets, or generated/provided replacements.
- Fail UI when screenshots show dev overlays, dummy text, fake controls, blank image frames, numeric-only service icons, or missing planned sections.
- For portfolio/reference/template work with hero art, portraits, project cards, thumbnails, testimonial/avatar clusters, blog cards, icon badges, or rich backgrounds, assume image-heavy until proven otherwise. Designer must return an image generation decision per section: `generate`, `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed`. If no licensed/provided assets exist, require legal style-equivalent generation by default instead of blank frames, CSS-only placeholders, or generic gradients.

## Generated asset art direction gate

For substantial image generation, create an art direction brief or style board before the asset manifest.

Required fields:

- visual thesis
- reference traits to preserve
- composition notes
- subject, props, and environment
- art medium/style constraints
- palette and lighting
- camera/crop/perspective
- texture/material details
- negative style constraints
- brand/domain specificity
- acceptance/rejection criteria

Reject generic AI aesthetics such as glossy cyberpunk dashboards, random neon blobs, vague “modern tech”, floating UI cards without domain meaning, cloned reference assets, fake logos/text, uncanny portraits/hands, inconsistent style sets, over-saturated stock-ish art, and same-looking thumbnails.

Require per-asset uniqueness and set cohesion. The generated set must feel like one art-directed family, but each asset still needs a distinct role, composition, and thumbnail identity.

## Playwright/browser capture

Use wait-stabilize-scroll-settle for reference/current/final screenshots. Capture full page and hero/mobile/tablet/desktop as needed. Record limitations and rendering errors.

## Local resources

- `references/playwright/` for E2E, ad-hoc, visual, and debugging patterns.
- `references/frontend-review/` for review checklists/output formats.
- `references/senior-frontend/` for React/frontend patterns.
- `scripts/ui_ux_search.py`, `scripts/design_system.py`, `data/ui-design-intelligence/` for design-system lookup.
- `scripts/design_token_generator.py` for token scaffolding.
- `scripts/persona_generator.py` for UX/persona tasks.

## Output

For reviews, provide concise findings with locations/sections. For implementation, include changed files, screenshots, validation commands, and remaining visual deltas.
