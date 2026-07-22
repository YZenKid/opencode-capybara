# Graphify Source Audit

- Claim level: `confirmed_docs`
- Upstream commit: `e32c9f431c5ed7ed8c980f6d34dc3fe6c99a389b`

## Installer behavior

`graphify install --platform opencode` is not used directly. Upstream `graphify/install.py` installs a global skill but also writes project-local `.opencode/plugins/graphify.js` and `.opencode/opencode.json`. That conflicts with this preset's no-plugin boundary and is not used. This audit predates later user approval of repository-local detached post-commit/post-checkout hooks; that later extension is documented separately in `commit-hook.md`.

## Supported safe primitives

- `uv tool install "graphifyy[mcp]"` installs Graphify and MCP extra.
- `graphify extract <root> --code-only` is local AST extraction without semantic LLM pass.
- `graphify-mcp <graph-path>` / `python -m graphify.serve <graph-path>` serves graph through stdio.
- Server only reads existing `graph.json`; wrapper must build/update before server start.

## OpenCode runtime configuration

Context7 source for `/anomalyco/opencode` confirms local MCP process cwd defaults to active OpenCode instance directory; local config supports optional `cwd`. Therefore a repo-relative wrapper can use `$PWD` as the active project root without hardcoded user path.

## Adopted integration

- Local code-only graph.
- Wrapper creates/updates graph, then `exec graphify-mcp`.
- One global `opencode.json` MCP entry starts wrapper per OpenCode project instance.
- Global inherited AGENTS guidance plus dedicated skill instruct all lanes to query graph first for broad architecture/dependency discovery and verify source before claims.

## Rejected

- Upstream OpenCode installer/plugin.
- Semantic extraction and LLM backends.
- HTTP transport.
- Unapproved automatic schedulers or hook changes beyond the later user-approved repository-local post-commit/post-checkout extension.
- Strict raw-source blocking.

## References

- https://github.com/Graphify-Labs/graphify/blob/e32c9f431c5ed8c980f6d34dc3fe6c99a389b/graphify/install.py
- https://github.com/Graphify-Labs/graphify/blob/e32c9f431c5ed8c980f6d34dc3fe6c99a389b/graphify/serve.py
- https://github.com/Graphify-Labs/graphify/blob/e32c9f431c5ed8c980f6d34dc3fe6c99a389b/graphify/skill-opencode.md
- Context7 `/anomalyco/opencode`: local MCP config and cwd behavior
