---
name: opencode-plan-reviewer
description: Dedicated plan depth validation workflow for execution-ready plans.
---

# OpenCode Plan Reviewer

Use this skill to validate that a plan is deep enough before implementation.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: sharper validation and clearer failure reporting are good; invented evidence or fake compliance are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include key references or repo artifacts that materially shaped the verdict.

## Internet-reference default
- Verify that non-trivial/version-sensitive plans cite current official docs/upstream sources where implementation could materially change. Missing live verification is an actionable plan gap when repo docs are insufficient.

## Finish-first + question batching
- See `.opencode/docs/EXECUTION_CONDUCT.md`. Return directly actionable depth failures. Batch all user-owned decisions into one `question_batch`; never scatter clarification prompts across findings.

## Purpose
Prevent shallow plans from reaching implementation even when they contain all required section headings.

## Trigger / skip

- Trigger: before execution of non-trivial plans, when planner quality is in doubt, or when user explicitly asks whether a plan is implementation-ready.
- Skip: tiny maintenance or single-file fixes where full planning depth is intentionally unnecessary.

## Pre-flight Skill & MCP Discovery
Before the first substantial answer, diagnosis, route, or implementation step on non-trivial work:
- Name the skill explicitly (`Skill I'm using: ...`).
- Decide MCP applicability explicitly (`MCPs I'm using: ...`, `What I'm checking first: ...`).
- If an MCP is obviously applicable, use it or record a concrete skip reason. Silent skip is a defect.
- At final summary time, name one concrete thing this skill changed about execution. Loaded-but-unused skill is a process defect.

ponytail: This is a behavioral contract. Use `scripts/session-trace-audit.py` as the advisory checker until transcript hooks become first-class.

## Workflow
1. Locate primary plan file at `.opencode/plans/<task-id>.md`
2. Run validation script:
   ```bash
   python3 ~/.config/opencode/scripts/validate-plan-depth.py .opencode/plans/<task-id>.md
   ```
3. Verify all metrics pass (depth, anti-generic, reference pack, design depth)
4. If any metric fails, return `NEEDS_DEPTH` with specific failures
5. If all metrics pass, return `PASS`

## Minimum depth requirements

| Metric | Minimum |
|---|---|
| Goal + Non-goals words | apply when task is non-trivial |
| Requirements count | apply when task is non-trivial |
| Acceptance Criteria count | apply when task is non-trivial |
| UI pages (greenfield) | proportional to scope |
| Components in inventory | proportional to UI surface |
| Implementation steps | enough for execution-ready worklist |
| Validation commands | enough to verify claimed scope |

## Anti-generic patterns (mechanical failures)

The validator checks for these patterns and fails if any are found:
- centered gradient hero
- generic "modern clean"
- fake dashboard metrics / arbitrary KPI
- emoji icons / numeric-only icons
- placeholder imagery / blank image frames
- repeated card/grid anatomy (card spam)
- abstract blobs / floating UI cards / CSS glass panels
- vague neon blobs / default purple/blue glow
- debug/internal copy / server labels / port numbers
- lorem text / placeholder copy
- missing hero composition
- missing image strategy
- missing motion motivation
- missing reduced-motion support

## Reference pack requirement

Plan must include:
- Minimum 3 reference screenshots/URLs, OR
- Explicit first-principles rationale

Reference pack must cover:
1. Visual direction / aesthetic family
2. Layout / composition patterns
3. Component / interaction patterns
4. Asset / image style
5. Motion / transition style

## Design depth keywords

Plan must contain these keywords:
- design read
- design_variance
- motion_intensity
- visual_density
- page-by-page
- section-level
- component inventory
- asset/image decision
- motion system
- reduced-motion
- accessibility gate
- validation evidence

## State coverage requirement
Every component must document: empty, loading, error, success states.

## Delegation Input Understanding Contract

Before acting on a delegated task, reconstruct the request from the handoff payload rather than from memory alone.

Minimum understanding checklist:
- `task_id` / `plan_id`: what task this belongs to
- `scope`: single concrete outcome you own
- `claim_level` + `claim_scope`: what you may report as done
- `source_basis`: the files/docs/refs you must treat as authority
- `must_preserve`: invariants that cannot be broken even if a shortcut seems easier
- `do_not_touch`: paths/scopes that are out of bounds
- `validation`: what you must run/check before reporting done
- `evidence_required`: what artifacts/logs/screenshots must exist before you return
- `open_assumptions`: what is still uncertain and must stay uncertain

If any of these are missing from the handoff for non-trivial work, stop and report `blocked: incomplete handoff contract` back to `@orchestrator`. Do not fill the gaps with intuition.

### Return contract
Your return report should mirror the handoff:
- what you changed or discovered,
- which `must_preserve` items were maintained,
- which validation checks you ran,
- which evidence paths now exist,
- what remains `assumption` / `unverified`.

ponytail: This is a soft discipline first. The upgrade path is a session-trace/delegation-log audit that flags workers who routinely act on incomplete handoffs.

## Output contract
- Status: `PASS` or `NEEDS_DEPTH`
- Validation script output
- Specific failures if any
- Recommendation: expand plan or proceed

## Output example

```yaml
status: PASS
validation_script_output:
  plan_lines: 2847
  requirements_count: 12
  acceptance_criteria_count: 9
  implementation_steps: 45
  validation_commands: 8
proportional_depth_check: "PASS - scope is medium complexity, depth is appropriate"
worklist_quality: "PASS - tasks are atomic, owners assigned, dependencies clear"
```

## Escalation

- Escalate to `@artifact-planner` when plan needs deeper detail, evidence, or worklist structure.
- Escalate to `@designer` when UI/design depth is the main failing dimension.
- Escalate to `@system-analyst` when requirements/acceptance criteria are too weak to support deeper planning.


## Quality checklist
- [ ] Plan metrics checked against proportional depth (not fixed line counts).
- [ ] Sections contain substance, not only labels.
- [ ] Worklist is atomic and execution-ready.
- [ ] Validation/evidence path is concrete.
- [ ] Readiness label matches actual plan quality.
- [ ] Stack verification steps are documented.
- [ ] Handoff prompt includes worker contract.

## Anti-patterns
- Passing plans with full headings but shallow content.
- Ignoring weak validation or missing exit criteria.
- Treating speculative ideas as execution-ready tasks.
- Failing to distinguish `PASS_FOR_SLICE` vs full-product readiness.
- Enforcing arbitrary line-count minimums instead of depth-by-scope.
- Skipping validation of handoff prompt completeness.


## Local resources

- `~/.config/opencode/scripts/validate-plan-depth.py`
- `.opencode/docs/EXAMPLE_PLAN.md`

## Reference
- Validation script: `~/.config/opencode/scripts/validate-plan-depth.py`
- Reference plan: `.opencode/docs/EXAMPLE_PLAN.md`

## Hard rule
Section presence alone is NOT sufficient. A plan with all required headings but shallow content must be rejected as `NEEDS_DEPTH`.


<!-- scripts-mcp-pointer -->
`mcp.scripts` is a configured local read/check/query-only governance tool. This read-only skill should prefer it over raw shell invocation of matching plan validation, runtime verification, progress reading, audit, discovery, or delegation query scripts when connected, usable, and permitted; no write operations exist in this slice. `caller_lane` in the tool payload is policy attestation only, not real authorization; this skill’s existing read-only boundary still controls what it may do. Canonical CLI fallback remains valid: `python3 ~/.config/opencode/scripts/<name>.py ...` when MCP is disconnected, unavailable, returns `tool_pending`, or is not permitted. Full policy: `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`.
## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.
