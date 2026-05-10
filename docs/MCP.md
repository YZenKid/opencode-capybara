# MCP

Configured MCP surfaces include:
- `time`
- `brave-search`
- `context7`
- `grep_app`
- `playwright`
- `shadcn`
- `stitch`
- `image-asset-generator`
- `semgrep`
- `github`

## Policy
- MCP usage should be explicit and task-relevant.
- Prefer local discovery before external tools when repo-local context is enough.
- Do not hardcode device-specific absolute paths in MCP configuration or prompts.
- Image generation must use explicit `project_root` and `target_path` relative to that root.
