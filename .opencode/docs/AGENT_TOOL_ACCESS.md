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

## Graphify discovery boundary

All lanes must query Graphify first for code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes when fresh graph is available and permitted. Use narrow `query`, `path`, or `explain` requests. `INFERRED` and `AMBIGUOUS` edges are leads, not facts. Direct source reading, tests, and runtime verification remain mandatory before edits or material claims. If graph is missing, stale, or unsupported, use normal repo discovery or an approved refresh and record fallback. Tiny known-file edits and non-code tasks may skip with explicit reason. Graphify does not grant write access or change lane ownership.

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
- **permitted**: UI/UX direction and implementation within designer contract; implementation only when directly routed, while `@artifact-planner` usage is read-only advisory input.
- **fallback**: if generation/design MCP is unavailable, continue with local design-system reasoning and mark limitation.

### `@fixer`
- **available**: implementation and validation toolchain.
- **preferred**: minimal scoped edits, tests, and validation against provided plan/handoff.
- **permitted**: bounded implementation (including tests/fixtures) within task scope.
- **fallback**: if requirements/spec are ambiguous, stop and route back for clarification/design.

### `@fixer with frontend skill`
- **available**: web implementation and validation toolchain.
- **preferred**: project-local design guidance, existing component patterns, focused tests, browser checks when relevant.
- **permitted**: bounded web UI edits after design direction exists.
- **fallback**: route missing UX/visual direction to `@designer`; route unclear API contracts to `@fixer with backend skill`/`@artifact-planner with system-analysis skill`.

### `@fixer with mobile skill`
- **available**: mobile implementation and safe validation toolchain.
- **preferred**: existing navigation/platform patterns and safe build/test/simulator checks.
- **permitted**: bounded React Native/Expo/Flutter/mobile app edits.
- **fallback**: route native architecture/privacy/store boundaries to `@architect`/`@quality-gate`.

### `@fixer with backend skill`
- **available**: API/server/data implementation and validation toolchain.
- **preferred**: existing service/validation/auth/migration/test patterns with TDD for production logic.
- **permitted**: bounded backend edits and safe local validation.
- **fallback**: route unclear requirements/contracts to `@artifact-planner with system-analysis skill`; route major data/security decisions to `@architect`/`@quality-gate`.

### `@fixer with devops skill`
- **available**: CI/CD, Docker, env, release, monitoring, and safe local validation tools.
- **preferred**: dry-run/read-only/local checks before mutation.
- **permitted**: bounded config/script/doc edits; deploy/destructive/credential/production commands require explicit ask/approval.
- **fallback**: route platform/release architecture to `@architect`; final release/security signoff to `@quality-gate`.

### `@artifact-planner with system-analysis skill` (read-only)
- **available**: read-only discovery/research and artifact drafting.
- **preferred**: requirements, user-flow, API contract, data-flow, edge-case, NFR, and acceptance-criteria analysis.
- **permitted**: read-only analysis and handoff output; no source edits.
- **fallback**: route delivery breakdown to `@artifact-planner with project-management skill`; implementation to domain/fixer lanes.

### `@artifact-planner with project-management skill` (read-only)
- **available**: read-only planning/research and artifact drafting.
- **preferred**: milestones, backlog, issue breakdown, dependency/risk register, release checklist, and handoff sequencing.
- **permitted**: read-only planning output; no source edits or external tracker writes unless explicitly approved/configured.
- **fallback**: route unclear requirements to `@artifact-planner with system-analysis skill`; implementation to domain/fixer lanes.

### `@fixer with fullstack skill`
- **available**: frontend + backend implementation and validation toolchain for small vertical slices.
- **preferred**: clear UI/API/data contract with focused tests and integration validation.
- **permitted**: bounded tightly-coupled FE/BE edits only.
- **fallback**: split to `@fixer with frontend skill` + `@fixer with backend skill` or plan first when scope grows.

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
CLI diagnostics first policy for edit-owning lanes (`@orchestrator` tiny direct edits, `@fixer` bounded implementation): use project stack/playbook CLI diagnostics such as lint, typecheck, and test first for rename/refactor/navigation/diagnostic-driven edits. If fallback path used, evidence must include limitation and confidence impact.

## Scripts MCP Access Policy

`mcp.scripts` is a configured local stdio server with fixed tool allowlist, strict schemas, and no arbitrary script/flag passthrough. First slice exposes read/check/query tools only. `caller_lane` is policy attestation, not authorization.

- **all lanes**: may use configured `mcp.scripts` only within role permissions and first-slice read/check/query boundary when connected/usable/permitted.
- **read-only lanes** (`@artifact-planner with system-analysis skill`, `@artifact-planner with project-management skill`, `@artifact-planner`, `@explorer`, `@librarian`, `@oracle`, `@visual-context-extractor`, `@designer with visual-asset skill`): use scripts MCP for evidence/query only. No write operations (deferred).
- **implementation lanes** (`@fixer`, `@fixer with frontend skill`, `@fixer with backend skill`, `@fixer with mobile skill`, `@fixer with fullstack skill`, `@fixer with devops skill`): use scripts MCP for validation/readiness checks within task scope. Cannot invoke deferred write operations because they do not exist in this slice.
- **core routing agents** (`@orchestrator`, `@quality-gate`): use scripts MCP per lane contract.

Fallback to canonical CLI when MCP is disconnected, unavailable after config change, `tool_pending`, not permitted, or lacks exact mapping. MCP availability never overrides existing role policy. See [TOOL_USAGE.md](./TOOL_USAGE.md) for executable fallback commands and [MCP.md](./MCP.md) for tool inventory.

## Agent Context Refresh (mandatory)
- Lanes are not sticky across session turns. Before any tool use, verify the currently active lane.
- If the active lane changed, discard assumptions inherited from the previous lane's read-only/implementation boundaries.
- Do not carry `@artifact-planner` read-only restrictions into `@orchestrator` or implementation lanes.
- Do not carry `@orchestrator` delegation preference into read-only reviewer lanes when they are the active lane.
- A lane switch resets which tools are permitted. Re-read the active agent contract when in doubt.


1. Availability does not override permission boundaries.
2. Preferred path can be skipped only with a concrete reason (not habit).
3. Fallback must preserve safety and evidence posture.
4. Read-only reviewers and read-only artifact lanes (`@artifact-planner with system-analysis skill`, `@artifact-planner with project-management skill`) must not modify source files.

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
## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.
