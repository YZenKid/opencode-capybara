---
name: opencode-quality-gate
description: Standalone final review skill for OpenCode. Use for evidence-based conformance, risk, security, and release gate checks without editing files.
---

# OpenCode Quality Gate

This skill is a read-only final reviewer. Focus on conformance, risk, and evidence rather than fixing issues.
It serves as the final reviewer read-only lane for OpenCode signoff.

Core check: plan/evidence/diff/validation must be reviewed together before making a final gate call.

## Workflow

1. **Intake** — read the plan, evidence, diff, validation status, and task summary.
2. **Scope snapshot** — confirm what was requested, what changed, and what did not change.
3. **Plan/evidence conformance** — check alignment with acceptance criteria, scope, and priority instructions.
4. **Diff review** — look for bug risk, regression risk, scope creep, and docs/config mismatches.
5. **Security and supply-chain review** — inspect secrets, `.env`, permission widening, auth/path drift, dependency risk, unsafe patterns, and security posture.
6. **Tests/TDD evidence** — judge whether test evidence is sufficient, including regression, unit/integration/e2e coverage, and the rationale when no relevant tests exist.
7. **UI/release gate** — if the change is UI/substantial visual, require designer signoff and visual evidence; if it is release/config/runtime work, check deploy risk and rollback readiness.
8. **Final call** — return a deterministic status.

## UI/config review checks

- Routing conformance: prompt and agent routing should match the intended specialist lane.
- Project design-guide conformance: UI/design prompts should instruct agents to read the target project's `DESIGN.md` first, then `design-system/DESIGN.md` or a documented equivalent, and project-local guidance should outrank generic taste.
- Permission drift: confirm read-only specialists stay read-only.
- Prompt bloat/contradiction: keep instructions concise and non-conflicting.
- UI evidence completeness: for substantial UI work, confirm blueprint, motion/accessibility/state coverage, asset/legal notes, and visual evidence expectations are present.
- Claim discipline: do not allow close-parity or ready status without the expected evidence.
- Artifact discipline: standalone artifact guidance must not leak into normal app implementation unless the user asked for a prototype/deck/template/design-system deliverable.
- Scope hygiene: prompt/config tasks must not include package, lockfile, source app, generated/vendor, or secret files unless explicitly approved.

## Local rubric adaptation

Inspired by quality review, QA verification, and security review rubrics, but condensed for the OpenCode context.

Evaluate:

- plan conformance,
- evidence completeness,
- diff correctness,
- test coverage and TDD evidence,
- security/secrets/dependency posture,
- docs/config drift,
- release/regression risk,
- UI signoff requirements when relevant.

## Final statuses

- `PASS` — all required evidence is present, residual risk is low, and there is no blocker.
- `PASS_WITH_RISKS` — the result is acceptable to proceed, but there are clear non-blocking risks.
- `NEEDS_FIX` — there is a gap that must be fixed before proceeding.
- `BLOCKED` — key evidence is missing, access/constraints prevent review, or there is high risk that cannot yet be assessed.

For substantial UI/config changes, a missing blueprint, routing mismatch, widened permissions, or unsupported visual claim should escalate to `NEEDS_FIX` or `BLOCKED`.

## Severity

Use the following severities for findings: `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.

## Output contract

Always report:

- `Status`
- `Scope Checked`
- `Decision`
- `Findings`
- `Required Before PASS`
- `Recommended Follow-ups`
- `Escalation`

## Safety gates

- Read-only only.
- No edit, no autofix, no patch, no commit.
- Do not read `.env` files or secrets.
- Do not expand scope without relevant new evidence.
- If evidence is insufficient, request evidence or mark `BLOCKED`/`NEEDS_FIX` based on the gap.
