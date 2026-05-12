# MCP

Configured MCP surfaces include:
- `time`
- `brave-search`
- `context7`
- `grep_app`
- `playwright`
- `shadcn`
- `figma`
- `image-asset-generator`
- `semgrep`
- `github`

## Policy
- MCP usage should be explicit and task-relevant.
- Prefer local discovery before external tools when repo-local context is enough.
- Do not hardcode device-specific absolute paths in MCP configuration or prompts.
- Image generation must use explicit `project_root` and `target_path` relative to that root.
- For UI/design tasks, treat Figma MCP output as design input only (context/rules/canvas artifacts), not final implementation.
- Figma MCP capabilities may vary by remote server/client support and seat permissions (for example write-to-canvas or live UI sync availability).
