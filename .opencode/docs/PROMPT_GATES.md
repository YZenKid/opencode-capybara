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
- `npm run docs:generate:check` → generated docs freshness validation
- `npm run check:harness` → aggregate harness check

## Invariant categories
- Routing and skill posture
- Orchestrator direct-vs-delegate thresholds
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

Routing hardening minimum:
- Ensure `.opencode/docs/AGENT_ROUTING.md` keeps explicit orchestrator direct-work thresholds, anti-pattern examples, and compact routing checklist/rubric.
- Ensure `skills/opencode-orchestrator/SKILL.md` keeps hard defaults that route read-heavy discovery to `@explorer` and multi-file bounded implementation to `@fixer`.
- Enforce via `npm run test:prompt-gates` (and `npm run doctor` as a quick local policy sanity check).

## Generated reports
- Refresh advisory generated summaries with `npm run docs:generate`.
- Validate freshness with `npm run docs:generate:check` or indirectly through `npm run check:docs`.
- Generated outputs live in `docs/generated/` and help maintainers inspect current agent metadata, prompt-gate coverage, and docs-integrity coverage.
- Generated reports are evidence helpers only; canonical policy remains in `.opencode/docs/` and the implementing scripts.
