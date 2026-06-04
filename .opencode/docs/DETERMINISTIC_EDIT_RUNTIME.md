
# Deterministic Edit Runtime

The deterministic edit helper remains proposal-first and fail-closed. Runtime execution should prefer it for risky multi-file or replay-sensitive edits when exact anchors matter.

## Guarantees
- explicit expected file hash,
- exact or uniquely-identifiable block target,
- no write side effects unless explicitly approved by a higher-level flow,
- structured reason codes.

## Runtime posture
- Use deterministic edit proposals for high-risk update plans.
- Store proposal output in evidence when it materially affects signoff.
- If helper limitations block a change, record the fallback path and confidence drop.

## Related checks
- `npm run test:deterministic-edit-helper`
- runtime foundation tests may reference deterministic edit posture but must not weaken proposal-only defaults.
