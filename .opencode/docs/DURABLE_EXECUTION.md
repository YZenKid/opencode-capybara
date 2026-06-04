
# Durable Execution

Use repo-local runtime runs when non-trivial work needs resumable state, explicit task decomposition, or staged verify/fix coordination.

## When to use
- multi-step maintenance work,
- parallel or pseudo-parallel worker batches,
- verify/fix loops that should not rely on chat memory alone,
- replay-heavy maintenance where status inspection matters.

## Run lifecycle
1. Create run metadata.
2. Add ordered tasks.
3. Route workers or helper scripts against those tasks.
4. Update run status as execution advances.
5. Enter verification loop.
6. Close as `done`, `blocked`, or `cancelled`.

## Required fields
- `run_id`
- `goal`
- `mode`
- `status`
- `created_at`
- `updated_at`
- `next_step`
- `evidence_paths`

## Relationship to planning
- Plans remain canonical for non-trivial work definition.
- Runtime runs are the operational ledger for execution progress.
- If a plan includes an `Execution-ready Worklist / Handoff Contract`, copy or map that worklist into runtime tasks before autonomous execution.

## Finish-first posture
- Continue until a true `hard_stop` exists.
- Record `soft_blocker`, `deferred_question`, and `follow_up` in run/task state instead of interrupting early.
- Final user-facing output must summarize runtime state in natural language rather than dumping raw JSON.

## Control surface
- create/update/read durable run records
- map execution-ready worklists into runtime tasks
- summarize mailbox and task state in evidence
- preserve a replayable event stream per run
- expose JSON-first runtime CLI entrypoints for `create`, `status`, `continue`, `dispatch`, and `execute`
