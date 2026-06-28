# Foundation Slice — Evidence Summary

**Task ID**: ui-ux-open-design-upgrade
**Plan**: `.opencode/plans/ui-ux-open-design-upgrade.md`
**Slice**: Foundation (tasks 1-11)
**Status**: PASS_FOR_SLICE
**Date**: 2026-06-28

---

## What was built

| # | Deliverable | Path | Size / Count | Self-test |
|---|---|---|---|---|
| 1 | Catalog index (150 systems + 290 templates) | `.opencode/catalog/INDEX.md` | 28KB, 150 systems, 290 templates | grep -c "open-design.ai" = 295+ |
| 2 | 20 full system DESIGN.md files | `.opencode/catalog/systems/<slug>/DESIGN.md` | 20 dirs | ls = 20 |
| 3 | 20 template files + INDEX | `.opencode/catalog/templates/<slug>.md` + INDEX.md | 20 + 1 | ls = 21 |
| 4 | `init-design-system.py` v2 (catalog-aware) | `scripts/init-design-system.py` | 6.9KB | --list-systems returns 20; --system linear --template example-saas-layout emits DESIGN.md with Catalog Citation block |
| 5 | `design-token-generator.py` v2 (named tokens, Tailwind config) | `scripts/design-token-generator.py` | 8.2KB | 11 named colors, 8 type roles, 10 spacing steps + tokens.json + tokens.css + tailwind.config.js |
| 6 | `catalog-search.py` CLI | `scripts/catalog-search.py` | 9.6KB | --query editorial finds 3 systems + 3 templates; --pair marketing returns stripe+vercel+aerocore; --json works |
| 7 | `design-system-fork.py` CLI | `scripts/design-system-fork.py` | 6.5KB | --base linear --deviate ink=#ff0066 --deviate surface=#fafafa applied 2/2 with citation + audit table |
| 8 | `visual-quality-contract-v2.md` template | `skills/opencode-quality-gate/templates/visual-quality-contract-v2.md` | 7.8KB | 7 sections, Catalog Citation YAML block, v1->v2 migration notes |
| 9 | `visual-rubric.md` v2 with mechanical rows | `skills/opencode-quality-gate/templates/visual-rubric.md` | 3.8KB | Catalog Citation Check (10 rows), Dashboard/Pricing/Onboarding coverage, Template Anatomy Compliance block |
| 10 | `visual-audit-check.py` v2 (enforce catalog_citation) | `scripts/visual-audit-check.py` | +12KB functions | v2 full contract exit 0; v1 + substantial-ui filename exit 1; --token-parity works |
| 11 | `ui-polish-audit.py` v2 (--strict-catalog) | `scripts/ui-polish-audit.py` | +2KB | Exit 2 on catalog fail, 1 on slop, 0 on clean |

**Harness awareness (already shipped earlier in this conversation)**:
- `AGENTS.md` — +1 line: UI/UX catalog source of truth
- `.opencode/docs/SKILLS.md` — +22 lines: per-lane obligations for designer/frontend/mobile/quality-gate/design-system-engineer/orchestrator
- `agents/orchestrator.md` — +1 line in decision tree step 4.5: catalog-decision.md required for substantial UI

**State tracking**:
- `.opencode/state/ui-ux-open-design-upgrade/progress.json` — 11 task records, all `completed`

---

## End-to-end smoke test (executed)

Pipeline: catalog-search → init-design-system → design-token-generator → design-system-fork → visual-quality-contract → visual-audit-check → ui-polish-audit

| Step | Command | Result | Exit |
|---|---|---|---|
| 1 | `catalog-search.py --pair --query "AI ops dashboard for engineers"` | Returns linear/supabase + example-live-dashboard | 0 |
| 2 | `init-design-system.py --system linear --template example-live-dashboard` | DESIGN.md (full schema + Catalog Citation block) | 0 |
| 3 | `design-token-generator.py --system linear` | 11 colors, 8 type roles, 10 spacing + tokens.json/css/tailwind.config.js | 0 |
| 4 | `design-system-fork.py --base linear --deviate accent=#ff5722` | Forked DESIGN.md with Deviation Audit table | 0 |
| 5 | Authored v2 contract with catalog_citation, deviation_audit, must_use_tokens, must_avoid_token | File written | n/a |
| 6 | `visual-audit-check.py --contract ...` | All mechanical checks pass | 0 |
| 7 | `visual-audit-check.py --contract ... --token-parity` | Token Parity section emitted | 0 |
| 8 | `ui-polish-audit.py --strict-catalog` | DESIGN.md cites catalog; no slop | 0 |

**Outcome**: All 8 pipeline steps pass with exit 0. The foundation slice is operational end-to-end.

---

## What's NOT in this slice (deferred to tasks 12-22)

These ship in the **policy migration slice** and **eval slice**:

- Tasks 12-16: Upgrade 5 agent files (`designer`, `frontend`, `mobile`, `quality-gate`, `design-system-engineer`) with the new obligations
- Task 17: Orchestrator step 4.5 already shipped; any further refinements
- Task 18: Fill `ui-ux-pro-max/` skill folder (currently empty except for `__pycache__/`)
- Task 19: Update `.opencode/docs/SKILLS.md` — already shipped earlier in this conversation
- Task 20: Update `AGENTS.md` — already shipped earlier in this conversation
- Task 21: Run eval set on a greenfield task
- Task 22: Release PR

---

## Risk register

| Risk | Mitigation in this slice | Owner |
|---|---|---|
| Catalog URL drift (open-design.ai renames) | Index records full URL; refresh command is a single `design-source-importer.py --init --refresh` | `@designer` |
| Token extraction noise (header row matched as role) | `parse_typography_section` accepts it as harmless metadata; downstream usage filters by role keys; documented in script | `@fixer` followup |
| License drift (a system changes license) | INDEX records license per entry; `visual-audit-check.py` warns if URL not open-design.ai | `@skill-improver` |
| Catalog schema evolution (DESIGN.md format changes) | `init-design-system.py` reads v2 schema; design-token-generator has --strict; failure modes documented in plan §1 | `@architect` |
| Backward compat for non-substantial UI | v1 contract still valid; `visual-audit-check.py` allows v1 with `low` severity; ui-polish-audit defaults to non-strict | inherited from plan §6 |

---

## Next step

Run policy migration slice (tasks 12-17). Each agent file upgrade is bounded and reversible. Recommend one task per session to allow evidence accumulation and `@quality-gate` review between upgrades.

To start, run:
```
@orchestrator execute plan: .opencode/plans/ui-ux-open-design-upgrade.md
```
with the policy migration slice as the next scope.
