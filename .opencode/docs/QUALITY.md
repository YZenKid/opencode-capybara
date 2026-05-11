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

## Standard agent loop
1. `@orchestrator` understands intent and chooses the route.
2. `@explorer` does discovery when context is still unclear.
3. `@artifact-planner` writes the plan for non-trivial tasks.
4. `@fixer` performs bounded implementation.
5. Run the relevant validation.
6. `@oracle` reviews architecture risk when material.
7. Conditional specialist reviewers are called when a risk trigger applies.
8. `@quality-gate` performs the final read-only conformance review.
9. The final summary is assembled from evidence.

## Minimal atomic migration rule
Changes that move policy between `AGENTS.md`, `README.md`, `.opencode/docs/`, and scripts must land together with the related gate/doctor updates.

## Remediation-oriented error standard
Error messages must state:
- the broken invariant,
- the relevant file/area,
- specific remediation steps.
