# Plan: Deep Open-Design Integration for UI/UX Lanes

**Plan ID**: `ui-ux-open-design-upgrade`
**Mode**: Maintenance Stability + bounded capability upgrade
**Plan Quality Gate (draft)**: `PASS_FOR_SLICE` (slice = greenfield/substantial UI; legacy/small UI keeps existing path until migrated)
**Owner lane**: `@designer` (design authority), `@quality-gate` (signoff), `@skill-improver` (routing)
**Executor lanes**: `@frontend`, `@mobile`, `@design-system-engineer`, `@fixer`
**Started**: 2026-06-28
**Target release**: 2026.07.x

---

## 0. Why this plan exists (Confirmed-vs-Assumed audit)

### Confirmed (repo/runtime evidence)

- `confirmed_repo`: `~/.config/opencode/agents/{designer,frontend,mobile,quality-gate,design-system-engineer}.md` already define a `Reference Feel Parity Gate`, `Structured Design Output Contract` (`must_show`/`must_not_show`/`reject_if`/`fake_warmth_patterns`/`template_smells`), and explicit anti-AI-slop rules. The structure is right; the *substance* is missing.
- `confirmed_repo`: `~/.config/opencode/skills/opencode-quality-gate/templates/visual-quality-contract.md` and `visual-rubric.md` exist but the visual-rubric is `Hero/Product/Companion/Garden/Deck` only — no coverage for SaaS dashboards, B2B tools, fintech, mobile-native, or retro/editorial surfaces.
- `confirmed_repo`: `skills/opencode-designer/references/DESIGN-MD-TEMPLATE.md` is a generic stub — it has sections but no concrete token table, type scale, motion scale, or component variant matrix an implementation lane can use without rewriting.
- `confirmed_repo`: `skills/ui-ux-pro-max/` exists but is **empty** (only `scripts/__pycache__/`). It is currently dead weight.
- `confirmed_repo`: `scripts/{init-design-system,design-audit,design-review-bundle,design-source-importer,design-token-generator,design-screenshot-compare,ui-polish-audit,visual-audit-check,verify-visual-quality-evidence}.py` already exist. The catalog side (`design-source-importer`, `design-token-generator`, `design-audit`) is **not yet wired to any external source**. They will form the runtime spine of this plan.
- `confirmed_repo`: AGENTS.md and `.opencode/docs/SKILLS.md` do not currently mention `open-design.ai` as an authoritative reference. Harness awareness is the first blocker — until SKILLS.md names the catalog, no agent will route to it.

### Assumptions (label, reversible, escalate if violated)

- `assumption`: The Open Design catalog is the right anchor for *generic, brand-neutral* design systems. It is Apache-2.0 / open format. The user's existing product brand (if any) overrides catalog defaults — never the other way around. *Upgrade path: swap or supplement catalog if user supplies a private brand kit.*
- `assumption`: 150 design systems × 290 templates is enough to cover 80%+ of greenfield asks. *Upgrade path: add a per-project DESIGN.md extension block for brand-specific tokens; catalog becomes fallback.*
- `assumption`: 9Router `medium` model can faithfully follow a 6-step design read + 3-craft-dial discipline when the prompt explicitly names them. *Upgrade path: if eval shows drift, move `@designer` to `high`.*

### Unverified (do not pretend otherwise)

- `unverified`: How often local subagents actually browse `open-design.ai` live vs. relying on cached material. *Probe via plan-evals.*
- `unverified`: Whether the existing `init-design-system.py` produces a DESIGN.md compatible with Open Design's expected schema. *Probe: run it on a scratch project and diff against Open Design's "Inspired by Linear" example.*

---

## Goal

Integrate Open Design as a concrete, cited design-system source of truth for substantial UI work so design direction, implementation, and quality-gate checks stop relying on generic taste prose alone.

## Validation Commands

- `node scripts/agent-boundary-check.mjs`
- `node scripts/skill-contract-check.mjs`
- `node scripts/capability-registry-check.mjs`
- `node scripts/evidence-contract-check.mjs`
- `npm run test:prompt-gates`

## Evidence Requirements

- `.opencode/evidence/ui-ux-open-design-upgrade/discovery.md`
- `.opencode/evidence/ui-ux-open-design-upgrade/verification.md`
- `.opencode/evidence/ui-ux-open-design-upgrade/index.json`
- Prompt/routing/script diffs that show where the catalog-citation workflow is enforced

## Final Planning Summary

This roadmap is a governance upgrade plan, not proof of full implementation. A valid evidence bundle for it must prove the roadmap artifact is grounded in real repo inspection and can be looked up by task id, while future slices still have to ship the runtime/design-system behavior it proposes.

## 1. Problem statement (anti-AI-slop root cause)

Generated UI currently fails not because of missing rules — the **rules already exist** (`@designer` has 256 lines, `@quality-gate` has 283). It fails because:

| Failure mode | Root cause |
|---|---|
| Centered gradient hero | Designer has no concrete *catalog* of hero anatomies; falls back to prose |
| "Modern clean" generic SaaS | No design system is *selected* before implementation; everything looks the same |
| Card spam | Section-anatomy variation comes from memory, not from a token/grammar library |
| "Foto menyusul" placeholders | No enforcement that hero/product/community sections declare image strategy up front |
| Decorative fake metrics | No design system carries a credible KPI grammar to imitate |
| Wrong aesthetic in wrong context | No `material grammar translation` library — "claymorphism" maps to whatever the model thinks |
| Designer/frontend disagree | Visual contract has `must_show/reject_if` but **no `must_use_token` or `must_use_pattern` field** — implementation lane is free to interpret |
| 6 empty `ui-ux-pro-max` skill | No one owns the meta-skill for pro-grade UI work |

The fix is **not more prose rules**. The fix is: **lock design decisions to a concrete, browsable, downloadable catalog of proven design systems and templates before any code is written**, then have the implementation lanes *cite* the catalog entry in their evidence.

---

## 2. The Open Design integration model

### 2.1 Source of truth hierarchy (locked)

```
1. User's existing project brand (DESIGN.md in repo root, if present and current)
2. Open Design catalog (150 systems + 290 templates at open-design.ai) — selected by @designer
3. Generic design principles from .opencode/docs/SHARED_POLICIES.md — fallback only
4. Agent memory — NEVER for visual direction
```

Hard rule: **the catalog is selected, not invented.** `@designer` cannot say "I'll go with a modern editorial feel." It must say "I selected `Editorial` design system (open-design.ai/plugins/systems/example-editorial) with `example-academic-paper` template variant, here is the chosen option's full DESIGN.md."

### 2.2 The DESIGN.md v2 schema (project-level)

Open Design's DESIGN.md is `~80 lines, single file, agent-readable`. We adopt it as the project standard. Replace the existing generic stub with the **open-design format** so any project generated under this plan is automatically compatible with the catalog.

Adopted schema (from `open-design.ai/plugins/systems/` excerpt):

```markdown
# Design System: <Name> (forked from <Open Design entry>)

> Category: <from catalog>
> Surface: <web | mobile | both>
> Vibe: <3-5 adjectives, e.g. "calm, dense, low-chrome, focused">

## 1. Visual Theme & Atmosphere
<2-4 sentences in real human voice, not marketing>

## 2. Color Palette & Roles
### Primary
- <name> (<hex>): <role>
- <name> (<hex>): <role>
### Surface / Ink / Accent / Semantic

## 3. Typography Scale
- Display / H1-H6 / Body / Caption
- Font family, weight, line-height, letter-spacing

## 4. Spacing & Layout
- Base unit, scale, container max-width, grid

## 5. Motion Language
- Duration scale, easing, intent (feedback/guidance/delight)
- Reduced-motion behavior

## 6. Voice & Copy
- 3 tone rules, 3 anti-tone rules, example before/after

## 7. Imagery Strategy
- Photo / illustration / icon / 3D, with rationale

## 8. Component Variants
- Button / Input / Card / Nav / Modal / Toast (variant matrix)

## 9. Anti-Patterns (Reject If)
- 5-10 concrete reject conditions in the project's domain

## 10. Source & Provenance
- open-design.ai/plugins/systems/<slug>
- License: Apache-2.0 (catalog), <project-specific for fork>
- Adapted by: <author/agent + date>
- Deviations: <list, with reason each>
```

### 2.3 The visual contract becomes enforceable (v2)

Current `visual-quality-contract.md` (139 lines) is a *checklist*. We add a **catalog-citation field** so the gate can verify a real system was selected:

```yaml
catalog_citation:
  design_system:
    name: "Editorial"
    source: "https://open-design.ai/plugins/systems/example-editorial"
    license: "Apache-2.0"
  template_pattern:
    name: "Academic Paper Deck"
    source: "https://open-design.ai/plugins/templates/example-hps-academic-paper"
  deviation_audit:
    - what: "<e.g. hero swapped to marketing variant>"
      why: "<user requested>"
      risk: "breaks reference feel parity, see reject_if #2"
  must_use_tokens: ["#0d0e10", "#5e6ad2", "Inter Display 56/64"]
  must_use_pattern: ["editorial grid 12-col", "ink-on-paper contrast"]
  must_avoid_token: ["#ffffff hero", "neon accent", "3D hero blobs"]
```

`@quality-gate` will reject any `visual-quality-contract.md` for substantial UI that does not include this block.

### 2.4 Runtime wiring

| Script (existing or new) | Role |
|---|---|
| `scripts/design-source-importer.py` | Pulls one or more design systems/templates from `open-design.ai` into `.opencode/catalog/`. Idempotent. Verifies license header. |
| `scripts/design-token-generator.py` | Reads a chosen DESIGN.md, emits Tailwind config / CSS variables / Figma tokens. |
| `scripts/design-audit.py` | Walks a UI implementation, checks tokens used vs tokens declared, flags deviations. |
| `scripts/init-design-system.py` | **Upgrade**: now seeds a DESIGN.md v2 using the catalog, not the stub. |
| `scripts/ui-polish-audit.py` | Adds a "catalog-citation present" check. |
| `scripts/visual-audit-check.py` | Upgraded to consume `must_use_tokens` / `must_avoid_token` from the contract. |
| **NEW** `scripts/catalog-search.py` | Search the local `.opencode/catalog/` (or live) by category, vibe keyword, surface type. |
| **NEW** `scripts/design-system-fork.py` | Clone a system, apply user-specific deviations, write DESIGN.md v2. |

---

## 3. The upgraded agent contracts

### 3.1 `@designer` (model: high, kept)

**Removed/relocated**: None — the prose rules stay. They are *reinforced*, not replaced.

**Added**:

1. **Catalog selection gate** (mandatory before substantial UI work):
   - If task is `greenfield` or `substance=substantial UI`, `@designer` must run `catalog-search.py --query "<domain vibe>" --surface <web|mobile|both>`.
   - Pick 2-3 candidate systems + 2-3 candidate templates from the result.
   - Document pick + rejected alternatives in `.opencode/evidence/<task-id>/catalog-decision.md`.
   - The chosen system + template **must be cited** by URL and license in the visual contract.
2. **Material Grammar Translation v2**: extend with a **pattern library** (e.g. "claymorphism" → 3 known catalog patterns that exemplify it → pick one with rationale). Stop being a single example; start being a search.
3. **Deviation transparency**: any deviation from the selected catalog system must be listed in `catalog-decision.md` with reason. Undocumented deviations → `needs-polish`.
4. **Reference Pack upgrade**: minimum 3 reference screenshots is replaced by "minimum 1 catalog system + 1 catalog template + 1 external reference (current industry standard)".

### 3.2 `@frontend` (model: low, kept)

**Added**:

1. **Token-first implementation**: before any component, read `DESIGN.md` v2 → load tokens from `.opencode/catalog/<system>/tokens.css|tailwind.config.json` (whichever the project uses). Do not re-derive tokens from memory.
2. **Catalog citation in evidence**: every material UI change must cite which catalog template the section anatomy comes from.
3. **Push-back authority upgraded**: if `DESIGN.md` exists but does not cite an Open Design source (for new projects), `@frontend` can write `design_pushback.md` asking `@designer` to add a catalog citation.
4. **Pattern-aware component selection**: instead of "use shadcn Card", the instruction becomes "use `<CatalogTemplate>/components/Card.tsx` (adapted from `example-aerocore` if a Bento-style is needed)".

### 3.3 `@mobile` (model: low, kept)

**Added**:

1. **Mobile-specific catalog section**: the catalog has 290 templates but few are mobile-first. `@mobile` must require `@designer` to select a *mobile-tested* template variant, or document the translation risk.
2. **Native-token parity**: if a design system is selected, the iOS/Android theme variables must be generated from the same token source (extend `design-token-generator.py` to output Swift/Kotlin theme stubs).
3. **Platform anti-patterns**: e.g. "Material You dynamic color override" must be rejected unless user explicitly opts in; catalog system wins by default.

### 3.4 `@quality-gate` (model: medium, kept)

**Added (high-impact, single line of behavior change)**:

1. **Catalog citation required**: for substantial UI claims, `visual-quality-contract.md` must include `catalog_citation` block. Missing → `NEEDS_FIX`, not `PASS_WITH_RISKS`.
2. **Deviation audit required**: deviations from the selected catalog system without a `deviation_audit` entry → `NEEDS_FIX`.
3. **must_use_token enforcement**: scan the implementation CSS/Tailwind for the listed tokens; missing → `NEEDS_FIX` (mechanical, not taste).
4. **Catalog source-of-truth check**: if the project has a `DESIGN.md` older than `n` days and the user has provided a new reference, `@designer` must have updated it; otherwise `NEEDS_FIX`.
5. **Visual rubric v2**: `visual-rubric.md` gets new rows: "Catalog cited?", "Token parity %", "Template anatomy used?", "Deviation count vs declared".

### 3.5 `@design-system-engineer` (model: medium, kept)

**Added**:

1. **Catalog ingestion**: when new shared tokens/primitives are needed, search the catalog first (`catalog-search.py --kind tokens`). Prefer reuse + extension over invention.
2. **Token source-of-truth**: the canonical token file location is `.opencode/catalog/<active-system>/tokens.json`. Components reference this path; no inline `#hex` in component code.
3. **Fork discipline**: when forking a catalog system, write `fork-of-<slug>.md` with `Adapted by`, `Deviations`, `License` blocks. No silent forks.

### 3.6 `@orchestrator` (model: high, kept)

**Added (routing cue only, no policy change)**:

- The Pre-flight Routing Gate now includes: "If task is `greenfield` or `substance=substantial UI`, ensure `@designer` has produced `catalog-decision.md` before `@frontend`/`@mobile` is invoked."
- This is added to the routing decision tree at the relevant step, not as a new gate (to avoid adding latency to tiny tasks).

### 3.7 `@skill-improver` (model: implicit)

- New responsibility: when `@quality-gate` returns `NEEDS_FIX` citing "missing catalog citation" more than 3 times across runs, `@skill-improver` updates the relevant skill to make the rule louder.

---

## 4. Skill upgrades (folder-level)

### 4.1 `opencode-designer/SKILL.md`

- Add §"Catalog-first workflow" at the top of the workflow section. Reorder so catalog selection is step 2 (after Design Read, before craft dials).
- Add a new reference file: `references/catalog-usage.md` with worked examples of how to pick from the catalog.
- Add `references/anti-slop-catalog.md` — concrete catalog references to copy/adapt when an AI-slop pattern is detected (e.g. "you wrote a centered gradient hero, see `example-aerocore` hero instead, here is the anatomy").

### 4.2 `opencode-frontend/SKILL.md`

- Add §"Token-first implementation". Pull from `.opencode/catalog/<active-system>/`.
- Add `references/catalog-component-mapping.md` — for the 12 most common components, show which catalog template to start from and what to adapt.
- Add `references/anti-slop-component-catalog.md` — paired anti-patterns.

### 4.3 `opencode-mobile/SKILL.md`

- Add §"Native token parity". Mobile is a token-shipping lane.
- Add `references/mobile-catalog-translation.md` — for the 6 most common mobile surfaces, which catalog template applies and what to drop (e.g. desktop hero parallax is invalid on mobile).

### 4.4 `opencode-quality-gate/SKILL.md`

- Update gate value-add to include "catalog citation verification" and "token parity check" as mechanical checks, not taste.
- Add a new template: `templates/visual-quality-contract-v2.md` (extends v1 with `catalog_citation` block).
- Update `templates/visual-rubric.md` with new mechanical rows.

### 4.5 `ui-ux-pro-max/` (currently dead — fill it)

- This becomes the **meta-skill** for UI/UX work. It is auto-loaded when `@designer`, `@frontend`, `@mobile`, or `@design-system-engineer` is active for substantial UI.
- Contents:
  - `SKILL.md` — index of all UI/UX skills, when to load which, and a "UI work checklist" of 20 items the lane must verify.
  - `references/catalog-index.md` — pointer to `.opencode/catalog/` plus the live URL.
  - `references/anti-slop-playbook.md` — playbook: for each known slop pattern, which catalog system to copy from.
  - `scripts/` — moved from `ui-ux-pro-max/scripts/__pycache__/`, plus new helper `select-catalog.py`.

### 4.6 New shared reference: `references/catalog-quickstart.md`

A single one-pager that any lane can load in <30s:
- 5 design systems by surface type (web SaaS, web editorial, mobile productivity, mobile consumer, marketing site)
- 5 templates by intent (landing, dashboard, docs, deck, prototype)
- 3 anti-patterns and their catalog-replacement
- How to fork a system

---

## 5. Execution-ready worklist / handoff contract

This is the **executor handoff prompt** that the orchestrator will issue. Each row is one task, in dependency order.

| # | Task | Lane | Depends on | Validation | Evidence |
|---|---|---|---|---|---|
| 1 | Run `catalog-search.py --init --source https://open-design.ai` to seed `.opencode/catalog/` with the 150 systems index (metadata + license only, not full content) | `@designer` (read-only) | — | Catalog index file exists, ≥150 entries, all have `license` field | `.opencode/catalog/INDEX.md`, license audit log |
| 2 | Download top 20 most-used systems (Linear, Editorial, Claude, OpenAI, Stripe-like, Tesla, etc.) full DESIGN.md into `.opencode/catalog/systems/` | `@designer` + `design-source-importer.py` | 1 | 20 DESIGN.md files, all pass v2 schema validation | file count + schema check output |
| 3 | Download top 20 most-used templates (Hero, Bento, SaaS landing, Dashboard, Mobile shell, etc.) into `.opencode/catalog/templates/` | `@designer` + `design-source-importer.py` | 1 | 20 template files | file count + manifest |
| 4 | Upgrade `init-design-system.py` to v2 — writes DESIGN.md v2 from catalog entry | `@fixer` | 2, 3 | Run on a scratch dir, output diffs against a known-good reference DESIGN.md | `python3 init-design-system.py --system editorial --out scratch/` + visual diff |
| 5 | Upgrade `design-token-generator.py` to read from catalog tokens | `@fixer` | 2 | Emits Tailwind config + CSS vars that match the chosen DESIGN.md palette | generated `tokens.css` + Tailwind config + visual check |
| 6 | Add `catalog-search.py` (CLI) — search local `.opencode/catalog/` by name, category, vibe, surface | `@fixer` | 1 | `catalog-search.py --query "editorial web"` returns ≥3 hits | CLI test output |
| 7 | Add `design-system-fork.py` — clone a system, apply user deviations, write fork file | `@fixer` | 2 | Fork the "Linear" system, change one color, verify the fork file lists the deviation | `python3 fork.py --base linear --deviate primary=#ff0066` output |
| 8 | Add `visual-quality-contract-v2.md` template | `@quality-gate` (template edit) | 2 | Template file exists, contains `catalog_citation` block | file diff + sample filled |
| 9 | Upgrade `visual-rubric.md` with `Catalog cited?`, `Token parity %`, `Deviation count` rows | `@quality-gate` | 8 | Rubric file shows the new rows | file diff |
| 10 | Upgrade `visual-audit-check.py` to enforce `catalog_citation` and `must_use_tokens` | `@fixer` | 8, 9 | Run on a test DESIGN.md + implementation; missing citation → exit 1 | CLI test output |
| 11 | Upgrade `ui-polish-audit.py` with "catalog-citation present" check | `@fixer` | 10 | Same as above | CLI test output |
| 12 | Upgrade `@designer` agent file: catalog-first workflow, deviation transparency, reference pack upgrade | `@skill-improver` | 1-11 | Agent file diffs; skill `opencode-designer/SKILL.md` updated; new `references/catalog-usage.md` and `references/anti-slop-catalog.md` exist | file diffs + content check |
| 13 | Upgrade `@frontend` agent file: token-first, catalog citation, pushback upgrade | `@skill-improver` | 1-11 | Same | file diffs |
| 14 | Upgrade `@mobile` agent file: mobile-catalog selection, native token parity, platform anti-patterns | `@skill-improver` | 1-11 | Same | file diffs |
| 15 | Upgrade `@quality-gate` agent file: catalog citation required, deviation audit, token enforcement, rubric v2 | `@skill-improver` | 8-11 | Same | file diffs |
| 16 | Upgrade `@design-system-engineer` agent file: catalog ingestion, token source-of-truth, fork discipline | `@skill-improver` | 1-11 | Same | file diffs |
| 17 | Upgrade `@orchestrator` agent file: routing cue for `catalog-decision.md` prerequisite on substantial UI | `@skill-improver` | 12-16 | Orchestrator file shows the cue | file diff |
| 18 | Fill `ui-ux-pro-max/` skill folder: SKILL.md + 3 references + 1 script | `@skill-improver` | 1-3 | Folder no longer empty, all four files exist with content | `ls -la` + size check |
| 19 | Update `.opencode/docs/SKILLS.md` — add `open-design.ai` as an authoritative reference; list new files | `@skill-improver` | 12-18 | SKILLS.md shows the new skills and references | file diff |
| 20 | Update `AGENTS.md` — add a 2-line note that UI/UX work now anchors to Open Design catalog | `@skill-improver` | 12-18 | AGENTS.md shows the note | file diff |
| 21 | Run the eval set `scripts/evals/ui-ux-catalog.yaml` (existing or new) against a small greenfield task | `@oracle` | 1-20 | Eval passes: catalog-decision.md created, design uses cited tokens, quality-gate returns PASS or PASS_WITH_RISKS only on a non-AI-slop output | eval log |
| 22 | Commit + push branch, open PR with the plan + diff + eval log | `@orchestrator` (via auto-commit policy) | 21 | PR exists, CI green | PR URL |

**Slice boundary**: tasks 1-11 are the **foundation slice** and can ship as `PASS_FOR_SLICE` to begin anchoring new greenfield work. Tasks 12-20 are the **policy migration slice**. Task 21 is the **eval slice**. Task 22 is the **release slice**. Each is independently shippable and reversible.

---

## 6. Non-negotiable implementation invariants

1. **Open Design format is the project's DESIGN.md format.** All projects under this harness use DESIGN.md v2. Legacy projects may keep their existing DESIGN.md until they need substantial UI work; then they migrate.
2. **Catalog citation is mechanical, not taste.** `@quality-gate` rejects substantial UI without it. No `PASS_WITH_RISKS` workaround.
3. **The catalog is selected, not invented.** `@designer` cannot produce a hero anatomy from prose. It must pick a system, then optionally deviate with audit.
4. **Token source is the catalog.** No inline `#hex` in component code; tokens are generated from `design-token-generator.py` and shared via Tailwind config or CSS variables.
5. **License discipline.** Every catalog-derived DESIGN.md, token file, or component includes the source URL + Apache-2.0 notice. Direct reuse of catalog assets without attribution = license violation = `BLOCKED`.
6. **Backward compatibility.** Existing `visual-quality-contract.md` and `visual-rubric.md` keep working for small/tiny UI. v2 is for substantial UI.
7. **Harness awareness.** AGENTS.md, SKILLS.md, and orchestrator all know about the catalog by the end of this plan. No "hidden upgrade" — anyone reading the harness post-rollout should see the change.

---

## 7. Do not / Reject If

- **Do not** invent hero/nav/dashboard anatomies from prose. Reject if `@designer` does so for substantial UI.
- **Do not** ship UI without a `catalog_citation` block in the visual contract. Reject if missing.
- **Do not** manually copy tokens from a catalog system into CSS — use `design-token-generator.py`. Reject if a hand-edited token file is committed.
- **Do not** allow a fork of a catalog system without a `Deviations` block. Reject if missing.
- **Do not** add a 7th way to write DESIGN.md. Reject any new design-doc template that diverges from v2.
- **Do not** treat this as a "vibe library" — the catalog is structural, not inspirational. Reject if a worker treats it as Pinterest.

---

## 8. Diff Boundary

- **In-scope (this plan)**: agents/, skills/, scripts/, .opencode/docs/SKILLS.md, AGENTS.md, new `.opencode/catalog/` directory, new evidence templates.
- **Out-of-scope**: any individual project's DESIGN.md, any user's product code, any private brand kits, the 9Router provider config, MCP server config.
- **Generated/vendor exceptions**: `.opencode/catalog/systems/*/tokens.css`, `tokens.json`, `tailwind.config.js` (when generated by `design-token-generator.py`) are allowed without per-line review as long as the generator script is reviewed and versioned.
- **Revert policy**: any single task (#1-22) can be reverted independently. Catalog files are read-only by default. Generated tokens are regenerable.

---

## 9. Acceptance criteria / Done criteria

- [ ] `.opencode/catalog/INDEX.md` exists with ≥150 entries, license per entry
- [ ] ≥20 full DESIGN.md v2 files in `.opencode/catalog/systems/`
- [ ] ≥20 template files in `.opencode/catalog/templates/`
- [ ] `init-design-system.py` v2 emits DESIGN.md v2 from a catalog entry
- [ ] `design-token-generator.py` reads from catalog and emits Tailwind + CSS
- [ ] `catalog-search.py` CLI works
- [ ] `design-system-fork.py` CLI works
- [ ] `visual-quality-contract-v2.md` template exists and is load-bearing
- [ ] `visual-rubric.md` v2 has new mechanical rows
- [ ] `visual-audit-check.py` + `ui-polish-audit.py` enforce citation
- [ ] All 5 target agent files (`designer`, `frontend`, `mobile`, `quality-gate`, `design-system-engineer`) updated with the new obligations
- [ ] `@orchestrator` has the routing cue
- [ ] `ui-ux-pro-max/` no longer empty
- [ ] `AGENTS.md` and `.opencode/docs/SKILLS.md` mention the catalog
- [ ] Eval run on a greenfield task: catalog-decision.md exists, tokens used, quality-gate PASS or PASS_WITH_RISKS only on a clean output
- [ ] PR opened with plan + diffs + eval log

---

## 10. Follow-ups / out-of-scope (post-slice)

- Live MCP server for `open-design.ai` (so `catalog-search.py` can hit the live site). *Deferred* — we cache first.
- Per-project DESIGN.md extension blocks (for private brand kits that override the catalog).
- Eval-driven auto-tuning of `@designer` model tier (medium vs high).
- A Figma plugin that round-trips catalog tokens.
- Catalog contribution: upstream patches to `open-design.ai` for new systems/templates.

---

## 11. Plan Quality Gate (self-assessed draft)

`PASS_FOR_SLICE` — the foundation slice (tasks 1-11) is independently usable. The policy migration (12-20) and eval (21) slices build on it. The whole plan is a slice, not a whole-system claim.

---

## 12. Executor handoff prompt (copy-paste ready)

```
@orchestrator execute plan: .opencode/plans/ui-ux-open-design-upgrade.md
Mode: Maintenance Stability + bounded capability upgrade
Plan Quality Gate value: PASS_FOR_SLICE
Worklist: see plan §5
Slice boundary: foundation tasks #1-11 ship independently. Policy tasks #12-20 require foundation done. Eval #21 requires all done.
Worker contract:
- scope: tasks in worklist only
- exact outcome: see Validation column per task
- file paths: see plan §5 + §8 (Diff Boundary)
- plan invariants: §6 (do not violate)
- do_not_touch: §8 out-of-scope
- validation: see Validation column per task
- evidence: see Evidence column per task
Workers execute; do not delegate further. Report back to @orchestrator when done or blocked.
On PASS of eval (#21), proceed to release #22 via auto-commit policy.
```
