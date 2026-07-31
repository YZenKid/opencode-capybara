---
name: browseros-runtime
description: BrowserOS MCP runtime playbook for OpenCode lanes. Use for browser/UI/runtime tasks that need real BrowserOS automation, DOM evidence, screenshots, or 40+ external app integrations.
---

# BrowserOS Runtime

Use this helper skill when the task depends on actual browser behavior, authenticated page state, DOM evidence, screenshots, downloads, or BrowserOS app integrations.

## Trigger / skip
- Trigger: browser/UI/runtime flow, reproduction, form filling, navigation, authenticated page scraping, visual checks, DOM evidence, or cross-app automation through BrowserOS.
- Trigger: when an agent would previously have reached for a browser MCP such as Playwright/Chrome DevTools MCP.
- Skip: purely backend/local code tasks with no browser surface.
- Skip: project-side E2E suite authoring with `@playwright/test`; keep using `references/playwright/` for that.

## Preconditions
- BrowserOS app must be running.
- OpenCode config should expose `browseros` as a remote MCP at `http://127.0.0.1:9333/mcp`.
- Shared OpenCode server health check:
  - `curl http://127.0.0.1:51777/global/health`
  - `curl http://127.0.0.1:51777/mcp`
- Direct BrowserOS MCP reachability check:
  - `curl http://127.0.0.1:9333/mcp`

If BrowserOS is closed, reopen it:
- `open -a /Applications/BrowserOS.app`

## Core loop
Observe → Act → Verify:
1. `tabs` to list pages and get a `page` id.
2. `navigate` when page/url must change.
3. `snapshot` to obtain fresh `[ref=eN]` handles.
4. `act` with ref-based interaction first: click, fill, type, press, hover, select, scroll.
5. `diff` after interaction for cheap confirmation.
6. `read` / `grep` / `evaluate` / `screenshot` for extraction and evidence.

Rules:
- Re-snapshot after navigation or major DOM changes; refs go stale.
- Prefer ref-based actions over coordinate actions.
- Use `wait` only when there is no reliable UI signal yet.
- For multi-step DOM logic, prefer `run` over a long chain of tiny actions.

## Tool surface summary
Browser automation:
- `tabs`, `tab_groups`, `navigate`, `snapshot`, `diff`, `act`, `download`, `upload`, `read`, `grep`, `screenshot`, `pdf`, `wait`, `windows`, `evaluate`, `run`

External app / Strata discovery:
- `connector_mcp_servers`, `discover_server_categories_or_actions`, `get_category_actions`, `get_action_details`, `execute_action`, `search_documentation`, `handle_auth_failure`

## What BrowserOS MCP is good at
- Real BrowserOS session with cookies/logins carried by the app.
- DOM-grounded runtime reproduction.
- Screenshot/PDF/download workflows.
- Cross-app automation through BrowserOS-managed OAuth integrations.
- Progressive action discovery for Gmail/Slack/GitHub/Linear/Figma/etc. without hand-writing API calls.

## What BrowserOS MCP is not
- Not a replacement for shipping an E2E suite in the repo.
- Not a substitute for `@playwright/test` fixtures, retries, traces, CI reporters, or project-owned tests.
- Not a guarantee that BrowserOS is open; if the app is closed, the MCP can be configured yet unusable.

## BrowserOS MCP vs `@playwright/test`
Use BrowserOS MCP when:
- the agent must interact with a live browser during the task,
- the user wants runtime evidence now,
- the workflow depends on existing logins/cookies,
- the workflow spans browser + external connected apps.

Use `@playwright/test` references when:
- you are creating or maintaining project E2E tests,
- the repo needs committed test code,
- CI/retries/traces/reporters matter,
- the task is test-suite engineering rather than agent runtime interaction.

## Strata discovery flow
Do not guess action names.
1. `connector_mcp_servers` to confirm the service is connected.
2. `discover_server_categories_or_actions` with the user's natural-language goal.
3. `get_category_actions` to expand likely categories.
4. `get_action_details` to inspect parameters.
5. `execute_action` with `include_output_fields` to keep responses small.
6. `handle_auth_failure` only for real auth failures.

## Evidence expectations
When BrowserOS MCP is used, record:
- target URL or page name
- action summary
- snapshot/diff/screenshot/PDF/read output used as evidence
- any auth gate, popup, captcha, or manual block
- if Strata used: server name, category/action, and output field filters

## Failure handling
- `CDP error: No browser window available` -> BrowserOS app likely closed or not ready; reopen BrowserOS and retry.
- `/mcp` configured but not usable -> verify both `http://127.0.0.1:9333/mcp` and `http://127.0.0.1:51777/mcp`.
- stale refs -> `snapshot` again.
- action name unknown on external service -> restart the Strata discovery flow; do not guess.

## Output
Mention explicitly:
- that BrowserOS MCP was used,
- which BrowserOS tools were used,
- what evidence came back,
- whether work relied on BrowserOS runtime or on project-side Playwright references.

ponytail: This skill is a runtime playbook, not a full BrowserOS product manual. Upgrade path: split BrowserOS browser-automation vs Strata-integration subskills if the guidance grows materially larger.

## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.
