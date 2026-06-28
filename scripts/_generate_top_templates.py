#!/usr/bin/env python3
"""Generate top 20 template files into .opencode/catalog/templates/.

Run once. Idempotent. Reads TEMPLATES from this file.
"""
from pathlib import Path
import sys

ROOT = Path("/var/home/ujang/.config/opencode/.opencode/catalog")
TEMPLATES_DIR = ROOT / "templates"
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)


TEMPLATE_MD = """# Template: {name}

> Category: {category_label}
> Source: https://open-design.ai/plugins/templates/{slug}
> License: Apache-2.0
> Indexed by: `python3 ~/.config/opencode/scripts/design-source-importer.py --download-template {slug}`
> Status: indexed (full prompt). Download: `--download-template {slug}`.

---

## What this template is

{description}

## When to use

{when}

## Recommended paired design systems

{paired}

## Anatomy (sections / components / motion)

{anatomy}

## Reuse notes

- Adapt the anatomy for the target project; keep the section order unless you have a reason.
- Cite this template in `catalog-decision.md` and in the visual contract's `catalog_citation.template_pattern` field.
- For deviations, list in `deviation_audit` with reason + risk.

## Source & Provenance

- **Catalog source**: https://open-design.ai/plugins/templates/{slug}
- **License**: Apache-2.0
- **Tags**: {tags}
"""


CATEGORY_LABEL = {
    "deck": "Slides",
    "image": "Image",
    "video": "Video",
    "hyperframes": "HyperFrames",
    "live": "Live Artifact",
    "audio": "Audio",
    "prototype": "Prototype",
}


def cat_for(slug):
    if "academic" in slug:
        return "deck"
    deck_keys = ("pitch", "launch", "update", "talk", "review", "enablement", "town-hall")
    if any(k in slug for k in deck_keys):
        return "deck"
    if slug.startswith("image-"):
        return "image"
    if slug.startswith("video-"):
        return "video"
    if slug.startswith("live-"):
        return "live"
    return "prototype"


TEMPLATES = [
    ("example-aerocore", "Cinematic Aerospace Engine Landing",
     "Premium scroll-cinematic aerospace propulsion marketing site: blue-to-warm-white gradient hero with parallax wordmark and engine still, mission thumbnail that grows into fullscreen sticky video, pinned tabbed showcase, bento capabilities grid with looping video cards, animated dark stats chart, horizontal video-story rail, starfield footer.",
     ["aerospace", "cinematic", "bento", "video-led", "marketing"]),
    ("example-acreage-farming", "Acreage - Precision Farming",
     "Premium precision-farming landing: dark/light alternating sections, fullscreen hero video background, animated stats grid, infinite logo marquee, image-backed service cards.",
     ["agriculture", "marketing", "video", "alternating"]),
    ("example-3d-creator-portfolio", "3D Creator Portfolio",
     "Dark, premium 3D-creator portfolio landing: full-viewport hero with gradient-text headline and mouse-following magnetic 3D portrait, scroll-driven horizontal image marquee, About with corner 3D decorations, white Services list, sticky-stacking project cards.",
     ["portfolio", "3d", "dark", "marketing"]),
    ("example-ai-designer-portfolio", "AI Designer Portfolio",
     "Editorial-grade AI designer portfolio: serif headlines, case study grid, generative artwork hero, dark mode primary.",
     ["portfolio", "ai", "editorial", "dark"]),
    ("example-hps-academic-paper", "Academic Paper Deck",
     "LaTeX-paper deck: paper-white ground, all-serif (Latin Modern Roman + Playfair Display fallback), ink-black body, link-blue underlined citations, zero radius, double-rule title, numbered Figure/Table captions, booktabs three-line tables.",
     ["deck", "academic", "editorial", "all-serif"]),
    ("example-brand-pitch", "Brand Pitch Deck",
     "Investor brand pitch deck: bold opening hero with metric callouts, single-color palette per chapter, chapter dividers with full-bleed image, closing CTA with team grid.",
     ["deck", "pitch", "investor"]),
    ("example-product-launch", "Product Launch Deck",
     "Product launch narrative deck: problem-solution-demo-impact arc, product screenshots framed in device, KPI summary closing.",
     ["deck", "product", "launch"]),
    ("example-live-dashboard", "Live Dashboard",
     "Live updating dashboard artifact: metric cards with sparklines, time-series charts, log feed, refresh indicator, last-updated timestamp.",
     ["dashboard", "live", "data-dense"]),
    ("example-saas-layout", "SaaS Layout",
     "Standard SaaS layout: sticky nav, alternating feature sections with screenshots, pricing table with featured tier, FAQ, footer with secondary nav.",
     ["saas", "marketing", "web"]),
    ("example-investor-update", "Investor Update",
     "Monthly investor update deck: KPI summary, wins, challenges, asks, runway, team updates.",
     ["deck", "investor", "internal"]),
    ("example-tech-talk", "Tech Talk",
     "Conference tech talk slides: code-heavy, dark mode, large code blocks, animation between steps, reference link at end.",
     ["deck", "tech", "developer"]),
    ("example-quarterly-review", "Quarterly Review",
     "Quarterly business review: KPI vs target, segment breakdown, OKR recap, next-quarter priorities.",
     ["deck", "internal", "business"]),
    ("example-sales-enablement", "Sales Enablement",
     "Sales enablement deck: objection handling, competitive matrix, proof points, pricing, next steps.",
     ["deck", "sales", "internal"]),
    ("example-town-hall", "Town Hall",
     "All-hands town hall: company wins, KPI snapshot, team shoutouts, Q&A, leadership notes.",
     ["deck", "internal", "company"]),
    ("image-editorial-hero", "Editorial Hero Image",
     "Editorial-grade hero photograph prompt generator: subject + environment + lighting + mood, with brief style grammar.",
     ["image", "editorial", "hero"]),
    ("image-product-hero-shot", "Product Hero Shot",
     "Product hero shot prompt generator: product + surface + light + angle + framing + background.",
     ["image", "product", "hero"]),
    ("image-social-card", "Social Card",
     "Square social card prompt generator: headline + visual + brand color + format.",
     ["image", "social"]),
    ("image-brand-mood-board", "Brand Mood Board",
     "Brand mood board prompt generator: 4-6 images that capture the brand vibe.",
     ["image", "brand"]),
    ("example-live-embed", "Live Embed",
     "Live embeddable component pattern: dashboard snippet, real-time metric, refresh policy.",
     ["live", "embed", "dashboard"]),
    ("example-live-pricing", "Live Pricing",
     "Live pricing component: plan toggle, currency, feature matrix, CTA.",
     ["live", "pricing", "saas"]),
]


ANATOMY = {
    "example-aerocore": "1. Hero (gradient + parallax wordmark + engine still) -> 2. Mission thumbnail -> 3. Pinned tabbed showcase -> 4. Bento capabilities grid (looping video cards) -> 5. Animated dark stats -> 6. Horizontal video-story rail -> 7. Starfield footer",
    "example-acreage-farming": "1. Fullscreen hero video bg -> 2. Dark intro section -> 3. Light stats grid (animated) -> 4. Logo marquee (infinite) -> 5. Service cards (image-backed) -> 6. CTA -> 7. Footer",
    "example-3d-creator-portfolio": "1. Full-viewport hero (gradient text + magnetic 3D portrait) -> 2. Horizontal scroll image marquee -> 3. About with 3D corner decorations -> 4. Services list (white, dense) -> 5. Sticky-stacking project cards -> 6. Footer",
    "example-ai-designer-portfolio": "1. Hero (generative art) -> 2. Case study grid -> 3. Featured case (long-form) -> 4. Process -> 5. Contact",
    "example-hps-academic-paper": "1. Title page (double rule) -> 2. Abstract -> 3. Section 1, 2, 3... -> 4. Figure/Table numbering -> 5. References (numbered, indented)",
    "example-brand-pitch": "1. Title -> 2. Problem -> 3. Solution -> 4. Market -> 5. Product -> 6. Traction -> 7. Team -> 8. Ask",
    "example-product-launch": "1. Hook -> 2. Demo -> 3. Use cases -> 4. Specs -> 5. Pricing -> 6. Availability",
    "example-live-dashboard": "1. Metric card row (sparklines) -> 2. Time-series chart -> 3. Log feed -> 4. Refresh indicator + last-updated",
    "example-saas-layout": "1. Sticky nav -> 2. Hero -> 3. Alternating feature sections -> 4. Pricing -> 5. FAQ -> 6. Footer",
    "example-investor-update": "1. KPI snapshot -> 2. Wins -> 3. Challenges -> 4. Asks -> 5. Runway -> 6. Team",
    "example-tech-talk": "1. Title -> 2. Motivation -> 3. Approach -> 4. Code -> 5. Result -> 6. Future",
    "example-quarterly-review": "1. KPI vs target -> 2. Segment breakdown -> 3. OKR recap -> 4. Next-quarter priorities",
    "example-sales-enablement": "1. Pitch -> 2. Objections -> 3. Competitive matrix -> 4. Proof -> 5. Pricing -> 6. Next steps",
    "example-town-hall": "1. Wins -> 2. KPI -> 3. Shoutouts -> 4. Q&A -> 5. Leadership",
    "image-editorial-hero": "1. Subject -> 2. Environment -> 3. Lighting -> 4. Mood -> 5. Composition",
    "image-product-hero-shot": "1. Product -> 2. Surface -> 3. Light -> 4. Angle -> 5. Background",
    "image-social-card": "1. Headline -> 2. Visual -> 3. Brand color -> 4. Format",
    "image-brand-mood-board": "1-6. Image set with vibe + color notes",
    "example-live-embed": "1. Embeddable component -> 2. Refresh policy -> 3. Theming via token",
    "example-live-pricing": "1. Plan toggle -> 2. Currency -> 3. Feature matrix -> 4. CTA",
}


PAIRED = {
    "example-aerocore": "vercel, stripe, editorial -- aerospace/cinematic, premium marketing",
    "example-acreage-farming": "vercel, stripe, calm -- agriculture/trade, video-led",
    "example-3d-creator-portfolio": "vercel, neon, cosmic -- creator/portfolio, 3D-heavy",
    "example-ai-designer-portfolio": "openai, editorial, claude-anthropic -- AI/creative, editorial",
    "example-hps-academic-paper": "editorial, medium, swiss -- academic/editorial, all-serif",
    "example-brand-pitch": "stripe, vercel, openai -- investor/pitch, premium",
    "example-product-launch": "stripe, vercel, openai -- product launch, marketing",
    "example-live-dashboard": "linear, supabase, github -- dashboard, data-dense",
    "example-saas-layout": "linear, stripe, shadcn -- SaaS marketing, standard",
    "example-investor-update": "stripe, vercel, calm -- investor, internal",
    "example-tech-talk": "github, vercel, openai -- developer, code-heavy",
    "example-quarterly-review": "linear, calm, asana -- business, internal",
    "example-sales-enablement": "stripe, vercel, calm -- sales, internal",
    "example-town-hall": "linear, calm, notion -- company, internal",
    "image-editorial-hero": "editorial, medium, openai -- editorial image",
    "image-product-hero-shot": "stripe, apple-hig, vercel -- product photography",
    "image-social-card": "vercel, stripe, openai -- social marketing",
    "image-brand-mood-board": "editorial, cosmic, claude-anthropic -- brand expression",
    "example-live-embed": "linear, supabase, github -- embeddable component",
    "example-live-pricing": "linear, stripe, shadcn -- pricing UI",
}


WHEN = {
    "example-aerocore": "Hardware/engineering marketing where cinematic atmosphere is justified.",
    "example-acreage-farming": "Agriculture/precision-farming or industrial B2B with video assets.",
    "example-3d-creator-portfolio": "Personal/creator portfolio with 3D identity.",
    "example-ai-designer-portfolio": "AI-adjacent creative portfolio or case-study heavy site.",
    "example-hps-academic-paper": "Academic/thesis/journal-style deck -- all-serif, zero chrome.",
    "example-brand-pitch": "Investor pitch, fundraising deck.",
    "example-product-launch": "Product launch announcement.",
    "example-live-dashboard": "Live-updating analytics surface.",
    "example-saas-layout": "Standard SaaS marketing site.",
    "example-investor-update": "Recurring investor communications.",
    "example-tech-talk": "Conference or meetup tech talk.",
    "example-quarterly-review": "Internal quarterly business review.",
    "example-sales-enablement": "Sales team enablement deck.",
    "example-town-hall": "Company-wide town hall.",
    "image-editorial-hero": "Generating hero imagery for editorial surfaces.",
    "image-product-hero-shot": "Generating product hero shots.",
    "image-social-card": "Generating square social cards.",
    "image-brand-mood-board": "Generating brand mood boards.",
    "example-live-embed": "Embedding a live component snippet.",
    "example-live-pricing": "Live updating pricing component.",
}


def main() -> int:
    count = 0
    rows = []
    for slug, name, desc, tags in TEMPLATES:
        cat = cat_for(slug)
        body = TEMPLATE_MD.format(
            name=name,
            slug=slug,
            description=desc,
            category_label=CATEGORY_LABEL[cat],
            when=WHEN[slug],
            paired=PAIRED[slug],
            anatomy=ANATOMY[slug],
            tags=", ".join(tags),
        )
        out = TEMPLATES_DIR / f"{slug}.md"
        out.write_text(body)
        rows.append((slug, name, CATEGORY_LABEL[cat], ", ".join(tags)))
        count += 1

    idx = ["# Templates Index", "",
           "Source: https://open-design.ai/plugins/templates/",
           "Total: 290 indexed (20 downloaded as full references)", "",
           "| Slug | Name | Category | Tags |",
           "|---|---|---|---|"]
    for slug, name, cat_label, tags in rows:
        idx.append(f"| {slug} | {name} | {cat_label} | {tags} |")
    (TEMPLATES_DIR / "INDEX.md").write_text("\n".join(idx) + "\n")

    print(f"Wrote {count} template files + INDEX.md into {TEMPLATES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
