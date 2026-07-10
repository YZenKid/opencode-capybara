# Maintenance Plan

## Mode
Maintenance Stability Mode. `substance: non-ui`. `plan_profile: maintenance`.

## Goal
Fix parser regression with minimal safe change and preserve existing API behavior.

## Non-goals
No UI, page, component, product redesign, or deployment changes.

## Requirements
1. Reproduce failing input.
2. Preserve valid input behavior.
3. Validate boundary input.
4. Return stable error.
5. Keep public API unchanged.
6. Avoid new dependencies.
7. Update regression coverage.
8. Record assumption.
9. Keep diff bounded.
10. Run targeted checks.

## Acceptance Criteria
1. Regression test fails before fix.
2. Regression test passes after fix.
3. Valid input remains supported.
4. Invalid input returns expected error.
5. No unrelated files change.
6. Existing tests pass.
7. Plan remains executable.
8. Evidence records commands.

## Existing Patterns/Reuse
Repo-backed parser tests and stdlib validation.

## Source Anatomy
Parser and focused regression test are confirmed. Runtime integration is unverified.

## Reference Map
- Repo-backed: parser module
- Test-backed: regression fixture
- Assumption: no API migration required

## Decisions/Assumptions
- confirmed: maintenance/non-UI profile.
- assumption: existing test command is sufficient.

## Execution Source of Truth
This plan is canonical and confirmed for bounded maintenance work.

## Implementation Steps
1. Add regression case.
2. Run focused test.
3. Patch parser.
4. Run focused test again.
5. Run compliance check.

## Validation Commands
1. `python3 scripts/tests/example.test.py`
2. `python3 scripts/plan-compliance-check.py`
3. `python3 scripts/tests/plan-retry-guard.test.py`

## Execution-ready Worklist / Handoff Contract
- task_id: maintenance-small-plan
- caller: orchestrator
- callee: fixer

## Evidence Requirements
- Record command outputs under `.opencode/evidence/maintenance-small-plan/`.

## Done Criteria
- Regression test passes and no unrelated files change.
