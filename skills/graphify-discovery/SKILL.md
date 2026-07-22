---
name: graphify-discovery
description: Optional Graphify code-only graph discovery workflow for broad architecture and dependency mapping before direct source verification.
---

# Graphify Discovery Skill

Use Graphify only as optional, local, code-only, read-only discovery context. It helps narrow broad architecture or dependency searches; it never proves behavior or replaces source verification.

## Workflow

1. Check whether `graphify-out/graph.json` exists and is fresh enough for current work.
2. Use narrow `query`, `path`, or `explain` requests before broad repository discovery.
3. Treat `INFERRED` and `AMBIGUOUS` edges as leads, not facts.
4. Read relevant source files directly before making claims or edits.
5. Run applicable tests and runtime checks; graph output cannot replace them.
6. If graph is missing or stale, refresh it only through an approved local code-only path, or use normal repo discovery.

## Boundaries

- No semantic LLM extraction.
- No credentials, HTTP server, telemetry, post-commit hook, or strict source-read blocking.
- No writes to source, config, or runtime state from Graphify queries.
- Do not block work when Graphify is unavailable.

## Output

Report graph status, narrow request used, leads discovered, direct source paths verified, tests/runtime checks run, and unresolved assumptions.
