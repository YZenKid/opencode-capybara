# Prompt Gates

## Purpose
Prompt gates convert important repository invariants into deterministic checks.

## Existing gate
- `npm run test:prompt-gates`
- implementation: `scripts/prompt-gate-regression.mjs`

## Mechanical checks
- `npm run check:docs` → `scripts/docs-integrity-check.mjs`
- `npm run check:agents` → `scripts/agent-boundary-check.mjs`
- `npm run check:skills` → `scripts/skill-contract-check.mjs`
- `npm run check:evidence` → `scripts/evidence-contract-check.mjs`
- `npm run check:harness` → aggregate harness check

## Invariant categories
- Routing and skill posture
- Read-only vs write-capable boundaries
- Docs as system of record
- Evidence contract
- Portability rules
- Setup safety / no hidden install hooks
- Auto-commit safety
- Finish-first execution with deferred non-blocking questions

## Change adjacency rule
If you change policy or docs guarded by a gate:
1. update canonical doc,
2. update the related gate/check,
3. rerun validation,
4. record decision/evidence.
