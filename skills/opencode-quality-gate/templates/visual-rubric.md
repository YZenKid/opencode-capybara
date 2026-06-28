# Visual Quality Rubric

> **v2**: extends v1 with mechanical catalog checks. For substantial UI, run with `visual-audit-check.py`.

**Task ID**: {{task_id}}
**Reviewer**: @quality-gate
**Date**: {{review_date}}
**Schema version**: v2

---

## Screenshot Evidence

| View | Reference Path | Implementation Path |
|---|---|---|
| Desktop (1440px) | {{reference_desktop_path}} | {{implementation_desktop_path}} |
| Tablet (768px) | {{reference_tablet_path}} | {{implementation_tablet_path}} |
| Mobile (390px) | {{reference_mobile_path}} | {{implementation_mobile_path}} |

---

## Catalog Citation Check (v2 — mechanical)

> These rows MUST pass for substantial UI. Any `no` here is a mechanical failure → `NEEDS_FIX`.

| Check | Result (yes/no/n-a) | Evidence / Notes |
|---|---|---|
| **Catalog citation block present in visual-quality-contract.md?** | | |
| **Design system URL points to open-design.ai/plugins/systems/?** | | |
| **Template URL points to open-design.ai/plugins/templates/?** | | |
| **Pair rationale written (≥2 sentences)?** | | |
| **Deviation audit populated (or `deviation_audit: []` with "no deviations" note)?** | | |
| **must_use_tokens declared?** | | |
| **must_avoid_token declared?** | | |
| **Tokens used in implementation match must_use_tokens (token parity ≥80%)?** | | |
| **Implementation avoids every entry in must_avoid_token?** | | |
| **visual-audit-check.py exits 0 against this contract?** | | |

---

## Taste & Texture Checks

| Check | Result (yes/no) | Evidence / Notes |
|---|---|---|
| **Feels real vs template?** | | |
| **Human warmth present?** | | |
| **Domain texture present?** | | |
| **Decorative abstraction dominating?** | | |
| **Screenshot evidence of lived reality?** | | |
| **Reference essence captured?** | | |
| **Sterile/corporate feel absent?** | | |

---

## Structured Contract Compliance

| Surface | must_show respected? | reject_if absent? | fake_warmth avoided? | template_smells absent? |
|---|---|---|---|---|
| Hero | | | | |
| Product | | | | |
| Companion | | | | |
| Garden | | | | |
| Deck | | | | |
| Dashboard (v2) | | | | |
| Pricing (v2) | | | | |
| Onboarding (v2) | | | | |

---

## Image Strategy Compliance

| Surface | Image decision | Real photography present? | No placeholder? | No abstract illustration/pattern card? |
|---|---|---|---|---|
| Hero | | | | |
| Product | | | | |
| Companion | | | | |
| Garden | | | | |
| Deck | | | | |

---

## Catalog Template Anatomy Compliance (v2)

> Per chosen catalog template (e.g. example-aerocore), verify the implementation kept the section anatomy unless deviation_audit justifies otherwise.

| Section (from template anatomy) | Present? | Deviation? | Deviation reason |
|---|---|---|---|
| 1. | | | |
| 2. | | | |
| 3. | | | |
| 4. | | | |
| 5. | | | |
| 6. | | | |
| 7. | | | |

---

## Failure Summary

If any check above is `no`, document the failure below with severity.

| Surface | Failure | Severity (hard_stop / required_before_PASS / non_blocking) | Owner |
|---|---|---|---|
| | | | |

---

## Overall Assessment

**Catalog Citation**: pass / fail (v2 mechanical)
**Token Parity**: pass / fail (v2 mechanical, ≥80%)
**Template Anatomy**: pass / fail (v2 mechanical, ≥80% of sections present)
**Reference Feel Parity**: pass / fail
**Domain Texture Gate**: pass / fail
**Image Strategy Enforcement**: pass / fail
**Overall Status**: PASS / PASS_WITH_RISKS / NEEDS_FIX / BLOCKED

---

## Notes

Any additional reasoning, edge cases, or follow-ups.

---

## v1 → v2 migration notes

- Added "Catalog Citation Check" block (10 mechanical rows).
- Added "Dashboard / Pricing / Onboarding" rows to surface coverage.
- Added "Catalog Template Anatomy Compliance" block (per-section).
- v1 rubric still valid for non-substantial UI; v2 is required for substantial UI claims.
