# Graphify Install and Runtime Evidence

Task: `graphify-opencode-integration` remediation.

## Current canonical runtime

- Wrapper: `scripts/graphify-mcp-wrapper`.
- Project root: wrapper argument or active `$PWD`.
- Graph path: `<root>/.opencode/graphify-out/graph.json`.
- Missing graph extraction: `graphify extract <root> --code-only --no-cluster --out <root>/.opencode`.
- MCP receives canonical graph path only.
- Freshness: graph mtime >= latest tracked code/config file mtime. Missing/stale/unsupported fallback must be recorded.

## Policy files changed

- `agents/*.md`: per-file `## Graphify query-first contract`.
- `skills/opencode-*/SKILL.md`: active per-file contract; intentional retired `opencode-build` and `opencode-general` excluded.
- `scripts/agent-boundary-check.mjs`: individual active agent marker verification.
- `scripts/skill-contract-check.mjs`: individual active skill marker verification.
- `.opencode/docs/MCP.md`: canonical path and minimal freshness definition.

## Validation evidence

- Graphify stats: 825 nodes, 1,256 edges, 100% extracted, 0 inferred, 0 ambiguous.
- Graphify query: wrapper, boundary checks, skill checks, session trace, runtime dispatcher, and harness eval paths found.
- `scripts/tests/graphify-wrapper-path.test.mjs`: executable temp-root behavioral test with stub `graphify` and `graphify-mcp`; asserts fallback `--out <root>/.opencode`, canonical MCP graph path, no old root/`graphify-out` output path, and existing canonical graph skips extraction.

## Safety

No production deploy, external mutation, migration, credential write, or secret change performed.
