# MCP

Configured MCP surfaces include:
- `time`
- `9router`
- `context7`
- `browseros`
- `shadcn`
- `semgrep`
- `github`

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

## BrowserOS MCP

Load the `browseros-runtime` helper skill (see `.opencode/docs/SKILLS.md`) for
the full runtime playbook, evidence rules, and failure handling. This MCP entry
is the index of the tool surface and the canonical loop pattern; the skill is
the operating manual for agents.
`http://127.0.0.1:9333/mcp` (default). BrowserOS must be running for the MCP
to be reachable; if the user closed the app, real calls return
`CDP error: No browser window available`. Restart with `open -a /Applications/BrowserOS.app`.

`browseros` exposes 23 top-level tools. The compact set still covers far more
ground than flat browser automation MCPs because `act`, `run`, and the
`discover_*`/`execute_action` family are meta-tools that resolve at call time.

Browser automation (real user session, cookies and logins carried over):
- `tabs` — list / new / close pages; returns `page` ids used by every other tool
- `tab_groups` — list / create / update / ungroup / close tab groups
- `navigate` — url / back / forward / reload on a `page`
- `snapshot` — accessibility tree with stable `[ref=eN]` handles for `act`
- `diff` — minimal change readout since last snapshot/diff (cheap loop signal)
- `act` — multi-action on refs: click, click_at, type, type_at, fill, press, hover, hover_at, select, scroll, drag_at (ref-based is preferred, coordinate-based is the fallback)
- `read` — page content as `markdown` / `text` / `links`, optional CSS selector
- `grep` — case-insensitive regex over the snapshot (`over="ax"`) or visible text (`over="content"`)
- `screenshot` — PNG, optionally full-page
- `pdf` — save page to PDF
- `wait` — for text / selector / time
- `download` — click an element to trigger a download, returns saved path
- `upload` — set local file path(s) on an `<input type="file">` ref
- `windows` — list / create / close / activate / set_visibility (visible or hidden)
- `evaluate` — `Runtime.evaluate` for page-context JS
- `run` — multi-step JS against a `browser` SDK (`browser.pages.*`, `browser.observe.*`, `browser.input.*`, `browser.nav.*`, `browser.cdp`)

External app integrations (40+ services via Klavis Strata — always go through
progressive discovery, do not guess action names):
- `connector_mcp_servers` — check whether a service is connected, or list the inventory
- `discover_server_categories_or_actions` — entry point for finding available actions
- `get_category_actions` — expand a category
- `get_action_details` — get parameter schema before calling `execute_action`
- `execute_action` — call a discovered action; supports `include_output_fields` to limit response size
- `search_documentation` — keyword search within a server's documentation
- `handle_auth_failure` — recover from `401`/expired-token errors by getting the auth URL

Supported services include: Gmail, Google Calendar, Google Docs, Google Drive,
Google Sheets, Slack, LinkedIn, Notion, Airtable, Confluence, GitHub, GitLab,
Linear, Jira, Figma, Salesforce, ClickUp, Asana, Monday, Microsoft Teams,
Outlook Mail, Outlook Calendar, Supabase, Vercel, Postman, Stripe, Cloudflare,
Brave Search, Mem0, Dropbox, OneDrive, WordPress, YouTube, Box, HubSpot,
PostHog, Mixpanel, Discord, WhatsApp, Shopify, Cal.com, Resend, Google Forms,
Zendesk, Intercom.

Quick loop pattern (Observe → Act → Verify):
1. `tabs` (list) → pick a `page` id.
2. `navigate` if needed → returns a fresh snapshot (refs invalidate after nav).
3. `snapshot` to get fresh `[ref=eN]` handles.
4. `act` with kind + ref for click / fill / type / press / hover / select / scroll.
5. `diff` to confirm the action moved the DOM; `screenshot` for visual confirmation.
6. `read` to extract content; `grep` for targeted text scan; `evaluate` for page JS.

Strata loop pattern (do not guess action names):
1. `connector_mcp_servers` to check whether the service is connected.
2. If not connected, follow the returned `authUrl`; user OAuths in BrowserOS.
3. `discover_server_categories_or_actions` with the user's natural-language query.
4. `get_category_actions` to expand a category.
5. `get_action_details` for parameter schema.
6. `execute_action` with `include_output_fields` to keep responses small.
7. On 401/auth errors, `handle_auth_failure` to refresh the auth URL.

Caveat: `references/playwright/` under `opencode-fixer` and `opencode-designer`
covers project-side E2E testing with the `@playwright/test` npm library
(scripts, fixtures, traces, CI). That is separate from the `browseros` MCP —
the MCP is for agent-driven runtime UI interaction during a task, while
`@playwright/test` is for shipping a real test suite inside a project.

## Policy
- MCP usage should be explicit and task-relevant.
- Prefer local discovery before external tools when repo-local context is enough.
- Do not hardcode device-specific absolute paths in MCP configuration or prompts.
- Image generation must use explicit `project_root` and `target_path` relative to that root.
- For `background=transparent` PNG flows, `9router` may apply bounded edge-connected near-white background repair when provider returns an opaque PNG. Treat `transparency_verified`, `transparency_warning`, and `png_info` as authoritative result metadata.
- Operator tuning: `NINEROUTER_REPAIR_WHITE_THRESHOLD` controls white cutoff (default `245`), and `NINEROUTER_REPAIR_VARIANCE_THRESHOLD` controls allowed RGB spread for removable background candidates (default `8`).
