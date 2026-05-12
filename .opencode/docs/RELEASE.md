# Release

## Local readiness
- Run `npm run check:harness`
- Run `npm run check:routing-release`
- Run `npm run doctor`
- Ensure `@quality-gate` has completed with `PASS` or `PASS_WITH_RISKS` for material changes

## Transcript routing gate
- Release-critical transcript fixtures must pass.
- Release-critical average routing score must be at least `4.5/5`.
- Borderline and negative fixtures may remain non-release-critical, but they must continue to exercise expected reason codes and score ranges.
- If transcript drift regresses materially, prefer fixing the evaluator/corpus before cutting a release.

## Future CI mirror
When CI is added or expanded, mirror the local harness checks instead of inventing a separate validation contract.

## Rollout posture
- Prefer atomic changes for docs + gates + doctor.
- Favor short follow-up fixes over prolonged blocked merges when the risk is low and evidence is clear.

## Maintainer workflow
- When a real routing failure occurs, add or update a transcript fixture before closing the issue.
- Keep the transcript corpus balanced across good, bad, borderline, and fallback-valid scenarios.
- Use release-critical marking sparingly; only stable fixtures with representative behavior should gate releases.
