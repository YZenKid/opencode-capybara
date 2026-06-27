# Anti-Slop Examples

Concrete examples for the **Mechanical anti-AI-slop preflight** gate in `opencode-designer` skill. Each example shows what to reject and what to do instead.

## 1. Centered gradient hero without product

**Reject**: full-bleed purple-to-blue gradient hero with floating glass cards, no product shot, no domain imagery.

**Instead**: hero with real product photo or domain-specific imagery (hands working, materials, environment), clear CTA, scannable hierarchy.

## 2. Card spam across sections

**Reject**: 3+ consecutive sections using the same 3-column card grid (icon + title + description) with cosmetic variation only.

**Instead**: vary section anatomy per purpose — feature section can be alternating left/right with image, social proof section is logo strip or testimonial slider, pricing section is comparison table, FAQ section is accordion.

## 3. Decorative stats without meaningful data

**Reject**: "10x faster", "99% uptime", "24k users" as headline metrics without source, methodology, or label.

**Instead**: real metrics from analytics/dashboard, or remove the section entirely. If demo/dev, label as `Demo data — not production`.

## 4. Emoji or numeric-only service icons

**Reject**: 🚀 ⚡ 🔥 or "1." "2." "3." as service/feature icons.

**Instead**: real icon system (Lucide, Phosphor, custom SVG) with consistent style; or domain-specific imagery when icons are too abstract.

## 5. `foto menyusul` / placeholder text in production-facing UI

**Reject**: hero image marked "foto menyusul", contact section labeled "kontak akan diperbarui", bio marked "coming soon".

**Instead**: real photography, real contact info (address, hours, email/phone), or do not ship the surface until content is real.

## 6. Vague neon blobs / default purple-blue glow

**Reject**: page background with abstract glowing blobs, no relation to content or domain.

**Instead**: contextual background (subtle texture, photo with overlay, geometric pattern tied to brand) — not generic glow.

## 7. Repeated section heading labels

**Reject**: every section starts with eyebrow "Discover" / "Explore" / "Learn more" before the actual heading.

**Instead**: limit eyebrow repetition to roughly `ceil(sectionCount / 3)`. Use direct headings instead, or skip eyebrows where they don't add info.
