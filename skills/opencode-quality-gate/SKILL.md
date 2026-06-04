---
name: opencode-quality-gate
description: Standalone final review skill for OpenCode. Use for evidence-based conformance, risk, security, and release gate checks without editing files.
---

# OpenCode Quality Gate

This skill is a read-only final reviewer. Focus on conformance, risk, and evidence rather than fixing issues.
It serves as the final reviewer read-only lane for OpenCode signoff.

Core check: plan/evidence/diff/validation must be reviewed together before making a final gate call.

Mode-aware check: for Greenfield App Accelerator, verify Plan Quality Gate status, `PASS_FOR_SLICE` safety, claim level, creative-depth evidence, and validation. For Maintenance Stability Mode, verify regression evidence and smallest safe diff rationale; do not block only because greenfield product thesis or 2-3 creative alternatives are absent.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Workflow

1. **Intake** — read the plan, evidence, diff, validation status, and task summary.
2. **Scope snapshot** — confirm what was requested, what changed, and what did not change.
3. **Plan/evidence conformance** — check alignment with acceptance criteria, scope, priority instructions, and source strategy.
4. **Diff review** — look for bug risk, regression risk, scope creep, and docs/config mismatches.
5. **Security and supply-chain review** — inspect secrets, `.env`, permission widening, auth/path drift, dependency risk, unsafe patterns, and security/privacy posture (PII, session/token, tenant isolation, payment/upload boundaries).
6. **Tests/TDD evidence** — judge whether test evidence is sufficient, including regression, unit/integration/e2e coverage, and the rationale when no relevant tests exist.
7. **Source trace gate** — for material factual, product, visual, and technical claims, verify whether they are repo-backed, reference-backed, docs-backed, runtime-backed, or explicitly first-principles-driven. Unsupported certainty is a finding.
8. **UI/release gate** — if the change is UI/substantial visual, require designer signoff, accessibility evidence (semantics/focus/labels/contrast/motion), and visual parity evidence before strong parity claims; if it is release/config/runtime work, check deploy risk and rollback readiness.
9. **Final call** — return a deterministic status.

## Open Design-inspired UI gate

For UI, visual asset, reference, motion, or design-system work, gate design taste through evidence and mechanical checks, not unsupported preference.

Required checks when relevant:

- `Design Read` present for substantial visual work.
- `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY` documented or clearly implied by existing `DESIGN.md`.
- Project `DESIGN.md` or `design-system/DESIGN.md` was read, followed, or absence/fallback recorded.
- Reference basis is explicit: repo/current UI, external references, or first-principles rationale for visual choices.
- Screenshot evidence supports readiness/parity claims: before/current/final and key responsive viewports when runnable.
- Accessibility evidence covers contrast, semantics, focus, labels, keyboard/touch, alt text, and reduced-motion.
- Motion evidence explains purpose and reduced-motion fallback; no gratuitous motion claim.
- Asset/image evidence includes generation decision, dimensions, alt/decorative strategy, legal notes, integration notes, `quality_bar`, and `reject_if`.
- Anti-AI-slop mechanical failures checked: hero fit, nav single-line, CTA contrast/wrap/duplicate intent, eyebrow restraint, layout repetition, image strategy, motion motivation, reduced-motion, fake dashboards/placeholders/generic neon.

### Status mapping for UI/design

- `BLOCKED`: required evidence absent and reviewer cannot assess claimed UI/design outcome; screenshot/access/design-system/reference evidence missing for strong readiness/parity claim.
- `NEEDS_FIX`: concrete mechanical failure exists: contrast/wrap/layout break, missing reduced-motion, missing asset/legal notes, unreviewed generic AI imagery, unsupported copied reference, widened permission/read-only violation, requested design scope not done, or strong claim without source basis.
- `PASS_WITH_RISKS`: implementation appears acceptable but evidence has non-blocking gaps or residual visual risk.
- `PASS`: evidence complete enough; no blocker; residual risk low.

Pure taste preference without request/design-system/evidence support is `LOW` or follow-up only. Do not block because reviewer personally prefers another style.

## UI/config review checks

- Routing conformance: prompt and agent routing should match the intended specialist lane.
- Project design-guide conformance: UI/design prompts should instruct agents to read the target project's `DESIGN.md` first, then `design-system/DESIGN.md` or a documented equivalent, and project-local guidance should outrank generic taste.
- Source-trace conformance: material conclusions and recommendations should identify repo evidence, docs, references, screenshots, or explicit first-principles basis.
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

This lane now absorbs the former standalone security-risk-reviewer, accessibility-reviewer, and visual-parity-auditor responsibilities at final gate time.

## Final statuses

- `PASS` — all required evidence is present, residual risk is low, and there is no blocker.
- `PASS_WITH_RISKS` — the result is acceptable to proceed, but there are clear non-blocking risks.
- `NEEDS_FIX` — there is a gap that must be fixed before proceeding.
- `BLOCKED` — key evidence is missing, access/constraints prevent review, or there is high risk that cannot yet be assessed.

For substantial UI/config changes, a missing blueprint, routing mismatch, widened permissions, mechanical design failure, missing visual evidence, or unsupported visual claim should escalate to `NEEDS_FIX` or `BLOCKED`.

## Severity

Use the following severities for findings: `BLOCKER`, `HIGH`, `MEDIUM`, `LOW`, `INFO`.

## Output contract

Always report:

- `Status`
- `Scope Checked`
- `Decision`
- `Findings`
- `Source Basis Checked`
- `Required Before PASS`
- `Recommended Follow-ups`
- `Escalation`

## Safety gates

- Read-only only.
- No edit, no autofix, no patch, no commit.
- Do not read `.env` files or secrets.
- Do not expand scope without relevant new evidence.
- If evidence is insufficient, request evidence or mark `BLOCKED`/`NEEDS_FIX` based on the gap.
## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
