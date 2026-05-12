# MCP

This document is the MCP **inventory** for this repository.

For operational usage guidance (when/why/how), use:
- [TOOL_USAGE.md](./TOOL_USAGE.md)
- [AGENT_TOOL_ACCESS.md](./AGENT_TOOL_ACCESS.md)
- [../../guide/ENVIRONMENT.md](../../guide/ENVIRONMENT.md)
- [../../guide/TROUBLESHOOTING.md](../../guide/TROUBLESHOOTING.md)

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

## MCP state terminology

Use this lightweight state model consistently across docs/prompt surfaces:

- **configured**: MCP entry exists in configuration/inventory.
- **auth-blocked / unauthenticated**: requires auth but valid auth/session is not established.
- **authenticated**: auth exists and is accepted by the provider.
- **connected**: transport/session to MCP endpoint is reachable.
- **usable**: connected + authenticated + capability supported for the needed action.
- **read-only / unsupported**: tool is reachable but requested capability is intentionally restricted or not supported in the current client/server/role.

Rule: `configured` does **not** mean `usable`.

## Figma state walkthrough (concrete example)

1. `figma` listed in inventory → **configured**.
2. OAuth not completed or rejected by environment policy → **auth-blocked / unauthenticated**.
3. OAuth accepted by provider → **authenticated**.
4. MCP endpoint responds in current runtime → **connected**.
5. Needed action works in current client/server + permission context → **usable**.
6. Canvas-write/live-sync not available in current setup or current role is review-only → **read-only / unsupported** for that action.

## Policy
- MCP usage should be explicit and task-relevant.
- Prefer local discovery before external tools when repo-local context is enough.
- Do not hardcode device-specific absolute paths in MCP configuration or prompts.
- Image generation must use explicit `project_root` and `target_path` relative to that root.
- For UI/design tasks, treat Figma MCP output as design input only (context/rules/canvas artifacts), not final implementation.
- Figma MCP capabilities may vary by remote server/client support and seat permissions (for example write-to-canvas or live UI sync availability).
- Figma config posture in this repo is remote + OAuth object (`oauth: {}`).
- Native `opencode mcp auth figma` may fail in some environments due to Figma approved-client restriction; use repo bootstrap helper when needed.
- OpenCode auth store file (`~/.local/share/opencode/mcp-auth.json`) is sensitive and must never be committed.
