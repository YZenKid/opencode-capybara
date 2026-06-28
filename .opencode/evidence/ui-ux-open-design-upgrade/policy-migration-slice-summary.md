# Policy Migration Slice — Evidence Summary

**Task ID**: ui-ux-open-design-upgrade
**Plan**: `.opencode/plans/ui-ux-open-design-upgrade.md`
**Slice**: Policy Migration (tasks 12-22) + Eval (task 21)
**Status**: PASS_FOR_SLICE
**Date**: 2026-06-28

---

## What was built in this slice

### Agent file upgrades (5 agents + orchestrator)

| Agent | Section added | Lines added | Key obligation |
|---|---|---|---|
| `@designer` | Catalog-First Workflow (v2) + Workflow step 0 | +55 | Pick from catalog before substantial UI; document pair + deviations; cite `open-design.ai` URL |
| `@frontend` | Token-First Implementation (v2) + pushback for catalog gaps | +34 | Load tokens from `.opencode/catalog/.../tokens.{json,css}`; cite template in PR; pushback if DESIGN.md lacks citation |
| `@mobile` | Mobile Catalog Selection (v2) + native token parity + platform anti-patterns | +31 | Verify mobile-tested system or document translation risk; derive iOS/Android theme from tokens.json; reject platform-cross chrome |
| `@quality-gate` | 4 MANDATORY v2 mechanical checks | +4 (with surrounding context) | Catalog citation required → NEEDS_FIX; deviation audit required; token parity ≥80%; visual rubric v2 mechanical |
| `@design-system-engineer` | Catalog-First Token Sourcing (v2) + fork discipline | +35 | Search catalog before adding new tokens; use design-system-fork.py with audit table; silent forks = license violation |
| `@orchestrator` | Step 4.5 routing cue (already shipped earlier) | verified | Catalog-decision.md required for substantial UI before routing to `@frontend`/`@mobile` |

### ui-ux-pro-max skill (was empty)

| File | Size | Purpose |
|---|---|---|
| `SKILL.md` | 7.1KB | Meta-skill for cross-lane UI/UX work: 20-item checklist + anti-slop catalog table + lane obligations |
| `references/catalog-quickstart.md` | 4.6KB | One-pager: 5 systems by surface + 5 templates by intent + 3 anti-pattern replacements + fork/search/verify howto |
| `references/anti-slop-playbook.md` | 9.3KB | 10 AI-slop patterns, each with detector (regex), catalog replacement (URL), rationale, deviation policy |
| `references/lane-routing-cheatsheet.md` | 5.2KB | Routing decision tree + "what is substantial UI" + per-lane mechanical checks + forbidden list |
| `scripts/select-catalog.py` | 4.8KB | One-shot brief → catalog recommendation helper; wraps `catalog-search.py --pair` with formatted output + JSON option |

### Harness awareness (verified)

- `AGENTS.md` — UI/UX catalog source of truth line (line 39)
- `.opencode/docs/SKILLS.md` — UI/UX design system source of truth section (lines 51-69) with per-lane obligations
- `agents/orchestrator.md` — step 4.5 routing cue (line 121)

### visual-audit-check.py upgrade (token parity enforcement)

| Before | After |
|---|---|
| Token parity was info-only | Parity < 80% on **effective** must_use → `NEEDS_FIX` (high severity) |
| must_avoid violations ignored | Any must_avoid violation → `NEEDS_FIX` (high severity) |
| Deviations not whitelisted | Tokens listed in `deviation_audit` "what" are excluded from "missing" count |

This fix was triggered by the eval: the greenfield eval initially showed 66.7% parity because `#635bff` (stripe violet) was in must_use but the project had deviated to `#4f46e5` (indigo) per deviation_audit. After the whitelist, parity correctly reports 100% (3 declared, 1 whitelisted by deviation, 2 effective, 2 found).

---

## End-to-end eval (task 21) — greenfield landing page

**Brief**: "marketing site for AI ops tool for engineers"

**Pipeline executed**:

1. `@orchestrator` step 4.5 fires: substantial UI detected → routes to `@designer` with catalog-decision.md requirement.
2. `@designer` runs `select-catalog.py`: returns `stripe` + `example-saas-layout` as primary pair (marketing use-case match).
3. `@designer` writes `catalog-decision.md` with chosen pair + 3 rejected alternatives + pair rationale + planned deviations.
4. `@designer` runs `init-design-system.py --system stripe --template example-saas-layout`: DESIGN.md created from catalog with full v2 schema (Source & Provenance block + Catalog Citation block).
5. `@designer` runs `design-system-fork.py --deviate accent=#4f46e5`: forked DESIGN.md with Catalog Citation (this fork) block + Deviation Audit table.
6. `@design-system-engineer` runs `design-token-generator.py --system stripe --strict`: 11 named colors + 8 type roles + 10 spacing steps + tokens.json/css/tailwind.config.js.
7. `@designer` authors `visual-quality-contract.md` v2 with complete catalog_citation block + deviation_audit + must_use_tokens + must_avoid_token.
8. `@frontend` implements minimal hero + CTA from tokens via CSS variables.
9. `@quality-gate` runs three mechanical checks.

**Quality gate results**:

| Check | Exit | Output |
|---|---|---|
| `visual-audit-check.py --contract <path>` | **0** | All mechanical checks pass |
| `visual-audit-check.py --contract <path> --token-parity` | **0** | 100% parity after deviation whitelist (3 declared, 1 whitelisted, 2 effective, 2 found, 0 must_avoid violations) |
| `ui-polish-audit.py --strict-catalog` | **0** | DESIGN.md cites catalog; no slop |

**Outcome**: greenfield eval mechanically passes `@quality-gate` at the catalog level. The gate will additionally check screenshots, accessibility, and taste in real review.

---

## What this slice changes for each lane

### @designer
- **Before**: design direction could be prose-only ("warm, focused, modern").
- **After**: for substantial UI, must run `select-catalog.py` (or `catalog-search.py --pair`), document pick in `catalog-decision.md`, generate DESIGN.md from catalog (or fork with documented deviation), embed `catalog_citation` in visual contract.

### @frontend
- **Before**: components could have inline `#hex` and ad-hoc tokens.
- **After**: components must reference tokens from `.opencode/catalog/.../tokens.{json,css,tailwind.config.js}`. Pushback authority for DESIGN.md that lacks catalog citation.

### @mobile
- **Before**: mobile work could pick desktop-only systems without translation notes.
- **After**: must pick mobile-tested system OR document translation risk in `deviation_audit`. Native token parity required (iOS Swift + Android Kotlin themes from tokens.json).

### @design-system-engineer
- **Before**: new shared tokens could be invented freely.
- **After**: search catalog first; reuse + extend; `design-system-fork.py` for forks with audit table. Silent forks = license violation.

### @quality-gate
- **Before**: visual contract was v1 with `must_show`/`reject_if` but no catalog requirement.
- **After**: substantial UI requires catalog citation (v2 schema) + deviation audit + token parity ≥80% + visual rubric v2. Mechanical, not taste.

### @orchestrator
- **Before**: routing to `@frontend`/`@mobile` was direct.
- **After**: step 4.5 verifies `catalog-decision.md` exists for substantial UI before implementation lanes are invoked.

---

## State tracking

- `.opencode/state/ui-ux-open-design-upgrade/progress.json` updated with both slices (foundation + policy_migration) and all 22 tasks marked `completed`.
- `.opencode/evidence/ui-ux-open-design-upgrade/foundation-slice-summary.md` (from earlier slice).
- `.opencode/evidence/ui-ux-open-design-upgrade/policy-migration-slice-summary.md` (this file).

---

## Risk register (slice-specific)

| Risk | Mitigation | Owner |
|---|---|---|
| Agent files drift from policy over time | `agents/agent-boundary-check.mjs` already exists; can extend to check for catalog_citation reference in design-adjacent agents | `@skill-improver` |
| ui-ux-pro-max skill gets out of sync with scripts | Skill references scripts by path; verify with monthly `find` audit | `@skill-improver` |
| Token parity threshold (80%) too lax or too strict | Eval showed 100% on intentional deviation; tune after first 5 production runs | `@oracle` |
| Eval hasn't been run on a real production UI yet | Foundation + policy migration slice complete; eval is on a simulated greenfield. Next step is one real production UI to verify the gate fires correctly. | user / project owner |

---

## `/init-harness` consistency audit (post-slice, follow-up to "pastiin command init-harness nya udah konsisten juga")

After the policy migration slice landed, the user asked to audit that `/init-harness` references are consistent across agents and skills. Audit pass:

- **14 files** reference `/init-harness`
- **27 total occurrences** across those files
- **27 occurrences** carry the `single entrypoint` marker
- **27 occurrences** reference `commands/init-harness.md` as the spec

```text
Total /init-harness:           27
Single entrypoint marker:      27 (100%)
commands/init-harness.md path: 27 (100%)
Files consistent:              14/14
```

**Why this matters.** Before the audit, references were inconsistent:
- `@design-system-engineer` had no `MANDATORY stack read` at all.
- Other agents and skills used a short pattern ("If missing or stale, run `/init-harness`...") without naming the command spec, making drift possible — an agent could redefine `/init-harness` behavior in its own doc.
- Some design-only contexts said "use /init-harness" without the guard "do not redirect to any separate design-init command".

**Standard pattern now applied (3 elements in every reference):**

1. **Specifier** — `(per `commands/init-harness.md`)` so the spec is discoverable.
2. **Marker** — `(single entrypoint for harness + design init)` so the invariant is explicit.
3. **Source-of-truth clause** — `The /init-harness command is the source of truth for what these docs contain; agents do not redefine it.` (in MANDATORY-stack-read contexts) OR `Do not redirect to any separate design-init command.` (in design-only contexts).

**Inconsistencies fixed:**

| File | Lines | Change |
|---|---|---|
| `agents/designer.md` | 155, 191, 298 | Added `single entrypoint` + `commands/init-harness.md` + close-the-loop clause |
| `agents/frontend.md` | 136 | Added spec reference + redefinition clause |
| `agents/mobile.md` | 93 | Same |
| `agents/design-system-engineer.md` | 91 | Was missing entirely — added the MANDATORY stack read pattern |
| `agents/quality-gate.md` | 69 | Added spec reference |
| `agents/devops.md` | 59 | Same |
| `agents/backend.md` | 60 | Same |
| `agents/fullstack.md` | 57 | Same |
| `agents/artifact-planner.md` | 147, 327 | Same |
| `agents/orchestrator.md` | 122, 276, 277, 314 | Same |
| `skills/opencode-designer/SKILL.md` | 189, 230, 272, 286 | Same |
| `skills/opencode-frontend/SKILL.md` | 69 | Same |
| `skills/opencode-quality-gate/SKILL.md` | 39, 202 | Same |
| `skills/opencode-orchestrator/SKILL.md` | 65, 91, 141, 142 | Same |

**Regression smoke test:** ran a thin contract through `visual-audit-check.py --contract` to verify the gate still fires correctly. The test contract had must_use_tokens declared but no source code referencing them; gate correctly returned exit 1 with token-parity 0% → expected NEEDS_FIX behavior. Pipeline works.

---

## Next step

Open PR with:
- `.opencode/catalog/INDEX.md` + 20 system DESIGN.md + 20 template files
- All upgraded scripts (init-design-system, design-token-generator, catalog-search, design-system-fork, visual-audit-check, ui-polish-audit)
- New `ui-ux-pro-max/` skill folder
- Upgraded agent files (designer, frontend, mobile, quality-gate, design-system-engineer, orchestrator)
- Updated harness awareness (AGENTS.md, SKILLS.md, orchestrator step 4.5)
- v2 visual-quality-contract.md template + v2 visual-rubric.md
- Plan file `.opencode/plans/ui-ux-open-design-upgrade.md`
- Both evidence summaries

Plan status: **PASS_FOR_SLICE**. Slice boundary: foundation + policy migration both shipped and eval-clean.
