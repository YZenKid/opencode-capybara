# Planning and Handoffs

Read this before plan-bound work, delegation, or remediation loops.

## Plan-bound execution

- `@artifact-planner` is triggered only when planning complexity, unresolved architecture/security/data/product decisions, multi-phase scope, or evidence-heavy work require durable artifacts.
- `PASS` and `PASS_FOR_SLICE` may proceed to implementation.
- `NEEDS_DEPTH` returns to planner or advisory lanes.
- `BLOCKED` means material decision missing and no safe slice exists.

## Delegation payload

Required fields:

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

## Worker rules

- Worker gets 3-10 highest-signal verified facts only.
- Preserve open assumptions explicitly.
- Non-trivial delegation without valid payload is a defect.
- Workers do not reroute or delegate.

## Quality Gate Remediation / Risk Worklist

- Treat non-`PASS` quality gate output as an execution input.
- Copy each remediation item into plan/evidence with `finding`, `blocker_or_risk_class`, `owner_lane`, `action`, `validation`, `exit_criteria`, and `requires_user_decision`.
- For `NEEDS_FIX` and `BLOCKED`, execute all items that are not `hard_stop` and do not require user decision.
- For `PASS_WITH_RISKS`, separate `required_before_PASS` from `non_blocking_follow_up`.
- Rerun targeted validation and reroute to `@quality-gate` after remediation.

## Trigger phrases to preserve

- Quality Gate Remediation / Risk Worklist
- non-`PASS` quality gate output as an execution input
- blocker_or_risk_class
- owner_lane
- exit_criteria
- requires_user_decision
- required_before_PASS
- non_blocking_follow_up
- Rerun targeted validation and reroute to `@quality-gate`
