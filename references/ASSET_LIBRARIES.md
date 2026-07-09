# Open-Source Asset Libraries

Curated reference for `@designer`, `@visual-asset-generator`, `@frontend`, `@mobile`, and `@fixer` when selecting open-source icon, illustration, stock, and 3D assets. This list favors permissive licenses (MIT, Apache-2.0, ISC, CC0, CC-BY) and explicitly notes when attribution is required.

> **Legal reminder**: this list is a starting point, not a license waiver. Always confirm the current license on the upstream source before reuse. The `npm run check:legal-source` gate and `.opencode/docs/SHARED_POLICIES.md` "External source reuse, scraping, and image-generation legal gate" still apply. Do not silently hotlink CDN assets that prohibit hotlinking.

## Icon libraries

| Library | License | Notes |
|---|---|---|
| [Lucide](https://lucide.dev/) | ISC | Default for many design systems; clean outline; React/Vue/Svelte packages |
| [Phosphor Icons](https://phosphoricons.com/) | MIT | Multiple weights (thin, light, regular, bold, fill, duotone) |
| [Heroicons](https://heroicons.com/) | MIT | Common in Tailwind UI projects; outline + solid |
| [Tabler Icons](https://tabler.io/icons) | MIT | 5000+ outline icons; consistent stroke |
| [Iconoir](https://iconoir.com/) | MIT | Clean, modern, multilingual icons |
| [Material Symbols](https://fonts.google.com/icons) | Apache-2.0 | Variable-font icons; weight/fill/optical-size axis |
| [Remix Icon](https://remixicon.com/) | Apache-2.0 | 2800+ outline/fill |
| [Carbon Icons](https://carbondesignsystem.com/guidelines/icons/library/) | Apache-2.0 | IBM Carbon design system; regular glyphs |
| [Hugeicons](https://hugeicons.com/) | Free/Pro tier | Per-icon licensing; verify per icon |
| [Bootstrap Icons](https://icons.getbootstrap.com/) | MIT | Drop-in for Bootstrap stacks |
| [Octicons](https://primer.style/octicons) | MIT | GitHub Primer; tech-shaped |
| [Nerd Fonts](https://www.nerdfonts.com/) | MIT (per-glyph) | Patched fonts; CLI/dev tooling, not for general UI |

### Icon anti-patterns
- Emoji icons, numeric-only service icons, fake brand marks, mismatched stroke weights across sets.
- Generated logos for functional UI; generate only for decorative badges or lookalike marks.
- Always pick a single icon family per project; do not mix.

## Illustrations

| Library | License | Notes |
|---|---|---|
| [Open Doodles](https://www.opendoodles.com/) | CC-BY 4.0 (attribution required) | Hand-drawn character set |
| [unDraw](https://undraw.co/) | MIT-ish (free, no attribution; recolor allowed) | Generic business illustrations |
| [Storyset](https://storyset.com/) | Free for personal/commercial; attribution optional on free tier | Animated + static |
| [Blush](https://blush.design/) | Free tier + Pro; check per-asset license | Customizable illustration collections |
| [Humaaans](https://www.humaaans.com/) | Free for personal/commercial; no attribution | Mix-and-match people illustrations |
| [Open Peeps](https://www.openpeeps.com/) | CC0 | Character builder |
| [Lukasz Adam](https://lukaszadam.com/illustrations) | Free for personal/commercial | Abstract vector illustrations |
| [IRA Design](https://iradesign.io/) | Free for personal/commercial | Gradient blob illustrations |
| [Glaze Illustrations](https://www.glaze.co/) | Free + Pro; check per-asset | Marketing-friendly scenes |
| [Kukacka](https://www.kukacka.cz/) | Free; per-asset license | Mascot/character style |

## Stock photography (license-clear)

> Stock providers are not strictly "open source". Treat them as licensed-aggregate sources. Always record which site/source the photo came from and the platform license (Unsplash License, Pexels License, Pixabay License, etc.) in evidence.

| Provider | License posture | Notes |
|---|---|---|
| [Unsplash](https://unsplash.com/) | Unsplash License (free, no permission needed, attribution appreciated) | Best for editorial/lifestyle |
| [Pexels](https://www.pexels.com/) | Pexels License (free, attribution appreciated) | Broad categories |
| [Pixabay](https://pixabay.com/) | Pixabay Content License (free, attribution appreciated; some images require model release verification) | Verify model release for portraits |
| [Wikimedia Commons](https://commons.wikimedia.org/) | Per-file license (CC-BY, CC-BY-SA, public domain) | Strong attribution discipline required |
| [Picsum](https://picsum.photos/) | Unsplash-derived, do not claim as your own | Placeholder only; not for production hero |
| [NASA Image Gallery](https://images.nasa.gov/) | Mostly public domain | Astronomy, Earth, mission imagery |
| [Coverr](https://coverr.co/) | Free; check per-video license | Looping video backgrounds |

> For real-photography sections, do **not** use generated imagery as a substitute. For sections that need a `person using product` or real subject, prefer licensed stock or user-provided real photography.

## 3D models and assets

| Library | License | Notes |
|---|---|---|
| [Poly Haven](https://polyhaven.com/) | CC0 | HDRIs, textures, models; production-ready |
| [Quaternius](https://quaternius.com/) | CC0 | Game-ready stylized assets |
| [Kenney](https://kenney.nl/) | CC0 | Game UI, props, characters; great for prototyping |
| [Sketchfab](https://sketchfab.com/) | Per-model; filter by CC license | Verify per-model license + attribution requirement |
| [glTF Sample Models](https://github.com/KhronosGroup/glTF-Sample-Models) | Various (CC-BY, public domain) | Reference for testing pipelines |
| [Three.js examples](https://threejs.org/examples/) | MIT | Reference for web 3D runtime |
| [Poly Pizza](https://poly.pizza/) | Per-model; mostly CC0/CC-BY | Free low-poly 3D model aggregator |
| [Mixamo](https://www.mixamo.com/) | Free for use in projects; not for resale of the asset itself | Animated character rigs |
| [Ready Player Me](https://readyplayer.me/) | Free for personal; check per-product license | Avatar/character API |
| [cgtrader Freebies](https://www.cgtrader.com/free-3d-models) | Per-asset; verify per license | Larger selection, mixed quality |

### 3D runtimes (web)

| Library | License | Notes |
|---|---|---|
| [Three.js](https://threejs.org/) | MIT | Default web 3D runtime |
| [react-three-fiber](https://r3f.docs.pmnd.rs/) | MIT | React renderer for Three.js |
| [drei](https://github.com/pmndrs/drei) | MIT | Helpers for r3f |
| [model-viewer](https://modelviewer.dev/) | MIT | Embed glTF in HTML, no JS needed |
| [Spline](https://spline.design/) | Free tier + Pro; verify hotlink/embed policy | Quick hero/visualization; some assets may have non-OSS license |
| [Babylon.js](https://www.babylonjs.com/) | Apache-2.0 | Heavier scenes, game-engine-grade |

### 3D anti-patterns
- 3D for the sake of 3D on dashboards, forms, settings, or transactional surfaces.
- Autoplay camera spins and endless rotations on first paint.
- Heavy assets (10MB+ GLB) on the critical path; lazy-load and dispose on unmount.
- 3D that hides the primary CTA or replaces real product context.
- Mixing multiple runtimes (e.g. Three.js + Spline + model-viewer) in the same project without reason.
- Watermark removal, asset origin falsification, or fake product mockups presented as real.

## How to use this list

1. Pick a single icon family per project; record the license in `Component Stylings > Icon system`.
2. Pick one or two illustration sources per project; record license in evidence.
3. For 3D: pick one runtime, one asset source pattern, and a single set of lighting/material defaults; record in `Component Stylings > 3D / spatial`.
4. Run `npm run check:legal-source -- --source <upstream-url>` before bulk-importing from any source listed here if the upstream license posture changes.
5. Always record source, license, and attribution in evidence when asset is consumed.
