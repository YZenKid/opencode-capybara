---
name: opencode-quality-gate
description: Standalone final review skill for OpenCode. Use for evidence-based conformance, risk, security, and release gate checks without editing files.
---

# OpenCode Quality Gate

This skill is a read-only final reviewer. Focus on conformance, risk, and evidence rather than fixing issues.
It serves as the final reviewer read-only lane for OpenCode signoff.

Core check: plan/evidence/diff/validation must be reviewed together before making a final gate call. When durable runtime state is used, include `.opencode/state/` run/task/mailbox/worktree/verification summaries in the final review basis.

Mode-aware check: for Greenfield App Accelerator, verify Plan Quality Gate status, `PASS_FOR_SLICE` safety, claim level, creative-depth evidence, and validation. For Maintenance Stability Mode, verify regression evidence and smallest safe diff rationale; do not block only because greenfield product thesis or 2-3 creative alternatives are absent. For Creativity Fast Path, allow lighter draft/prototype/exploration evidence, but verify that claim level stayed exploratory, assumptions/confidence are explicit, hard rails were not bypassed, and any strong completion claim went through a Promotion Gate first.

## Trigger / skip

- Trigger: non-trivial implementation, prompt/config/routing change, security-sensitive change, substantial UI/release claim, or any task where a `done` / `ready` / `PASS` claim needs independent evidence-based review.
- Skip: trivial low-risk edits with no completion claim, or tasks with no concrete diff/evidence to inspect yet.

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
3. **Plan depth audit** — verify plan meets minimum depth requirements (see Plan Depth Gate below). If plan is shallow, return `NEEDS_FIX` with specific depth failures.
4. **Plan/evidence conformance** — check alignment with acceptance criteria, scope, priority instructions, and source strategy.
5. **Diff review** — look for bug risk, regression risk, scope creep, and docs/config mismatches.
6. **Security and supply-chain review** — inspect secrets, `.env`, permission widening, auth/path drift, dependency risk, unsafe patterns, and security/privacy posture (PII, session/token, tenant isolation, payment/upload boundaries).
7. **Tests/TDD evidence** — judge whether test evidence is sufficient, including regression, unit/integration/e2e coverage, and the rationale when no relevant tests exist.
8. **Source trace gate** — for material factual, product, visual, and technical claims, verify whether they are repo-backed, reference-backed, docs-backed, runtime-backed, or explicitly first-principles-driven. Unsupported certainty is a finding.
9. **Generator-first conformance** — for new framework artifacts, verify official CLI/scaffold/generator/MCP was used when available, or fallback evidence exists.
10. **Project playbook conformance** — for framework-managed artifacts, verify `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` were read when present, or that `/init-harness` / discovery follow-up was used when they were missing or stale.
11. **UI/release gate** — if the change is UI/substantial visual, require designer signoff, accessibility evidence (semantics/focus/labels/contrast/motion), and visual parity evidence before strong parity claims; if it is release/config/runtime work, check deploy risk and rollback readiness.
12. **Final call** — return a deterministic status.

## Plan Depth Gate

Before reviewing implementation, quality-gate MUST verify plan depth. If plan is shallow, return `NEEDS_FIX` immediately.

**Minimum depth requirements:**

| Metric | Minimum |
|---|---|
| Total plan lines | 5000 |
| Goal + Non-goals words | 200 |
| Requirements count | 10 |
| Requirements words | 500 |
| Acceptance Criteria count | 8 |
| Acceptance Criteria words | 300 |
| UI pages (greenfield) | 3 |
| Words per UI page | 1000 |
| Components in inventory | 20 |
| Implementation steps | 50 |
| Validation commands | 10 |

**State coverage requirement:**
Every component in the inventory must have state coverage: empty, loading, error, success. Missing state coverage = `NEEDS_FIX`.

**Enforcement:**
If any metric fails, return `NEEDS_FIX` with specific failures listed. Do not proceed to implementation review until plan depth is adequate.

**Status mapping for plan depth:**
- `NEEDS_FIX`: Plan under 5000 lines, or any metric below minimum
- `NEEDS_FIX`: Missing state coverage for components
- `NEEDS_FIX`: UI spec under 1000 words per page
- `NEEDS_FIX`: Implementation steps under 50

## Reference Pack Gate

For greenfield/UI-heavy/substantial visual work, quality-gate MUST verify plan includes a reference pack.

**Minimum reference pack requirements:**
- Minimum 3 reference screenshots/URLs, OR explicit first-principles rationale
- Reference pack must cover:
  1. Visual direction / aesthetic family
  2. Layout / composition patterns
  3. Component / interaction patterns
  4. Asset / image style
  5. Motion / transition style

**Enforcement:**
If reference pack is missing, return `NEEDS_FIX`. Do not proceed to implementation review until reference pack is adequate.

## Anti-Generic Landing Page Gate

For greenfield/UI-heavy/substantial visual work, quality-gate MUST check plan for mechanical failures.

**Hard fail patterns (mechanical failures, not taste preferences):**
- Centered gradient hero without product/domain composition
- Generic "modern clean" without source-backed specifics
- Fake dashboard metrics or arbitrary KPI numbers
- Emoji icons or numeric-only service icons
- Placeholder imagery or blank image frames
- Repeated card/grid anatomy across sections (card spam)
- Abstract blobs, floating UI cards, CSS glass panels as hero
- Vague neon blobs or default purple/blue glow
- Debug/internal copy, server labels, port numbers in UI
- Lorem text or placeholder copy in user-facing UI
- Missing hero composition
- Missing image strategy per visual section
- Missing motion motivation
- Missing reduced-motion support

**Enforcement:**
If any hard fail pattern is present, return `NEEDS_FIX`. These are mechanical failures, not taste preferences.

## Design Depth Gate

For greenfield/UI-heavy/substantial visual work, quality-gate MUST verify plan explicitly states design depth items.

**Minimum design depth requirements:**
- Design Read
- Craft dials (`DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`)
- Page-by-page UX blueprint (minimum 3 pages)
- Section-level visual spec (minimum 5 sections per page)
- Component inventory (minimum 20 components)
- Asset/image decision per visual area
- Motion system and reduced-motion strategy
- Accessibility gate
- Validation evidence plan

**Enforcement:**
If any design depth item is missing, return `NEEDS_FIX`. Do not proceed to implementation review until design depth is adequate.

## Remediation worklist contract

For any status other than `PASS` (`NEEDS_FIX`, `BLOCKED`, or `PASS_WITH_RISKS`), include a structured remediation worklist. Quality gate stays read-only: prescribe fixes and validation, but do not edit, autofix, patch, commit, or execute remediation.

Each remediation item must include:

- `finding`: concise issue tied to evidence.
- `blocker_or_risk_class`: `hard_stop`, `soft_blocker`, `required_before_PASS`, or `non_blocking_follow_up`.
- `owner_lane`: target lane such as `@orchestrator`, `@fixer`, `@designer`, `@backend`, `@devops`, `@librarian`, or `user`.
- `action`: concrete remediation step.
- `validation`: command, review, evidence, or check needed after action.
- `exit_criteria`: condition that closes item.
- `requires_user_decision`: `yes` or `no`.

For `PASS_WITH_RISKS`, distinguish required-before-`PASS` work from non-blocking follow-ups. Non-blocking follow-ups may remain residual risk; required-before-`PASS` work must be explicit so orchestrator can remediate and rerun validation/gate when user needs full `PASS`.

## Open Design-inspired UI gate

For UI, visual asset, reference, motion, or design-system work, gate design taste through evidence and mechanical checks, not unsupported preference.

Required checks when relevant:

- `Design Read` present for substantial visual work.
- `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY` documented or clearly implied by existing `DESIGN.md`.
- Project `DESIGN.md` or `design-system/DESIGN.md` was read, followed, or absence/fallback recorded.
- Reference basis is explicit: repo/current UI, external references, or first-principles rationale for visual choices.
- Screenshot evidence supports readiness/parity claims: before/current/final and key responsive viewports when runnable. When before/after screenshot folders exist, require `python3 ~/.config/opencode/scripts/design-screenshot-compare.py --before-dir .opencode/evidence/<task-id>/before --after-dir .opencode/evidence/<task-id>/after --output .opencode/evidence/<task-id>/design-compare.md` evidence.
- For source-approved 1:1 tasks, require source inventory plus evidence that upstream file/component/layout anatomy was reused/adapted, not merely reinterpreted.
- Accessibility evidence covers contrast, semantics, focus, labels, keyboard/touch, alt text, and reduced-motion. For polish-mode or substantial UI claims, require `python3 ~/.config/opencode/scripts/ui-polish-audit.py --project-root .` and `python3 ~/.config/opencode/scripts/design-audit.py --project-root .` results or explicit rationale why they are inapplicable.
- For substantial UI debt-sensitive projects, require `python3 ~/.config/opencode/scripts/design-debt-tracker.py --project-root .` report or explicit rationale why design debt tracking is not needed for this slice.
- Motion evidence explains purpose and reduced-motion fallback; no gratuitous motion claim.
- Asset/image evidence includes generation decision, dimensions, alt/decorative strategy, legal notes, integration notes, `quality_bar`, and `reject_if`.
- Anti-AI-slop mechanical failures checked: hero fit, nav single-line, CTA contrast/wrap/duplicate intent, eyebrow restraint, layout repetition, image strategy, motion motivation, reduced-motion, fake dashboards/placeholders/generic neon.
- Requested Aesthetic Fidelity Gate checked: explicit requested style has grammar (user phrase -> tokens -> surfaces -> layout rules -> reject_if) and final evidence shows matching tokens, surfaces, layout, hero, copy, and assets.
- Card Spam / Layout Repetition Gate checked: repeated card/grid anatomy across substantial sections is a mechanical failure when it replaces purposeful section composition.
- User-facing Copy Gate and Fake Metric / Debug Artifact Gate checked: debug/internal copy, port/server labels, arbitrary KPI/dashboard numbers, fake controls, placeholder claims, and local dev artifacts are blockers unless explicitly demo/dev and labeled.
- Hero Composition Gate checked: placeholder/abstract hero, floating cards, CSS glass panels, or generic blobs are `NEEDS_FIX` when imagery/product/domain composition matters.

### Status mapping for UI/design

- `BLOCKED`: required evidence absent and reviewer cannot assess claimed UI/design outcome; screenshot/access/design-system/reference evidence missing for strong readiness/parity claim.
- `NEEDS_FIX`: concrete mechanical failure exists: contrast/wrap/layout break, missing reduced-motion, missing asset/legal notes, unreviewed generic AI imagery, unsupported copied reference, widened permission/read-only violation, requested design scope not done, or strong claim without source basis.
- `NEEDS_FIX`: also use for substantial UI with explicit requested aesthetic mismatch, missing style grammar, card spam/layout repetition, fake metrics/debug copy, user-facing internal artifacts, or placeholder/abstract hero when imagery matters. These are not pure taste.
- `NEEDS_FIX`: for source-approved `1:1`/`clone`/`port`/`copy from` tasks when source inventory, visual comparison, or evidence of actual upstream anatomy/file/component reuse/adaptation is missing, or when the result is mostly original generated UI/code even if build/tests pass.
- `PASS_WITH_RISKS`: implementation appears acceptable but evidence has non-blocking gaps or residual visual risk.
- `PASS`: evidence complete enough; no blocker; residual risk low.

Pure taste preference without request/design-system/evidence support is `LOW` or follow-up only. Do not block because reviewer personally prefers another style.

## UI/config review checks

- Routing conformance: prompt and agent routing should match the intended specialist lane.
- Project design-guide conformance: UI/design prompts should instruct agents to read the target project's `DESIGN.md` first, then `design-system/DESIGN.md` or a documented equivalent, and project-local guidance should outrank generic taste.
- Source-trace conformance: material conclusions and recommendations should identify repo evidence, docs, references, screenshots, or explicit first-principles basis.
- Plan-grounding conformance: for non-trivial plan-bound work, require `Execution Source of Truth`, `Existing Patterns / Reuse`, `Source Anatomy`, `Reference Map`, and explicit Confirmed-vs-Assumed labels. If implementation or final claims rely on plan statements such as `already exists`, `already running`, `already configured`, or `current repo has` without confirming file path/command/runtime evidence, return `NEEDS_FIX`.
- Open Source Reuse conformance: if the user provided an open source reference and the license is permissive (MIT, BSD, Apache-2.0, ISC, Unlicense, CC0, MPL-2.0), do not penalize direct reuse/adaptation; prefer evidence that source anatomy/components/code were reused appropriately. Return `NEEDS_FIX` when the agent ignored a reusable permissive source and invented replacement UI/code without evidence-backed reason. For copyleft/caution licenses (LGPL, GPL, AGPL, SSPL, custom/nonstandard), verify the agent escalated with license/risk note instead of silently reusing or silently discarding. For no-license/unclear cases, verify the agent asked or recorded why reuse was skipped — do not assume blocked by default.
- Permission drift: confirm read-only specialists stay read-only.
- Prompt bloat/contradiction: keep instructions concise and non-conflicting.
- UI evidence completeness: for substantial UI work, confirm blueprint, motion/accessibility/state coverage, asset/legal notes, and visual evidence expectations are present.
- Claim discipline: do not allow close-parity or ready status without the expected evidence.
- Creativity Fast Path promotion discipline: `draft`, `prototype`, or `exploration` output may pass with mode-appropriate evidence, but any `done`, `ready`, `production-ready`, or release-ready claim without promotion evidence is `NEEDS_FIX` or `BLOCKED` depending on risk.
- Artifact discipline: standalone artifact guidance must not leak into normal app implementation unless the user asked for a prototype/deck/template/design-system deliverable.
- Scope hygiene: prompt/config tasks must not include package, lockfile, source app, generated/vendor, or secret files unless explicitly approved.
- Generator-first conformance: flag `NEEDS_FIX` when new Laravel controllers/models/migrations/FormRequests/policies/jobs/events/listeners/mail/notifications/resources/factories/seeders/tests or new shadcn `components/ui/*` artifacts were manually created without command/tool evidence or fallback rationale. This applies to existing-app development too, not only from-scratch work. **Manually creating components that a generator/CLI can produce is a mechanical failure — do not allow `PASS` or `PASS_WITH_RISKS` for generator-bypassed UI components.**
- AI-slop conformance: for substantial UI, flag `NEEDS_FIX` when any of these mechanical failures are present in shipped UI: card spam / repeated grid anatomy, fake metrics or arbitrary KPIs, debug/internal copy or port numbers in UI, placeholder imagery or blank image frames, centered gradient hero without product/domain composition, generic "modern clean" without source-backed specifics, abstract blobs or CSS glass panels as hero, lorem text, missing reduced-motion support, missing state coverage (empty/loading/error/success). **Slop-containing UI must not receive `PASS` or `PASS_WITH_RISKS`.**
- Project playbook conformance: flag `NEEDS_FIX` when material manual framework artifact creation happened without reading `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present, or without `/init-harness` / discovery follow-up when those docs were missing or stale.
- Existing generated-file customization is allowed when evidence states customization scope.

## Local rubric adaptation

Inspired by quality review, QA verification, and security review rubrics, but condensed for the OpenCode context.

Evaluate:

- plan conformance,
- evidence completeness,
- diff correctness,
- test coverage and TDD evidence,
- security/secrets/dependency posture,
- docs/config drift,
- generator-first compliance for detected stacks,
- release/regression risk,
- UI signoff requirements when relevant.

This lane now absorbs the former standalone security-risk-reviewer, accessibility-reviewer, and visual-parity-auditor responsibilities at final gate time.

## Project memory gate

During review, verify:
- `@orchestrator`/`@fixer` searched `.opencode/memory/knowledge.json` before starting if it exists,
- high-signal findings were saved directly (importance `high` or well-justified `medium`),
- borderline/high-value findings were proposed instead of silently discarded,
- memory findings that affected the task are referenced in evidence,
- `python3 ~/.config/opencode/scripts/project-memory.py --cleanup --archive-old` was run before final completion on non-trivial work.

If a task produced reusable high-value knowledge but no memory was saved or proposed, add it as a `required_before_PASS` remediation item.

### Quality-gate memory proposal authority
`@quality-gate` may also create proposals for important lessons discovered during review that the implementation lanes missed.

### Proposal review during gate
List pending proposals and decide per proposal:
- **apply**: if lesson is reusable and not duplicate,
- **archive**: if outdated or irrelevant,
- **leave pending**: if user decision is needed.

```bash
python3 ~/.config/opencode/scripts/project-memory.py --list-proposals
python3 ~/.config/opencode/scripts/project-memory.py --apply-proposal <proposal-id>
```

## Functional evidence gate

Do not return `PASS` or `PASS_WITH_RISKS` from mechanical checks alone.

Default runnable path for app/release/API/PWA work:
- run `python3 ~/.config/opencode/scripts/runtime-verify.py` with task-specific `--route`, `--asset`, and `--env` flags when the project contains `~/.config/opencode/scripts/runtime-verify.py`,
- store output under `.opencode/evidence/<task-id>/runtime-verify.json` or equivalent,
- fall back to direct-source runtime proof only when the script is unavailable or inapplicable.

Require functional evidence for each core subsystem in scope:
- real endpoint/route status,
- real asset existence and non-zero size when assets are required,
- real manifest/icon/asset-path resolution when installability/PWA is claimed,
- real env presence for env-dependent features.

## Placeholder and empty-surface gate

These are mechanical failures and map to `NEEDS_FIX`:
- 0-byte, demo, or placeholder assets when real assets are required,
- manifest referencing missing files,
- empty homepage, tagline-only landing, or placeholder primary surface when the slice claims usable MVP,
- core feature claimed complete while required env/keys/services are not configured.

## Stack-drift gate

If implemented stack/API/asset format materially diverges from the plan or project stack docs, do not allow `PASS` based only on a documentation note. Require resolution or explicit escalation.

## Final statuses

- `PASS` — all required evidence is present, residual risk is low, and there is no blocker.
- `PASS_WITH_RISKS` — the result is acceptable to proceed, but there are clear non-blocking risks.
- `NEEDS_FIX` — there is a gap that must be fixed before proceeding.
- `BLOCKED` — key evidence is missing, access/constraints prevent review, or there is high risk that cannot yet be assessed.

For substantial UI/config changes, a missing blueprint, routing mismatch, widened permissions, mechanical design failure, missing visual evidence, or unsupported visual claim should escalate to `NEEDS_FIX` or `BLOCKED`.

## Escalation

- Escalate to `@explorer` or `@librarian` when reviewer cannot confirm facts because evidence source is missing.
- Escalate to `@designer` for missing substantial UI evidence or design ambiguity before parity/readiness claims.
- Escalate to `user` only when risk hinges on an explicit owner decision rather than missing remediation.

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
- `Remediation Worklist`
- `Recommended Follow-ups`
- `Escalation`

## Safety gates

- Read-only only.
- No edit, no autofix, no patch, no commit.
- Do not read `.env` files or secrets.
- Do not expand scope without relevant new evidence.
- If evidence is insufficient, request evidence or mark `BLOCKED`/`NEEDS_FIX` based on the gap.
## Quality checklist
- [ ] Plan, diff, validation, and evidence reviewed together.
- [ ] Plan-depth gate uses proportional execution-grade depth, not arbitrary line inflation.
- [ ] Generator-first, playbook, and source-trace conformance checked when relevant.
- [ ] UI/design claims are backed by evidence, not taste.
- [ ] Remediation worklist is concrete and lane-owned for every non-PASS status.
- [ ] Final status matches actual evidence completeness and residual risk.

## Anti-patterns
- Blocking solely on missing arbitrary depth metrics.
- Returning taste-based UI critique as blocker without evidence.
- Mixing fixes into a read-only gate.
- Giving PASS when evidence or validation path is incomplete.
- Returning vague remediation with no owner or exit criteria.

## Output example

```yaml
Status: NEEDS_FIX
Scope Checked:
  - auth middleware diff
  - regression tests
  - plan + evidence
Decision: Plan adequate, implementation incomplete for rollback evidence
Findings:
  - severity: HIGH
    issue: "Refresh-token rollback note missing"
Source Basis Checked:
  - repo diff
  - test output
  - plan worklist
Required Before PASS:
  - "Add rollback note in evidence and rerun quality gate"
Remediation Worklist:
  - finding: "Missing rollback note"
    owner_lane: "@fixer"
    action: "Document rollback behavior in evidence"
    validation: "quality-gate rerun"
    exit_criteria: "rollback note present"
    requires_user_decision: no
Escalation: none
```


## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
