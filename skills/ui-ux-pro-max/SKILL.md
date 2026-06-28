---
name: ui-ux-pro-max
description: Cross-lane UI/UX meta-skill for substantial UI work. Use when designing, implementing, reviewing, or shipping user-facing surfaces (web or mobile) that need polished visuals, design-system alignment, motion, accessibility, and reference feel parity. Auto-loads in @designer, @frontend, @mobile, @design-system-engineer when task is substantial UI.
---

# UI/UX Pro Max — Cross-lane Meta-skill

This is the **meta-skill** for UI/UX work. It is auto-loaded by the relevant lanes for substantial UI tasks and serves as the playbook that ties the catalog, the design contract, the token generator, the audit scripts, and the quality-gate together.

## Why this skill exists

Each lane (`@designer`, `@frontend`, `@mobile`, `@design-system-engineer`, `@quality-gate`) has its own scope. But substantial UI work requires all five lanes to **agree on the same source of truth** and **mechanically verify that agreement**. This skill:

1. Names the source of truth (the Open Design catalog).
2. Names the contract that all lanes must populate (visual-quality-contract.md v2).
3. Names the scripts that bind the lanes (`init-design-system`, `design-token-generator`, `design-system-fork`, `catalog-search`, `visual-audit-check`, `ui-polish-audit`).
4. Names the failure modes that always map to `NEEDS_FIX` (missing citation, undocumented deviation, token parity < 80%, must_avoid_token violation).

## When to load

| Trigger | Lane | What to do |
|---|---|---|
| Task is `greenfield` or `substance=substantial UI` | @designer | Run `catalog-search.py --pair`, select system+template, document in `catalog-decision.md` |
| Web implementation from a design handoff | @frontend | Verify `DESIGN.md` cites catalog; load tokens from generated files; implement from template anatomy |
| Mobile implementation from a design handoff | @mobile | Verify mobile-tested system or document translation risk; generate iOS/Android theme from `tokens.json` |
| Adding new shared tokens / primitives | @design-system-engineer | `catalog-search.py` first; reuse + extend; `design-system-fork.py` for new forks |
| Final review of substantial UI | @quality-gate | Run `visual-audit-check.py --contract`; require all mechanical catalog checks pass |
| Tiny / non-visual / reversible | any | Skip this skill. Use lane defaults. |

## 20-item UI work checklist

Before any substantial UI claim reaches `@quality-gate`, verify:

**Selection & contract (steps 1-5)**
1. `catalog-decision.md` exists in `.opencode/evidence/<task-id>/`.
2. Cited system + template URLs both point to `open-design.ai`.
3. `pair_rationale` is ≥2 sentences.
4. `deviation_audit` is populated (or contains explicit "no deviations" note).
5. `visual-quality-contract.md` v2 is authored with complete `catalog_citation` block.

**Token sourcing (steps 6-10)**
6. `DESIGN.md` is generated from the chosen system (`Source & Provenance` block present).
7. `tokens.json`, `tokens.css`, `tailwind.config.js` are generated under `.opencode/generated-design/`.
8. `tokens.json` has at least 5 named colors and 5 type roles.
9. Components reference tokens via Tailwind/CSS-vars/JSON; no inline `#hex` (except labeled one-offs).
10. `must_use_tokens` are ≥80% present in the implementation (verified by `visual-audit-check.py --token-parity`).

**Implementation discipline (steps 11-15)**
11. Section anatomy follows the cited template; deviations are in `deviation_audit`.
12. No `bg-gradient` from `purple/indigo/blue/violet` without catalog citation.
13. No "foto menyusul", "akan diperbarui segera", "pasti bisa", "solusi terbaik" copy in production UI.
14. No `picsum`, `lorem ipsum`, `placeholder.com` in production.
15. Touch targets ≥ 44x44pt (mobile); contrast ≥ 4.5:1 (web).

**Evidence & gate (steps 16-20)**
16. Reference screenshots (reference vs implementation) saved under `.opencode/evidence/<task-id>/`.
17. `visual-quality-contract.md` is filled with `must_show`, `must_not_show`, `reject_if`, `fake_warmth_patterns`, `template_smells`.
18. `visual-rubric.md` v2 has all 10 Catalog Citation Check rows passing.
19. `visual-audit-check.py --contract <path>` exits 0.
20. `ui-polish-audit.py --strict-catalog` exits 0.

**If any of 1-20 fails, return `needs-polish` or `blocked`. Do not claim `ready` or `reference-ready`.**

## Anti-slop playbook (catalog-driven)

When you spot a known slop pattern, route to the catalog replacement:

| AI-slop pattern detected | Catalog replacement | Reference |
|---|---|---|
| Centered gradient hero, no product | `example-aerocore` or `example-3d-creator-portfolio` hero | open-design.ai/plugins/templates/example-aerocore |
| Card-spam section anatomy | `example-bento` system or `Bento` template variant | open-design.ai/plugins/systems/example-bento |
| "Modern clean" generic SaaS | `linear` or `stripe` system | open-design.ai/plugins/systems/example-linear |
| Lorem ipsum / placeholder | Generate real content OR use `example-live-dashboard` for live data | n/a |
| Decorative stats (5, 10, 100) | Use `example-saas-layout` for honest KPI patterns | open-design.ai/plugins/templates/example-saas-layout |
| Card-only product grid | `example-3d-creator-portfolio` sticky-stacking projects | open-design.ai/plugins/templates/example-3d-creator-portfolio |
| "Foto menyusul" copy | Block, do not ship; require real photography or `direct-reuse-user-approved` | n/a |
| Decorative emoji icons | `apple-hig` SF Symbols or `material-you` Material Symbols | open-design.ai/plugins/systems/example-apple-hig |
| "Warm" but sterile feel | `claude-anthropic` or `anthropic-clay` for actual warmth | open-design.ai/plugins/systems/example-claude-anthropic |
| Card without domain texture | `example-acreage-farming` (image-backed service cards) | open-design.ai/plugins/templates/example-acreage-farming |

## Anti-patterns (forbidden in this skill)

- Inventing hero/nav/dashboard anatomies from prose without catalog selection.
- Shipping UI without a `catalog_citation` block in the visual contract.
- Hand-editing `tokens.json` instead of regenerating from catalog.
- Forking a catalog system without a `Deviations` block.
- Adding a 7th way to write DESIGN.md (the v2 schema is the standard).
- Treating the catalog as Pinterest / vibe library (it is structural, not inspirational).

## See also

- `.opencode/catalog/INDEX.md` — the catalog index (150 systems + 290 templates)
- `.opencode/catalog/systems/<slug>/DESIGN.md` — full system definitions
- `.opencode/catalog/templates/<slug>.md` — full template definitions
- `skills/opencode-quality-gate/templates/visual-quality-contract-v2.md` — the contract
- `skills/opencode-quality-gate/templates/visual-rubric.md` — the rubric (v2)
- `scripts/catalog-search.py`, `scripts/design-system-fork.py`, `scripts/design-token-generator.py`, `scripts/init-design-system.py`, `scripts/visual-audit-check.py`, `scripts/ui-polish-audit.py` — the binding tools
- `.opencode/plans/ui-ux-open-design-upgrade.md` — the plan that produced this skill
- `.opencode/docs/SKILLS.md` §"UI/UX design system source of truth" — the lane obligations
