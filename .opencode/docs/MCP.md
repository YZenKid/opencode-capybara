# MCP

This document is the MCP **inventory** for this repository.

Risk/governance registry: `.opencode/capabilities/registry.json`. Generated advisory view: `docs/generated/mcp-risk-matrix.md`.

For operational usage guidance (when/why/how), use:
- [TOOL_USAGE.md](./TOOL_USAGE.md)
- [AGENT_TOOL_ACCESS.md](./AGENT_TOOL_ACCESS.md)
- [../../guide/ENVIRONMENT.md](../../guide/ENVIRONMENT.md)
- [../../guide/TROUBLESHOOTING.md](../../guide/TROUBLESHOOTING.md)

Configured MCP surfaces include:
- `time`
- `9router`
- `context7`
- `sequential-thinking`
- `grep_app`
- `playwright`
- `shadcn`
- `semgrep`
- `github`
- Legacy `image-asset-generator` removed; image asset tools live under `9router`.

## Sequential Thinking MCP

`sequential-thinking` exposes `sequential_thinking`.

Use it after loading a skill and before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback. Use it as a reasoning scaffold only: it does not replace repo evidence, docs, tests, browser/runtime validation, or role boundaries. Do not expose raw chain-of-thought to the user; summarize decisions and evidence only.

After changing `opencode.json`, restart OpenCode before expecting this MCP to become usable.

## 9Router MCP

`9router` exposes:

- `health_check_9router`
- `list_9router_models`
- `get_9router_model_info`
- `web_search`
- `web_fetch`
- `generate_image`
- `generate_image_asset`
- `generate_image_assets_batch`

Use `web_search` for fresh public web lookup.
Use `web_fetch` for URL-to-markdown/text/html extraction.
Use `generate_image_asset` for project assets that must be saved to disk.
Use `generate_image` for direct image generation without project file output.

Operational image rules:
- For saved assets, prefer `generate_image_asset` or `generate_image_assets_batch` with explicit `project_root` and a `target_path` relative to that root.
- Before required image generation, run `health_check_9router`, list image models, and inspect `get_9router_model_info` for the chosen model. Verify capability for requested `output_format`, `background`, `quality`, and dimensions, or adapt params before calling the generator.
- Default content imagery to raster outputs (`webp`, `png`, `jpeg`/`jpg`). Use transparent backgrounds only with alpha-capable formats.
- Validate width/height, aspect ratio, and pixel budget before generation. Use provider-valid dimensions.
- If the provider rejects dimensions, retry with a provider-supported size/aspect. If it rejects pixel budget, retry with a provider-supported size that stays within budget before fallback or failure.
- Do not claim an asset was generated if the endpoint failed. Deterministic SVG/CSS/local placeholder fallback is placeholder/demo output, not generated imagery.

## MCP state terminology

Use this lightweight state model consistently across docs/prompt surfaces:

- **configured**: MCP entry exists in configuration/inventory.
- **auth-blocked / unauthenticated**: requires auth but valid auth/session is not established.
- **authenticated**: auth exists and is accepted by the provider.
- **connected**: transport/session to MCP endpoint is reachable.
- **usable**: connected + authenticated + capability supported for the needed action.
- **read-only / unsupported**: tool is reachable but requested capability is intentionally restricted or not supported in the current client/server/role.

Rule: `configured` does **not** mean `usable`.

## Policy
- MCP usage should be explicit and task-relevant.
- Prefer local discovery before external tools when repo-local context is enough.
- Do not hardcode device-specific absolute paths in MCP configuration or prompts.
- Image generation must use explicit `project_root` and `target_path` relative to that root.
- For `background=transparent` PNG flows, `9router` may apply bounded edge-connected near-white background repair when provider returns an opaque PNG. Treat `transparency_verified`, `transparency_warning`, and `png_info` as authoritative result metadata.
- Operator tuning: `NINEROUTER_REPAIR_WHITE_THRESHOLD` controls white cutoff (default `245`), and `NINEROUTER_REPAIR_VARIANCE_THRESHOLD` controls allowed RGB spread for removable background candidates (default `8`).
- OpenCode auth store file (`~/.local/share/opencode/mcp-auth.json`) is sensitive and must never be committed.
