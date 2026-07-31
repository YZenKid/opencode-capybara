# MCP

This document is the MCP **inventory** for this repository.

Risk/governance registry: `.opencode/capabilities/registry.json`. Generated advisory view: `docs/generated/mcp-risk-matrix.md`.

For operational usage guidance (when/why/how), use:
- [TOOL_USAGE.md](./TOOL_USAGE.md)
- [AGENT_TOOL_ACCESS.md](./AGENT_TOOL_ACCESS.md)
- [../../guide/ENVIRONMENT.md](../../guide/ENVIRONMENT.md)
- [../../guide/TROUBLESHOOTING.md](../../guide/TROUBLESHOOTING.md)

Configured MCP surfaces include:

Core enabled:
- `9router`
- `context7`
- `browseros`
- `scripts`
- `graphify`

Enabled by default:
- `github`
- `semgrep`
- `shadcn`
- `21st`
- `stitch`
- `playwright` (failure-only fallback; BrowserOS primary)

Enabled configuration does not imply authenticated, connected, or usable. Permissions, auth, and task-specific safeguards still apply.

Legacy `image-asset-generator` removed; image asset tools live under `9router`.

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

Use `web_search` for fresh public web lookup. Agent input: `query`, optional `max_results` only.
Use `web_fetch` for URL-to-markdown/text/html extraction. Agent input: `url` only.
`NINEROUTER_URL` and `NINEROUTER_KEY` configure endpoint and authentication. MCP internally sends `model: "search"`, `search_type: "web"`, `max_results: 5` by default for search; and `model: "fetch"`, `format: "markdown"` for fetch.
Use `generate_image_asset` for project assets that must be saved to disk.
Use `generate_image` for direct image generation without project file output.

Operational image rules:
- For saved assets, prefer `generate_image_asset` or `generate_image_assets_batch` with explicit `project_root` and a `target_path` relative to that root.
- Before required image generation, run `health_check_9router`, list image models, and inspect `get_9router_model_info` for the chosen model. Verify capability for requested `output_format`, `background`, `quality`, and dimensions, or adapt params before calling the generator.
- Default content imagery to raster outputs (`webp`, `png`, `jpeg`/`jpg`). Use transparent backgrounds only with alpha-capable formats.
- Validate width/height, aspect ratio, and pixel budget before generation. Use provider-valid dimensions.
- If the provider rejects dimensions, retry with a provider-supported size/aspect. If it rejects pixel budget, retry with a provider-supported size that stays within budget before fallback or failure.
- Do not claim an asset was generated if the endpoint failed. Deterministic SVG/CSS/local placeholder fallback is placeholder/demo output, not generated imagery.

## Playwright MCP

`playwright` exposes browser automation tools (snapshot, act, navigate, screenshot, read, etc.).

**Primary/fallback relationship:** BrowserOS is the **primary** browser automation MCP. Playwright MCP is a **failure-only fallback** — invoke it only after a concrete BrowserOS failure (endpoint unreachable, MCP tool error/timeout, browser process crash). Do not run both MCPs in automatic parallel or duplicate a state-changing action across both.

**Failure trigger:** A concrete BrowserOS tool/connection error. Not operator preference, not speed comparison.

**Restart gate:** After changing `opencode.json`, restart OpenCode before this MCP becomes reachable.

**Defaults:** Headless mode. Chromium-only browser set (no Firefox/WebKit in this slice). For headed mode or additional browser engines, operator must explicitly opt in and record the choice.

**No duplicate invocation:** When both MCPs are reachable, the lane picks BrowserOS first. Automatic same-task duplicate actions against both MCPs are forbidden.

**Selection guidance:** See [TOOL_USAGE.md](./TOOL_USAGE.md) for when to use `playwright` tools.

## 21st MCP

`21st` is enabled as local stdio proxy via `bash {env:HOME}/.config/opencode/bin/21st-mcp-proxy`. Wrapper sources `$HOME/.config/opencode/.env` unless `OPENCODE_ENV_FILE` overrides it, requires a nonempty `API_KEY_21ST` without printing it, then starts `mcp-remote` with HTTP-only transport and silent output. Upstream endpoint uses HTTP JSON-RPC; native OpenCode 1.18.5 remote transport emitted SSE `GET` and received HTTP `405`. Config has no API-key interpolation, environment mapping, or inline header arguments; timeout is 60000 ms. No credential literal belongs in config, logs, evidence, or terminal output.

Restart doctrine: config loads once. After changing `opencode.json`, quit and restart OpenCode; validate in a new `opencode mcp list` subprocess before claiming `connected`. Then use only safe JSON-RPC `tools/list` through stdio proxy and record tool names/count, never request headers. `configured` or CLI discovery does not mean `authenticated`, `connected`, or `usable`.

Use only after design authority and React/shadcn compatibility basis are checked. No automatic `21st add`, `21st generate`, login, publish, delete, or other mutation. If key, quota, or service is unavailable, use repo-local/Open Design/shadcn sources and record exact blocker.

## Scripts MCP

`mcp.scripts` is configured as an enabled local stdio server with command `node {env:HOME}/.config/opencode/bin/scripts-mcp.mjs`. Configuration is `confirmed_repo`; OpenCode must be restarted (`/exit` and relaunch) after changing `opencode.json` before `mcp.scripts` is connected/usable. A prior stdio smoke passed before restart, but that does not make the current OpenCode process connected.

First slice exposes fixed read/check/query tools only:

- `scripts_catalog`
- `scripts_plan_validate`
- `scripts_runtime_verify`
- `scripts_pre_gate_smoke`
- `scripts_template_discover`
- `scripts_visual_audit`
- `scripts_legal_source_check`
- `scripts_design_audit`
- `scripts_progress_read`
- `scripts_delegation_read`
- `scripts_session_trace_audit`
- `scripts_backup_scan`
- `scripts_rules_dry_run`

Tools use fixed script mappings and strict schemas. No caller-supplied script, flag, command, executable, environment, cwd, or arbitrary argument passthrough exists. The wrapper uses `spawn` with `shell:false`, project-root containment, bounded output, and sanitized errors. `caller_lane` is policy attestation only, not authorization. Availability never overrides existing role permission.

`scripts_visual_audit` is reachable but returns structured `tool_pending` while `scripts/visual-audit.py` is absent. This means unsupported in this slice, not an error and not permission escalation. Fixed inventory and classifications live in `scripts_catalog`; this document does not duplicate tool schemas.

Excluded from MCP: `backup-cleanup.py --trash|--purge|--apply`, `rules-harmonizer.py --forward-to`, arbitrary script/argument execution, and write/update actions such as `progress_update`, memory write, delegation record, and rules apply. Write actions are deferred.

When `scripts` is connected, permitted, and exactly maps a first-slice read/check/query task, prefer it. Use canonical CLI as fallback when MCP is disconnected, unavailable, `tool_pending`, not permitted, or exact operation is absent. MCP never replaces CLI. See [TOOL_USAGE.md](./TOOL_USAGE.md) for executable fallback commands.

## Graphify discovery context

Graphify is local, code-only, and read-only. When `graphify-out/graph.json` exists and is fresh, query it first for code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes. Use narrow `query`, `path`, or `explain` requests. Treat `INFERRED` and `AMBIGUOUS` edges as leads, never verified facts. Graphify output never replaces direct source reading, tests, or runtime checks. If graph is missing, stale, or unsupported, refresh it when permitted or use normal repo discovery and record fallback. Tiny known-file edits and non-code tasks may skip with explicit reason. Repository-local `graphify hook install` installs detached, background post-commit and post-checkout code-only refresh hooks; commits do not wait for rebuild. Hooks log to `$HOME/.cache/graphify-rebuild.log`, honor `GRAPHIFY_SKIP_HOOK=1`, and remain opt-out/recoverable with `graphify extract <repo> --code-only --no-cluster --out <repo>/.opencode`. Fresh means `.opencode/graphify-out/graph.json` mtime is >= latest tracked code/config file mtime; stale fallback must be recorded. No semantic LLM extraction, HTTP server, telemetry, credentials, strict source-read blocking, or other scheduler belongs in this integration.

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
## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.
