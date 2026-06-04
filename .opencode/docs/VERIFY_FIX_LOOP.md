
# Verify / Fix Loop

The runtime verification loop turns existing quality posture into an explicit state machine.

## Status mapping
- `PASS` → verification complete, no remedial task required
- `PASS_WITH_RISKS` → verification complete with residual risk notes
- `NEEDS_FIX` → return to implementation/remediation
- `BLOCKED` → stop and surface blocker

## Runtime phases
- `executing`
- `verifying`
- `needs_fix`
- `retesting`
- `done`
- `blocked`

## Rules
- Maintenance work should prefer smallest safe diff + targeted validation.
- Greenfield slices may use `PASS_FOR_SLICE` planning readiness but still need verification evidence before final completion claims.
- Quality-gate remains read-only final arbiter for non-trivial work.

## Evidence expectations
Record:
- validation command,
- result,
- whether remediation was required,
- residual risks,
- final decision state.
