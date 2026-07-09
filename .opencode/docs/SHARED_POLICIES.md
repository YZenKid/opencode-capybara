# Shared Policies

This document contains policy blocks shared across multiple agents and skills. Agents should reference this document instead of duplicating content.

## Reference-first creativity contract

All agents must follow this contract when generating outputs:

- Prefer repo-local evidence, official docs, upstream source/examples, screenshots/references, and runtime/browser evidence before inventing material details.
- If a reasonable source exists, use it or explicitly record why it was skipped.
- Treat creativity as grounded option generation: for greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with tradeoff rationale.
- Do not present assumptions as facts. Label assumptions explicitly, keep them reversible, and route/ask when they affect architecture, product behavior, UX direction, data, security, or release risk.
- Do not follow the workflow mechanically when stronger repo/reference evidence points elsewhere; adapt and record the reason.
- In outputs/evidence, name the key references used or state that the result is based on repo-local evidence only.

## Anti-generic UI rules

For substantial UI work, these are mechanical failures (not taste preferences):

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
| Missing icon strategy or icon library decision | `needs-polish` |
| Missing motion motivation (no explanation for non-trivial motion) | `needs-polish` |
| Missing reduced-motion support | `needs-polish` |
| 3D used without runtime/asset/performance/fallback rules | `blocked` |

If any failure is present, return `needs-polish` or `blocked`. Do not mark substantial UI `ready` when these failures exist.

## Icon, motion, and 3D system rules

For substantial UI, the project `DESIGN.md` must declare a system (not a one-off) for icons, motion, and 3D. These rules extend the anti-generic table above.

### Icon system
- Pick a single icon family per project (Lucide, Phosphor, Heroicons, Tabler, Iconoir, Material Symbols, Remix Icon, Carbon Icons, Octicons, Bootstrap Icons, etc.). Do not mix.
- Use functional icons from the chosen library; never replace functional UI icons with generated substitutes or emoji.
- Generated icons are only acceptable for decorative badges, lookalike marks, or non-logo imagery; record license and source in evidence.
- Always record the icon library name and license in `Component Stylings > Icon system`.

### Motion system
- The 9-section `DESIGN.md` template (`skills/opencode-designer/references/DESIGN-MD-TEMPLATE.md`) carries explicit `### Motion system` and `### Reduced motion` sub-sections. Substantial UI work that needs motion must fill them in.
- Surface the runtime/library choice in the design system itself, not as a per-implementation choice. Common anchors:
  - Web: CSS native, `motion.dev`, `animejs`, `animate.css` (only for quick ready-made effects).
  - React Native/Expo: built-in `Animated`/`LayoutAnimation`, Reanimated + Gesture Handler, Lottie for valid motion assets.
  - Flutter: implicit/explicit animations, `AnimationController`, Hero.
- Never `transition: all`, layout-janky animation, interaction-blocking overlays, or unbounded loops.
- Always support reduced-motion (`prefers-reduced-motion: reduce`, `accessibilityReduceMotion`, platform APIs) and provide instant alternatives.

### 3D / spatial system
- 3D is allowed when the section materially benefits (product configurator, hero with product-on-stage, data visualization, map/geospatial). Default to flat for dashboards, forms, settings, and transactional surfaces.
- Pick one 3D runtime per project (Three.js + react-three-fiber, model-viewer, Spline, Babylon.js). Do not mix multiple runtimes without a reason.
- Asset pipeline: source (Poly Haven / Quaternius / Kenney / Sketchfab CC filter) -> glTF/GLB -> license recorded in evidence.
- Performance budget: bundle size cap, draw-call / triangle budget, lazy-load, dispose on unmount.
- 3D anti-patterns: 3D for the sake of 3D, autoplay camera spins, heavy assets on the critical path, 3D that hides the primary CTA, fake-material 3D that does not match real product context, watermark removal or origin falsification.
- Always provide a `no-3d` fallback (static image, icon, 2D illustration) under reduced-motion or when 3D fails to load.

### Open-source asset library anchor
- `references/ASSET_LIBRARIES.md` is the curated reference for open-source icon, illustration, stock photography, and 3D model sources with their license posture.
- Always record the chosen library, license, and attribution posture per section in evidence; do not silently hotlink CDN assets that prohibit hotlinking.
- Pair every asset choice with the legal gate: `npm run check:legal-source -- --source <upstream-url>` when reuse posture is unclear.

## Reference pack requirement

For greenfield/UI-heavy/substantial visual work, the plan must include:

- Minimum 3 reference screenshots/URLs, OR
- Explicit first-principles rationale explaining why reference-based design is not used.

Reference pack must cover:
1. Visual direction / aesthetic family
2. Layout / composition patterns
3. Component / interaction patterns
4. Asset / image style
5. Motion / transition style

Missing reference pack = automatic `NEEDS_DEPTH` or `BLOCKED`.

## Design depth requirements

Before marking design as `ready`, verify all minimums are met:

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

## Plan depth requirements

Before reviewing implementation, verify plan meets minimum depth:

| Metric | Minimum |
|---|---|
| Total plan lines | 5000 |
| Goal + Non-goals words | 200 |
| Requirements count | 10 |
| Requirements words | 500 |
| Acceptance Criteria count | 8 |
| Acceptance Criteria words | 300 |
| UI pages (greenfield) | 3 |
| Words per UI page | 1000 |
| Components in inventory | 20 |
| Implementation steps | 50 |
| Validation commands | 10 |

**State coverage requirement:**
Every component must have state coverage: empty, loading, error, success. Missing state coverage = `NEEDS_FIX`.

## Evidence contract

All material changes must end with evidence, not just claims.

Canonical task evidence path: `.opencode/evidence/<task-id>/`.

### Final summary template
```md
## Summary
- ...

## Changes
- ...

## Evidence
- Command: `npm run test:prompt-gates`
- Result: PASS
- Additional validation: ...

## Risks / Limitations
- ...

## Next Steps
- ...
```

If evidence is unavailable, write an explicit limitation note.

## Remediation worklist contract

For any status other than `PASS` (`NEEDS_FIX`, `BLOCKED`, or `PASS_WITH_RISKS`), include a structured remediation worklist. Quality gate stays read-only: prescribe fixes and validation, but do not edit, autofix, patch, commit, or execute remediation.

Each remediation item must include:

- `finding`: concise issue tied to evidence.
- `blocker_or_risk_class`: `hard_stop`, `soft_blocker`, `required_before_PASS`, or `non_blocking_follow_up`.
- `owner_lane`: target lane such as `@orchestrator`, `@fixer`, `@designer`, `@backend`, `@devops`, `@librarian`, or `user`.
- `action`: concrete remediation step.
- `validation`: command, review, evidence, or check needed after action.
- `exit_criteria`: condition that closes item.
- `requires_user_decision`: `yes` or `no`.

For `PASS_WITH_RISKS`, distinguish required-before-`PASS` work from non-blocking follow-ups.

## Source-approved 1:1 porting contract

When the user explicitly asks for `1:1`, `clone`, `port`, `copy`, `copy from`, `make exactly like`, or provides a source URL/repo/file plus explicit approval to reuse it, default to literal copy/adapt/prune/direct reuse rather than redesign or style-equivalent recreation.

Route `@explorer` for source inventory, `@artifact-planner` for copy/adapt/prune/create mapping, `@designer` for exact UI anatomy when visual, `@frontend`/`@fixer` for literal implementation, and `@quality-gate` for parity/reuse evidence.

Keep legal/security/scope safeguards: restricted assets, secrets, unsafe code, incompatible licenses, privacy hazards, fake testimonials/claims, logos/trademarks, and out-of-scope behavior still require blocking, pruning, or substitution with documented rationale.

## External source reuse, scraping, and image-generation legal gate

Use this gate whenever the work involves a third-party website, repository, CDN asset, screenshot, illustration, logo, icon pack, stock image, or AI-generated image prompt that references a real brand, creator, or protected work.

### Source classification
- `user-owned`: the user created it or controls it.
- `user-provided`: the user uploaded it or pasted it into the session.
- `licensed`: license/terms are known and compatible with the intended use.
- `public-but-unlicensed`: publicly reachable, but no clear reuse license/permission is present.
- `restricted`: terms, robots, watermark, paywall, auth wall, or copyright notice indicate scraping/reuse restrictions.
- `unknown`: source exists but permission status is not yet verified.

### Scraping / extraction rules
- Browsing a public website for reference, structure, or factual observation is allowed.
- Copying raw source, bulk extracting assets, or reusing copy/images/styles from a third-party site is **not** allowed silently.
- If the user explicitly asks to clone/port/copy from a site, classify the source first and record one of: license known, user permission asserted, or permission unknown.
- `public-but-unlicensed` and `unknown` sources are allowed for reference, adaptation, layout/structure analysis, and style-equivalent recreation by default. Verbatim code/asset reuse from those sources still requires explicit user direction plus source tracking.
- `restricted` sources remain blocked for bypass/scraping/reuse without permission.
- Do not bypass paywalls, auth walls, anti-bot controls, signed URLs, hotlink restrictions, or robots/terms restrictions.
- Do not scrape or retain personal data, private dashboards, non-public documents, or user-specific content from third-party sites.
- For template/source-driven tasks, inventory what is reused verbatim vs adapted vs generated, and record that in evidence/final notes.

### Asset reuse rules
- Direct asset reuse requires explicit user direction plus source tracking.
- Final notes/evidence should record, when known: source URL/repo, asset type, license/permission status, trademark/logo status, and production-use risk.
- Logos, trademarks, mascots, character art, celebrity likenesses, product screenshots, and watermarked images are high-risk assets. Default to block, prune, or substitute unless the user clearly owns them or provides permission.
- If an external asset is not clearly reusable, prefer style-equivalent generation, licensed replacement, or omission over silent copying.
- Do not fabricate authenticity signals such as testimonials, customer logos, press logos, security badges, award seals, app store badges, or partner marks.

### Image-prompt legal check
Before generating an image, the responsible lane should classify the prompt/output intent:
- `safe-original`: original composition with generic descriptors and no protected identity dependence.
- `style-equivalent`: inspired by broad observable traits, but not asking for a named artist/brand/logo/character/person to be replicated.
- `directed-reuse`: user explicitly wants provided/licensed/owned assets reused.
- `high-risk`: asks for a named artist's exact style, trademark/logo replication, copyrighted character, celebrity/public figure likeness, product UI screenshot cloning, watermark removal, or source-obscuring transformation.

Rules:
- `safe-original` and `style-equivalent` are allowed.
- `directed-reuse` is allowed only with explicit user direction and recorded source/permission notes when known.
- `high-risk` must be blocked, narrowed, or rewritten into a non-infringing/style-equivalent prompt.
- Do not claim generated images are licensed stock, official brand assets, real customers, real employees, or documentary photographs unless that is actually verified.
- Do not remove watermarks, signatures, or attribution marks from source images.
- When generation is used as fallback, record `why_generation_instead_of_reuse` in evidence or final notes.

### Reuse posture (medium-loose default)

`scripts/legal-source-check.py` now emits a `reuse_posture` field so downstream lanes can decide without re-deriving the posture. Allowed values:

- `allowed-direct`: license is clear, source is licensed/user-owned/user-provided, no high-risk signals. Default for reference + adaptation + most direct reuse tasks.
- `allowed-direct-with-risk`: source is public-but-unlicensed or unknown, or carries a high-risk signal (logo, premium, celebrity, lookalike). Adaptation and reference-only are still allowed; verbatim reuse needs explicit user direction.
- `allowed-adapt`: explicit adaptation intent (`reference-only` or `style-equivalent`). Visual anatomy, layout, spacing, composition, and structural code patterns are allowed; verbatim code/asset copying is not the default.
- `allowed-adapt-with-risk`: same as `allowed-direct-with-risk` but for adaptation intent.
- `blocked`: source is restricted, license is copyleft/nonstandard, or bypass would be required. Escalate to user with risk note; do not auto-replace.

The legal source check still emits `needs_user_clarification: true` when:
- intent is `clone` / `1:1` / `copy-from` / `direct-reuse` AND the source is public-but-unlicensed, unknown, restricted, or has a high-risk signal;
- license is copyleft / nonstandard;
- risk signals include brand/logo/celebrity/character or premium-pro assets AND the intent is verbatim reuse.

For all other cases the default is to proceed with `reuse_posture` and record source + risk in evidence instead of asking.

### Escalation defaults
- Permissive OSS code/assets with clear license: reuse/adapt is acceptable.
- Copyleft, custom, marketplace, or clearly restrictive website terms: escalate with risk note before reuse.
- No-license / unclear public sources: adaptation is allowed; escalate only when the task requires verbatim redistribution, premium assets, or brand/trademark-sensitive reuse.
- Trademark/logo/celebrity/character/press-logo requests: default to substitute or ask for explicit ownership/permission.
- If uncertainty remains material, downgrade to analysis-only, structure-only, adapted output, or style-equivalent output instead of silent verbatim reuse.

## Mode-aware execution

Before non-trivial routing, classify the request into one mode and record the mode in evidence or handoff notes.

### Greenfield App Accelerator
Use for new apps, blank repos, MVPs, SaaS/product builds, or major product revamps.

- Always route new app/MVP/SaaS/product builds to `@artifact-planner` before implementation except explicitly tiny prototype-only work labeled `draft`/`prototype`.
- Optimize for the first usable vertical slice, not whole-app perfection.
- Explore 2-3 credible product/UX/architecture options, compare tradeoffs, then converge.
- Allow `PASS_FOR_SLICE` execution when whole-product decisions remain open but the selected slice avoids locking those decisions.
- Final claim should be `MVP slice complete` unless the whole app is actually finished and validated.

### Maintenance Stability Mode
Use for bugfixes, regressions, refactors, dependency updates, small features in existing apps, and incident follow-up.

- Maintenance work should not be forced through greenfield product thesis, 2-3 creative alternatives, or whole-app planning by default.
- Start with repro, regression test, targeted evidence, or clear failing behavior.
- Prefer the smallest safe diff and preserve existing architecture/UX unless the bug proves they are broken.
- Use `@explorer` for local facts, `@fixer` or the domain lane for implementation, and `@quality-gate` for material/risky changes.

### Creativity Fast Path
Use for explicit natural-language requests such as `brainstorm`, `explore options`, `generate ideas`, `sketch first`, `prototype cepat`, `draft UI`, `draft copy`, or `jangan terlalu production-grade dulu`.

- Opt-in and reversible, never default-on.
- Activated by explicit user intent, not by a dedicated command.
- For exploration output, not a production-bypass path.
- Label the result `draft`, `prototype`, or `exploration`.
- Record assumptions, confidence, and reversible scope.
- Exit Creativity Fast Path and return to normal routing when the user asks for permanent implementation, material source edits, commit, deploy, release, strong completion claims, or anything crossing a hard rail.
