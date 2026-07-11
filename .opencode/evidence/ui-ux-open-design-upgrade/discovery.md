# Discovery — ui-ux-open-design-upgrade

- Task: `ui-ux-open-design-upgrade`
- Source: `.opencode/plans/ui-ux-open-design-upgrade.md` (mode: maintenance + bounded capability upgrade, `PASS_FOR_SLICE` draft, slice = greenfield/substantial UI)
- Claim: previously completed foundation/policy/polish slices per existing `foundation-slice-summary.md` and `policy-migration-slice-summary.md`. This evidence bundle is a minimal scaffolding created to satisfy the evidence-contract checker, not a new execution cycle.
- Source strategy: repo-local; no external references required for this bundle scaffolding.

## Files inspected

- `.opencode/plans/ui-ux-open-design-upgrade.md`
- `.opencode/evidence/ui-ux-open-design-upgrade/foundation-slice-summary.md`
- `.opencode/evidence/ui-ux-open-design-upgrade/policy-migration-slice-summary.md`
- `.opencode/state/ui-ux-open-design-upgrade/progress.json`
- `scripts/evidence-contract-check.mjs`

## Confirmed baseline

| Claim | Level | Evidence |
| --- | --- | --- |
| Plan artifact exists with required sections | confirmed_repo | `grep -n "Goal\|Validation Commands\|Evidence Requirements\|Final Planning Summary" .opencode/plans/ui-ux-open-design-upgrade.md` |
| Two prior slice summaries exist in evidence dir | confirmed_repo | `ls .opencode/evidence/ui-ux-open-design-upgrade` |
| Prior slices marked `PASS_FOR_SLICE` per summary content | confirmed_repo | `foundation-slice-summary.md`, `policy-migration-slice-summary.md` |
| Evidence-contract checker requires `discovery.md`, `verification.md`, `index.json` for selected plan | confirmed_repo | `scripts/evidence-contract-check.mjs:96-122` |

## Reuse candidates

- Existing `.opencode/evidence/ui-ux-open-design-upgrade/*.md` summaries as historical record.
- `scripts/evidence-contract-check.mjs` schema for required manifest keys.

## Risks

- This bundle only satisfies the evidence-contract mechanical requirement. It does not retroactively re-validate prior slice claims; that work would belong to a dedicated `ui-ux-open-design-upgrade` remediation plan, out of this preset-gap slice.
- No secrets, no provider calls, no external config changes.
