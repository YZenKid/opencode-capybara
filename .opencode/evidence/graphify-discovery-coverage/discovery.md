# G1 Discovery Audit

- task_id: `graphify-discovery-coverage-G1`
- plan_id: `graphify-discovery-coverage`
- scope: read-only inventory; evidence only
- source basis: `.opencode/plans/graphify-discovery-coverage.md`, root `AGENTS.md`, canonical docs, Graphify skill, local agent/skill files, existing checks
- status: `confirmed_repo`; no runtime/server enforcement claim

## Counts

- Agent files: **23** under `agents/*.md`.
- Local `skills/opencode-*` skill files: **23** under `skills/opencode-*/SKILL.md`.
- Active Sequential Thinking cap-3 files: **22** total:
  - 3 canonical docs: `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`
  - 1 derived doc: `docs/generated/mcp-risk-matrix.md`
  - 18 local skills listed below
- Graphify canonical policy surfaces: **6**: `AGENTS.md`, `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`, `.opencode/docs/SKILLS.md`, `skills/graphify-discovery/SKILL.md`.

## Canonical Graphify inheritance chain

1. Root `AGENTS.md:33-34` gives global inheritance: Graphify optional/local/code-only/read-only; query-first only for broad architecture/dependency discovery when graph fresh; inferred/ambiguous edges remain leads; source/tests/runtime checks remain authoritative.
2. `.opencode/docs/MCP.md:109-111` defines Graphify discovery context and points operational guidance to `.opencode/docs/TOOL_USAGE.md`; lines `28-32` define Sequential Thinking policy.
3. `.opencode/docs/TOOL_USAGE.md` and `.opencode/docs/AGENT_TOOL_ACCESS.md` carry operational/access wording.
4. `.opencode/docs/SKILLS.md` indexes the dedicated Graphify skill and local skill policy.
5. `skills/graphify-discovery/SKILL.md:8-24` supplies dedicated workflow and boundaries: optional, local, code-only, read-only, direct source verification mandatory, no blocking when unavailable.

No Graphify prose needs copying into all agents/skills. Inheritance-first coverage should extend existing mechanical checks to assert root/canonical policy and enumerate all local surfaces.

## Exact active cap-3 files

### Canonical docs

- `.opencode/docs/MCP.md:32`
- `.opencode/docs/TOOL_USAGE.md:61-62`
- `.opencode/docs/AGENT_TOOL_ACCESS.md:35-36`

### Derived output

- `docs/generated/mcp-risk-matrix.md:19` — generated/advisory; not policy source. Refresh/check only after canonical source changes.

### Local skills (18)

- `skills/opencode-architect/SKILL.md:188`
- `skills/opencode-artifact-planner/SKILL.md:556`
- `skills/opencode-backend/SKILL.md:160`
- `skills/opencode-council/SKILL.md:135`
- `skills/opencode-designer/SKILL.md:622`
- `skills/opencode-devops/SKILL.md:158`
- `skills/opencode-explorer/SKILL.md:151`
- `skills/opencode-fixer/SKILL.md:254`
- `skills/opencode-frontend/SKILL.md:296`
- `skills/opencode-fullstack/SKILL.md:156`
- `skills/opencode-librarian/SKILL.md:178`
- `skills/opencode-mobile/SKILL.md:166`
- `skills/opencode-oracle/SKILL.md:146`
- `skills/opencode-orchestrator/SKILL.md:676`
- `skills/opencode-plan-reviewer/SKILL.md:186`
- `skills/opencode-project-manager/SKILL.md:156`
- `skills/opencode-quality-gate/SKILL.md:475`
- `skills/opencode-skill-improver/SKILL.md:129`

The remaining five local skill files had no exact `at most 3 thought steps` match in targeted search: `opencode-design-system-engineer`, `opencode-plan-validator`, `opencode-system-analyst`, `opencode-visual-asset-generator`, `opencode-visual-context-extractor`. Re-run broader semantic grep during implementation if policy wording changes. The count above follows exact phrase matches: 18 skills.

## Minimum mechanical audit proposal

Extend existing checks, not add redundant policy prose:

1. `scripts/agent-boundary-check.mjs`: assert root `AGENTS.md` contains required Graphify invariants (`optional`, `local`, `code-only`, `read-only`, fresh-graph query-first, source verification), and assert every `agents/*.md` is covered by root inheritance. Keep agent count inventory output.
2. `scripts/skill-contract-check.mjs`: enumerate every `skills/opencode-*/SKILL.md`; fail on active non-trivial cap-3 wording in local skills/docs; allow tiny fast path `1`; assert dedicated `skills/graphify-discovery/SKILL.md` exists and preserves direct source verification/no-blocking boundaries.
3. Keep `docs/generated/mcp-risk-matrix.md` derived. Run `npm run docs:generate:check` after canonical changes; do not treat generated text as source of truth.
4. Audit command can be existing check extension output, avoiding new wrapper/config/runtime surface. Validation target: `npm run check:agents`, `npm run check:skills`, `npm run docs:generate:check`, plus targeted grep for cap `3` and Graphify invariants.

## Confirmed vs derived vs unknown

- Confirmed: inventory counts and file/line locations above from repo-local glob/grep and source reads.
- Confirmed: Graphify policy is centralized through root `AGENTS.md` plus canonical docs and dedicated skill.
- Derived: `docs/generated/mcp-risk-matrix.md`.
- Unknown/unverified: existing npm checks do not yet enforce Graphify coverage or cap-2 policy; no implementation run performed by this read-only slice.

## Must preserve

- Graphify stays optional, local, code-only, read-only.
- Direct source verification remains mandatory; Graphify never replaces source/tests/runtime checks.
- Cap applies to non-trivial work only; tiny fast path remains one brief thought.
- Cap is prompt-policy/documentation/check contract, not server enforcement.

## Evidence

- Handoff: `.opencode/state/graphify-discovery-coverage/G1-handoff.json`
- Plan: `.opencode/plans/graphify-discovery-coverage.md:48-59, 109-119, 240-252`
- Root policy: `AGENTS.md:33-34`
- MCP policy: `.opencode/docs/MCP.md:28-32, 109-111`
- Existing checks: `scripts/agent-boundary-check.mjs:8-90`, `scripts/skill-contract-check.mjs:10-68`
- Discovery method: repo-local `glob`, targeted `grep`, and line-level source reads; no external docs used.
