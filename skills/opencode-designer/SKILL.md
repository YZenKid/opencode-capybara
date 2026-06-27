---
name: opencode-designer
description: Standalone UI/UX, motion direction, and visual parity workflow for designer. Use for frontend design, design systems, responsive layouts, reference replication, motion/reduced-motion review, accessibility review, visual polish, asset planning, and browser-validated UI quality.
---

# OpenCode Designer Skill

Use this as the designer’s self-contained UI/UX manual.

## Lane position
This lane owns UI/UX direction, blueprinting, reference parity, motion strategy, and design-quality review. It is **not** the primary production screen-code lane.

After design handoff:
- shared tokens/primitives/component APIs -> `@design-system-engineer`
- web screen/page implementation -> `@frontend`
- mobile screen/native implementation -> `@mobile`
- simple bounded UI fix -> `@fixer`

Adopted from Open Design: strong `DESIGN.md` authority, artifact/source-pack discipline, screenshot-based evidence, and reusable design grammar. Not adopted: upstream-specific plugin/export/runtime assumptions unless explicitly installed here.

## Trigger / skip

- Trigger: UI/UX direction, design systems, responsive layouts, motion direction, accessibility review, visual parity work, design blueprinting, and any substantial user-facing visual decision.
- Trigger: when implementation quality depends on explicit visual, interaction, asset, or motion guidance rather than generic existing patterns.
- Trigger: for substantial UI/reference work, create/update `.opencode/evidence/<task-id>/visual-quality-contract.md` and `.opencode/evidence/<task-id>/reference-essence.md`.
- Skip: tiny reversible UI tweaks with clear existing design guidance, or pure implementation tasks where the design/handoff is already settled.
- Skip: final conformance/risk signoff. This lane defines or reviews design quality; `@quality-gate` owns the last gate.

For canonical tool policy and boundaries, refer to:
- `.opencode/docs/TOOL_USAGE.md`
- `.opencode/docs/AGENT_TOOL_ACCESS.md`

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Design Depth Enforcement

**Hard fail metrics — design spec MUST meet these minimums or auto-reject to `needs-polish`/`blocked`:**

| Metric | Minimum |
|---|---|
| Design Read statement | Required for substantial work |
| Craft dials documented | DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY |
| Reference pack | Minimum 3 reference screenshots/URLs or explicit first-principles rationale |
| Page-by-page UX blueprint | Minimum 3 pages with full detail |
| Section-level visual spec | Minimum 5 sections per page with layout/hierarchy/spacing/typography/color/interaction/motion/responsive |
| Component system plan | Minimum 20 components with variants/states/accessibility/responsive/motion |
| Visual system | Palette roles, typography scale, spacing scale, radius, border, elevation, icon style, image style, grid, breakpoints, focus states |
| Asset/image decision | Per visual area: generate/use-provided/licensed/no-generation-needed with reason |
| Motion system | Purpose, API/library choice, per-page motion map, interaction motion, reduced-motion fallback |
| Interaction/state design | Default/hover/focus/active/disabled/loading/empty/error/success/permission/unauthenticated/offline/partial/skeleton/validation |
| Responsive plan | Mobile/tablet/desktop layout rules, nav changes, CTA placement, sticky behavior, data display adaptation |
| Accessibility gate | Semantic headings, keyboard support, visible focus, form labels, contrast, screen-reader, touch targets, reduced motion |
| Validation evidence | Screenshots by viewport and key states, interaction checks, motion/reduced-motion checks, accessibility notes |

**Auto-reject rules:**
- Missing Design Read = `blocked`
- Missing craft dials = `needs-polish`
- Missing reference pack (3+ references or first-principles rationale) = `blocked`
- Missing page-by-page blueprint (3+ pages) = `blocked`
- Missing section-level spec (5+ sections per page) = `needs-polish`
- Missing component system (20+ components) = `needs-polish`
- Missing visual system = `needs-polish`
- Missing asset/image decision = `blocked`
- Missing motion system = `needs-polish`
- Missing interaction/state design = `needs-polish`
- Missing responsive plan = `needs-polish`
- Missing accessibility gate = `needs-polish`
- Missing validation evidence = `blocked`

**Enforcement mechanism:**
Before marking design as `ready`, verify all minimums are met. If any minimum fails, mark `needs-polish` or `blocked` and specify which minimums failed.

## Anti-Generic Landing Page Gate

**Hard fail rules — these are mechanical failures, not taste preferences:**

| Failure | Status |
|---|---|
| Centered gradient hero without product/domain composition | `blocked` |
| Generic "modern clean" without source-backed specifics | `blocked` |
| Fake dashboard metrics (arbitrary KPI numbers, 99%/24k/10x claims) | `needs-polish` |
| Emoji icons or numeric-only service icons | `needs-polish` |
| Placeholder imagery or blank image frames | `needs-polish` |
| Repeated card/grid anatomy across sections (card spam) | `needs-polish` |
| Abstract blobs, floating UI cards, CSS glass panels as hero | `blocked` |
| Vague neon blobs or default purple/blue glow | `needs-polish` |
| Debug/internal copy, server labels, port numbers in UI | `needs-polish` |
| Lorem text or placeholder copy in user-facing UI | `needs-polish` |
| Missing hero composition (no meaningful product/domain content) | `blocked` |
| Missing image strategy per visual section | `blocked` |
| Missing motion motivation (no explanation for non-trivial motion) | `needs-polish` |
| Missing reduced-motion support | `needs-polish` |

**Enforcement:**
These are mechanical failures, not taste preferences. If any failure is present, return `needs-polish` or `blocked`. Do not mark substantial UI `ready` when these failures exist.

## Smart UI artifact workflow

- Use an artifact-first design workflow that makes the agent behave like a senior product designer with a clear brief, design-system context, craft rules, and validation evidence.
- Work discovery-first on substantial briefs: confirm audience, surface, goal, brand, content, constraints, device priority, assets, motion, accessibility, and success criteria before design direction.
- In Greenfield App Accelerator, provide creative product/UX options and mark design readiness as `MVP design enough`, `needs-polish`, `reference-ready`, or `blocked`; do not force full visual parity unless reference/image-heavy.
- In Maintenance Stability Mode, preserve existing UX and focus on the smallest design decision needed for the fix.
- In Creativity Fast Path, you may move faster for explicit draft/prototype/exploration asks: generate bolder options, looser wireframes, or rough visual directions, but keep them labeled `draft`, `prototype`, or `exploration`, state assumptions/confidence, and avoid claiming parity/final readiness.
- For tiny, reversible tweaks, you may proceed with light assumptions.

## Discovery-first design intake

For a fresh substantial design request, do not start with pixels or code when the brief leaves material choices open. Ask or explicitly lock the missing details that affect direction: product type, target users, primary job, platform, brand constraints, content availability, reference intent, asset availability, motion expectations, accessibility baseline, and acceptance criteria.

Use an assumption-first path only when the missing details are reversible and low risk. Record assumptions in the handoff so implementers and reviewers know what was decided.

### Required source pack for substantial work

Before converging on a substantial UI/design direction, assemble and cite a source pack:

- project `DESIGN.md` / `design-system/DESIGN.md` / repo-local style guidance,
- current UI screenshots or current-state notes when editing an existing product,
- reference screenshots/URLs when the user points to inspiration or parity,
- component/token inventory and notable reusable patterns,
- asset availability and image/legal constraints.

If a source category is relevant but unavailable, record that explicitly and keep the resulting decision conservative.

## Quality bar

- Pick a clear visual direction before coding or reviewing.
- Avoid generic AI UI: default purple gradients, bland centered cards, emoji icons, numeric-only service icons, placeholder imagery, blank image frames, and accidental system-font sameness.
- Design typography, hierarchy, color, spacing, surfaces, motion, visual density, responsive behavior, and accessibility deliberately.
- Prefer existing components/tokens; create small tokens only when missing.
- For build-from-scratch, substantial app, dashboard, landing, mobile/web, or design-system work, the Design Gate is not satisfied by high-level visual intent alone. It must produce a general end-to-end UI/UX Design Blueprint before implementation is called ready.
- For greenfield, revamp, or taste-sensitive work, do not settle on the first plausible design direction. Generate 2-3 bounded directions, section anatomies, or interaction approaches when that materially improves quality, then converge with explicit rationale.
- Late polish is not a substitute for core design quality. If hierarchy, composition, density, imagery, or interaction model remain generic, return `needs-polish` or `blocked` instead of pretending the work is premium-ready.

## Material Grammar Gate

Explicit requested aesthetics are acceptance requirements. For substantial UI, translate style before implementation/review:

- user phrase -> exact requested phrase and intent.
- tokens -> color roles, typography feel, radius, shadow/elevation, blur/opacity, texture, spacing, motion tone.
- surfaces -> buttons, cards, panels, hero layers, nav, forms, media frames, backgrounds.
- layout rules -> section anatomy, density, rhythm variation, hero composition, responsive behavior.
- reject_if -> concrete mismatch blockers.

Example: `claymorphism + glassmorphism` -> soft warm/pastel tokens, rounded tactile clay surfaces with pressed/raised shadows, frosted translucent glass overlays with restrained blur, layered highlights, airy product/domain hero composition; reject_if generic neon SaaS, flat repeated card grids, unreadable blur, random abstract blobs, fake dashboard metrics, debug copy, CSS filler where imagery matters.

If style grammar is missing or final screenshots visibly mismatch the requested aesthetic, return `needs-polish` or `blocked`; do not mark substantial UI `ready`.

## Source-approved 1:1 Porting / Literal Porting Contract

When the user explicitly says `1:1`, `clone`, `port`, `copy`, `copy from`, `make exactly like`, or provides a source URL/repo/file plus explicit approval to reuse it, literal porting overrides inspiration-only reinterpretation. Prefer exact layout/component/class anatomy, tokens, spacing, DOM structure, and section composition from the approved source for code/layout/tokens. Preserve legal/security/scope safeguards: do not copy restricted assets, fake testimonials/claims, logos/trademarks without approval, privacy/security hazards, secrets, or unsafe behavior. Any deviation must be documented as a scope-preserving deviation or remaining parity debt.

### Open Source Reuse Policy

When the user provides an open source reference (repo, package, component, pattern), do not reject it and invent a replacement from scratch. Verify the license first:

- **Permissive (MIT, BSD, Apache-2.0, ISC, Unlicense, CC0, MPL-2.0)**: reuse and adapt freely. Prefer source anatomy/components/code over reinventing. Record source URL + license in evidence.
- **Copyleft / caution (LGPL, GPL, AGPL, SSPL, custom/nonstandard)**: escalate to user with license class and risk note before reuse. Do not auto-generate replacement either — ask.
- **No license / unclear**: ask user for direction. Do not assume blocked.
- Fallback to self-generate only when: license is genuinely unclear AND user cannot clarify, scope genuinely diverges, or reuse would introduce incompatible dependencies. Record why reuse was skipped.

## Mechanical UI failure gates

- Non-empty Primary Surface Gate: homepage, landing, or primary surface cannot be empty, tagline-only, or placeholder when the slice claims usable MVP. This is a mechanical failure.
- Card Spam / Layout Repetition Gate: repeated card/grid anatomy across sections is a mechanical failure for substantial UI. Vary section structure by content purpose; repeated cards without hierarchy or domain meaning are `needs-polish`/blocked.
- User-facing Copy Gate: no debug/internal copy, server labels, port numbers, framework jargon, implementation notes, lorem, review/status labels, or `foto menyusul` placeholder text in user-facing UI unless target audience is explicitly technical and rationale is recorded.
- Fake Metric / Debug Artifact Gate: no arbitrary KPI numbers, fake dashboard metrics, demo counters, fake controls, local dev artifacts, placeholder charts, or “99%/24k/10x” claims unless clearly demo/dev content with label and source. Decorative symbolic numbers without meaningful data are `needs-polish`.
- Hero Composition Gate: substantial landing/app hero needs meaningful product/domain composition, content hierarchy, CTA path, and asset/image decision. Abstract blobs, floating UI cards, CSS glass panels, dashboard fragments, or illustration/pattern-card heroes are not enough when reference/domain requires real photography.
- Reference Feel Parity Gate: reference parity is not structural similarity alone. For community/craft/food/agriculture/artisan/organization work, design must capture warmth, humanity, texture, domain-specific content, and lived reality. Sterile/template feel despite structural similarity is `needs-polish`/`blocked`.
- Domain Texture Requirement: hero/product/community sections must include domain-specific content — real photography or generated domain-specific imagery, physical objects, natural materials, hands working, environment, or local context when those drive trust/warmth in the reference. Missing domain texture is `needs-polish`/`blocked`.
- Manifest/Asset Consistency Gate: do not accept icon/manifest/asset-path references that point to missing files, wrong formats, or placeholder assets when real assets are required.
- Style Fidelity Evidence/Signoff: final substantial UI claim needs screenshots/reference evidence or designer signoff. Missing evidence lowers claim to `draft`, `needs-polish`, or `blocked`.

## Open Design skill adaptation

Adapt useful Open Design patterns locally; do not paste upstream wholesale or claim upstream tools/scripts exist here.

| Open Design source | Local rule |
|---|---|
| `frontend-design` | Establish point of view, real states, responsive/a11y, production-grade UI, no generic gradients/cards/blobs, self-review before final. |
| `taste-skill` | Write `Design Read`; set `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`; run mechanical anti-slop checks. |
| `design-brief` | Convert vague ask into palette, accent, typography, display, layout, mood, density, assets, platform, constraints, and defaults. |
| `reference-design-contract` | Split references into `Keep`, `Change`, `Do not copy`; preserve intent by default, but under Source-approved 1:1 Porting / Literal Porting Contract exact layout/component/class anatomy, tokens, and code structure may be preferred when the user explicitly approved/licensed the source. Protected assets, fake testimonials/claims, restricted logos/trademarks, privacy/security hazards, and unsafe copied behavior still remain blocked. |
| `design-md` | Treat project `DESIGN.md` as design source of truth and create/update it through `/init-harness` when substantial guidance is missing. |
| `web-design-guidelines` | Apply layout/type/color/motion/a11y basics before taste flourishes. |
| `design-review` | Score critique with evidence; state what a 10/10 would require; flag AI slop. |
| `plan-design-review` | Require before/after screenshot plan and viewport/state evidence for substantial visual work. |
| `ui-ux-pro-max` | Caveat: use only as inspiration category. Do not claim its pattern library/assets/scripts are active unless installed locally. |

### Design Read and craft dials

For substantial work, write:

`Reading this as: <surface> for <audience>, with <vibe>, leaning toward <design system/aesthetic family>.`

Then set:

- `DESIGN_VARIANCE`: low/medium/high divergence from common patterns/reference.
- `MOTION_INTENSITY`: none/subtle/moderate/expressive, tied to user value.
- `VISUAL_DENSITY`: airy/balanced/dense, tied to content and device priority.

Project-local `DESIGN.md` overrides these defaults.

### Mechanical anti-AI-slop preflight

Run before output or handoff. Failures map to `needs-polish` or blocker. Concrete examples: see `references/slop-examples.md`.

- **Hero & CTA**: hero fits initial viewport without cropping primary CTA; nav stays single-line on desktop; CTAs meet contrast and don't duplicate intent.
- **Section variety**: vary section anatomy by purpose; reject same card/grid rhythm across 3+ sections.
- **Image strategy**: every visual section declares `generate`, `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed`.
- **Motion**: every non-trivial motion explains meaning; support `prefers-reduced-motion` or platform equivalent.
- **AI tells**: reject default purple/blue glow, fake dashboards, vague neon blobs, emoji icons, placeholder frames, numeric-only service icons, and cloned reference visuals.
- **Eyebrow restraint**: avoid repetitive eyebrow labels; max roughly `ceil(sectionCount / 3)` unless design system says otherwise.
- **Style fidelity**: verify requested style grammar is visible in tokens, surfaces, layout, hero, copy, and assets; mismatch is not pure taste.

### Generation taste contract

For UI, image, mockup, hero, thumbnail, avatar, badge, or background generation:

1. Brief lock: target surface, audience, brand, constraints, platform, assets, acceptance.
2. Design Read and dials.
3. Read `DESIGN.md` first; fallback `design-system/DESIGN.md`; suggest `/init-harness` for substantial missing guidance so the consolidated harness/design initialization can create or update project-local guidance.
4. Manifest/art direction: section title, semantic subject, composition, palette/light, medium, dimensions, alt/decorative strategy, legal notes, integration notes, `quality_bar`, `reject_if`.
5. Reference contract when applicable: `keep`, `change`, `do_not_copy`.
6. Execute generation only after manifest is art-directed; prefer visual-asset-generator/9router saved asset path.
7. Require integration evidence before ready/parity claims.

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
- If substantial UI/design work has no project-local design guide, recommend `/init-harness` before inventing a new visual direction so the consolidated harness/design initialization can create or update `DESIGN.md`.
- Existing project design systems and tokens win over generic taste.

If any required blueprint section is missing for substantial work, return `blocked` or `needs-polish`; do not mark the design `ready`.

## Craft gates

- Anti-AI-slop: avoid generic gradients, bland centered cards, emoji icons, numeric-only service icons, placeholder imagery, blank frames, and accidental system-font sameness.
- State coverage: define default, hover, focus, active, disabled, loading, empty, error, success, permission, unauthenticated, offline, partial, skeleton, and validation states when relevant.
- Animation discipline: motion must serve meaning, use the smallest fit-for-platform system, and include reduced-motion handling.
- Typography/color/icon craft: keep hierarchy legible, color roles intentional, and icons legal and functional.

## Workflow

1. **MANDATORY stack read**: Read `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` before any non-trivial UI work. If missing or stale, run `/init-harness` or route to `@librarian` for current stack docs — do not implement blind.
2. Inspect target project's `DESIGN.md` first. If absent, run `python3 ~/.config/opencode/scripts/init-design-system.py --project-root .` to seed `DESIGN.md` and `.opencode/design-system/registry.md` from templates.
3. Inspect framework, styling, tokens, assets, components, tests, and build the source pack.
3. **DESIGN.md reference**: If creating or updating `DESIGN.md`, use `references/DESIGN-MD-TEMPLATE.md` as the canonical structure to ensure all 9 sections are covered.
4. Define the full Design Readiness Gate blueprint for substantial work: experience direction, page map, section specs, component/visual systems, asset decisions, motion map, states, responsive rules, accessibility, and evidence plan.
5. When quality would benefit, generate 2-3 bounded directions or section strategies, compare them against the source pack, and record why one direction wins.
6. For substantial work, own motion direction/reduced-motion review directly and consume specialist handoffs from `@architect` as needed; final cross-cutting security/accessibility/visual-parity signoff is handled by `@quality-gate`.
7. **Generator-first implementation**: For new UI components, use the documented official generator/CLI/MCP path first (e.g. `shadcn add`, framework generators, repo scripts from `PROJECT_COMMANDS.md`). **Do not manually create components that a generator can produce.** If manual fallback is used, record the exact command attempted and why it failed.
8. Implement/review section-by-section and component-by-component against the blueprint.
9. Check accessibility: semantics, labels, focus-visible, alt text, touch targets, reduced motion.
10. **MANDATORY visual validation**: Validate with Playwright browser screenshots. Do not accept "browser not available" as reason to skip; if browser automation cannot run, report `blocked` and require environment remediation. For substantial UI/reference work, require reference/current/final captures and section-by-section comparison.

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

Repeated card/grid anatomy, fake metrics/debug artifacts, user-facing internal copy, placeholder/abstract hero where imagery matters, or explicit aesthetic mismatch must be `needs-polish` or `blocked` for substantial UI.

Required deliverables for substantial work: experience direction, page-by-page UX blueprint, section-level visual spec matrix, component system plan, visual system, interaction/state design, responsive plan, accessibility gate notes, validation evidence plan, reference capture report when applicable, section anatomy table, motion storyboard, icon system matrix, visual density checklist, asset manifest, image generation decision, and final pass/fail comparison.

Also include:
- source pack summary,
- chosen direction plus rejected alternatives when explored,
- explicit note when the result is reference-backed versus first-principles-driven.

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

Permissive/Public Source Reuse
User-directed Direct Reuse
Asset/Source Inventory

Capture reference/current, extract visual spec, inventory assets, classify licensing, preserve user content, implement for section density/composition, then compare final screenshots. Do not silently copy restricted assets; if the user explicitly directs reuse of provided/public/user-approved assets, record the source, permission/license status when known, and risk. Otherwise use legal icon libraries, existing assets, or generated/style-equivalent replacements.
- Fail UI when screenshots show dev overlays, dummy text, fake controls, blank image frames, numeric-only service icons, or missing planned sections.
- For portfolio/reference/template work with hero art, portraits, project cards, thumbnails, testimonial/avatar clusters, blog cards, icon badges, or rich backgrounds, assume image-heavy until proven otherwise. Designer must return an image generation decision per section: `generate`, `use-provided-assets`, `licensed-existing-assets`, `no-generation-needed`, or `direct-reuse-user-approved`. If no licensed/provided assets exist, require style-equivalent generation fallback instead of blank frames, CSS-only placeholders, or generic gradients.

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

For reviews, provide concise findings with locations/sections. For implementation, include changed files, screenshots, validation commands, generator-first compliance evidence (which commands/tools were used for new components), and remaining visual deltas.

## Escalation

- Escalate to `@librarian` when current library/component/API facts matter for design feasibility.
- Escalate to `@artifact-planner` when the work needs a durable execution plan before implementation.
- Escalate to `@visual-asset-generator` when the asset/image strategy requires generation jobs.
- Escalate to `user` when reference intent, asset legality/reuse approval, or product taste direction remains materially ambiguous.
## Quality checklist
- [ ] Design Read and craft dials are explicit for substantial work.
- [ ] Source pack is complete or missing inputs are recorded conservatively.
- [ ] Requested style grammar is translated into tokens, surfaces, layout rules, and reject_if.
- [ ] Anti-AI-slop gate passed.
- [ ] Asset/image decision exists per visual area.
- [ ] Motion and reduced-motion behavior are specified.
- [ ] Accessibility and responsive evidence are part of readiness.
- [ ] **MANDATORY**: Playwright/browser screenshots captured for substantial UI/reference work; no "browser unavailable" skip without explicit `blocked` status and remediation plan.
- [ ] **Reference feel parity verified**: captures warmth/humanity/texture/domain-specific content, not just structure.
- [ ] **Domain texture verified**: real photography, human element, physical objects, local context present when reference/domain requires them.
- [ ] **No placeholder text in production-facing UI**: no `foto menyusul`, no decorative stats without meaningful data.
- [ ] **Structured design output contract fields present** for major surfaces: `must_show`, `must_not_show`, `reject_if`, `fake_warmth_patterns`, `template_smells`.
- [ ] **Frontend design pushback artifact exists** if pushback occurred: `.opencode/evidence/<task-id>/design_pushback.md`.
- [ ] **Quality-gate visual rubric exists**: `.opencode/evidence/<task-id>/visual-rubric.md`.
- [ ] **Reference-driven work has side-by-side screenshot comparison** annotated for essence match/mismatch.

## Anti-patterns
- Generic dashboard/landing direction with no source-backed character.
- Placeholder imagery or abstract hero filler where imagery matters.
- Repeated card/grid anatomy across substantial sections.
- Claiming premium/polished without evidence.
- Ignoring explicit requested aesthetic grammar.

## Output example

```yaml
status: needs-polish
design_read: "Reading this as wellness journaling app for reflective solo users, soft tactile editorial mood."
craft_dials:
  DESIGN_VARIANCE: medium
  MOTION_INTENSITY: subtle
  VISUAL_DENSITY: airy
finding:
  - "Hero composition still generic and image strategy missing for reflection deck section"
required_before_ready:
  - "Add section-level image decision and motion rationale"
```


## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
