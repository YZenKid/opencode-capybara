# Anti-Slop Playbook — UI/UX Pro Max

This is the catalog-driven playbook for replacing AI-slop patterns. When you detect a slop pattern, route to the catalog replacement — do not invent.

## The anti-slop taxonomy

Each slop pattern below has:
- A **detector** (regex / visual / copy heuristic) for the `@quality-gate` to use
- A **catalog replacement** with URL
- A **rationale** for why the catalog entry is the right fix
- A **deviation policy** (when can the implementation diverge?)

---

## 1. Centered gradient hero without product/domain composition

**Detector** (CSS / Tailwind):
```regex
class="[^"]*bg-gradient[^"]*(from|to|via)-(purple|indigo|blue|violet|pink|fuchsia)[^"]*"
class="[^"]*bg-\[url\([^)]*\)\][^"]*"
```

**Catalog replacement**:
- `example-aerocore` (premium hardware/engineering marketing) — https://open-design.ai/plugins/templates/example-aerocore
- `example-3d-creator-portfolio` (creator/portfolio) — https://open-design.ai/plugins/templates/example-3d-creator-portfolio
- `editorial` system if editorial-grade — https://open-design.ai/plugins/systems/example-editorial

**Rationale**: gradient heroes work when the gradient is atmosphere around a product still, not the subject. The catalog templates show parallax + product still as the hero.

**Deviation policy**: only deviate with explicit first-principles rationale. The deviation must be listed in `deviation_audit` with risk and approval.

---

## 2. Card-spam section anatomy (same grid repeated 3+ times)

**Detector** (visual scan or code):
- Same `grid-cols-3` or `flex-row` repeated across sections
- All sections use identical card anatomy: media-top + body + footer
- 3+ sections in a row that are all "feature card grids"

**Catalog replacement**:
- `example-bento` system (bento grid variant) — https://open-design.ai/plugins/systems/example-bento
- `example-aerocore` template (uses bento for capabilities, then video rail, then dark stats) — https://open-design.ai/plugins/templates/example-aerocore

**Rationale**: section anatomy variation is the discipline. Bento varies cell sizes; the catalog templates show bento + sticky-stack + horizontal-rail + dark-chart as alternation.

**Deviation policy**: section anatomy can match the catalog template; it cannot match 3+ consecutive sections of the same grid.

---

## 3. "Modern clean" generic SaaS without source-backed specifics

**Detector** (copy + structure):
- Hero copy is "Build faster. Ship smarter." or "The all-in-one platform for X."
- No concrete user count, no concrete metric, no specific feature with screenshot
- Stack of identical feature cards

**Catalog replacement**:
- `linear` system (concrete, low-chrome, no marketing fluff) — https://open-design.ai/plugins/systems/example-linear
- `stripe` system (premium marketing with concrete mesh + product) — https://open-design.ai/plugins/systems/example-stripe
- Pair with `example-saas-layout` template — https://open-design.ai/plugins/templates/example-saas-layout

**Rationale**: the catalog systems are concrete about what to show. Linear shows the actual product, Stripe shows a real mesh background with the API docs surface. Generic SaaS hides the product.

**Deviation policy**: when deviating from `linear` or `stripe`, document in `deviation_audit` why a different system better serves the user. Reject if the deviation is "we just want it to feel modern."

---

## 4. Lorem ipsum / placeholder content

**Detector** (HTML/text):
```regex
lorem\s+ipsum
placeholder\.com|via\.placeholder|picsum
```

**Catalog replacement**:
- `example-live-dashboard` for live data surfaces (real metrics, not lorem) — https://open-design.ai/plugins/templates/example-live-dashboard
- For marketing copy: write actual copy that follows the `DESIGN.md` voice rules in the cited system.

**Rationale**: lorem ipsum is detectable and rejecting. Catalog templates use real content patterns; copy them with the user's actual product name.

**Deviation policy**: none. Never ship lorem ipsum in production-facing UI.

---

## 5. Decorative stats (5, 10, 100) without context

**Detector** (copy):
```regex
\b(99%|24/7|10x|100k|1M)\b
```

**Catalog replacement**:
- `example-saas-layout` for honest KPI patterns (real customers, real numbers) — https://open-design.ai/plugins/templates/example-saas-layout
- `example-live-dashboard` for live updating metric cards — https://open-design.ai/plugins/templates/example-live-dashboard

**Rationale**: catalog templates show real customer counts, real metrics from real systems, with attribution. The slop pattern is "5 users" with no context.

**Deviation policy**: a "10,000+" stat is acceptable if there is a citation or the system is a demo. Otherwise reject.

---

## 6. "Foto menyusul" / "Akan diperbarui segera" / placeholder copy

**Detector** (copy):
```regex
(foto\s+(menyusul|stok\s+ilustrasi)|dokumentasi\s+asli\s+menyusul|akan\s+diperbarui\s+segera|kontak\s+resmi.*diperbarui)
```

**Catalog replacement**: n/a. **Reject, do not replace.** This is a hard block. If the project lacks photography, use a `direct-reuse-user-approved` asset or generate via the catalog's image templates (e.g. `image-product-hero-shot` — https://open-design.ai/plugins/templates/image-product-hero-shot).

**Rationale**: trust-breaking copy in production UI is the most common AI-slop tell. The catalog never has placeholder copy because each system is a real brand.

**Deviation policy**: none. Hard reject. Route to `@designer` to provide real assets or remove the section.

---

## 7. Decorative emoji icons

**Detector** (HTML):
```regex
<[^>]*>[✨🚀💡🎉🔥💯][^<]*</[^>]*>
```

**Catalog replacement**:
- `apple-hig` SF Symbols — https://open-design.ai/plugins/systems/example-apple-hig
- `material-you` Material Symbols — https://open-design.ai/plugins/systems/example-material-you
- Or use a Lucide / Heroicons set aligned with the chosen catalog system's idiom.

**Rationale**: emoji icons are decorative and inconsistent across platforms. The catalog systems use real icon sets with consistent stroke / weight / grid.

**Deviation policy**: emoji in conversational UI (chat, comments) is OK. Decorative emoji in chrome is rejectable.

---

## 8. "Warm" but sterile feel (community / craft / food domain)

**Detector**: visual scan + copy. Domain requires warmth (community, craft, food, agriculture, artisan) but design delivers centered gradient + Inter + 4 cards.

**Catalog replacement**:
- `claude-anthropic` system (warm editorial) — https://open-design.ai/plugins/systems/example-claude-anthropic
- `anthropic-clay` system (tactile warm) — https://open-design.ai/plugins/systems/example-anthropic-clay
- `notion` system (warm neutral) — https://open-design.ai/plugins/systems/example-notion
- Pair with `example-acreage-farming` (image-backed service cards) for agriculture/craft — https://open-design.ai/plugins/templates/example-acreage-farming

**Rationale**: the warm catalog systems carry actual warmth (terracotta + cream, soft tactile, low-contrast friendly) — not just a "warm" label. They also use real photography by default.

**Deviation policy**: warmth must be in tokens, type, photography, and copy. Warmth-as-color is not enough.

---

## 9. Card-only product grid (no detail, no story)

**Detector**: product section is 6-12 identical cards with image + name + price.

**Catalog replacement**:
- `example-3d-creator-portfolio` sticky-stacking projects — https://open-design.ai/plugins/templates/example-3d-creator-portfolio
- `example-aerocore` bento capabilities — https://open-design.ai/plugins/templates/example-aerocore
- `editorial` system for long-form case studies — https://open-design.ai/plugins/systems/example-editorial

**Rationale**: catalog templates show bento, sticky-stacking, and long-form patterns. Card-only is the slop default.

**Deviation policy**: card-only is acceptable for inventory-style pages (e.g. e-commerce catalog) but must include at least one "feature" section with bento or sticky-stack.

---

## 10. Decorative stats without source

(Same as #5; called out for emphasis. Decorative KPI numbers in hero are the most common AI-slop tell.)

**Catalog replacement**:
- `linear` system with concrete product UI in hero
- `example-live-dashboard` template with live metrics
- `claude-anthropic` system with editorial proof points

**Rationale**: catalog systems earn their place with concrete, sourced content.

---

## How `@quality-gate` uses this playbook

1. Run `ui-polish-audit.py --strict-catalog` for mechanical checks.
2. Run `visual-audit-check.py --contract <path>` for catalog citation.
3. For each detected slop pattern, look up the replacement in this playbook.
4. Reject with `NEEDS_FIX` and a link to the relevant replacement.
5. Designer or implementer can resolve by either:
   - Adopting the catalog replacement wholesale (preferred), or
   - Documenting a `deviation_audit` entry with first-principles rationale.

## How `@designer` uses this playbook

When picking a system + template pair, the playbook is the "what NOT to do" companion to the catalog. Use both:
- Catalog tells you what to do (the systems exist as anti-slop exemplars).
- Playbook tells you what to avoid (the patterns that don't survive `@quality-gate`).
