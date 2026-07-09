---
description: Run the @plan-validator agent against a plan to confirm it is execution-ready before /start-work
agent: orchestrator
model: 9router/high
---

Validate whether a plan is execution-ready before `/start-work` is allowed to dispatch work. This is a read-only mechanical compliance gate. It does not edit the plan and does not implement.

Arguments from user, if any:

```text
$ARGUMENTS
```

Execution contract:

1. Refresh active-lane context.
   - Confirm the active lane is `@orchestrator`.
   - Load the `opencode-orchestrator` skill.
   - State in the first substantial response:
     - `Skill I'm using: opencode-orchestrator`
     - `MCPs I'm using: ...`
     - `What I'm checking first: ...`

2. Identify the target plan.
   - If `$ARGUMENTS` provides a plan path, use it.
   - Else, if `$ARGUMENTS` provides a task id, resolve to `.opencode/plans/<task-id>.md`.
   - Else, find the most recent file under `.opencode/plans/`.
   - If multiple plans match and the target is unclear, stop and ask which plan to validate.

3. Confirm the plan exists.
   - If the plan file is missing, return `BLOCKED` and tell the user to run `@artifact-planner` first.

4. Prepare evidence directory.
   - `mkdir -p .opencode/evidence/<task-id>/check-plan/`
   - All validator outputs go there.

5. Delegate to `@plan-validator` using the standard worker handoff contract. The handoff must include:
   - `task_id`
   - `plan_id`
   - `caller`: orchestrator
   - `callee`: plan-validator
   - `scope`: validate this plan file is execution-ready
   - `claim_level`: scoped
   - `claim_scope`: validator returns PASS / PASS_FOR_SLICE / NEEDS_DEPTH / BLOCKED only
   - `source_basis`: the plan file path and validator scripts
   - `must_preserve`: validator neutrality, no edits to the plan
   - `do_not_touch`: the plan file
   - `validation`:
     - `python3 ~/.config/opencode/scripts/validate-plan-depth.py <plan.md>`
     - `python3 ~/.config/opencode/scripts/plan-compliance-check.py --project-root . --plan <plan.md> --task-id <task-id>`
     - `python3 ~/.config/opencode/scripts/subagent-handoff-check.py --plan <plan.md>`
   - `exit_criteria`: validator returns a deterministic status with failures and evidence paths
   - `evidence_required`: outputs under `.opencode/evidence/<task-id>/check-plan/`
   - `depends_on`: none
   - `context_bundle`: the plan file path, the task id, and the evidence directory

6. Apply the `Start Here` rule.
   - If the user invoked `/check-plan` directly, just run validation and report.
   - If `@start-work` is being prepared, only proceed if the validator returns `PASS` or `PASS_FOR_SLICE`.

7. Interpret the validator result.
   - `PASS`: plan is execution-ready. Remind the user to invoke `/start-work`.
   - `PASS_FOR_SLICE`: first slice is ready. Clearly state which slice and what remains.
   - `NEEDS_DEPTH`: route back to `@artifact-planner` with the validator's failure list. Do not edit the plan from this command.
   - `BLOCKED`: ask the user or `@orchestrator` to resolve the blocker (missing plan, missing validator, contradictory requirements).

8. Output contract.
   - Status line first.
   - Then a short, structured summary in Bahasa Indonesia.
   - Include:
     - validator outputs (depth, compliance, handoff)
     - list of failures (if any)
     - recommendation
     - evidence paths
     - next action (e.g. "jalankan `/start-work <task-id>`" or "kembalikan ke `@artifact-planner` untuk memperbaiki daftar failure")

9. Hard rules.
   - Do not edit the plan from this command.
   - Do not implement from this command.
   - Do not promote a failing plan to `PASS`.
   - Do not skip the validator because the plan "looks good". Mechanical checks are mandatory for non-trivial plans.
   - Do not run `/start-work` from this command. Validation must finish first.

10. After validation, remind the user to restart OpenCode if any command/config file changed in this run.

Start by:
1. identifying the target plan,
2. preparing the evidence directory,
3. delegating to `@plan-validator`,
4. then returning the validator's verdict.
