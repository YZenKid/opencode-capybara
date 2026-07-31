---
description: Check plan readiness without modifying plan or source
agent: orchestrator
model: 9router/high
---

Validate execution readiness for `/start-work`. This command is strictly read-only. It never edits plans, source, config, providers, dependencies, runtime files, or evidence content.

Arguments:

```text
$ARGUMENTS
```

Execution contract:

1. Resolve target plan from `$ARGUMENTS` task ID/path, or newest `.opencode/plans/*.md` when unambiguous.
2. Confirm plan exists. Missing plan returns `BLOCKED`; route planning request to `@artifact-planner`.
3. Prepare evidence directory `.opencode/evidence/<task-id>/check-plan/` only when directory creation is already permitted by command runtime.
4. Run canonical read-only validators through scripts MCP when connected, usable, and permitted. Use CLI fallback otherwise:
   - `python3 ~/.config/opencode/scripts/validate-plan-depth.py <plan> --mode check-only`
   - `python3 ~/.config/opencode/scripts/plan-compliance-check.py --project-root . --plan <plan> --task-id <task-id>`
   - `python3 ~/.config/opencode/scripts/subagent-handoff-check.py --plan <plan>`
5. Return `PASS`, `PASS_FOR_SLICE`, `NEEDS_DEPTH`, or `BLOCKED` with validator output, failures, evidence paths, and recommendation.
6. Only `PASS` or `PASS_FOR_SLICE` permits `/start-work`.
7. Mechanical plan repair belongs to `/fix-plan`. `/fix-plan` may use deterministic scripts or current `@artifact-planner`; no removed agent target is valid.

Hard rules:

- No agent delegation from `/check-plan`.
- No plan mutation.
- No auto-fix, remediation loop, or mutation mode.
- Do not invoke removed agent IDs.
- Do not edit files to make validation pass.
- Do not run `/start-work`.

Output must include:

- status
- depth/compliance/handoff results
- failures
- evidence paths
- recommendation
- next action

Restart OpenCode after command-file changes.
