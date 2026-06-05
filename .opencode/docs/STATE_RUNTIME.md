
# State Runtime

`scripts/runtime/` is the repo-local execution control plane for durable runs, task queues, mailbox state, runtime memory, worktree helpers, and replayable run artifacts.

## Goal
Add first-class runtime primitives without pretending to modify OpenCode core internals. This layer stays local, deterministic, and script-auditable.

## Canonical state root
- Project-local runtime root: `.opencode/state/`
- Durable run records: `.opencode/state/runs/<run-id>/run.json`
- Event stream: `.opencode/state/runs/<run-id>/events.ndjson`
- Task queue: `.opencode/state/tasks/<run-id>/*.json`
- Mailbox: `.opencode/state/mailbox/<run-id>/<worker>/*.json`
- Shared memory: `.opencode/state/memory/`
- Locks: `.opencode/state/locks/*.lock.json`

## Safety rules
- Runtime scripts fail closed on malformed state.
- Lock files must be atomic JSON writes.
- Cleanup preserves dirty worker worktrees by default.
- Deletion helpers only remove known runtime-managed paths.
- Runtime state is evidence-bearing and may be inspected by `@quality-gate`.

## Contract
- `run.json` is the source of truth for durable execution status.
- Tasks and mailbox entries are separate files for simple replay and partial recovery.
- Worker execution records live under `.opencode/state/runs/<run-id>/workers/*.json`.
- Runtime state complements `.opencode/plans/` and `.opencode/evidence/`; it does not replace them.

## CLI entrypoints
- `node scripts/runtime/cli.mjs create --run-id <id> --goal <goal> --mode maintenance --json`
- `node scripts/runtime/cli.mjs status --run-id <id> --json`
- `node scripts/runtime/cli.mjs continue --run-id <id> --json`
- `node scripts/runtime/cli.mjs dispatch --run-id <id> --task-id <task> --worker-name <worker> --prompt <prompt> --json`
- `node scripts/runtime/cli.mjs execute --run-id <id> --execution-id <id> --json`
- `node scripts/runtime/cli.mjs board --run-id <id>`
- `node scripts/runtime/cli.mjs poll --run-id <id>`
- `node scripts/runtime/cli.mjs retry --run-id <id> --task-id <task> --execution-id <id>`
- `node scripts/runtime/cli.mjs consume --run-id <id> --worker-name <worker>`
- `node scripts/runtime/cli.mjs supervise --run-id <id> --max-retries 2`
- `node scripts/runtime/cli.mjs tail --run-id <id> --execution-id <id> --lines 20`
- `node scripts/runtime/cli.mjs tail --run-id <id> --execution-id <id> --follow --ticks 5 --interval-ms 250`
- `node scripts/runtime/cli.mjs heartbeat --run-id <id> --worker-name <worker> --owner <owner> --lease-ms 30000`
- `node scripts/runtime/cli.mjs lease-status --run-id <id> --worker-name <worker>`
- `node scripts/runtime/cli.mjs lease-cleanup --run-id <id> --worker-name <worker> --force`
- `node scripts/runtime/cli.mjs lease-sweep --run-id <id> --force`
- `node scripts/runtime/cli.mjs diagnostics --run-id <id>`
- `node scripts/runtime/cli.mjs diagnostics-snapshot --run-id <id> --snapshot-id snap-1`
- `node scripts/runtime/cli.mjs dashboard-export --run-id <id> --snapshot-id dash-1`
- `node scripts/runtime/cli.mjs tail-session-start --run-id <id> --execution-id <id> --session-id tail-1`
- `node scripts/runtime/cli.mjs tail-session-status --run-id <id> --session-id tail-1`
- `node scripts/runtime/cli.mjs tail-session-stop --run-id <id> --session-id tail-1`
- `node scripts/runtime/cli.mjs tail-session-gc --run-id <id> --max-age-ms 3600000 --include-stopped`
- `node scripts/runtime/cli.mjs board --run-id <id> --watch --ticks 5 --interval-ms 250`

## Minimum statuses
- Run: `planning`, `executing`, `verifying`, `blocked`, `done`, `cancelled`
- Task: `pending`, `claimed`, `completed`, `failed`, `blocked`, `cancelled`
- Mailbox: `pending`, `acked`

## Ops loop
- Retry loops must be bounded and persisted via worker execution/task metadata.
- Mailbox consumption must acknowledge concrete messages rather than deleting them silently.
- Process polling may upgrade `spawned` -> `running` or `exited` conservatively based on pid liveness.
- Live board summaries should expose execution counts plus actionable tasks.
- Supervisor ticks may poll, consume, retry, and persist fresh board snapshots without requiring a daemon.
- Retry backoff is bounded and can add deterministic jitter for staggered retries without breaking replayability.
- Mailbox consumers can use worker lease locks under `.opencode/state/locks/` for single-consumer safety, with heartbeat renewal to extend active leases and diagnostics/sweeper CLI for stale locks.
- Execution stdout/stderr logs live under `.opencode/state/runs/<run-id>/logs/<execution-id>/`.

## Evidence expectations
For material autonomous execution, final evidence should preserve:
- run id,
- task summary,
- mailbox summary,
- execution status summary,
- validation outputs,
- residual blocked or failed items,
- worktree preservation notes when relevant.

- Diagnostics history snapshots live under `.opencode/state/runs/<run-id>/diagnostics-history/`.
- Dashboard export writes `.opencode/state/runs/<run-id>/dashboard/dashboard.txt` and `.html`.
