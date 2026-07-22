# Verification — graphify-discovery-coverage

## Commands

- `npm run check:agents` — PASS; centralized Graphify assertions and agent boundary checks passed.
- `npm run check:skills` — PASS; 23 active skills passed contract and centralized Graphify coverage checks.
- `npm run docs:generate` — PASS; generated docs refreshed.
- `npm run docs:generate:check` — PASS; all generated docs current.
- `npm run check:docs` — PASS; docs integrity passed.
- `grep -RInE 'cap-3|at most 3 thought steps|totalThoughts.*\`3\`' AGENTS.md .opencode/docs skills/opencode-* docs/generated` — PASS after registry/source refresh; no active policy matches.
- `git diff --check` — PASS.

## Claim limit

Partial claim only: Graphify inheritance audit and Sequential Thinking prompt cap policy. No server-enforcement claim.
