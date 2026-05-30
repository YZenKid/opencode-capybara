# MCP

Configured MCP surfaces include:
- `time`
- `9router`
- `context7`
- `grep_app`
- `playwright`
- `shadcn`
- `semgrep`
- `github`
- `brave-search` (disabled legacy)

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

## Policy
- MCP usage should be explicit and task-relevant.
- Prefer local discovery before external tools when repo-local context is enough.
- Do not hardcode device-specific absolute paths in MCP configuration or prompts.
- Image generation must use explicit `project_root` and `target_path` relative to that root.
- For `background=transparent` PNG flows, `9router` may apply bounded near-white-to-alpha repair when provider returns an opaque PNG. Treat `transparency_verified`, `transparency_warning`, and `png_info` as authoritative result metadata.
