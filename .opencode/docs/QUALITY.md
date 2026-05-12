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
