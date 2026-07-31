---
name: opencode-explorer
description: Standalone Read-only codebase discovery workflow for explorer. Use for finding files, symbols, tests, fixtures, patterns, architecture maps, repository structure, and reuse candidates with fast targeted search.
---

# OpenCode Explorer Skill

Use this for read-only discovery after intent classification in `.opencode/docs/AGENT_ROUTING.md`. `tiny-readonly-compare` stays narrow and stops at answer; `read-only-deep-review` may gather broader evidence with an explicit scope checkpoint. Explorer maps facts; it does not decide architecture, write plans, edit files, promote scope, or sign off risk.


See `.opencode/docs/SHARED_POLICIES.md` for reference-first creativity contract.

## Internet-reference default
- Explorer is read-only and primarily repo-local. If the discovery question depends on external/version-sensitive source beyond what local evidence shows, escalate to `@librarian` with the exact unresolved question rather than guessing.
- For symbol/pattern/file mapping, prefer repo-local search; do not pull external refs unless the local evidence does not settle it.

## Finish-first + question batching
- See `.opencode/docs/EXECUTION_CONDUCT.md` for the source-of-truth contract. The short version:
  - Do not bounce minor uncertainty back as a fresh user question. Either narrow the scope further, recommend a safe next lane, or fold the residual into `question_batch`.
  - If the discovery question really depends on external/version-sensitive source, escalate to `@librarian` with the exact open question, not as a generic "please clarify" message.

## When to trigger

| Need | Route |
| --- | --- |
| Find files, symbols, tests, fixtures, patterns, reuse candidates | `@explorer` |
| Current library/API behavior outside repo | `@librarian` |
| Requirements/flows/contracts missing | `@artifact-planner` with system-analysis skill |
| Implementation after scope clear | `@fixer` or domain implementation agent |
| Architecture tradeoff or final risk decision | `@architect`/`@oracle`/`@quality-gate` |

## Search strategy

- Start narrow: filenames, package manifests, routes, tests, configs, known symbols.
- Greenfield App Accelerator: discover repo/project patterns only as deep as needed to ground first-slice options.
- Maintenance Stability Mode: focus discovery on repro area, ownership, tests, and existing patterns for smallest safe fix.
- Search before reading; read only relevant snippets and line ranges.
- Parallelize independent searches: structure, implementation, tests, docs, config.
- Prefer local evidence over assumptions; report "not found" with search patterns used.
- Use AST/LSP-style structure when symbol relationships matter; use codemap/cartography only for unfamiliar repos, broad architecture maps, or explicit mapping requests.
- Avoid broad file dumps and duplicate reads. Link paths/lines instead of pasting long content.

## Pre-flight Skill & MCP Discovery
Before the first substantial answer, diagnosis, route, or implementation step on non-trivial work:
- Name the skill explicitly (`Skill I'm using: ...`).
- Decide MCP applicability explicitly (`MCPs I'm using: ...`, `What I'm checking first: ...`).
- If an MCP is obviously applicable, use it or record a concrete skip reason. Silent skip is a defect.
- At final summary time, name one concrete thing this skill changed about execution. Loaded-but-unused skill is a process defect.

ponytail: This is a behavioral contract. Use `scripts/session-trace-audit.py` as the advisory checker until transcript hooks become first-class.

## Workflow

1. Confirm exact discovery question: files, symbols, tests, patterns, ownership, or architecture map.
2. Start narrow with filenames, manifests, routes, known symbols, tests, and config.
3. Expand only as needed into implementation, docs, fixtures, and related modules.
4. Collect path/line evidence, reuse candidates, tests, and risk hotspots.
5. Return a concise read-only map that enables the next lane to act without re-discovering basics.

## Discovery playbooks

### Bug/feature scope
1. Locate entry points, owning modules, tests, fixtures, and config.
2. Identify current behavior pattern and nearest prior implementation.
3. Find validation commands from package scripts/docs/CI.
4. Return minimal change candidates and risk hotspots.

### Architecture map
1. Identify stack, package boundaries, runtime entry points, data stores, external integrations.
2. Map flow across UI/API/service/data/infra only to needed depth.
3. Highlight ownership seams, hidden coupling, and missing docs.

### Test/fixture discovery
1. Find closest test files and test helpers.
2. Identify factories, mocks, snapshots, browser fixtures, and command patterns.
3. Note gaps where no test path exists.

### Reuse search
1. Search existing components/utilities/services before suggesting new files.
2. Compare naming, error handling, styling, validation, and dependency patterns.
3. Return reuse candidates ranked by fit.

### Reference clone / source-approved 1:1 search
1. Build an upstream/source file/component/asset inventory from the approved reference.
2. Map likely local target files/components/asset destinations.
3. Recommend `copy`, `adapt`, `prune`, or `create` per source item with concise evidence/rationale.
4. Call out missing sources, restricted assets, or parity-risk areas that planner/implementer must track as remaining parity debt.

## Evidence rules

- Every claim should include path + line or explicit search evidence.
- If evidence is partial, mark confidence and next search.
- Do not infer product intent from code alone; route ambiguity to analyst/planner/architect.

## Output

Use concise fields: `summary`, `findings`, `files`, `patterns`, `tests`, `reuse_candidates`, `risks`, `next_actions`, `evidence`. Keep output read-only and implementation-ready.

## Escalation

- Escalate to `@librarian` when the missing answer is not in repo-local code and needs current docs/API/source facts.
- Escalate to `@artifact-planner` with system-analysis skill when the repo cannot answer product requirements, flows, or acceptance criteria.
- Escalate to `@architect` or `@oracle` when the task shifts from discovery into architecture/risk judgment.
- Escalate to implementation lanes only after the discovery question is sufficiently grounded in evidence.

## Local resources

- `scripts/codemap/`, `references/codemap.md`, `references/codemap-README.md` for code maps.
- `scripts/cartography/`, `references/cartography-README.md` for hierarchical repo cartography.

Never edit files.
## Quality checklist
- [ ] Discovery question is precise.
- [ ] Search started narrow before expanding.
- [ ] Claims include path/line or explicit search evidence.
- [ ] Reuse candidates are ranked, not dumped.
- [ ] Output stays read-only and avoids architecture/product inference.
- [ ] Next lane can act without redoing discovery.

## Anti-patterns
- Broad file dumps with no prioritization.
- Claiming "not found" without showing search basis.
- Drifting into architecture judgment or implementation advice.
- Reading large files wholesale when snippets would do.

## Output example

```yaml
summary: Located auth token expiry logic and nearest regression tests
files:
  - src/auth/middleware.ts:41-79
  - tests/auth-expiry.test.ts:1-62
patterns:
  - "Existing auth helpers live under src/auth/utils.ts"
reuse_candidates:
  - "Reuse parseTokenExpiry() from src/auth/utils.ts"
risks:
  - "No existing test covers exact-equality expiry boundary"
next_actions:
  - "Route to @fixer for bounded patch + regression test"
```


## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.


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



<!-- scripts-mcp-pointer -->
`mcp.scripts` is a configured local read/check/query-only governance tool. This read-only skill should prefer it over raw shell invocation of matching plan validation, runtime verification, progress reading, audit, discovery, or delegation query scripts when connected, usable, and permitted; no write operations exist in this slice. `caller_lane` in the tool payload is policy attestation only, not real authorization; this skill’s existing read-only boundary still controls what it may do. Canonical CLI fallback remains valid: `python3 ~/.config/opencode/scripts/<name>.py ...` when MCP is disconnected, unavailable, returns `tool_pending`, or is not permitted. Full policy: `.opencode/docs/MCP.md`, `.opencode/docs/TOOL_USAGE.md`, `.opencode/docs/AGENT_TOOL_ACCESS.md`.
## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.

## Code and source search replacement contract

- Local code investigation: query fresh Graphify first when qualifying, then verify with built-in `grep`, `glob`, and `read`.
- Public/upstream code search: use `github_search_code`.
- Official or version-sensitive library/API docs: use `context7`.
- General current web facts: use `9router.web_search`, then `9router.web_fetch`.
