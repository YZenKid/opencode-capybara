# UI/UX Lane Routing Cheatsheet — UI/UX Pro Max

This is the routing table. When a UI/UX task arrives, decide which lane owns it.

## Decision tree

```
Is the task visual / user-facing / design-related?
├─ No  → not a UI/UX task. Route elsewhere.
└─ Yes ↓

Is the task substantial UI (greenfield, revamp, image-heavy, taste-sensitive, multi-page)?
├─ No  (tiny fix, bounded tweak, bug fix)
│   ├─ Web    → @frontend (with @designer if visual direction unclear)
│   ├─ Mobile → @mobile
│   └─ Token / primitive change → @design-system-engineer
└─ Yes ↓

Is the task design direction (no implementation)?
├─ Yes → @designer (must select from Open Design catalog first)
└─ No ↓

Is the task web implementation from a clear design handoff?
├─ Yes → @frontend (load tokens from catalog; implement from cited template)
└─ No ↓

Is the task mobile implementation from a clear design handoff?
├─ Yes → @mobile (verify mobile-tested system or document translation risk)
└─ No ↓

Is the task adding a shared token / primitive / component API?
├─ Yes → @design-system-engineer (search catalog first; fork if needed)
└─ No ↓

Is the task the final conformance / risk review of substantial UI?
├─ Yes → @quality-gate (mechanical catalog checks mandatory)
└─ No ↓

Default → @designer (they will route further as needed)
```

## What "substantial UI" means (precise)

A task is **substantial UI** if any of the following is true:

- `greenfield` mode (new app / new product)
- The user mentions "redesign", "refresh", "revamp", "rebrand"
- The surface is image-heavy (hero photography, product photography)
- The task is a multi-page surface (≥3 pages) with shared tokens
- The user provides a reference URL/screenshot for visual parity
- The aesthetic is taste-sensitive (the user names a vibe: "cozy", "editorial", "claymorphism")
- The domain requires warmth (community, craft, food, agriculture, artisan, organization)

If none of these apply, the task is **non-substantial** and can skip the catalog-mandatory workflow.

## Lane obligations under the Open Design policy

| Lane | Mandatory on substantial UI | Skip on non-substantial |
|---|---|---|
| `@designer` | `catalog-decision.md` + v2 DESIGN.md + visual contract with `catalog_citation` | Existing workflow |
| `@frontend` | Load tokens from `.opencode/catalog/.../tokens.{css,json}`; cite template in PR | Existing workflow |
| `@mobile` | Verify mobile-tested system or document translation risk; derive iOS/Android theme from `tokens.json` | Existing workflow |
| `@design-system-engineer` | Search catalog before adding new tokens; fork via `design-system-fork.py` with audit | Existing workflow |
| `@quality-gate` | Run `visual-audit-check.py --contract`; require mechanical catalog pass; reject missing citation with `NEEDS_FIX` | Existing workflow |
| `@orchestrator` | Verify `catalog-decision.md` exists before routing to `@frontend`/`@mobile` | Existing workflow |

## Mechanical checks per lane (for self-verification)

### @designer
- `python3 ~/.config/opencode/scripts/init-design-system.py --list-systems` returns ≥20
- `python3 ~/.config/opencode/scripts/catalog-search.py --pair --query "<task>"` returns a recommendation
- `.opencode/evidence/<task-id>/catalog-decision.md` exists with chosen pair + rejected alternatives

### @frontend
- `.opencode/generated-design/tokens.json` exists with ≥5 named colors
- `visual-audit-check.py --contract <path> --token-parity` exits 0 (parity ≥ 80%)
- No inline `#hex` in component files (one-off values labeled)

### @mobile
- `tokens.json` is referenced in `colors.ts` / `Theme.swift` / `app_colors.dart`
- Touch targets ≥ 44x44pt (verify via visual check or measurement)
- iOS/Android theme variables are generated from `tokens.json` (even if hand-written, document the source)

### @design-system-engineer
- `catalog-search.py --query "<token>"` was run before adding a new shared token
- Forks use `design-system-fork.py` and contain `Catalog Citation (this fork)` + `Deviation Audit` blocks
- `tokens.json` provenance has `system` + `source` + `license` fields

### @quality-gate
- `visual-audit-check.py --contract <path>` exits 0
- `ui-polish-audit.py --strict-catalog` exits 0
- `visual-rubric.md` v2 has all 10 Catalog Citation Check rows passing
- Screenshots exist in `.opencode/evidence/<task-id>/` (NOT just HTML diffs)

## Forbidden

- Inventing hero/nav/dashboard anatomies from prose without catalog selection.
- Skipping `deviation_audit` when forking a catalog system.
- Hand-editing `tokens.json` instead of regenerating from the catalog.
- Shipping UI without a `catalog_citation` block in the visual contract.
- Treating the catalog as inspiration only (it is the source of truth).
- Adding a 7th way to write DESIGN.md (v2 is the standard).

## See also

- `references/catalog-quickstart.md` — one-pager for the catalog
- `references/anti-slop-playbook.md` — catalog replacements for known slop patterns
- `.opencode/docs/SKILLS.md` §"UI/UX design system source of truth" — the policy that drives this routing
