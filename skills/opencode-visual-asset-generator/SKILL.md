---
name: opencode-visual-asset-generator
description: Standalone visual asset generation workflow for visual-asset-generator. Use for legal style-equivalent hero art, portraits, badges, mockups, avatars, thumbnails, product visuals, and rich backgrounds from an asset manifest.
---

# OpenCode Visual Asset Generator Skill

Use this to transform asset manifests into legal generation jobs and integration notes.

## Input contract

Require asset id, type, priority, target path, dimensions/aspect ratio, prompt, negative prompt, alt text, placement notes, legal notes, section title/description, semantic subject, palette notes, and background/output format when relevant.
For substantial UI/reference/image-heavy work, the manifest must also include an image generation decision, icon strategy, art direction, style board, reference traits, composition notes, quality_bar, reject_if, and explicit legal notes for each generated asset; otherwise return error instead of guessing. If the decision is `generate`, return executable jobs; if it is `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed`, return integration/validation notes instead of silently creating placeholders.

Prompts must be written like a professional art director, not as generic tags. Reject manifests that only say "modern tech dashboard", "futuristic", "cyberpunk", or "abstract UI" without domain-specific objects, composition, and meaning.

## Rules

- Never copy restricted/reference assets without license/proof.
- Preserve visual qualities as legal style-equivalent: palette, crop, mood, density, lighting, placement intent.
- Avoid readable text, watermarks, trademarks, and logo lookalikes.
- Prefer legal icon libraries for brand/tech marks.
- For functional UI icons, prefer existing icon libraries over generated substitutes.
- Require an explicit image-generation decision per section: `generate`, `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed`.
- Make prompts section-aware and concrete.
- Include a negative prompt that blocks generic AI aesthetics, placeholder visuals, fake text/logos, and copied reference assets when relevant.
- Do not use CSS-only or blank placeholders when imagery is a material part of the section.
- Keep generated sets cohesive, but ensure each asset has a unique differentiator so thumbnails and supporting visuals are not all the same-looking.
- Generated icons are only acceptable for decorative badges or non-logo imagery; do not use generation to replace a proper icon library for functional UI icons.
- Never hardcode device-specific absolute paths in manifests or generated artifacts.
- Derive absolute paths from the active workspace/project root when targeting an app.
- Keep the OpenCode config root separate from the target application root.
- For image asset jobs, pass the target app `project_root` explicitly and keep `target_path` relative to that root.

## Output

Return generated/failed metadata, paths, dimensions, prompts used, alt text, legal notes, warnings, and integration notes. Require integrated browser screenshots and designer review before visual parity claims.

## Open Design-style asset gate

For image-heavy UI, require a section-aware manifest before generation. Each job must include section title/description, semantic subject, placement notes, dimensions or aspect ratio, art direction, palette and lighting notes, target path relative to the target app root, alt/decorative strategy, legal note, and rejection criteria.

Use generated assets for rich hero art, portraits, thumbnails, avatars, mockups, atmospheric backgrounds, and decorative badges when licensed/provided assets are unavailable. Use icon libraries for functional symbols and brand marks. Do not generate logo lookalikes or substitute vague neon/abstract filler for meaningful section imagery.
