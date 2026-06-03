# Quality

## Quality gate statuses
- `PASS`
- `PASS_WITH_RISKS`
- `NEEDS_FIX`
- `BLOCKED`

## Evidence contract
Every material change must end with evidence, not just claims.

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

## Replay bundle minimum
- `task_id`
- `timestamp`
- harness/prompt version metadata
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
- selected mode: `Greenfield App Accelerator`;
- product thesis and target user pain;
- considered product/UX/architecture options plus tradeoff score or rationale;
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
