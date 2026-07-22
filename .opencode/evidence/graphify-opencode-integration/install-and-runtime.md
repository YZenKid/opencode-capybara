# Graphify Install and Runtime Evidence

Task: `graphify-opencode-integration`
Scope: runtime tooling/config only. Existing `commands/init-harness.md` modification preserved.

## Changes

- Installed `graphifyy[mcp]` globally with `uv tool install 'graphifyy[mcp]'`.
- Added executable `scripts/graphify-mcp-wrapper`.
  - Uses active project root from argument, default `$PWD`.
  - Builds missing graph with `graphify extract <root> --code-only --no-cluster --out <root>`.
  - Updates existing graph with `graphify update <root> --no-cluster`.
  - Starts stdio server with `exec graphify-mcp <root>/graphify-out/graph.json`.
  - No hook, HTTP transport, semantic extraction, credentials, or hardcoded user path.
- Added enabled local `graphify` MCP entry to `opencode.json`.
  - Command uses `{env:HOME}` and `{env:PWD}`.
  - OpenCode restart required before MCP becomes usable, per `.opencode/docs/MCP.md`.

## Validation

1. `uv tool install 'graphifyy[mcp]'`
   - PASS. Installed 59 packages.
2. `graphify --version`
   - PASS. `graphify 0.9.23`.
3. `graphify extract --help`
   - PASS. Confirms `--code-only`, `--no-cluster`, and `--out`.
4. Temp project wrapper smoke:
   - Command: `scripts/graphify-mcp-wrapper "$tmp"`
   - PASS. Created `$tmp/graphify-out/graph.json`.
5. Query smoke:
   - Command: `graphify query 'answer function' --graph "$tmp/graphify-out/graph.json" --budget 200`
   - PASS. Returned `answer()` and `sample.py`, with extracted `contains` edge.
6. MCP stdio handshake:
   - Command: `printf '<initialize JSON-RPC>' | timeout 10s graphify-mcp "$tmp/graphify-out/graph.json"`
   - PASS. Returned JSON-RPC initialize result; server name `graphify`.
7. `python3 -m json.tool opencode.json`
   - PASS.
8. `python -m graphify.serve --help`
   - NOT USED as runtime validation. Active `python` is `/var/home/ujang/.hermes/hermes-agent/venv/bin/python3`, which lacks installed uv-tool package (`ModuleNotFoundError: No module named 'graphify'`). Handoff requires `graphify-mcp`, which passed handshake.

## Safety checks

- No production deploy, external mutation, migration, credential write, or secret change performed.
- No policy docs, `AGENTS.md`, skills, or `commands/init-harness.md` changed.
- Graph output was generated only in temporary validation directory; no repo `graphify-out/` added.

## Rollback

Remove `graphify` object from `opencode.json`, delete `scripts/graphify-mcp-wrapper`, then run `uv tool uninstall graphifyy` if global installation must be reverted. Restart OpenCode after config rollback.

## Residual risk

`graphify update` behavior is upstream runtime behavior. It runs code-only update without `--force`; stale/deletion-heavy graphs may need explicit operator rebuild. No production readiness claim.

## Remediation

- Removed `{env:PWD}` from `opencode.json` Graphify command. Wrapper now receives no explicit root and uses OpenCode active instance cwd through its `$PWD` default.
- Preserved local stdio MCP, `bash` + `{env:HOME}` wrapper command, `enabled: true`, and `timeout: 120000`.
- Validation: `python3 -m json.tool opencode.json` PASS; Graphify command contains exactly `bash` plus wrapper path and no `{env:PWD}` PASS.
- OpenCode restart required before runtime MCP usability check.
