---
name: opencode-plan-validator
description: Mechanical plan contract validation and safe plan-artifact remediation for /check-plan.
---

# OpenCode Plan Validator

## Purpose
Validate execution readiness against repository plan, compliance, and handoff contracts. In `check-and-fix` mode, repair only mechanical omissions in the plan artifact.

## Reference-first
Use plan-local and repository-local evidence first. Treat assumptions as assumptions; avoid turning them into fake certainty. Record validator evidence and residual failures.

## Workflow
1. Locate target plan and read caller mode.
2. Run `validate-plan-depth.py`, `plan-compliance-check.py`, and `subagent-handoff-check.py`.
3. Classify failures as mechanically auto-fixable or requiring planner input.
4. In `check-and-fix`, edit only `.opencode/plans/**/*.md` for safe mechanical repairs.
5. Re-run validators and return deterministic status: `PASS`, `PASS_FOR_SLICE`, `NEEDS_DEPTH`, or `BLOCKED`.

## Quality checklist
- [ ] Plan path exists.
- [ ] Required validators ran.
- [ ] Auto-fixes stay inside plan artifact.
- [ ] Status matches post-fix output.
- [ ] Evidence paths and residual failures are listed.

## Anti-patterns
- Do not invent requirements, owners, references, or scope.
- Do not edit source code, configuration, or unrelated evidence.
- Do not promote failing validation to `PASS`.
- Do not auto-fix domain decisions.

## Output example

```yaml
status: PASS_FOR_SLICE
task_id: <task-id>
plan_path: <plan-path>
mode: check-and-fix
validators_run: []
auto_fixes: []
requires_planner: []
failures: []
evidence: []
```


<!-- scripts-mcp-pointer -->
`mcp.scripts` is a configured local read/check/query-only governance tool. This read-only skill should prefer it over raw shell invocation of matching plan validation, runtime verification, progress reading, audit, discovery, memory query, or delegation query scripts when connected, usable, and permitted; no write operations exist in this slice. `caller_lane` in the tool payload is policy attestation only, not real authorization; this skill’s existing read-only boundary still controls what it may do. Canonical CLI fallback remains valid: `python3 ~/.config/opencode/scripts/<name>.py ...` when MCP is disconnected, unavailable, returns `tool_pending`, or is not permitted. Full policy: `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`.
