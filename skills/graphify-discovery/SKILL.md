---
name: graphify-discovery
description: Mandatory query-first Graphify code-only discovery for code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes when graph is fresh, before direct source verification.
---

# Graphify Discovery Skill

Use Graphify as mandatory query-first, local, code-only, read-only context for code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes when graph is available and fresh. It narrows searches; it never proves behavior or replaces direct source reading.

## Workflow

1. Check whether `.opencode/graphify-out/graph.json` exists and is fresh enough for current work.
2. Use narrow `query`, `path`, or `explain` requests before broad repository discovery.
3. Treat `INFERRED` and `AMBIGUOUS` edges as leads, not facts.
4. Read relevant source files directly before making claims or edits.
5. Run applicable tests and runtime checks; graph output cannot replace them.
6. If graph is missing, stale, or unsupported, refresh it only through an approved local code-only path, or use normal repo discovery and record fallback. Tiny known-file edits and non-code tasks may skip with explicit reason.

## Boundaries

- No semantic LLM extraction.
- No credentials, HTTP server, telemetry, post-commit hook, or strict source-read blocking.
- No writes to source, config, or runtime state from Graphify queries.
- Do not block work when Graphify is unavailable.

## Output

Report graph status, narrow request used, leads discovered, direct source paths verified, tests/runtime checks run, and unresolved assumptions.
## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.
