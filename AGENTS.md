# Global OpenCode instructions

Do not prefix shell commands with `rtk` in OpenCode/OpenChamber sessions.
Run package manager and test/build commands directly, for example:
- `bun run build`, not `rtk bun run build`
- `npm run test:coverage`, not `rtk npm run test:coverage`
- `npx vitest ...`, not `rtk proxy npx vitest ...`

RTK is configured separately for Claude Code and should not be used by OpenCode/OpenChamber unless the user explicitly asks for it.

## Standalone opencode skill policy

Each OpenCode agent should rely on its single standalone `opencode-*` skill instead of loading many domain skills. Use agent routing rather than manually combining overlapping skill instructions.

- UI/design/reference work → `@designer` using `opencode-designer`.
- Implementation/testing → `@fixer` or build agent using `opencode-fixer` / `opencode-build`.
- Planning artifacts → `@artifact-planner` using `opencode-artifact-planner`.
- Architecture/review/simplification → `@oracle` using `opencode-oracle`.
- Docs/library research → `@librarian` using `opencode-librarian`.
- Codebase search/map → `@explorer` using `opencode-explorer`.
- Visual asset generation → `@visual-asset-generator` using `opencode-visual-asset-generator`.
- Document/PDF/spreadsheet/Office processing → `@document-specialist` using `opencode-document-specialist`.

## Anti-AI-slop UI policy

For any user-facing frontend, web app, mobile app, dashboard, landing page, form, navigation, React/Next, Tailwind, shadcn/ui, or reference/Figma-style work:

1. Route planning/review/polish to `@designer` unless the change is tiny and non-visual.
2. Do not produce generic UI: no default purple gradients, bland centered cards, random emoji icons, numeric-only service icons, raw placeholders, blank image frames, or accidental system-font sameness unless the existing design system requires it.
3. Pick a clear visual direction, then implement spacing, typography, color, hierarchy, motion, visual density, responsive behavior, and accessibility deliberately.
4. Prefer existing project components/tokens; create small coherent tokens only when missing.
5. Validate rendered UI with browser/visual checks when runnable and do not call a UI task done without production-like screenshots.
6. For image-heavy UI, use the visual asset pipeline below.
7. For substantial UI/reference/image-heavy work, require designer signoff and section-by-section evidence before finalizing.
8. Do not hardcode device-specific absolute paths in prompts, configs, or scripts; derive absolute paths from the active workspace/project root or portable env-based roots. When OpenCode config files live in a different root than the target app, keep those roots distinct and pass the target app `project_root` explicitly.

## Frontend/mobile animation policy

For website, frontend, mobile app, React/Next, React Native/Expo, Flutter, landing page, dashboard, or reference UI work, use an **Animation System Gate** instead of defaulting to generic fades/slides.

1. Inspect existing animation dependencies, project components, tokens, utilities, `package.json`, lockfiles, and `pubspec.yaml` before adding anything.
2. Prefer: reuse existing animation system → CSS/native platform primitives → existing dependency → justified new dependency.
3. Web choices:
   - CSS native for small hover/focus/opacity/transform interactions.
   - `motion.dev` for non-trivial React/Next/Vue layout, state, gesture, scroll, route, modal/drawer, spring, and staggered motion.
   - `animejs` for timeline-heavy, SVG, hero logo/brand, advanced stagger, counter/graph, or decorative choreography.
   - `animate.css` only for quick ready-made entrance/attention effects where it will not look generic.
4. Mobile choices:
   - React Native built-in `Animated` / `LayoutAnimation` for simple motion when sufficient.
   - React Native Reanimated + Gesture Handler for non-trivial Expo/React Native UI-thread, gesture, layout, sheet, swipe, carousel, drawer, keyboard/sensor motion.
   - Lottie / `lottie-react-native` for valid bodymovin motion assets such as onboarding, loading, empty state, brand, and celebration illustrations.
   - Flutter implicit animations for simple state/property changes; explicit `AnimationController` for complex choreography; Hero for shared-element route transitions.
5. Do not use web-only libraries (`motion.dev`, `animejs`, `animate.css`) for native mobile screens unless target is web/webview.
6. Support `prefers-reduced-motion` or platform reduced-motion/accessibility behavior where relevant; avoid `transition: all`, janky layout motion, interaction-blocking motion, and unbounded loops.
7. For substantial UI/reference work, generic hover-only motion is not enough: require motion that matches the reference/brand or explicitly mark the result as draft.
8. Validate web animation in browser and mobile animation in simulator/device when runnable. Final summaries should state the animation library/API choice and rationale.

## Visual asset generation pipeline

Use for image-heavy UI, reference replication, portfolios, product mockups, testimonial/avatar clusters, blog thumbnails, hero art, icon badge sets, and rich backgrounds.

1. For portfolio/reference/template work that has hero art, portraits, project cards, thumbnails, testimonial/avatar clusters, blog cards, icon badges, or rich backgrounds, assume it is image-heavy until the designer proves otherwise.
2. `@designer` returns an asset manifest before final implementation when rich imagery materially affects quality.
3. The planner/designer must make an explicit image generation decision: `generate`, `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed` with a section-by-section reason. Do not silently choose CSS placeholders or omit imagery.
4. If the reference contains meaningful imagery and project-owned/licensed assets are unavailable, plan legal style-equivalent generation for hero, thumbnails, and rich section visuals by default.
5. Check whether image generation is available. Prefer `@visual-asset-generator` when exposed.
6. Generate legal style-equivalent replacements for unavailable/unlicensed assets. Do not copy restricted reference assets.
7. If generation is unavailable, ask whether to proceed with user-provided assets, prompt manifest only, or temporary placeholders; if the user does not approve placeholders, mark the work `blocked` or `draft`.
8. In image asset jobs, pass the target app `project_root` explicitly and keep `target_path` relative to that root; never bake in config-root absolute paths or device-specific home directories.
9. Integrate assets with explicit dimensions, correct loading priority, meaningful `alt` for content images, and decorative `alt=""`/`aria-hidden` when appropriate.
10. Validate with screenshots and section-by-section comparison before claiming visual parity.
11. For substantial reference work, do not claim close parity without reference/current/final evidence and designer pass/fail review.

## Reference UI replication policy

For requests with a reference URL, screenshot, template, portfolio, dashboard, or phrases like "mirip", "clone", "match", "replicate", "revamp like", or "jadikan seperti ini":

1. Treat as visual parity unless the user says inspiration only.
2. Capture evidence before editing with Playwright/browser automation that reflects what a real user sees.
3. Use wait → stabilize → scroll → settle → screenshot:
   - exact viewport,
   - load/network idle best-effort,
   - wait preloaders/loading overlays when known,
   - settle entrance animations,
   - scroll incrementally to trigger lazy/reveal,
   - wait at each scroll position,
   - return to intended capture position for hero screenshots,
   - capture stable screenshots.
4. Required captures: reference/current/final full-page and hero screenshots at desktop `1440x1200`, tablet `768x1024`, and mobile `390x844` unless task specifies otherwise.
5. Extract visual spec: section order, hero composition, CTA placement, grids, spacing, card sizes, fonts, colors, buttons, cards, background details, icon style, image treatment, motion, and responsive behavior.
6. Extract asset inventory and classify as project-owned/provided, licensed, or third-party requiring legal replacement.
7. Preserve user content unless explicitly asked to clone text.
8. Do not claim close visual parity without final screenshots, comparison notes, and final designer signoff.
