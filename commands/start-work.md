---
description: Execute approved plan-bound work strictly from the existing plan with measurable progress, evidence, and verification
agent: orchestrator
model: 9router/high
---

Execute the work strictly from the approved existing plan. Do not re-plan unless the current plan is missing, blocked, stale, contradictory, or explicitly fails its own execution gate.

Arguments from user, if any:

```text
$ARGUMENTS
```

Primary objective:
- turn the existing approved plan into execution without drifting from it,
- keep execution finish-first but bounded by the plan,
- require evidence before claims,
- avoid code, config, or behavior decisions based on assumptions,
- and preserve clear progress tracking from first step to final verification.

Execution contract:

0. Scripts MCP preference.
   - For governance read/check/query tasks (plan validation, readiness, smoke, runtime verify, template discovery, progress read), prefer `scripts` MCP when connected, usable, and permitted.
   - Fallback to canonical CLI when MCP is disconnected, unavailable after config change, `tool_pending`, not permitted, or exact operation absent.
   - All existing `python3` CLI command lines below remain valid and executable. MCP does not replace them.

1. Refresh active-lane context first.
   - Confirm the active lane is `@orchestrator`.
   - Re-anchor on the current role contract, not the previous lane's assumptions.
   - Load the `opencode-orchestrator` skill first.
   - State explicitly in the first substantial response:
     - `Skill I’m using: opencode-orchestrator`
     - `MCPs I’m using: ...`
     - `What I’m checking first: ...`

2. Treat the existing plan as the execution source of truth.
   - Look for the relevant plan under `.opencode/plans/`.
   - If `$ARGUMENTS` names a task id, plan id, feature, or file, use that to identify the target plan.
   - If more than one plausible plan matches, stop and ask which plan to execute.
   - If no plan exists, do not silently improvise implementation. Route to planning first.

3. Before any implementation, read and extract from the plan:
   - Plan Quality Gate value
   - mode (`PASS` or `PASS_FOR_SLICE` required)
   - Execution Source of Truth
   - Existing Patterns / Reuse
   - Source Anatomy
   - Reference Map
   - Confirmed vs Assumed audit or equivalent labels
   - Non-negotiable Implementation Invariants
   - Do Not / Reject If
   - Diff Boundary
   - Executor Handoff Prompt
   - Execution-ready Worklist / Handoff Contract
   - validation commands
   - evidence path
   - Done Criteria

4. Hard execution gate.
   - Execute only when the plan is clearly `PASS` or `PASS_FOR_SLICE`.
   - If plan status is `NEEDS_DEPTH`, `BLOCKED`, missing, contradictory, or missing execution-critical sections, stop and route back to `@artifact-planner`.
   - Do not downgrade this gate just because the plan “looks good enough”.

5. No assumption rule.
   - Do not claim `already exists`, `already running`, `already configured`, `repo uses`, `package version is`, or `current code does` without verification.
   - Every material claim about code, runtime, config, dependencies, or docs must be labeled as one of:
     - `confirmed_repo`
     - `confirmed_runtime`
     - `confirmed_docs`
     - `user_confirmed`
     - `assumption`
     - `unverified`
   - Never write code from guessed file paths, guessed APIs, guessed config keys, or guessed project patterns.
   - If a fact is missing and materially affects implementation, verify first or ask.

6. Harness and stack preflight.
   - Before non-trivial execution, verify the target project has:
     - root `AGENTS.md`
     - canonical `.opencode/docs/`
     - root `DESIGN.md` when UI/design work is involved
     - `.opencode/docs/PROJECT_STACK.md`
     - `.opencode/docs/PROJECT_COMMANDS.md`
     - `.opencode/docs/FRAMEWORK_PLAYBOOK.md`
     - `.opencode/docs/PROJECT_DETECTED_TOOLS.md`
   - If these are missing or stale for non-trivial work, run `/init-harness` first or tell the user it must be run before broad execution.
   - Tiny, read-only, or emergency exceptions must be explicitly recorded.

7. Progress tracking is mandatory and must run at every status transition.
    - Run execution readiness before reading the task map, initializing progress, or dispatching workers:
      - `python3 ~/.config/opencode/scripts/plan-execution-readiness.py <plan.md> --project-root .`
    - Nonzero readiness output is a planner contract defect. Route back to `@artifact-planner`; do not ask user to manually repair planner syntax.
    - Initialize plan progress from the selected plan before the first implementation step:
      - `python3 ~/.config/opencode/scripts/task-progress.py <task-id> --init --plan <plan.md>`
    - The plan must contain a `## Progress Tracking` section. If it is missing, stop and route back to `@artifact-planner` — do not invent tracker commands.
   - Use the plan's `task_map` to drive every tracker update. Use the exact `task-progress.py --update <id> ...` command from the plan.
   - Keep exactly one active task `in_progress` at a time unless the plan explicitly allows independent parallel branches.
   - Update the tracker at every transition:
     - `pending` -> `in_progress` immediately before a task is started
     - `in_progress` -> `completed` immediately after exit verification passes
     - `in_progress` -> `blocked` whenever a blocker is hit (with `--evidence <blocker-note.md>`)
     - `in_progress` -> `cancelled` if the task is removed or merged
     - any time the worker writes new evidence for a task, also re-run `--update` with the latest `--evidence` path
   - Allowed statuses: `pending`, `in_progress`, `completed`, `blocked`, `cancelled`.
   - Record owner, depends_on, validation result, and evidence path on every update.
   - Do not claim completion while pending non-blocked tasks remain.
   - Before any user-facing progress report, cross-check with:
     - `python3 ~/.config/opencode/scripts/task-progress.py <task-id> --summary`
     - `python3 ~/.config/opencode/scripts/task-progress.py <task-id> --checklist`
   - Tracker drift is a process defect. If the tracker and the actual worklist disagree, reconcile them before moving on.

8. Execute in plan order.
   - Start from `start_with` if present.
   - Then execute one ready task at a time respecting:
     - `depends_on`
     - `must_preserve`
     - `do_not_touch`
     - `validation`
     - `exit_verification`
     - `evidence_update`
   - Do not skip ahead just because a later task looks easier.
   - Do not expand scope beyond the accepted diff boundary.

9. Delegation must preserve the plan.
   - For non-trivial worker delegation, send a structured handoff payload with at least:
     - `task_id`
     - `plan_id`
     - `caller`
     - `callee`
     - `scope`
     - `claim_level`
     - `claim_scope`
     - `source_basis`
     - `must_preserve`
     - `do_not_touch`
     - `validation`
     - `exit_criteria`
     - `evidence_required`
     - `depends_on`
     - `context_bundle`
   - Validate the payload with:
     - `python3 ~/.config/opencode/scripts/subagent-handoff-check.py --payload -`
   - Write delegation log entries to:
     - `.opencode/state/<task-id>/delegation.jsonl`
   - Workers execute only. They must not silently reroute, redesign, or re-scope the task.
   - For delegated tasks, the executor must also enforce tracker discipline on the worker's behalf:
     - mark the delegated task `in_progress` when handing it off
     - mark the task `completed`, `blocked`, or `cancelled` as soon as the worker reports back
     - record the worker's evidence path in the tracker `--evidence` field

10. Reference-first execution.
   - Reuse existing repo patterns before creating new abstractions.
   - Prefer stdlib, native platform features, existing project utilities, and already-installed dependencies.
   - Use official docs or repo-local docs when behavior is version-sensitive.
   - For UI/reference-heavy work, the project `DESIGN.md` and cited references remain binding inputs.
   - For template/clone/1:1/reference-copy work, run the template/source discovery gate first when applicable.

11. Finish-first blocker handling.
   - Classify blockers as:
     - `hard_stop`
     - `soft_blocker`
     - `deferred_question`
     - `follow_up`
   - Continue safe execution for `soft_blocker` items.
   - Defer non-blocking questions to the end.
   - Stop only for true `hard_stop` conditions: irreversible actions, security/privacy boundary requiring approval, missing mandatory external access, contradictory requirements, or a material non-reversible decision with no safe subset.

12. Verification before moving on.
   - After each task, run the task's exit verification.
   - If validation fails, remediate within scope before proceeding.
   - Before any completion claim, run a Plan Compliance Checkpoint against:
     - all non-blocked worklist tasks,
     - Non-negotiable Implementation Invariants,
     - Do Not / Reject If,
     - validation results,
     - evidence updates,
     - Diff Boundary,
     - Done Criteria.

13. Functional evidence is required.
   - Mechanical checks alone are not enough.
   - Run static smoke verification when available:
     - `python3 ~/.config/opencode/scripts/pre-gate-smoke-check.py --project-root .`
   - Run runtime verification when the work touches app/runtime/API behavior:
     - `python3 ~/.config/opencode/scripts/runtime-verify.py --project-root . --base-url <url>`
   - If runtime verification cannot be performed, do not claim full readiness. Report exactly what remains unverified.

14. Non-trivial work must go through `@quality-gate` before final completion claim.
   - If quality gate returns `NEEDS_FIX`, `BLOCKED`, or `PASS_WITH_RISKS`, convert findings into remediation tasks.
   - Execute every non-blocked remediation item finish-first.
   - Re-run targeted validation.
   - Return to `@quality-gate` before finalizing.

15. User-facing communication rules.
   - Default to Bahasa Indonesia.
   - Keep technical literals unchanged.
   - Do not present assumptions as facts.
   - Do not dump raw internal schemas to the user.
   - When summarizing, distinguish clearly between completed work, residual risks, deferred questions, and follow-ups.

16. Completion rule.
   - Only claim `done`, `ready`, or equivalent when:
     - the selected plan passed the execution gate,
     - all non-blocked plan tasks required for the slice are completed,
     - validation and functional evidence exist,
     - diff stayed within boundary or deviations were justified,
     - and `@quality-gate` has passed for non-trivial work.
   - If the plan is `PASS_FOR_SLICE`, report slice completion only. Do not inflate to full-project completion.

17. If command/config/prompt files are changed during this work, remind the user at the end to restart OpenCode so startup-loaded files are refreshed.

Start by:
1. identifying the target plan,
2. verifying the plan is execution-ready,
3. initializing progress tracking,
4. then executing strictly from the worklist.

If any of those four cannot be done, stop and report the exact blocking reason without improvising code.
