---
name: opencode-designer
description: Standalone UI/UX, motion direction, and visual parity workflow for designer. Use for frontend design, design systems, responsive layouts, reference replication, motion/reduced-motion review, accessibility review, visual polish, asset planning, and browser-validated UI quality.
---

# OpenCode Designer Skill

Use this as the designer’s self-contained UI/UX manual.

For canonical tool policy and boundaries, refer to:
- `.opencode/docs/TOOL_USAGE.md`
- `.opencode/docs/AGENT_TOOL_ACCESS.md`

## Smart UI artifact workflow

- Use an artifact-first design workflow that makes the agent behave like a senior product designer with a clear brief, design-system context, craft rules, and validation evidence.
- Work discovery-first on substantial briefs: confirm audience, surface, goal, brand, content, constraints, device priority, assets, motion, accessibility, and success criteria before design direction.
- For tiny, reversible tweaks, you may proceed with light assumptions.

## Discovery-first design intake

For a fresh substantial design request, do not start with pixels or code when the brief leaves material choices open. Ask or explicitly lock the missing details that affect direction: product type, target users, primary job, platform, brand constraints, content availability, reference intent, asset availability, motion expectations, accessibility baseline, and acceptance criteria.

Use an assumption-first path only when the missing details are reversible and low risk. Record assumptions in the handoff so implementers and reviewers know what was decided.

## Quality bar

- Pick a clear visual direction before coding or reviewing.
- Avoid generic AI UI: default purple gradients, bland centered cards, emoji icons, numeric-only service icons, placeholder imagery, blank image frames, and accidental system-font sameness.
- Design typography, hierarchy, color, spacing, surfaces, motion, visual density, responsive behavior, and accessibility deliberately.
- Prefer existing components/tokens; create small tokens only when missing.
- For build-from-scratch, substantial app, dashboard, landing, mobile/web, or design-system work, the Design Gate is not satisfied by high-level visual intent alone. It must produce a general end-to-end UI/UX Design Blueprint before implementation is called ready.

## General Design Readiness Gate

For build-from-scratch or substantial UI/UX work, treat this gate as blocking until the plan/spec contains enough detail to implement without guessing. Keep it domain-agnostic: apply it to SaaS, dashboards, marketplaces, mobile apps, internal tools, portals, landing pages, and other product surfaces.

Required blueprint sections:

1. **Experience direction**
   - Target users and primary/secondary personas.
   - Usage context, device priority, tone/personality, visual richness, visual density, accessibility baseline, and performance expectations.
2. **Page-by-page UX blueprint**
   - For each major page/screen: purpose, user goal, primary/secondary actions, information hierarchy, section order, navigation behavior, responsive behavior, and empty/loading/error/success/permission/offline states when relevant.
3. **Section-level visual specification**
   - For each important section: role, layout, hierarchy, spacing, typography, color/background treatment, card/list/table/form treatment, CTA placement, imagery/icon usage, interaction behavior, motion behavior, state behavior, and mobile/tablet/desktop behavior.
4. **Component system plan**
   - Reusable components, variants, states, usage rules, accessibility requirements, responsive behavior, and motion behavior. Include forms, buttons, cards, navigation, data displays, feedback, empty states, and other core primitives as applicable.
5. **Visual system**
   - Palette roles, typography scale, spacing scale, radius, border, elevation/shadow, icon style, image/illustration style, layout grid, breakpoints, focus states, and light/dark mode rules when relevant.
6. **Asset and image decision**
   - Per visual area/section: `generate`, `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed`, with reason, asset type, dimensions, alt-text strategy, legal replacement policy, and integration notes. Do not leave final UIs with raw placeholders when visual quality depends on imagery.
7. **Motion system**
   - Motion purpose, animation API/library choice, per-page/section motion map, interaction motion, loading/success/error motion, reduced-motion fallback, timing/easing guidance, and performance constraints.
8. **Interaction and state design**
   - Default, hover, focus, active, disabled, loading, empty, error, success, permission denied, unauthenticated, offline/unavailable, partially loaded, skeleton, and validation states where applicable.
9. **Responsive plan**
   - Mobile/tablet/desktop layout rules, navigation changes, CTA placement, sticky/fixed behavior, data display adaptation, form layout changes, and image crop/ratio behavior.
10. **Accessibility gate**
   - Semantic headings, keyboard support, visible focus, form labels, contrast, screen-reader behavior for async state when needed, touch target sizing, reduced motion, and no color-only meaning.
11. **Validation evidence**
   - Required screenshots or review evidence by viewport and key states, interaction checks, motion/reduced-motion checks, accessibility notes, console/network notes when runnable, and final designer signoff.

## DESIGN.md / design-system contract

- Inspect the target project's `DESIGN.md` at the project root first. If it is absent, look for `design-system/DESIGN.md` or another documented project-specific equivalent before relying on generic preferences.
- The target project's own `DESIGN.md` is the first design authority; project-local guidance wins over generic taste.
- Use a 9-section DESIGN.md mental model for design-system reasoning: visual atmosphere, color roles, typography rules, component styling, layout principles, depth/elevation, do/don't rules, responsive behavior, and agent prompt guidance.
- Map design-system input to existing project tokens, components, and breakpoints first; extend only when gaps are real.
- If substantial UI/design work has no project-local design guide, recommend `/init-design` before inventing a new visual direction.
- Existing project design systems and tokens win over generic taste.

If any required blueprint section is missing for substantial work, return `blocked` or `needs-polish`; do not mark the design `ready`.

## Craft gates

- Anti-AI-slop: avoid generic gradients, bland centered cards, emoji icons, numeric-only service icons, placeholder imagery, blank frames, and accidental system-font sameness.
- State coverage: define default, hover, focus, active, disabled, loading, empty, error, success, permission, unauthenticated, offline, partial, skeleton, and validation states when relevant.
- Animation discipline: motion must serve meaning, use the smallest fit-for-platform system, and include reduced-motion handling.
- Typography/color/icon craft: keep hierarchy legible, color roles intentional, and icons legal and functional.

## Build/review workflow

1. Inspect framework, styling, tokens, assets, components, and tests.
2. Define the full Design Readiness Gate blueprint for substantial work: experience direction, page map, section specs, component/visual systems, asset decisions, motion map, states, responsive rules, accessibility, and evidence plan.
3. Use Figma MCP when it adds value, then adapt the output to existing project tokens/components instead of copying blindly.
4. For substantial work, own motion direction/reduced-motion review directly and consume specialist handoffs from `@architect` as needed; final cross-cutting security/accessibility/visual-parity signoff is handled by `@quality-gate`.
5. Implement/review section-by-section and component-by-component against the blueprint.
6. Check accessibility: semantics, labels, focus-visible, alt text, touch targets, reduced motion.
7. Validate with browser screenshots when runnable; for substantial UI/reference work, require reference/current/final captures and section-by-section comparison.

## Figma MCP Design/Canvas Gate

For substantial UI/UX, web, mobile, app design, design-system, dashboard, landing page, reference replication, or revamp work, use Figma MCP as a design-system and canvas assistant when the `figma` MCP is available. Figma MCP can provide design context, search design systems, create design-system rules, write to canvas, and in supported clients send live UI to Figma. Treat Figma MCP output as design input, not final implementation.

Decision order:

1. Inspect existing project UI, tokens, component library, assets, routing, accessibility conventions, responsive breakpoints, and animation patterns.
2. Decide whether Figma MCP adds value. Use it for new visual direction, substantial redesign, design-context extraction, design-system search/rules, canvas updates, or reference-to-system translation. Skip it for tiny visual fixes, backend-only tasks, or projects with a strict existing design system where extra MCP steps add noise.
3. If Figma MCP is available, provide a focused brief instead of a generic prompt: target platform, target users, primary flows, existing tokens/components, brand constraints, content constraints, accessibility requirements, responsive breakpoints, motion direction, asset/image decisions, and legal/reference limitations.
4. Ask Figma MCP for structured design outputs: visual thesis, design-system principles/rules, token recommendations, typography scale, color roles, spacing/radius/elevation, component anatomy, canvas/layout rules, responsive behavior, interaction states, accessibility notes, and implementation guidance.
5. Adapt Figma MCP output to project patterns using Reuse > Extend > Create. Do not copy generated design blindly, introduce unrelated libraries, override established tokens without reason, or bypass accessibility and browser validation.
6. Record Figma MCP usage in the design output: `used`, `unavailable`, `read-only`, `skipped`, or `blocked`, with MCP/client/seat status and reason. If unavailable or write unsupported, continue with local design-system reasoning and mark the limitation.

Figma MCP must not replace these gates: anti-AI-slop quality bar, Animation System Gate, asset inventory/legal replacement handling, image generation decision, Playwright/browser evidence, and final designer signoff. `impeccable` from `skills.sh` may be used as an optional design-quality checklist reference; the deprecated `frontend-design` skill must not be used for new work.

## Artifact output contract

- Use artifact mode vocabulary when the user asks for a standalone deliverable: `prototype`, `deck`, `template`, or `design-system`.
- For HTML artifact requests, output `<artifact identifier="..." type="text/html" title="...">` only when the request is explicitly for an artifact/prototype/deck.
- Do not force the artifact wrapper when editing existing app code or when the user asked for implementation changes.
- For standalone artifacts, prefer seed/template discipline: inspect available templates/references/assets first, map the active design system to tokens, compose from existing section/layout primitives, and self-check before returning the artifact.

## Designer signoff contract

For substantial UI/reference/image-heavy work, return one of these statuses: `ready`, `blocked`, or `needs-polish`.

- `ready`: the plan/spec is sufficient for implementation and the visual direction is coherent.
- `blocked`: missing reference evidence, motion storyboard, icon strategy, asset manifest, image generation decision, or other required visual spec.
- `needs-polish`: the structure is sound but the design still needs targeted refinement before implementation is called complete.

Required deliverables for substantial work: experience direction, page-by-page UX blueprint, section-level visual spec matrix, component system plan, visual system, interaction/state design, responsive plan, accessibility gate notes, validation evidence plan, reference capture report when applicable, section anatomy table, motion storyboard, icon system matrix, visual density checklist, asset manifest, image generation decision, and final pass/fail comparison.

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
