# Quality

## Quality gate statuses
- `PASS`
- `PASS_WITH_RISKS`
- `NEEDS_FIX`
- `BLOCKED`

## Evidence contract
Every material change must end with evidence, not just claims.

Canonical task evidence path: `.opencode/evidence/<task-id>/`.

### Final summary template
```md
## Summary
- ...

## Changes
- ...

## Evidence
- Command: `npm run test:prompt-gates`
- Result: PASS
- Additional validation: ...

## Risks / Limitations
- ...

## Next Steps
- ...
```

If evidence is unavailable, write an explicit limitation note.

## Plan compliance and diff-boundary evidence

For non-trivial plan-bound work, verification evidence must include a Plan Compliance Checkpoint before any completion claim:
- plan path and task id;
- Plan Quality Gate value (`PASS` or `PASS_FOR_SLICE`); if `PASS_FOR_SLICE`, final claim must be slice-scoped only;
- Execution Source of Truth conflicts and chosen resolution, or explicit `none`;
- Non-negotiable Implementation Invariants preserved;
- Do Not / Reject If checks passed or remediated;
- worklist task status, including per-task exit criteria, `must_preserve`, `do_not_touch`, `evidence_update`, and `exit_verification` where present;
- validation commands/results;
- evidence paths updated;
- quality-gate status and remediation/risk worklist status.

Diff Boundary result evidence must list allowed file groups from the plan, actual changed files, generated-report exceptions, and out-of-boundary changes. Out-of-boundary changes require either revert or rationale in verification evidence before final quality gate.

Quality gate non-`PASS` results must become Persistent remediation evidence before final user-facing completion claim. Copy remediation/risk items into `.opencode/evidence/<task-id>/verification.md` or a plan appendix, execute non-blocked required items, rerun targeted validation, then rerun `@quality-gate` when pursuing a full completion claim.

## Quality gate remediation worklist contract

`@quality-gate` is read-only. It must not edit files, fix issues, apply patches, commit, or execute remediation. When status is `NEEDS_FIX`, `BLOCKED`, or `PASS_WITH_RISKS`, it must return a structured remediation worklist that `@orchestrator` can copy into plan/evidence and execute through the correct lane.

Each remediation item must use this shape:

```md
### Remediation item
- finding: ...
- blocker_or_risk_class: hard_stop | soft_blocker | required_before_PASS | non_blocking_follow_up
- owner_lane: @orchestrator | @fixer | @designer | @frontend | @backend | @mobile | @devops | @librarian | user | other named lane
- action: ...
- validation: ...
- exit_criteria: ...
- requires_user_decision: yes | no
```

For `PASS_WITH_RISKS`, split work into:
- `Required Before PASS`: items needed to upgrade to full `PASS`.
- `Recommended Follow-ups`: non-blocking follow-ups that can remain residual risk.

`@orchestrator` must transform non-`PASS` quality-gate output into plan/evidence sections named `Quality Gate Remediation` and/or `Risk Worklist`, execute every non-blocked item finish-first when `requires_user_decision: no`, rerun targeted validation, and rerun `@quality-gate`. Stop and ask only for `hard_stop` or `requires_user_decision: yes`.

### Quality Gate Remediation / Risk Worklist section template

```md
## Quality Gate Remediation
- Gate status: NEEDS_FIX | BLOCKED | PASS_WITH_RISKS
- Gate evidence reviewed: ...

### Worklist
1. finding: ...
   blocker_or_risk_class: ...
   owner_lane: ...
   action: ...
   validation: ...
   exit_criteria: ...
   requires_user_decision: yes | no
   execution_status: pending | in_progress | done | blocked | deferred_follow_up

## Risk Worklist
- Required Before PASS: ...
- Recommended Follow-ups: ...

## Remediation Validation
- Command/check: ...
- Result: ...
- Rerun quality gate result: ...
```

## Evidence retention categories

Use retention categories in task evidence and manifests so cleanup does not destroy gate-critical proof:

- `keep`: concise artifacts that must remain for replay, audit, or future maintenance. Examples: `discovery.md`, `verification.md`, `index.json`, final screenshots that prove visual state, command summaries, and gate verdicts.
- `summarize-and-delete`: bulky or noisy raw outputs after their key facts are copied into `discovery.md` or `verification.md`. Examples: long logs, exploratory scratch files, temporary browser traces, duplicate screenshots, and generated debug dumps.
- `never-delete-until-gate`: artifacts required to complete review or final conformance. Examples: failing repro evidence, before/after screenshots for UI work, security/privacy review notes, raw validation logs for failing/flaky commands, and quality-gate input bundles.

Do not delete `never-delete-until-gate` evidence until `@quality-gate` has recorded a verdict. After gate, either move it to `keep` if needed for replay or summarize it before deletion.

## Exemplar bundle expectations

Curated exemplar bundles should live under `.opencode/plans/` and `.opencode/evidence/<task-id>/` and include:
- plan artifact with goal, scope/mode, validation commands, evidence requirements, and final planning summary;
- `discovery.md` with source basis, mode, routing decision, and assumptions/deferred decisions;
- `verification.md` with validation commands/results and quality-gate decision or simulated exemplar verdict;
- `index.json` with `task_id`, `plan_file`, `evidence_dir`, `required_files`, `validation_commands`, retention notes, and final verdict.

Each manifest `required_files` must include `discovery.md` and `verification.md`.

## Reference trace minimum
For material planning, implementation, review, or design claims, evidence should make the source basis legible:
- key repo files or artifacts used,
- authoritative docs/source URLs or identifiers when external behavior mattered,
- reference screenshots/URLs when visual or UX choices mattered,
- unresolved assumptions and why they were still necessary,
- whether the final choice is reference-backed, repo-backed, or first-principles-driven.

If no reliable source existed, say so explicitly and keep the claim level conservative.

## Replay bundle minimum
- `task_id`
- `timestamp`
- harness/prompt version metadata
- runtime run id/status when durable execution is used
- task queue + mailbox summary when runtime state is used
- tool trace summary
- changed files summary
- validation outputs
- final verdict
- reason codes / failure category if not `PASS`

For routing-quality work, replay evidence should also preserve:
- transcript fixture score summary,
- score bands / source-mode coverage,
- release-gate readiness state,
- drift summary against the previous harness snapshot when available.

For drift-enforcement work, evidence must additionally include:
- baseline results for `npm run check:harness:strict` and `npm run check:routing-release`, or explicit baseline blockers;
- changed drift sentinel fixture ids with classifications, release-critical state, source mode, and reason codes;
- `npm run eval:harness` report path: `.opencode/evidence/harness-evals/latest/report.json` and `.opencode/evidence/harness-evals/latest/report.md`;
- `npm run check:routing-release` result showing sentinel id/classification/source-mode/release-critical coverage;
- `npm run check:release` result, or a remediation worklist if blocked by unrelated/out-of-boundary failures.

## Strict golden path
Use this lightweight end-to-end path to prove the harness is operational, not only well-documented:

1. Start from a real plan artifact in `.opencode/plans/`.
2. Ensure matching task evidence exists under `.opencode/evidence/<task-id>/` with `discovery.md`, `verification.md`, and `index.json`.
3. Refresh advisory generated docs with `npm run docs:generate`.
4. Run `npm run docs:generate:check`.
5. Run `npm run check:evidence`.
6. Run `npm run check:docs`.
7. Run `npm run check:harness:strict`.
8. Record the outcome in the task's verification artifact.

The curated exemplar task bundles in `.opencode/plans/` and `.opencode/evidence/` are intended to keep this path replayable for maintainers.

## Standard agent loop
Validation ladder baseline: plan/handoff check → discovery/research evidence → implementation/docs change → diff review → targeted validation commands → final `@quality-gate` for non-trivial/risky completion claims.

Typed output baseline for active lanes (non-trivial work): `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`.
This schema is internal/non-user-facing. Final user-facing messaging must be normalized by orchestrator into natural Bahasa Indonesia prose, with technical literals kept exact.

LSP-first baseline: use LSP for rename/refactor/navigation/diagnostic-driven edits when available; if fallback path used, record limitation/evidence impact explicitly.

1. `@orchestrator` understands intent and chooses the route.
2. `@explorer` does discovery when context is still unclear.
3. `@artifact-planner` writes the plan for non-trivial tasks; trivial single-step and easily reversible tasks may skip planner.
4. `@fixer` performs bounded implementation.
5. Run the relevant validation.
6. `@oracle` reviews architecture risk when material.
7. Conditional specialist reviewers are called when a risk trigger applies.
8. `@quality-gate` performs the final read-only conformance review.
9. The final summary is assembled from evidence.

Non-trivial implementation should be treated as plan-bound work: plan artifact under `.opencode/plans/` plus evidence under `.opencode/evidence/` before completion claims.

## Mode-aware Plan Quality Gate
Run this before non-trivial implementation and again before final completion when plan quality changed during execution.

- `PASS`: material decisions, acceptance criteria, creative alternatives where required, tradeoffs, TDD, validation, and worklist are ready.
- `PASS_FOR_SLICE`: whole-product ambiguity remains, but the first vertical slice is explicit, safe, validated, and does not lock unresolved decisions.
- `NEEDS_DEPTH`: plan has the expected sections but lacks substance, alternatives, mapping, evidence, or validation detail.
- `BLOCKED`: a material decision or required access is missing and no safe slice exists.

Only `PASS` and `PASS_FOR_SLICE` can proceed to implementation.

## Greenfield evidence minimum
For new app, MVP, SaaS/product build, blank repo, or major revamp work, evidence must include:
- starter matrix from [GREENFIELD_STARTER.md](./GREENFIELD_STARTER.md) with `answered`, `deferred`, `slice-safe`, or `blocked` state for material decisions;
- selected mode: `Greenfield App Accelerator`;
- product thesis and target user pain;
- considered product/UX/architecture options plus tradeoff score or rationale;
- key references, screenshots, docs, upstream examples, or first-principles basis for those options;
- selected first vertical slice and why it is slice-safe;
- journey-to-contract map: `user journey → data model → API/contracts → UI screens → tests`;
- design readiness level (`MVP design enough`, `needs-polish`, `reference-ready`, or `blocked`);
- validation commands/results and final claim level (`MVP slice complete`, `draft`, `prototype`, or whole-app complete only when true).

## Maintenance evidence minimum
For bugfix, regression, refactor, dependency update, small feature, or incident follow-up work, evidence must include:
- selected mode: `Maintenance Stability Mode`;
- repro, failing behavior, regression test, or targeted local evidence;
- smallest safe diff rationale;
- validation commands/results;
- any behavior/security/product decision that was asked, assumed, or deferred.

Maintenance work should not be forced through greenfield product thesis or creative alternatives unless the bug itself requires a product/UX decision.

## Creativity Fast Path evidence minimum
For explicit ideation/generate/prototype/draft work running in `Creativity Fast Path`, evidence may stay lightweight, but it must still include:
- selected mode: `Creativity Fast Path`;
- the natural-language trigger or explicit user intent that activated the mode;
- delivered claim level: `draft`, `prototype`, or `exploration` only;
- assumptions, confidence level, and why the result is reversible;
- repo-local evidence used when cheap/relevant, or an explicit note that the output is first-principles-driven;
- skipped heavy gates or validations, with reason;
- the exact promotion condition if the user later wants production behavior.

`Creativity Fast Path` lowers evidence burden only for reversible exploratory output. It does not lower the bar for security/privacy, destructive, release, prompt/config, or material UI completion claims.

## Prototype Promotion Gate
Before a `draft`, `prototype`, or `exploration` result can be presented as `done`, `ready`, `production-ready`, `close parity`, or release-ready, evidence must show:
- the mode exited `Creativity Fast Path` and re-entered the normal routing flow;
- required planning depth was added when the scope became multi-phase, material, or ambiguous;
- implementation/validation evidence exists for the promoted behavior;
- hard rails were re-checked if auth, PII, payments, uploads, privacy, destructive ops, deploy/release, or permission boundaries are involved;
- `@quality-gate` reviewed the change whenever the usual material/risky/prompt/config/security/UI rules require it.

If promotion evidence is missing, the highest allowed claim stays `draft`, `prototype`, or `exploration`.

## Style fidelity and mechanical UI failure rules

For substantial UI, explicit aesthetic requests are requirements, not optional taste. Evidence must include a Requested Aesthetic Fidelity Gate result when user asks for a style family such as `claymorphism`, `glassmorphism`, brutalism, luxury dark, cozy, editorial, playful, or similar.

Required style evidence:
- Material Grammar Translation: user phrase -> tokens -> surfaces -> layout rules -> reject_if.
- Source basis: `DESIGN.md`, designer blueprint, reference screenshots/URLs, current UI evidence, or first-principles rationale.
- Final evidence: screenshots/designer signoff or lowered claim (`draft`, `needs-polish`, `blocked`).

Mechanical UI failure rules for substantial UI:
- Explicit requested aesthetic mismatch = `NEEDS_FIX`, not pure taste.
- Card Spam / Layout Repetition Gate: repeated card/grid anatomy across sections without purpose-specific hierarchy is `NEEDS_FIX` or `needs-polish`.
- User-facing Copy Gate: debug/internal copy, port numbers, server labels, framework jargon, implementation notes, lorem, or review/status labels in user-facing UI are blockers unless the audience is explicitly technical and rationale is recorded.
- Fake Metric / Debug Artifact Gate: arbitrary KPI numbers, fake dashboard metrics, demo counters, fake controls, placeholder charts, and local dev artifacts are blockers unless clearly demo/dev and labeled.
- Hero Composition Gate: placeholder/abstract hero, floating cards, generic blobs, CSS glass panels, or style-only filler are `NEEDS_FIX` when imagery/product/domain composition matters.

Tiny UI polish remains lightweight: if the task is reversible and does not change material visual direction, record existing design basis and skip full grammar.

## UI Slop Evaluation Harness contract

`npm run eval:ui-slop` runs deterministic fixture-based UI slop evaluation and writes replayable reports to `.opencode/evidence/ui-slop/latest/report.json` and `.opencode/evidence/ui-slop/latest/report.md`.

`npm run check:ui-slop` enforces fixture `expectedStatus` and `expectedReasonCodes`. Expected failing fixtures pass the check only when expected remediation-oriented reason codes are detected. This check is wired into `check:harness:strict` only; normal `check:harness` intentionally stays lighter.

Fixture source path: `scripts/evals/ui-slop-fixtures/`. Each fixture records `id`, `requestedAesthetic`, `surface`, `expectedStatus`, `expectedReasonCodes`, and `html`.

Reason codes preserved by the harness:
- `requested-aesthetic-mismatch`
- `material-grammar-missing`
- `card-spam-repetition`
- `generic-neon-glass-overuse`
- `fake-metric`
- `debug-copy-user-facing`
- `abstract-hero-filler`
- `placeholder-visual`
- `missing-state-evidence`
- `missing-accessibility-evidence`
- `missing-screenshot-evidence-for-visual-claim`

Every finding must include `reason_code`, `severity`, `category`, `remediation`, and fixture/source id. Treat this harness as baseline deterministic evidence, not a complete visual proof. Browser, screenshot, computed-style, contrast, and visual-diff analysis remain follow-up evidence when visual completion claims are material.

## Minimal atomic migration rule
Changes that move policy between `AGENTS.md`, `README.md`, `.opencode/docs/`, and scripts must land together with the related gate/doctor updates.

Tool-selection quality references:
- Operational tool guidance: [TOOL_USAGE.md](./TOOL_USAGE.md)
- Role boundary matrix: [AGENT_TOOL_ACCESS.md](./AGENT_TOOL_ACCESS.md)

## Remediation-oriented error standard
Error messages must state:
- the broken invariant,
- the relevant file/area,
- specific remediation steps.
