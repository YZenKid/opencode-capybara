# Release

## Local readiness
- Run `npm run check:harness`
- Run `npm run doctor`
- Ensure `@quality-gate` is non-blocking for material changes

## Future CI mirror
When CI is added or expanded, mirror the local harness checks instead of inventing a separate validation contract.

## Rollout posture
- Prefer atomic changes for docs + gates + doctor.
- Favor short follow-up fixes over prolonged blocked merges when the risk is low and evidence is clear.
