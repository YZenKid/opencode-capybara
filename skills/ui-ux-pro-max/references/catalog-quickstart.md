# Catalog Quickstart — UI/UX Pro Max

This is the one-pager. Any UI/UX lane can load this in <30s to recall the catalog defaults.

## Source of truth

- **Catalog index**: `.opencode/catalog/INDEX.md` (150 systems + 290 templates)
- **Catalog source**: https://open-design.ai
- **License**: Apache-2.0 (catalog format); each system/template is open-source per its own attribution
- **Local cache**: read-only by default; refresh with `python3 ~/.config/opencode/scripts/design-source-importer.py --init --refresh`

## 5 systems by surface (default picks)

| Surface | System | Why |
|---|---|---|
| Web SaaS / productivity | `linear` | Focused low-chrome, Inter, restrained color. The default. |
| Web editorial / docs | `editorial` | Serif-led hierarchy, ink-on-paper, single link-blue accent. |
| Web premium marketing | `stripe` | Premium SaaS marketing, soft gradient mesh, violet accent. |
| Mobile productivity | `apple-hig` | SF Pro, native gestures, generous spacing. |
| Mobile consumer | `spotify` or `discord` | Dark, content-first, optimized for thumb reach. |

## 5 templates by intent

| Intent | Template | Anatomy |
|---|---|---|
| Landing | `example-aerocore` | Hero (parallax + product) → Bento → dark stats → video rail |
| SaaS marketing | `example-saas-layout` | Sticky nav → alternating features → pricing → FAQ |
| Dashboard | `example-live-dashboard` | Metric cards + sparklines → time-series → log feed |
| Deck / pitch | `example-hps-academic-paper` (editorial) or `example-brand-pitch` (premium) | All-serif (academic) or bold hero (pitch) |
| Mobile shell | `example-live-embed` | Embeddable component with refresh policy |

## 3 anti-patterns and their catalog replacement

| Anti-pattern | Catalog replacement |
|---|---|
| Centered gradient hero, no product | `example-aerocore` hero anatomy (parallax + product still) |
| Card-spam section anatomy | `example-bento` system with bento-grid variant |
| "Modern clean" without source | `linear` system + `example-saas-layout` template (cite both) |

## How to fork a system

```bash
# 1. List available systems
python3 ~/.config/opencode/scripts/init-design-system.py --list-systems

# 2. Generate DESIGN.md from a system
python3 ~/.config/opencode/scripts/init-design-system.py --project-root . --system linear --template example-saas-layout --force

# 3. (Optional) Fork with token deviations
python3 ~/.config/opencode/scripts/design-system-fork.py --base linear --out DESIGN.md \
  --deviate "accent=#ff5722" --deviate "surface=#fafafa" \
  --author "Mang Ujang" --purpose "ScyllaX ops dashboard"

# 4. Generate tokens for the implementation lane
python3 ~/.config/opencode/scripts/design-token-generator.py --project-root . --system linear --strict
```

## How to search the catalog

```bash
# by vibe keyword
python3 ~/.config/opencode/scripts/catalog-search.py --query "editorial"

# by surface
python3 ~/.config/opencode/scripts/catalog-search.py --query "premium" --surface web

# template only
python3 ~/.config/opencode/scripts/catalog-search.py --kind templates --query "dashboard"

# pair suggestion for a use case
python3 ~/.config/opencode/scripts/catalog-search.py --pair --query "marketing site for AI startup"

# JSON for programmatic use
python3 ~/.config/opencode/scripts/catalog-search.py --query "premium" --json
```

## How to verify a substantial UI is ready for `@quality-gate`

```bash
# 1. Author the v2 contract
cp ~/.config/opencode/skills/opencode-quality-gate/templates/visual-quality-contract-v2.md \
   .opencode/evidence/<task-id>/visual-quality-contract.md
# fill in catalog_citation block

# 2. Mechanical audit
python3 ~/.config/opencode/scripts/visual-audit-check.py \
  --project-root . \
  --contract .opencode/evidence/<task-id>/visual-quality-contract.md

# 3. Token parity
python3 ~/.config/opencode/scripts/visual-audit-check.py \
  --project-root . \
  --contract .opencode/evidence/<task-id>/visual-quality-contract.md \
  --token-parity

# 4. UI polish audit
python3 ~/.config/opencode/scripts/ui-polish-audit.py --project-root . --strict-catalog
```

If all three exit 0, the UI is mechanically ready for `@quality-gate`. The gate will additionally check screenshots, accessibility, and taste — but the mechanical catalog checks will not be the gate's blocker.

## Forbidden

- Inventing a hero from prose. Pick from the catalog.
- Hand-editing `tokens.json` instead of regenerating from the catalog.
- Skipping `deviation_audit` when forking.
- Treating the catalog as inspiration only — it is the source of truth.
