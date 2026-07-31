# UI, Reference, and Asset Policy

Read this before UI direction, visual parity, image-heavy work, or asset generation.

## Reference order

1. Project-local `DESIGN.md`.
2. `design-system/DESIGN.md` or documented equivalent.
3. Open Design catalog selection or explicit first-principles rationale.

## Reference Pack Requirement

- Greenfield, UI-heavy, or substantial visual work needs a reference pack with at least 3 screenshots or URLs, or explicit first-principles rationale.
- Reference pack must cover visual direction, layout, component patterns, asset/image style, and motion style.

## Anti-Generic Landing Page Hard Fail Rules

- Centered gradient hero without product/domain composition is a fail.
- Fake metrics, emoji icons, placeholder imagery, card spam, vague neon blobs, blank image frames, and lorem copy are fails.
- Missing image strategy, motion motivation, or reduced-motion support is a fail.

## Animation and capture

- Animation System Gate: reuse existing system first, then CSS/native primitives, then existing dependency, then justified new dependency.
- Playwright/browser capture: wait, stabilize, scroll, settle, then screenshot.
- Visual evidence needs reference, current, and final captures when parity matters.

## Asset handling

- Image-heavy work needs an explicit image generation decision and direct reuse inventory.
- `@visual-asset-generator` is used for image-heavy legal replacements and style-equivalent fallback only when direct reuse is not requested, not allowed, unavailable, or unsafe.

## Trigger phrases to preserve

- See `DESIGN.md`
- Reference Pack Requirement
- Anti-Generic Landing Page Hard Fail Rules
- Animation System Gate
- Playwright/browser capture
- visual-asset-generator
- visual parity evidence
- first-principles rationale
