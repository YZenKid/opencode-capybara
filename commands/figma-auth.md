---
description: Guide auth or re-auth for the configured Figma MCP server
agent: orchestrator
model: cliproxyapi/gpt-5.4
---

Help the user authenticate or re-authenticate the configured Figma MCP server for this OpenCode setup.

Arguments from user, if any:

```text
$ARGUMENTS
```

Workflow:

1. Inspect `opencode.json` and confirm whether the repo is currently configured with a `figma` MCP entry.
2. Read `guide/ENVIRONMENT.md` and `guide/TROUBLESHOOTING.md` first so the response matches the repo's current guidance.
3. Determine the requested mode from `$ARGUMENTS`:
   - default to **auth** when no mode is provided,
   - use **reauth** when the user asks to reconnect, re-login, reset auth, or re-authenticate,
   - use **bootstrap** when the user asks for workaround/fallback because native auth is blocked.
4. If the `figma` MCP entry is missing or misconfigured, explain the exact mismatch before suggesting auth steps.
5. For **auth** mode:
   - explain that this repo expects the remote Figma MCP server at `https://mcp.figma.com/mcp` with `oauth: {}`,
   - route user to repo wrapper: `bash scripts/figma-mcp-auth.sh auth --verify`,
   - mention native flow may fail with approved-client restriction (403), then route to bootstrap mode.
6. For **reauth** mode:
   - route user to wrapper: `bash scripts/figma-mcp-auth.sh reauth --verify`,
   - if still blocked, route to bootstrap mode.
7. For **bootstrap** mode:
   - route user to wrapper: `bash scripts/figma-mcp-auth.sh bootstrap --verify`,
   - explain bootstrap helper writes tokens to `~/.local/share/opencode/mcp-auth.json`.
8. Include security reminder that token file is sensitive and must not be committed.
9. For machine/device baru, remind to rerun auth per-device (native first, bootstrap if needed), not copy token by default.
10. Do not invent API-key-based auth for Figma MCP.
11. Keep the answer concise, action-oriented, and in Indonesian.

Use this guidance baseline when the config is correct:

## Expected repo posture

- MCP name: `figma`
- Remote URL: `https://mcp.figma.com/mcp`
- Auth style: OAuth via host/client flow with `oauth: {}` in config
- Capability caveat: actual write-to-canvas / live UI sync support can depend on client support and Figma seat/plan

Native OpenCode auth can fail in some environments due to approved-client restriction (`HTTP 403 Forbidden`).

## OpenCode-first auth steps

Use these steps when the user is authenticating for the first time:

```bash
bash scripts/figma-mcp-auth.sh auth --verify
```

## OpenCode-first re-auth steps

Use these steps when the user specifically needs re-auth:

```bash
bash scripts/figma-mcp-auth.sh reauth --verify
```

## Bootstrap fallback (repo-supported)

Saat native auth gagal (mis. 403), gunakan:

```bash
bash scripts/figma-mcp-auth.sh bootstrap --verify
```

Bootstrap helper akan menulis token ke `~/.local/share/opencode/mcp-auth.json`.

## Supported-client fallback examples

Only use these as secondary comparison/debug fallback when OpenCode + bootstrap repo flow cannot be completed:

- **Codex CLI**
  ```bash
  codex mcp add figma --url https://mcp.figma.com/mcp
  ```

- **Claude Code**
  ```bash
  claude mcp add --transport http figma https://mcp.figma.com/mcp
  ```

  Optional user-scope variant:

  ```bash
  claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp
  ```

When giving fallback guidance, explain that the goal is to prove whether the auth problem is in the Figma account/server or in client-specific OAuth handling.

Output format:

```markdown
## Status
- <configured|misconfigured|oauth-blocked|reauth-blocked|fallback-needed>

## Current Config
- MCP name: <...>
- URL: <...>
- OAuth posture: <...>

## Next Steps
1. ...
2. ...

## If It Still Fails
- ...
```
