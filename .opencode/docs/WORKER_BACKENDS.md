
# Worker Backends

Routing decides **who should own work**. Worker backend selection decides **how that worker is launched**.

## Current backend types
- `opencode-subagent`
- `opencode-session`
- `external-cli-codex`
- `external-cli-claude`
- `external-cli-gemini`

## Policy
- Lane ownership still comes from `.opencode/docs/AGENT_ROUTING.md`.
- Backend choice must not silently override lane boundaries.
- External CLI backends are optional integrations, not required dependencies.
- When a backend is unavailable, fail with explicit remediation rather than fabricating success.

## Suggested defaults
- `@designer`, `@oracle` → stronger reasoning backend acceptable.
- `@fixer`, `@backend`, `@frontend` → lower-cost execution backend acceptable.
- `@quality-gate` → deterministic/read-only backend preferred.

## Execution contract
- Dispatcher creates a persisted worker execution record before claiming and mailing work.
- Executor stores `command`, `args`, `cwd`, backend, workspace metadata, and execution status in `.opencode/state/runs/<run-id>/workers/*.json`.
- `execute` may remain dry-run / `ready` unless `--spawn` is explicitly requested.
- Retry loops and process polling update those same execution records instead of inventing side channels.

## Evidence
Material autonomous runs should preserve the selected backend per worker so replay bundles explain how execution happened.
