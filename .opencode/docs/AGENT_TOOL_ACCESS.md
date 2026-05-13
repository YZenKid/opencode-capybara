# Agent Tool Access Matrix

This document is the canonical matrix for tool access behavior by agent role.

Operating model context (routing details stay in `AGENT_ROUTING.md`):
- 6 core agents handle default daily flow.
- Trigger-only helper/specialist lanes are exception lanes (including unified `@architect`).
- `@artifact-planner` is a triggered planning lane (not default-first).

It complements:
- [TOOL_USAGE.md](./TOOL_USAGE.md) for operational selection guidance
- [AGENT_ROUTING.md](./AGENT_ROUTING.md) for role routing
- [MCP.md](./MCP.md) for MCP inventory only

## Definitions

- **available**: tool exists in runtime.
- **preferred**: default best tool path for that role/task.
- **permitted**: allowed by role contract/permission boundary.
- **fallback**: safe alternate when preferred is unavailable/not permitted.

## MCP state interpretation

Use MCP state terms from [MCP.md](./MCP.md) when discussing tool readiness.

- configured alone is inventory-level only, not execution readiness.
- Runtime use should require `authenticated + connected + role-permitted` for the needed capability.
- If capability is unavailable by role/client/server limits, classify it as `read-only/unsupported constraints` and route to the documented fallback.

## Matrix (documented lanes and helpers)

### `@orchestrator`
- **available**: broad OpenCode + delegated specialist paths.
- **preferred**: route first to the best specialist lane; use local tools for small direct tasks.
- **permitted**: bounded by orchestrator permissions and delegation contracts.
- **fallback**: if specialist/tool unavailable, choose next permitted lane and record limitation.

### `@artifact-planner`
- **available**: discovery/research tools and advisory subagents.
- **preferred**: repo-local discovery + targeted external verification for planning confidence.
- **permitted**: planning artifacts only (`.opencode/plans`, `.opencode/draft`, `.opencode/evidence`), no implementation edits.
- **fallback**: if a stronger source is unavailable, record assumptions and confidence limits in plan evidence.

### `@explorer` (read-only discovery)
- **available**: local search/read pathways.
- **preferred**: `glob` + `grep` + `read` for fast codebase mapping.
- **permitted**: read-only discovery behavior.
- **fallback**: escalate unresolved ambiguity to `@orchestrator`/`@oracle` with evidence.

### `@librarian`
- **available**: documentation/research-oriented tools.
- **preferred**: official docs path first (`context7`), then source/examples.
- **permitted**: research and explanation, not implementation edits.
- **fallback**: if official docs unavailable, use source/GitHub + explicit uncertainty notes.

Note: `@librarian` is a supporting research helper, not one of the 6 core agents or 6 specialist lanes in the simplified routing model.

### `@designer`
- **available**: UI/design analysis and relevant MCP surfaces when configured.
- **preferred**: project-local `DESIGN.md` + structured UI evidence + design specialist workflows.
- **permitted**: UI/UX direction and implementation within designer contract.
- **fallback**: if generation/design MCP is unavailable, continue with local design-system reasoning and mark limitation.

### `@fixer`
- **available**: implementation and validation toolchain.
- **preferred**: minimal scoped edits, tests, and validation against provided plan/handoff.
- **permitted**: bounded implementation (including tests/fixtures) within task scope.
- **fallback**: if requirements/spec are ambiguous, stop and route back for clarification/design.

### `@oracle`
- **available**: read-heavy analysis/review pathways.
- **preferred**: architecture/risk/tradeoff review with concrete repo evidence.
- **permitted**: review/advisory output, not direct implementation lane.
- **fallback**: provide bounded recommendation + risk framing when data is incomplete.

### `@quality-gate`
- **available**: read-only conformance/review pathways.
- **preferred**: evidence-based final gate using validation outputs and policy docs.
- **permitted**: no edits; final quality/risk verdict only.
- **fallback**: return `PASS_WITH_RISKS`/`NEEDS_FIX`/`BLOCKED` with explicit reason codes when evidence is incomplete.

## Boundary rules

1. Availability does not override permission boundaries.
2. Preferred path can be skipped only with a concrete reason (not habit).
3. Fallback must preserve safety and evidence posture.
4. Read-only reviewers must not modify source files.

## Conflict resolution examples

- Tool is available globally, but current role is read-only:
  - Do not execute write action; delegate to permitted implementation lane.
- Fastest tool conflicts with policy/safety:
  - Choose compliant tool path and note tradeoff.
- Preferred external research unavailable:
  - Use local/source fallback and downgrade confidence explicitly.

## Maintenance

Update this matrix when any of the following changes:
- role permissions/contracts,
- tool inventory that materially changes preferred paths,
- routing policy that changes which role should execute which class of tool work.
