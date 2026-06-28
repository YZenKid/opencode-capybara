---
name: opencode-visual-asset-generator
description: Standalone visual asset generation workflow for visual-asset-generator. Use for style-equivalent fallback hero art, portraits, badges, mockups, avatars, thumbnails, product visuals, and rich backgrounds from an asset manifest.
---

# OpenCode Visual Asset Generator Skill

Use this to transform asset manifests into generation jobs and integration notes, including direct-reuse awareness when the user has already approved a source.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Input contract

Require asset id, type, priority, target path, dimensions/aspect ratio, prompt, negative prompt, alt text, placement notes, legal notes, section title/description, semantic subject, palette notes, and background/output format when relevant.

Manifest-level taste fields:

- `design_read`
- `DESIGN_VARIANCE`
- `MOTION_INTENSITY`
- `VISUAL_DENSITY`
- `quality_bar`
- `reject_if`
- `keep`, `change`, `do_not_copy` for reference-inspired work

For substantial UI/reference/image-heavy work, the manifest must also include an image generation decision, icon strategy, art direction, style board, reference traits, composition notes, quality_bar, reject_if, and explicit legal notes for each generated asset; otherwise return error instead of guessing. If the decision is `generate`, return executable jobs; if it is `use-provided-assets`, `licensed-existing-assets`, or `no-generation-needed`, return integration/validation notes instead of silently creating placeholders.

Prompts must be written like a professional art director, not as generic tags. Reject manifests that only say "modern tech dashboard", "futuristic", "cyberpunk", or "abstract UI" without domain-specific objects, composition, and meaning.

## Trigger / skip

- Trigger: image-heavy UI work, missing licensed/provided assets, section-aware generation jobs, style-equivalent fallback needs, or orchestrator/designer asset manifest execution.
- Skip: design critique -> `@designer`; observable image description -> `@visual-context-extractor`; implementation/source edits -> `@fixer`; legal approval decisions -> `user` or `@quality-gate` after implementation.

## Material Aesthetic Asset Gate

For explicit material aesthetics in hero/image-heavy work, require tactile/product-specific/domain-specific prompts. Translate styles such as `claymorphism + glassmorphism` into material behavior, subject matter, props/environment, composition, lighting, texture, palette, and reject_if. CSS abstract filler, floating UI cards, generic glass/neon panels, and style labels alone are not sufficient when imagery matters.

## Rules

- Open Design influence: use `taste-skill` for Design Read/dials/anti-slop, `reference-design-contract` for `keep/change/do_not_copy`, and `frontend-design` for production-grade, section-meaningful visuals.
- Never silently copy restricted/reference assets without license/proof.
- If the user explicitly directs reuse of provided/public/user-approved assets, record the source, permission/license status when known, and risk instead of generating a substitute by default.
- Do not generate style-equivalent fallback when direct asset reuse is explicitly user-approved and safe; generate only for unavailable, unlicensed, restricted, or unsafe-to-copy assets.
- Preserve visual qualities as style-equivalent fallback when generation is needed: palette, crop, mood, density, lighting, placement intent.
- Avoid readable text, watermarks, trademarks, and logo lookalikes.
- Prefer legal icon libraries for brand/tech marks.
- For functional UI icons, prefer existing icon libraries over generated substitutes.
- Require an explicit image-generation decision per section: `generate`, `use-provided-assets`, `licensed-existing-assets`, `no-generation-needed`, or `direct-reuse-user-approved`.
- Make prompts section-aware and concrete.
- For clay/glass or similar material requests, include tactile surface details plus real product/domain composition; reject abstract CSS filler where the section needs meaningful imagery.
- Include a negative prompt that blocks generic AI aesthetics, placeholder visuals, fake text/logos, and copied reference assets when relevant.
- Do not use CSS-only or blank placeholders when imagery is a material part of the section.
- Keep generated sets cohesive, but ensure each asset has a unique differentiator so thumbnails and supporting visuals are not all the same-looking.
- Generated icons are only acceptable for decorative badges or non-logo imagery; do not use generation to replace a proper icon library for functional UI icons.
- Never hardcode device-specific absolute paths in manifests or generated artifacts.
- Derive absolute paths from the active workspace/project root when targeting an app.
- Keep the OpenCode config root separate from the target application root.
- For image asset jobs, pass the target app `project_root` explicitly and keep `target_path` relative to that root.

## Execution provider

Use 9Router image generation for executable image asset jobs.
Preferred MCP tool: `generate_image_asset` from `9router`.

Do not call raw image providers directly. Route image generation through 9Router so model/account/fallback policy stays centralized.

### 9router MCP generation contract

Before calling `generate_image_asset` or `generate_image_assets_batch`, verify each job has:

- explicit `project_root` for target app and relative `target_path`
- section-aware `prompt` with subject, composition, palette/light, medium, camera/crop/perspective, texture/material, brand/domain specificity
- `negative_prompt` blocking fake text, logos, watermarks, copied reference assets, generic cyberpunk/neon, placeholder UI, uncanny hands/faces when relevant
- `width`, `height`, `format`, `output_format`, `background`, `quality`
- `alt` and `legal_note`
- `quality_bar`, `reject_if`, and integration notes available in manifest/handoff

Generation flow: brief -> `design_read` -> dials -> manifest/art direction -> 9router generation -> integration evidence -> designer/quality-gate review. Do not claim `generated` unless files were actually created by tool output.

## Pre-flight Skill & MCP Discovery
Before the first substantial answer, diagnosis, route, or implementation step on non-trivial work:
- Name the skill explicitly (`Skill I'm using: ...`).
- Decide MCP applicability explicitly (`MCPs I'm using: ...`, `What I'm checking first: ...`).
- If an MCP is obviously applicable, use it or record a concrete skip reason. Silent skip is a defect.
- At final summary time, name one concrete thing this skill changed about execution. Loaded-but-unused skill is a process defect.

ponytail: This is a behavioral contract. Use `scripts/session-trace-audit.py` as the advisory checker until transcript hooks become first-class.

## Workflow

1. Validate manifest completeness, legal notes, and generation decision.
2. Reject under-specified art direction instead of inventing generic prompts.
3. Normalize target paths, dimensions, output format, and background policy.
4. Build section-aware prompts and negative prompts with cohesive set direction.
5. Run generation through 9Router only when tooling and manifest are ready; otherwise return executable jobs plus integration notes.
6. Return asset metadata, warnings, and required downstream validation notes.

## Quality checklist
- [ ] Manifest completeness and legal notes validated.
- [ ] Generation decision is explicit per asset or section.
- [ ] Prompts are section-aware, concrete, and non-generic.
- [ ] Negative prompts block copied references, fake text/logos, and generic AI filler.
- [ ] Output paths stay relative to `project_root`.
- [ ] Direct reuse is preferred when user-approved and safe.
- [ ] `generated` is claimed only when real image files were actually produced.
- [ ] Integration notes include dimensions, alt behavior, and validation follow-up.

## Anti-patterns
- Generating assets when user-approved direct reuse is already safe.
- Writing vague prompts like "modern tech dashboard" with no subject or composition.
- Replacing proper icon libraries with generated logo lookalikes.
- Claiming `generated` without real files or concrete output paths.
- Silently substituting CSS placeholders for required imagery.

## Output example

```json
{
  "status": "ready_for_generation",
  "summary": "Prepared 2 executable image generation jobs for hero and testimonial assets.",
  "project_root": "/workspace/app",
  "asset_dir": "public/assets/generated",
  "jobs": [
    {
      "id": "hero-portrait",
      "type": "portrait",
      "priority": "required",
      "target_path": "public/assets/generated/hero-portrait.webp",
      "width": 1024,
      "height": 1024,
      "format": "webp",
      "output_format": "webp",
      "background": "transparent",
      "prompt": "Three-quarter portrait of a founder in a soft studio scene with tactile glass desk objects and warm rim light, editorial product-photography feel.",
      "negative_prompt": "generic tech dashboard, readable text, logos, watermark, copied reference, uncanny face",
      "alt": "Founder portrait for hero section",
      "placement_notes": "Above fold hero visual, left of headline",
      "legal_note": "Generate style-equivalent fallback only; do not copy reference image."
    }
  ],
  "generated": [],
  "failed": [],
  "warnings": ["No image generation tool available in this subagent session."],
  "integration_notes": [
    "Set explicit width/height to avoid CLS.",
    "Validate integrated screenshots with browser capture before parity claims."
  ]
}
```

## Output

Return generated/failed metadata, paths, dimensions, prompts used, alt text, legal notes, warnings, and integration notes. Require integrated browser screenshots and designer review before visual parity claims.

## Escalation

- Escalate to `@designer` when manifest lacks sufficient style grammar, art direction, or section meaning.
- Escalate to `user` when asset reuse/license approval is unclear.
- Escalate to `@quality-gate` after integration when strong visual parity/readiness claims are made.

## Smart asset gate

For image-heavy UI, require a section-aware manifest before generation. Each job must include section title/description, semantic subject, placement notes, dimensions or aspect ratio, art direction, palette and lighting notes, target path relative to the target app root, alt/decorative strategy, legal note, and rejection criteria.

Use generated assets for rich hero art, portraits, thumbnails, avatars, mockups, atmospheric backgrounds, and decorative badges when licensed/provided assets are unavailable. Use icon libraries for functional symbols and brand marks. Do not generate logo lookalikes or substitute vague neon/abstract filler for meaningful section imagery.
## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
