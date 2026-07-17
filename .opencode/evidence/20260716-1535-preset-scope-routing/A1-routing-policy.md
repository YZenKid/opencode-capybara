# A1 routing policy evidence

- task_id: `20260716-1535-preset-scope-routing`
- claim_scope: policy text and agent/skill routing only
- claim_level: `confirmed_repo`

## Policy added

`.opencode/docs/AGENT_ROUTING.md` now defines canonical intent classification before size, risk, planner, delegation, or finish-first:

- `read_only`: inspection, comparison, audit, review, explanation, search, or diagnosis without explicit change intent.
- `implementation`: explicit user change verbs or approved implementation plan.
- Security/risk keywords affect review depth, not authorization.
- Finding, risk, gap, recommendation, or failed check is not authorization.
- Scope Promotion Gate requires explicit user change intent or approved implementation plan.

## Read-only routes

- `tiny-readonly-compare`: narrow local evidence, zero mutation, no external research unless requested, target ≤3 reads and ≤10 total tool calls, stop at answer.
- `read-only-deep-review`: broad or risk-sensitive evidence, zero mutation, no planner, no automatic remediation, explicit checkpoint when scope grows.

## Target references

- `agents/orchestrator.md` points to canonical policy and forbids planner/remediation for `read_only`.
- `skills/opencode-orchestrator/SKILL.md` references canonical routes and separates implementation planning.
- `agents/explorer.md` defines lite/deep read-only behavior and no promotion authority.
- `skills/opencode-explorer/SKILL.md` references canonical classification and keeps explorer read-only.
- `agents/artifact-planner.md` hard-forbids activation for `read_only`; explicit promotion plus material trigger required.

Security/material implementation gates remain unchanged after promotion. Runtime performance and model behavior are not claimed.
