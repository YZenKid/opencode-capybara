---
description: Run the @plan-validator agent against a plan to confirm it is execution-ready before /start-work
agent: orchestrator
model: 9router/high
---

Validate whether a plan is execution-ready before `/start-work` is allowed to dispatch work. Default behavior is **check + auto-fix** for mechanical plan-contract failures that are safe to repair directly in the plan artifact. This command may edit the plan file under `.opencode/plans/`, but it must never implement product/source code or change scope.

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
   - `scope`: validate and mechanically repair this plan file
   - `mode`: `check-and-fix` (default) or `check-only` (when `$ARGUMENTS` contains `--check-only`)
   - `claim_level`: scoped
   - `claim_scope`: validator returns PASS / PASS_FOR_SLICE / NEEDS_DEPTH / BLOCKED; in `check-and-fix` mode, may also edit the plan file under `.opencode/plans/`
   - `source_basis`: the plan file path and validator scripts
   - `must_preserve`: existing plan content stays intact (append/fill only); in `check-and-fix` mode, do not remove or rewrite existing content
   - `do_not_touch`: any path outside the plan file (no source code, no configs, no non-`.opencode/` files)
   - `validation`:
      - `python3 ~/.config/opencode/scripts/validate-plan-depth.py .opencode/plans/<task-id>.md --mode auto`
     - `python3 ~/.config/opencode/scripts/plan-compliance-check.py --project-root . --plan <plan.md> --task-id <task-id>`
     - `python3 ~/.config/opencode/scripts/subagent-handoff-check.py --plan <plan.md>`
   - `exit_criteria`: validator returns a deterministic status with failures, auto-fixes (in `check-and-fix`), and evidence paths
   - `evidence_required`: outputs under `.opencode/evidence/<task-id>/check-plan/`
   - `depends_on`: none
   - `context_bundle`: the plan file path, the task id, and the evidence directory

6. Mode selection.
   - If `$ARGUMENTS` contains `--check-only`: use mode `check-only`. The validator must not edit the plan.
   - If `$ARGUMENTS` contains `--fix-only`: use mode `check-and-fix` but skip the user-facing report; just run validators, auto-fix, and re-validate.
   - Default: `check-and-fix`. The validator may edit the plan, re-run validators, and return the post-fix verdict.

7. Apply the `Start Here` rule. The remediation driver is `python3 scripts/plan_remediation_loop.py <task-id> --mode auto`; it validates the canonical plan, records evidence, bounds retries, and emits `NO_PROGRESS` without asking the user.


   - If the user invoked `/check-plan` directly, run validation and report.
   - If `@start-work` is being prepared, only proceed when the validator returns `PASS` or `PASS_FOR_SLICE`.

8. Interpret the validator result.
   - `PASS`: plan is execution-ready. Remind the user to invoke `/start-work`.
   - `PASS_FOR_SLICE`: first slice is ready. Clearly state which slice and what remains.
   - `NEEDS_DEPTH` in `check-and-fix` mode: auto-fixable failures are already repaired; only `requires_planner` items remain. Route those back to `@artifact-planner` with the failure list. The plan file may already be partially updated — say so.
   - `NEEDS_DEPTH` in `check-only` mode: no plan edits. Route all failures to `@artifact-planner`.
   - `BLOCKED`: ask the user or `@orchestrator` to resolve the blocker (missing plan, missing validator, contradictory requirements).

9. Output contract.
   - Status line first.
   - Then a short, structured summary in Bahasa Indonesia.
   - Include:
     - validator outputs (depth, compliance, handoff)
     - `auto_fixes` list (what the validator already repaired in the plan file)
     - `requires_planner` list (what still needs the planner)
     - list of `failures` (if any remain)
     - recommendation
     - evidence paths
     - next action (e.g. "jalankan `/start-work <task-id>`" or "kembalikan ke `@artifact-planner` untuk memperbaiki daftar failure")

10. Hard rules.
   - In `check-and-fix` mode (default): the plan file may be edited, but only the plan file under `.opencode/plans/`.
   - Never edit implementation source, configs outside `.opencode/`, or anything outside the plan file.
   - Never invent scope, requirements, references, or claim labels. Auto-fix only fills in missing mechanical fields.
   - Do not implement from this command.
   - Do not promote a failing plan to `PASS`.
   - Do not skip the validator because the plan "looks good". Mechanical checks are mandatory for non-trivial plans.
   - Do not run `/start-work` from this command. Validation must finish first.

11. After validation, remind the user to restart OpenCode if any command/config file changed in this run.

Start by:
1. identifying the target plan,
2. preparing the evidence directory,
3. delegating to `@plan-validator` in `check-and-fix` mode (default) or `check-only` when `--check-only` is passed,
4. then returning the validator's verdict, including what was auto-fixed and what still needs the planner.
