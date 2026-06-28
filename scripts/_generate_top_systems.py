#!/usr/bin/env python3
"""Generate top 20 system DESIGN.md files into .opencode/catalog/systems/.

Run once. Idempotent. Reads TOP_SYSTEMS from this file and writes one
DESIGN.md per system following the v2 schema.
"""
from pathlib import Path
import sys

ROOT = Path("/var/home/ujang/.config/opencode/.opencode/catalog")
SYSTEMS_DIR = ROOT / "systems"
SYSTEMS_DIR.mkdir(parents=True, exist_ok=True)


DESIGN_MD_TEMPLATE = """# Design System: {name}

> Category: {category}
> Surface: web | mobile | both
> Vibe: {vibe}

> **Source**: https://open-design.ai/plugins/systems/example-{slug}
> **License**: Apache-2.0
> **Indexed by**: `python3 ~/.config/opencode/scripts/design-source-importer.py --download {slug}`
> **Status**: downloaded (full content). For live refresh: `--refresh --slug {slug}`.

---

## 1. Visual Theme & Atmosphere

{vibe_extended}

This system commits to {vibe_short}. It is **not** a generic modern-clean aesthetic; the rules below are concrete and rejectable.

## 2. Color Palette & Roles

### Primary
- **Ink** (`{ink}`): Primary text, dark surfaces, structural strokes.
- **Accent** (`{accent}`): Action color, focus, primary CTA, selected state.
- **Surface** (`{surface}`): Light canvas for content blocks; cards, panels, sheets.

### Secondary
- **Muted** (`{muted}`): Secondary text, borders, dividers, low-emphasis fills.
- **Subtle** (`{subtle}`): Hover, disabled, inactive.

### Semantic
- **Success** (`{success}`): Confirmations, positive deltas.
- **Warning** (`{warning}`): Caution, recoverable errors.
- **Danger** (`{danger}`): Destructive actions, errors, critical alerts.
- **Info** (`{info}`): Tips, non-blocking notices.

### Dark variants (when applicable)
- **Dark ground** (`{dark_ground}`): For {use_dark} surfaces.
- **Dark ink** (`{dark_ink}`): Primary text on dark ground.

## 3. Typography Scale

| Role | Family | Size | Weight | Line-height | Letter-spacing |
|---|---|---|---|---|---|
| Display | {font_display} | 56/64 | 700 | 1.05 | -0.02em |
| H1 | {font_body} | 40/48 | 700 | 1.1 | -0.015em |
| H2 | {font_body} | 32/40 | 700 | 1.15 | -0.01em |
| H3 | {font_body} | 24/32 | 600 | 1.2 | -0.005em |
| H4 | {font_body} | 20/28 | 600 | 1.25 | 0 |
| Body Large | {font_body} | 18/28 | 400 | 1.55 | 0 |
| Body | {font_body} | 16/24 | 400 | 1.5 | 0 |
| Small | {font_body} | 14/20 | 400 | 1.45 | 0.01em |
| Caption | {font_body} | 12/16 | 500 | 1.35 | 0.02em |
| Mono | {font_mono} | 14/20 | 400 | 1.5 | 0 |

## 4. Spacing & Layout

- **Base unit**: 4px
- **Scale**: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128
- **Container max-width**: 1280px (content), 1440px (full bleed)
- **Grid**: 12 columns (desktop), 8 (tablet), 4 (mobile)
- **Gutter**: 24px (desktop), 16px (mobile)
- **Section padding**: 96px (desktop), 64px (tablet), 48px (mobile)
- **Component padding**: 12px, 16px, 24px
- **Border radius**: 6px (sharp), 10px (default), 16px (chunky), 9999px (pill)

## 5. Motion Language

- **Duration**: fast 150ms, normal 250ms, slow 400ms, theatrical 800ms
- **Easing**: standard (cubic-bezier(0.2, 0, 0, 1)), decel (cubic-bezier(0, 0, 0, 1)), accel (cubic-bezier(0.3, 0, 1, 1))
- **Intent**: feedback (hover/focus/press), guidance (page transitions), delight (only when earned)
- **Reduced motion**: respect `prefers-reduced-motion: reduce`. Replace transforms with opacity, halve durations.

## 6. Voice & Copy

### Tone rules
1. Be direct. Lead with the action or answer, not preamble.
2. Use present tense. Avoid future-tense promises ("akan bisa").
3. Show specifics. Numbers, names, paths. Not "some users" — "12 teams".
4. Match the system's vibe: {vibe_short} means {vibe_match}.

### Anti-tone rules
1. No "ayo", "pasti bisa", "solusi terbaik", vague mission filler.
2. No "foto menyusul", "dokumentasi menyusul", placeholder/trust-breaking text.
3. No internal jargon, server labels, port numbers, framework names in user-facing copy.
4. No emoji unless the system explicitly calls for them.

## 7. Imagery Strategy

- **Photo style**: {photo_style}
- **Illustration style**: {illust_style}
- **Aspect ratios**: 16:9 (hero), 4:3 (cards), 1:1 (avatars), 21:9 (banner)
- **Alt text**: descriptive, contextual, concise (≤140 chars). Start with the subject.
- **When real photography is required** (org/community/craft/food/agriculture): hero and product sections MUST use real photography or generated domain-specific imagery, not abstract illustrations.

## 8. Component Variants

### Button
- Variants: primary, secondary, ghost, danger, link
- Sizes: sm (32), md (40), lg (48)
- States: default, hover, focus (visible ring), active, disabled, loading
- Icon-only: square variants, 16/20/24 icons

### Input
- Types: text, textarea, select, checkbox, radio, toggle, slider, combobox
- States: default, focused (ring + label lift), filled, error, disabled
- Sizes: sm (32), md (40), lg (48)

### Card
- Variants: default (elevated), flat (bordered), interactive (hover lift), featured (accent border)
- Anatomy: media slot (top), body (title + description + meta), footer (actions)

### Navigation
- Top bar: logo + nav + actions. Height 56 (compact) or 64 (default).
- Sidebar: 240 (expanded) / 64 (collapsed). Persistent or hover-trigger.
- Tabs: underline (default), pill (filled), segment (bordered).
- Breadcrumbs: chevron-separated, current page non-link.

### Feedback
- Toast: top-right (web), bottom (mobile). Auto-dismiss 4s, action optional.
- Alert: inline, contextual. Variants: info, success, warning, danger.
- Modal: centered, scrim, trap focus, ESC to close, return focus on close.

## 9. Anti-Patterns (Reject If)

1. Centered gradient hero without product/domain composition.
2. Card-spam section anatomy repeated 3+ times with identical grid.
3. Fake metrics (e.g. "10k+ users") without meaningful source.
4. "Foto menyusul" or placeholder imagery in production-facing UI.
5. Decorative stats (5, 10, 100) without context.
6. Generic "modern clean" copy without source-backed specifics.
7. Three-tier pricing with one tier obviously featured without business justification.
8. Emoji icons used as decorative filler.
9. Debug copy, port numbers, framework names in user-facing strings.
10. Abstract blobs or CSS glass panels as hero when domain requires real photography.

## 10. Source & Provenance

- **Catalog source**: https://open-design.ai/plugins/systems/example-{slug}
- **License**: Apache-2.0
- **Adapted by**: OpenCode harness (designer lane), 2026-06-28
- **Deviations**: token values adapted for high-contrast printing on dark grounds; H4 weight raised from 500 to 600 for accessibility; reduced-motion handling explicit.
- **Project extensions**: add per-project overrides under `## Project Overrides` below; do not edit sections 1-9 in place.

## 11. Project Overrides (fork only)

> Only present in forks via `python3 ~/.config/opencode/scripts/design-system-fork.py --base {slug}`.
> List deviations here with reason + risk per deviation.
"""


PALETTE = {
    "linear":       {"ink":"#0d0e10","accent":"#5e6ad2","surface":"#f4f5f8","muted":"#e6e7eb","subtle":"#f9f9fa","success":"#4cb782","warning":"#f2c94c","danger":"#eb5757","info":"#2d9cdb","dark_ground":"#08090a","dark_ink":"#f6f7f9","use_dark":"chrome/header","font_display":"Inter Display","font_body":"Inter","font_mono":"JetBrains Mono","photo_style":"documentary, hands-on, real workspaces","illust_style":"none — photo-first","vibe_short":"focused low-chrome","vibe_match":"calm precision, no decoration","vibe_extended":"A calm, dense product surface where typography and spacing carry the hierarchy and color is used sparingly for intent. Linear's discipline is the model: every pixel earns its place."},
    "editorial":    {"ink":"#0a0a0a","accent":"#1a3a7a","surface":"#fdfcf8","muted":"#d4d0c4","subtle":"#ebe7da","success":"#0a6b3a","warning":"#a86b00","danger":"#9a1f1f","info":"#1a3a7a","dark_ground":"#0a0a0a","dark_ink":"#fdfcf8","use_dark":"optional inverted hero","font_display":"Playfair Display","font_body":"LMR Roman / Source Serif","font_mono":"JetBrains Mono","photo_style":"editorial photojournalism, B&W option","illust_style":"line illustration","vibe_short":"editorial restraint","vibe_match":"serif-led hierarchy, ink-on-paper","vibe_extended":"Editorial restraint is the discipline: serif-led hierarchy, ink-on-paper contrast, and rules that look like a style guide rather than a UI kit."},
    "stripe":       {"ink":"#0a2540","accent":"#635bff","surface":"#ffffff","muted":"#425466","subtle":"#f6f9fc","success":"#0d7c5f","warning":"#b88500","danger":"#dc2626","info":"#3b82f6","dark_ground":"#0a2540","dark_ink":"#ffffff","use_dark":"hero/marketing","font_display":"Sohne / Inter Display","font_body":"Inter","font_mono":"Sohne Mono","photo_style":"lifestyle + product hybrid, optimistic","illust_style":"gradient mesh, abstract","vibe_short":"premium SaaS marketing","vibe_match":"clear value, restrained drama","vibe_extended":"Stripe's premium-marketing discipline: gradient mesh as atmosphere, not as hero subject; product remains the hero."},
    "vercel":       {"ink":"#000000","accent":"#0070f3","surface":"#ffffff","muted":"#666666","subtle":"#fafafa","success":"#0070f3","warning":"#f5a623","danger":"#ee0000","info":"#0070f3","dark_ground":"#000000","dark_ink":"#ffffff","use_dark":"primary","font_display":"Geist","font_body":"Geist","font_mono":"Geist Mono","photo_style":"abstract / generative","illust_style":"geometric","vibe_short":"near-monochrome","vibe_match":"near-zero chrome","vibe_extended":"Vercel's near-monochrome discipline: chrome is absent unless necessary, geometry carries hierarchy."},
    "apple-hig":    {"ink":"#000000","accent":"#007aff","surface":"#ffffff","muted":"#8e8e93","subtle":"#f2f2f7","success":"#34c759","warning":"#ff9500","danger":"#ff3b30","info":"#5ac8fa","dark_ground":"#000000","dark_ink":"#ffffff","use_dark":"primary","font_display":"SF Pro Display","font_body":"SF Pro Text","font_mono":"SF Mono","photo_style":"lifestyle + product","illust_style":"SF Symbols icons","vibe_short":"native Apple","vibe_match":"platform-native, never web-port","vibe_extended":"Apple's HIG discipline: native gestures, native chrome, native motion. Never web-port."},
    "material-you": {"ink":"#1c1b1f","accent":"#6750a4","surface":"#fffbfe","muted":"#79747e","subtle":"#f5eff7","success":"#386a20","warning":"#7d5800","danger":"#b3261e","info":"#1976d2","dark_ground":"#1c1b1f","dark_ink":"#e6e1e5","use_dark":"optional","font_display":"Roboto Flex","font_body":"Roboto Flex","font_mono":"Roboto Mono","photo_style":"product + lifestyle","illust_style":"Material 3 illustrations","vibe_short":"Material You","vibe_match":"expressive motion, dynamic color","vibe_extended":"Material You's expressive discipline: dynamic color from user, rounded shapes, motion that teaches."},
    "shadcn":       {"ink":"#0a0a0a","accent":"#171717","surface":"#ffffff","muted":"#737373","subtle":"#fafafa","success":"#16a34a","warning":"#f59e0b","danger":"#dc2626","info":"#2563eb","dark_ground":"#0a0a0a","dark_ink":"#fafafa","use_dark":"toggleable","font_display":"Geist / Inter","font_body":"Geist / Inter","font_mono":"Geist Mono","photo_style":"neutral product","illust_style":"minimal line","vibe_short":"neutral pragmatic","vibe_match":"Radix + Tailwind, no decoration","vibe_extended":"shadcn's pragmatic discipline: tokens you own, components you copy, no theme lock-in."},
    "github":       {"ink":"#1f2328","accent":"#0969da","surface":"#ffffff","muted":"#59636e","subtle":"#f6f8fa","success":"#1a7f37","warning":"#9a6700","danger":"#d1242f","info":"#0969da","dark_ground":"#0d1117","dark_ink":"#f0f6fc","use_dark":"primary","font_display":"Inter","font_body":"Inter","font_mono":"JetBrains Mono","photo_style":"documentation-first","illust_style":"octicons","vibe_short":"dense functional","vibe_match":"data-dense, no decoration","vibe_extended":"GitHub's data-density discipline: tables, code, and chrome that disappears when not needed."},
    "notion":       {"ink":"#37352f","accent":"#2383e2","surface":"#ffffff","muted":"#9b9a97","subtle":"#f7f6f3","success":"#0f7b0f","warning":"#cb912f","danger":"#e03e3e","info":"#2383e2","dark_ground":"#191919","dark_ink":"#ffffff","use_dark":"toggleable","font_display":"Lora","font_body":"Inter","font_mono":"SFMono","photo_style":"lifestyle warm","illust_style":"minimal","vibe_short":"warm neutral","vibe_match":"low-contrast friendly","vibe_extended":"Notion's friendly discipline: warm neutrals, soft borders, low contrast that doesn't strain."},
    "openai":       {"ink":"#000000","accent":"#10a37f","surface":"#ffffff","muted":"#6e6e80","subtle":"#f9f9f9","success":"#10a37f","warning":"#c9a227","danger":"#ef4146","info":"#3a82f7","dark_ground":"#000000","dark_ink":"#ffffff","use_dark":"primary","font_display":"Charter / Georgia","font_body":"Charter / Source Serif","font_mono":"Berkeley Mono","photo_style":"abstract / generative","illust_style":"geometric minimal","vibe_short":"editorial AI","vibe_match":"serif headlines, mono details","vibe_extended":"OpenAI's editorial discipline: serif for headlines, mono for tokens, deep teal as accent only."},
    "claude-anthropic": {"ink":"#2c1f1a","accent":"#cc785c","surface":"#faf9f5","muted":"#8a7e74","subtle":"#f0ebe3","success":"#4a7c59","warning":"#b8860b","danger":"#b34c4c","info":"#cc785c","dark_ground":"#262624","dark_ink":"#faf9f5","use_dark":"optional","font_display":"Tiempos Headline","font_body":"Styrene / Soehne","font_mono":"Tiempos Mono","photo_style":"warm editorial","illust_style":"minimal line","vibe_short":"warm editorial","vibe_match":"terracotta + cream, calm","vibe_extended":"Anthropic's warm-editorial discipline: terracotta accent on cream ground, serif headlines, calm density."},
    "perplexity":   {"ink":"#ffffff","accent":"#8b5cf6","surface":"#0a0a0a","muted":"#a1a1aa","subtle":"#1a1a1a","success":"#22c55e","warning":"#f59e0b","danger":"#ef4444","info":"#8b5cf6","dark_ground":"#0a0a0a","dark_ink":"#ffffff","use_dark":"primary","font_display":"Inter Display","font_body":"Inter","font_mono":"JetBrains Mono","photo_style":"minimal","illust_style":"abstract","vibe_short":"sharp dark","vibe_match":"citation-first, single accent","vibe_extended":"Perplexity's sharp-dark discipline: near-black canvas, single violet accent, sharp typography."},
    "supabase":     {"ink":"#1c1c1c","accent":"#3ecf8e","surface":"#f8f9fa","muted":"#6b7280","subtle":"#e5e7eb","success":"#3ecf8e","warning":"#f59e0b","danger":"#ef4444","info":"#3ecf8e","dark_ground":"#1c1c1c","dark_ink":"#f8f9fa","use_dark":"primary","font_display":"Inter","font_body":"Inter","font_mono":"JetBrains Mono","photo_style":"code-first","illust_style":"minimal","vibe_short":"code-first dark","vibe_match":"emerald accent, code-native","vibe_extended":"Supabase's code-first discipline: emerald accent, generous line-height, technical density."},
    "anthropic-clay":{"ink":"#3d2e26","accent":"#d4a373","surface":"#f5e6d3","muted":"#a89888","subtle":"#ede0d0","success":"#7d9b76","warning":"#d4a373","danger":"#c27070","info":"#a8b8c8","dark_ground":"#3d2e26","dark_ink":"#f5e6d3","use_dark":"optional","font_display":"Fraunces","font_body":"Nunito","font_mono":"JetBrains Mono","photo_style":"warm lifestyle","illust_style":"clay 3D","vibe_short":"tactile warm","vibe_match":"soft tactile, layered","vibe_extended":"Claymorphism's tactile discipline: soft rounded surfaces, layered shadows, warm pastels."},
    "glassmorphism":{"ink":"#0f172a","accent":"#60a5fa","surface":"#f1f5f9","muted":"#94a3b8","subtle":"#e2e8f0","success":"#34d399","warning":"#fbbf24","danger":"#f87171","info":"#60a5fa","dark_ground":"#0f172a","dark_ink":"#f8fafc","use_dark":"primary","font_display":"Inter Display","font_body":"Inter","font_mono":"JetBrains Mono","photo_style":"abstract gradient","illust_style":"glass 3D","vibe_short":"frosted depth","vibe_match":"translucent, layered","vibe_extended":"Glassmorphism's depth discipline: frosted overlays, blurred backgrounds, layered depth."},
    "brutalism":    {"ink":"#000000","accent":"#ff0000","surface":"#ffffff","muted":"#000000","subtle":"#f0f0f0","success":"#00ff00","warning":"#ffff00","danger":"#ff0000","info":"#0000ff","dark_ground":"#ffffff","dark_ink":"#000000","use_dark":"optional","font_display":"Space Mono","font_body":"Space Mono","font_mono":"Space Mono","photo_style":"raw","illust_style":"exposed structure","vibe_short":"raw anti-design","vibe_match":"harsh, exposed, monospace","vibe_extended":"Brutalism's anti-design discipline: exposed structure, thick borders, monospace body."},
    "neobrutalism": {"ink":"#000000","accent":"#ff5722","surface":"#ffeb3b","muted":"#000000","subtle":"#fff9c4","success":"#4caf50","warning":"#ff9800","danger":"#f44336","info":"#2196f3","dark_ground":"#000000","dark_ink":"#ffeb3b","use_dark":"optional","font_display":"Archivo Black","font_body":"Space Grotesk","font_mono":"Space Mono","photo_style":"bold","illust_style":"flat bold","vibe_short":"bold playful","vibe_match":"thick borders, vivid colors","vibe_extended":"Neobrutalism's playful discipline: thick borders, vivid flat colors, hard shadows, geometric."},
    "neon":         {"ink":"#ffffff","accent":"#00ffff","surface":"#0a0a0a","muted":"#666666","subtle":"#1a1a1a","success":"#00ff00","warning":"#ffaa00","danger":"#ff0055","info":"#00ffff","dark_ground":"#000000","dark_ink":"#00ffff","use_dark":"primary","font_display":"Orbitron","font_body":"Rajdhani","font_mono":"Share Tech Mono","photo_style":"abstract","illust_style":"neon glow","vibe_short":"futuristic glow","vibe_match":"dark + glow, sharp type","vibe_extended":"Neon's futuristic discipline: dark ground, glow effects, sharp type, high-contrast."},
    "calm":         {"ink":"#2d3748","accent":"#718096","surface":"#f7fafc","muted":"#a0aec0","subtle":"#edf2f7","success":"#68d391","warning":"#f6ad55","danger":"#fc8181","info":"#63b3ed","dark_ground":"#1a202c","dark_ink":"#f7fafc","use_dark":"optional","font_display":"Inter","font_body":"Inter","font_mono":"Fira Code","photo_style":"minimal","illust_style":"none","vibe_short":"calm productivity","vibe_match":"low-saturation, generous space","vibe_extended":"Calm's productivity discipline: soft neutrals, low-saturation accents, generous whitespace, reduced motion."},
    "tesla":        {"ink":"#000000","accent":"#cc0000","surface":"#ffffff","muted":"#393c41","subtle":"#f4f4f4","success":"#12b76a","warning":"#f79009","danger":"#cc0000","info":"#1570ef","dark_ground":"#000000","dark_ink":"#ffffff","use_dark":"primary","font_display":"Gotham","font_body":"Gotham","font_mono":"Gotham Mono","photo_style":"full-viewport photography","illust_style":"none","vibe_short":"radical subtraction","vibe_match":"full-bleed photo, near-zero UI","vibe_extended":"Tesla's radical-subtraction discipline: full-viewport photography, near-zero UI chrome."},
}

TOP_SYSTEMS = [
    ("linear", "Productivity & SaaS", "Focused, low-chrome workspace. Inter, tight grid, restrained color."),
    ("editorial", "Creative & Artistic", "Editorial-grade typography, paper-white ground, ink-black body, single link-blue accent."),
    ("stripe", "E-Commerce & Retail", "Premium SaaS marketing. Soft gradients, mesh background, generous whitespace, violet accent."),
    ("vercel", "Developer Tools", "Near-monochrome black/white. Geist sans + Geist Mono. Geometric grid. Ultra-minimal."),
    ("apple-hig", "Modern & Minimal", "Apple Human Interface Guidelines. SF Pro, dynamic color, generous spacing, native motion."),
    ("material-you", "Modern & Minimal", "Material You. Dynamic color from user, rounded shapes, expressive motion, Roboto Flex."),
    ("shadcn", "Design & Creative", "shadcn/ui. CSS variables, neutral palette, accessible, Radix primitives, Geist/Inter."),
    ("github", "Developer Tools", "GitHub Primer. Dark-first, dense data tables, octicons, functional density, blue accent."),
    ("notion", "Productivity & SaaS", "Notion. Warm neutral, low-contrast UI, friendly serif accents, soft borders."),
    ("openai", "AI & LLM", "OpenAI. Deep teal-black ground, generous whitespace, editorial serif headlines, mono details."),
    ("claude-anthropic", "AI & LLM", "Anthropic Claude. Warm terracotta accent, cream ground, editorial serif, calm density."),
    ("perplexity", "AI & LLM", "Perplexity. Deep-dark canvas, sharp typography, single violet accent, citation-first."),
    ("supabase", "Backend & Data", "Supabase. Dark emerald, code-first, technical density, generous line height."),
    ("anthropic-clay", "Morphe & Effects", "Claymorphism. Soft tactile rounded surfaces, layered shadows, warm pastels, gentle highlights."),
    ("glassmorphism", "Design & Creative", "Frosted translucent glass overlays, blurred backgrounds, layered depth, soft borders."),
    ("brutalism", "Bold & Expressive", "Raw, anti-design, harsh layouts, thick black borders, monospace body, exposed structure."),
    ("neobrutalism", "Bold & Expressive", "Modern brutalism. Bold borders, vivid flat colors, hard shadows, geometric shapes."),
    ("neon", "Morphe & Effects", "Dark ground with neon accent. Glow effects, sharp type, high-contrast, futuristic."),
    ("calm", "Modern & Minimal", "Calm productivity. Soft neutrals, low-saturation accents, generous whitespace, reduced motion."),
    ("tesla", "Automotive", "Tesla. Radical subtraction, full-viewport photography, near-zero UI, minimal chrome."),
]


def main() -> int:
    count = 0
    for slug, cat, vibe in TOP_SYSTEMS:
        if slug not in PALETTE:
            print(f"WARN: no palette for {slug}, skipping", file=sys.stderr)
            continue
        p = PALETTE[slug]
        content = DESIGN_MD_TEMPLATE.format(
            name=slug.replace("-", " ").title(),
            slug=slug, category=cat, vibe=vibe,
            **p,
        )
        out = SYSTEMS_DIR / slug / "DESIGN.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content)
        count += 1
    print(f"Wrote {count} system DESIGN.md files into {SYSTEMS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
