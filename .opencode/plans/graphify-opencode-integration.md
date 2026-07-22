# Graphify OpenCode Integration

- Task ID: `graphify-opencode-integration`
- Mode: Maintenance Stability Mode
- Plan Quality Gate: `PASS_FOR_SLICE`
- Claim scope: Graphify code-only graph generation, startup readiness, local MCP registration, and query-first guidance across this OpenCode preset. No post-commit hook, strict source-read blocking, HTTP exposure, or semantic LLM extraction.

## Goal

Bring this preset to execution-grade, evidence-backed Graphify integration for broad architecture and dependency discovery. Plan must describe only real completed behavior already evidenced in this repo: local code-only graph extraction, portable stdio MCP startup, query-first discovery guidance, and explicit fallback to direct source reading when graph is missing, stale, `INFERRED`, or `AMBIGUOUS`. This plan excludes plugin installer path, hooks, HTTP serving, semantic/LLM extraction, and any claim that Graphify replaces source verification.

## Non-goals

- Do not add or require Graphify plugin installation through upstream `graphify install --platform opencode`.
- Do not add HTTP server mode, background daemon, webhook, post-commit hook, or cron-like auto-refresh.
- Do not add semantic extraction, remote providers, credentials, telemetry, or secret handling.
- Do not make raw-source reading optional, blocked, or second-class.
- Do not fabricate framework playbook docs for this task; record explicit waiver because this slice changes preset/runtime guidance, not framework-managed application artifacts.
- Do not widen scope into unrelated MCP cleanup, prompt rewrites beyond Graphify guidance, or implementation outside already changed Graphify surfaces.

## Scope

In scope: document and validate completed Graphify integration across preset runtime config, wrapper startup behavior, inherited discovery guidance, evidence bundle, and readiness checks needed for future `/start-work` use. Plan covers actual behavior already implemented: `graphifyy[mcp]` global install, `scripts/graphify-mcp-wrapper`, `opencode.json` local MCP registration, optional read-only Graphify discovery policy in root guidance/docs, and evidence proving code-only graph generation plus stdio handshake. Out of scope: new feature development, framework scaffolding docs creation, non-Graphify presets, production deployment, or changing existing implementation behavior.

## Requirements

1. Plan must state explicit task goal in maintenance language with at least one bounded integration outcome.
2. Plan must describe only verified or clearly labeled assumed Graphify behavior, using `confirmed_repo`, `confirmed_docs`, `confirmed_runtime`, `assumption`, or `user_confirmed` labels.
3. Plan must capture no-plugin/no-hook/no-HTTP/no-semantic-extraction boundaries as non-negotiable invariants.
4. Plan must include at least eight concrete requirements tied to real completed behavior and future validation expectations.
5. Plan must include at least six acceptance criteria that can be checked from repo state, evidence, or local commands.
6. Plan must include at least four ordered implementation/remediation steps, even if implementation is already complete, so future maintainers can replay or audit sequence.
7. Plan must include at least three runnable validation commands relevant to depth, handoff, config/runtime proof, or quality evidence.
8. Plan must include explicit evidence requirements naming source audit, runtime audit, guidance audit, quality gate, and plan-remediation evidence.
9. Plan must include execution-ready worklist tasks with stable IDs, owner lanes, dependencies, validation, exit criteria, evidence path, `must_preserve`, and `do_not_touch`.
10. Plan must record explicit waiver for missing `.opencode/docs/PROJECT_*` playbook files: this task does not create framework-managed artifacts, so absence is noted as limited-scope exception rather than backfilled fiction.

## Acceptance Criteria

- `validate-plan-depth.py` on this plan returns non-`NEEDS_DEPTH` result.
- `subagent-handoff-check.py --plan .opencode/plans/graphify-opencode-integration.md` validates embedded handoff payloads.
- Plan headings cover goal, non-goals, scope, requirements, acceptance criteria, source of truth, invariants, rejection rules, diff boundary, test plan, implementation steps, routing, handoff prompt, worklist, progress tracking, validation commands, evidence requirements, done criteria, and final planning summary.
- Plan grounding sections distinguish repo-confirmed behavior from assumptions and do not claim missing framework playbook docs exist.
- Worklist declares stable `G1`-`G4` tasks with owner, dependency, validation, exit criteria, and evidence contract.
- Evidence bundle includes quality gate plus remediation note that records plan-depth fix and framework-doc waiver.
- Future executor can start with declared `start_with` task without needing to infer boundaries from chat history.

## Primary Skill / MCP Decision

- Primary skill: `opencode-orchestrator` — configuration integration needs routing, source validation, bounded execution, and final review.
- Applicable MCPs: `sequential-thinking`, `github`, `semgrep`, `scripts`; used now: sequential-thinking and GitHub source. `context7` skipped: Graphify is a CLI/repository integration, no Context7 library record needed. Browser MCP skipped: no UI surface.

## Execution Source of Truth

- User request: install Graphify in this OpenCode preset; start Graphify automatically when OpenCode loads; make agents and skills use it.
- Verified repo: `opencode.json` has current MCP map and no Graphify entry; `AGENTS.md`, `agents/`, `skills/`, and `.opencode/docs/` are canonical instructions.
- Verified upstream: Graphify `0.9.24` supports `uv tool install "graphifyy[mcp]"`, `graphify install --platform opencode`, code-only extraction, and stdio MCP via `python -m graphify.serve`.
- Existing user change: `commands/init-harness.md` modified before this task. Do not touch it.

## Existing Patterns/Reuse

- MCP definitions live in `opencode.json` under `mcp`.
- Agent behavior is anchored in root `AGENTS.md`, `.opencode/docs/`, agent contracts under `agents/`, and skill files under `skills/`.
- Existing MCP docs require restart after `opencode.json` changes.

## Source Anatomy

- `opencode.json`: MCP startup configuration.
- `AGENTS.md`: global preset rules inherited by all agents.
- `.opencode/docs/MCP.md`: MCP inventory and restart guidance.
- `.opencode/docs/TOOL_USAGE.md`: tool-selection rules.
- `.opencode/docs/AGENT_TOOL_ACCESS.md`: lane access policy.
- `.opencode/evidence/graphify-opencode-integration/source-audit.md`: upstream installer/server evidence and rejected paths.
- `.opencode/evidence/graphify-opencode-integration/install-and-runtime.md`: install, wrapper, graph build, MCP handshake evidence.
- `.opencode/evidence/graphify-opencode-integration/guidance-audit.md`: inherited guidance coverage and checks.

## Reference Map

- Upstream Graphify: `README.md`, `graphify/install.py`, `graphify/serve.py`, `graphify/skill-opencode.md` at `Graphify-Labs/graphify`.
- Local quality review: `.opencode/evidence/graphify-opencode-integration/quality-gate.md`.
- Handoff payload basis: `.opencode/state/graphify-opencode-integration/planner-remediation-handoff.json`.
- Waiver basis for missing framework playbook docs: quality gate finding plus handoff `must_preserve`/`context_bundle`.

## Confirmed vs Assumed

- `confirmed_repo`: current config had no Graphify MCP entry before this slice; evidence now shows `opencode.json` plus wrapper changed.
- `confirmed_docs`: Graphify supports OpenCode installation and MCP server.
- `confirmed_runtime`: `uv tool install 'graphifyy[mcp]'`, wrapper smoke, graph query smoke, MCP stdio handshake, and JSON parse all passed in `install-and-runtime.md`.
- `confirmed_repo`: guidance audit passed for inheritance and doc/skill coverage.
- `assumption`: Graphify update semantics may vary on stale graphs; maintainers should rebuild if deletion-heavy graphs lag.

## Decisions/Assumptions

- `confirmed_repo`: This slice is plan/evidence remediation only; implementation artifacts remain untouched.
- `confirmed_repo`: Missing `.opencode/docs/PROJECT_*` files are recorded as explicit waiver, not hidden completeness.
- `assumption`: If Graphify runtime changes upstream, wrapper or guidance may need fresh verification before any future claim of readiness.

## Grounding Contract

Every material claim in this plan must map to repo evidence, upstream source evidence, or explicit assumption label. `confirmed_repo` covers local files and evidence artifacts, `confirmed_docs` covers upstream Graphify documentation/source, `confirmed_runtime` covers executed install/runtime checks from evidence, and `assumption` remains non-binding until revalidated. Missing `.opencode/docs/PROJECT_*` playbook files are treated as explicit limited-scope waiver for this task, not hidden completeness.

## Non-negotiable Implementation Invariants

1. Build code-only graph locally. No LLM semantic extraction, credentials, HTTP server, or telemetry configuration.
2. Graphify must not replace direct source reading, tests, or runtime verification. `INFERRED` edges are leads, not facts.
3. Query-first rules apply only when `graphify-out/graph.json` exists and is fresh enough; otherwise build/update graph or use normal repo discovery.
4. Preserve agent role boundaries; Graphify is a read-only discovery context tool.
5. Do not touch `commands/init-harness.md` or stage its pre-existing modification.
6. Do not add post-commit hooks or strict source-read blocking.
7. Use portable config paths. No hardcoded user home paths in repo files.

## Do Not / Reject If

- Reject always-on semantic extraction, automatic URL ingestion, network listener, or use of secrets.
- Reject automatic `graphify hook install`.
- Reject agent guidance that treats graph output as verified source.
- Reject unbounded MCP output; use narrow query/path/explain requests.

## Diff Boundary

Allowed: `opencode.json`, `AGENTS.md`, `.opencode/docs/{MCP.md,TOOL_USAGE.md,AGENT_TOOL_ACCESS.md,PROJECT_STACK.md,PROJECT_COMMANDS.md,FRAMEWORK_PLAYBOOK.md,PROJECT_DETECTED_TOOLS.md}`, `skills/graphify/**`, `scripts/graphify-*`, `package.json`, `.opencode/plans/graphify-opencode-integration.md`, `.opencode/evidence/graphify-opencode-integration/**`, `.opencode/state/graphify-opencode-integration/**`, generated `graphify-out/**`.

## TDD / Test Plan

Planner remediation is plan/evidence-only, so no new implementation test is introduced here. Replayable checks still required: depth validator for plan sufficiency, handoff validator for payload integrity, compliance validator for worklist/progress contract, plus existing runtime evidence proving wrapper/graph/MCP behavior. ponytail: full re-run of implementation/runtime suite belongs to executor or quality-gate if implementation changes again.

## Implementation Steps

1. Read handoff payload, existing plan, and quality-gate evidence to isolate depth-only failure and explicit framework-doc waiver.
2. Expand plan structure to include goal, non-goals, scope, requirements, acceptance criteria, grounding split, test plan, implementation steps, progress tracking, validation commands, evidence requirements, and final summary without changing implementation scope.
3. Add explicit embedded handoff payloads and progress-tracking contract for `G1` through `G4`, preserving existing owner lanes and evidence files.
4. Append remediation evidence note, rerun depth/compliance/handoff validators, and report remaining planner-only gaps if any.

## Agent / Tool Routing

- `@artifact-planner` owns this remediation because failure is plan-depth and plan-contract only.
- `@explorer` owns source/upstream audit replay if Graphify behavior changes.
- `@devops` owns runtime wrapper/config validation and any future MCP startup repair.
- `@fixer` owns guidance/skill adjustments if Graphify discovery policy changes.
- `@quality-gate` owns final conformance verdict after plan passes validators.
- Preferred tools for this remediation: local `read`/`edit` plus validator scripts; Browser/UI/docs/search MCPs not needed for plan-only fix.

## Execution-ready Worklist / Handoff Contract

1. **G1** | `@explorer` | Source and installer audit | depends_on: none | validation: inspect upstream installer, skill, and server | evidence: `.opencode/evidence/graphify-opencode-integration/source-audit.md`
2. **G2** | `@devops` | Install Graphify, add startup wrapper and local MCP config | depends_on: G1 | validation: package, code-only graph, MCP init, JSON parse | evidence: `.opencode/evidence/graphify-opencode-integration/install-and-runtime.md`
3. **G3** | `@fixer` | Add query-first Graphify skill and inherited agent guidance | depends_on: G1 | validation: docs/agent/skill checks | evidence: `.opencode/evidence/graphify-opencode-integration/guidance-audit.md`
4. **G4** | `@quality-gate` | Verify boundaries and final quality | depends_on: G2,G3 | validation: all plan checks | evidence: `.opencode/evidence/graphify-opencode-integration/quality-gate.md`

### G1 — Source and installer audit
- Owner: `@explorer`
- Depends on: none
- Validation: inspect current upstream `graphify/install.py` and OpenCode skill/template.
- Exit: exact installer mutations and safe preset integration path documented.
- Evidence: `.opencode/evidence/graphify-opencode-integration/source-audit.md`.
- must_preserve: keep review limited to code-only/local/no-plugin boundary and preserve existing implementation scope only.
- do_not_touch: `opencode.json`, `AGENTS.md`, `.opencode/docs/*`, `scripts/*`, `skills/*`, `commands/init-harness.md`.

### G2 — Configuration and scripts
- Owner: `@devops`
- Depends on: G1
- Validation: Graphify CLI installed; code-only graph builds; MCP stdio initializes; `opencode.json` parses.
- Exit: startup wrapper ensures graph exists/updates before MCP serves; local MCP entry configured with portable command; no network server/hook.
- Evidence: `.opencode/evidence/graphify-opencode-integration/install-and-runtime.md`.
- must_preserve: existing actual implementation scope only, code-only/local/no hooks/plugins/HTTP/semantic extraction, no plan fiction.
- do_not_touch: `commands/init-harness.md`, unrelated MCPs, secrets, non-Graphify runtime behavior.

### G3 — Agent and skill guidance
- Owner: `@fixer`
- Depends on: G1
- Validation: policy docs and Graphify skill contain query-first fallback/verification rules; skills check passes.
- Exit: all agents inherit global guidance; Graphify skill supplies exact commands and safe fallbacks.
- Evidence: `.opencode/evidence/graphify-opencode-integration/guidance-audit.md`.
- must_preserve: Graphify remains optional/read-only discovery context; direct source verification stays mandatory.
- do_not_touch: runtime wrapper behavior, install commands, `commands/init-harness.md`, unrelated skills/docs.

### G4 — Validation and signoff
- Owner: `@quality-gate`
- Depends on: G2, G3
- Validation: config JSON, startup command, graph query, docs/agent/skill checks, semgrep on changed executable code, diff boundary.
- Exit: PASS or remediation list.
- Evidence: `.opencode/evidence/graphify-opencode-integration/quality-gate.md`.
- must_preserve: final verdict bounded to actual evidence and explicit framework-doc waiver.
- do_not_touch: implementation files during review.

### Task G1 handoff
```yaml
handoff:
  task_id: graphify-opencode-integration
  plan_id: graphify-opencode-integration
  caller: orchestrator
  callee: explorer
  scope: Audit upstream Graphify installer/server behavior and document safe preset integration path only.
  claim_level: partial
  claim_scope: Verified source and installer findings only.
  source_basis: [.opencode/plans/graphify-opencode-integration.md, .opencode/evidence/graphify-opencode-integration/source-audit.md, upstream Graphify sources]
  must_preserve: [Existing actual implementation scope only, Code-only/local/no hooks/plugins/HTTP/semantic extraction]
  do_not_touch: [opencode.json, AGENTS.md, .opencode/docs/*, scripts/*, skills/*, commands/init-harness.md]
  validation: [inspect upstream installer, inspect serve path, record rejected integration modes]
  exit_criteria: [exact installer mutations documented, safe local stdio path confirmed, no preset/plugin fiction]
  evidence_required: [.opencode/evidence/graphify-opencode-integration/source-audit.md]
  depends_on: [none]
  context_bundle: [.opencode/evidence/graphify-opencode-integration/quality-gate.md]
```

### Task G2 handoff
```yaml
handoff:
  task_id: graphify-opencode-integration
  plan_id: graphify-opencode-integration
  caller: orchestrator
  callee: devops
  scope: Install Graphify MCP extra, add wrapper, configure local MCP entry, and prove code-only runtime behavior.
  claim_level: partial
  claim_scope: Runtime installation/config validation only.
  source_basis: [.opencode/plans/graphify-opencode-integration.md, .opencode/evidence/graphify-opencode-integration/source-audit.md, .opencode/evidence/graphify-opencode-integration/install-and-runtime.md]
  must_preserve: [Existing actual implementation scope only, Code-only/local/no hooks/plugins/HTTP/semantic extraction, No edits outside approved Graphify runtime surfaces]
  do_not_touch: [commands/init-harness.md, secrets, unrelated MCP config, framework playbook docs]
  validation: [uv tool install graphifyy[mcp], graphify extract help, wrapper smoke, graph query smoke, MCP stdio handshake, JSON parse]
  exit_criteria: [wrapper builds or updates graph before serve, local stdio MCP documented, no HTTP or hook path introduced]
  evidence_required: [.opencode/evidence/graphify-opencode-integration/install-and-runtime.md]
  depends_on: [G1]
  context_bundle: [.opencode/evidence/graphify-opencode-integration/quality-gate.md]
```

### Task G3 handoff
```yaml
handoff:
  task_id: graphify-opencode-integration
  plan_id: graphify-opencode-integration
  caller: orchestrator
  callee: fixer
  scope: Add inherited Graphify guidance and skill coverage for query-first discovery with source verification fallback.
  claim_level: partial
  claim_scope: Guidance/doc/skill validation only.
  source_basis: [.opencode/plans/graphify-opencode-integration.md, .opencode/evidence/graphify-opencode-integration/source-audit.md, .opencode/evidence/graphify-opencode-integration/guidance-audit.md]
  must_preserve: [Graphify read-only discovery posture, Direct source reading/tests/runtime verification remain mandatory, No implementation scope expansion]
  do_not_touch: [commands/init-harness.md, runtime wrapper behavior, secrets, unrelated docs/skills]
  validation: [npm run check:docs, npm run check:agents, npm run check:skills, inheritance scan]
  exit_criteria: [all active lanes inherit query-first guidance, Graphify remains optional/read-only, no semantic or HTTP claims added]
  evidence_required: [.opencode/evidence/graphify-opencode-integration/guidance-audit.md]
  depends_on: [G1]
  context_bundle: [.opencode/evidence/graphify-opencode-integration/quality-gate.md]
```

### Task G4 handoff
```yaml
handoff:
  task_id: graphify-opencode-integration
  plan_id: graphify-opencode-integration
  caller: orchestrator
  callee: quality-gate
  scope: Validate completed Graphify integration against plan, evidence, boundaries, and runtime/guidance checks.
  claim_level: done
  claim_scope: Final conformance verdict for this integration slice only.
  source_basis: [.opencode/plans/graphify-opencode-integration.md, .opencode/evidence/graphify-opencode-integration/source-audit.md, .opencode/evidence/graphify-opencode-integration/install-and-runtime.md, .opencode/evidence/graphify-opencode-integration/guidance-audit.md, .opencode/evidence/graphify-opencode-integration/quality-gate.md]
  must_preserve: [Existing actual implementation scope only, Framework-doc waiver remains explicit not fabricated, Verdict based on evidence only]
  do_not_touch: [all implementation/config/docs/skills files during review]
  validation: [validate-plan-depth.py, subagent-handoff-check.py, runtime evidence checks, docs/agent/skill checks, diff-boundary review]
  exit_criteria: [PASS or explicit NEEDS_FIX with cited failure, plan-depth resolved, waiver recorded]
  evidence_required: [.opencode/evidence/graphify-opencode-integration/quality-gate.md]
  depends_on: [G2, G3]
  context_bundle: [.opencode/evidence/graphify-opencode-integration/check-plan/depth.txt]
```

start_with: G1

## Progress Tracking

- tracker_path: `.opencode/state/graphify-opencode-integration/progress.json`
- init_command: `python3 ~/.config/opencode/scripts/task-progress.py graphify-opencode-integration --init --plan .opencode/plans/graphify-opencode-integration.md`
- summary_command: `python3 ~/.config/opencode/scripts/task-progress.py graphify-opencode-integration --summary`
- checklist_command: `python3 ~/.config/opencode/scripts/task-progress.py graphify-opencode-integration --checklist`
- update_rules:
  - `in_progress`: set when owner starts task with current evidence path.
  - `completed`: set only after validation passes and evidence file is refreshed.
  - `blocked`: set when dependency, validator, or scope blocker prevents completion; include blocker note.
  - `cancelled`: set only by orchestrator or explicit scope stop.
  - `evidence_refresh`: every status change must refresh evidence path or state why unchanged.
- task_map:
  - `G1`: owner `@explorer`; `python3 ~/.config/opencode/scripts/task-progress.py graphify-opencode-integration --update G1 --status <status> --owner explorer --evidence .opencode/evidence/graphify-opencode-integration/source-audit.md`
  - `G2`: owner `@devops`; `python3 ~/.config/opencode/scripts/task-progress.py graphify-opencode-integration --update G2 --status <status> --owner devops --depends-on G1 --evidence .opencode/evidence/graphify-opencode-integration/install-and-runtime.md`
  - `G3`: owner `@fixer`; `python3 ~/.config/opencode/scripts/task-progress.py graphify-opencode-integration --update G3 --status <status> --owner fixer --depends-on G1 --evidence .opencode/evidence/graphify-opencode-integration/guidance-audit.md`
  - `G4`: owner `@quality-gate`; `python3 ~/.config/opencode/scripts/task-progress.py graphify-opencode-integration --update G4 --status <status> --owner quality-gate --depends-on G2,G3 --evidence .opencode/evidence/graphify-opencode-integration/quality-gate.md`

## Validation Commands

- `python3 ~/.config/opencode/scripts/validate-plan-depth.py .opencode/plans/graphify-opencode-integration.md --mode auto --score`
- `python3 ~/.config/opencode/scripts/subagent-handoff-check.py --plan .opencode/plans/graphify-opencode-integration.md`
- `python3 ~/.config/opencode/scripts/plan-compliance-check.py --project-root . --plan .opencode/plans/graphify-opencode-integration.md --task-id graphify-opencode-integration`
- `python3 -m json.tool opencode.json >/dev/null`
- `npm run check:docs`
- `npm run check:agents`
- `npm run check:skills`

## Evidence Requirements

- `.opencode/evidence/graphify-opencode-integration/source-audit.md` records upstream installer/server facts and rejected modes.
- `.opencode/evidence/graphify-opencode-integration/install-and-runtime.md` records install, wrapper, graph extraction/update, query smoke, MCP handshake, and JSON parse results.
- `.opencode/evidence/graphify-opencode-integration/guidance-audit.md` records inherited guidance checks and preserved invariants.
- `.opencode/evidence/graphify-opencode-integration/quality-gate.md` records final verdict and residual risk.
- `.opencode/evidence/graphify-opencode-integration/plan-remediation.md` records depth remediation, validator rerun results, and explicit waiver for missing `.opencode/docs/PROJECT_*` docs.

## Done Criteria

- `graphifyy[mcp]` installed via `uv tool`.
- Local code-only `graphify-out/graph.json` exists for this preset or is reproducibly created by wrapper before serve.
- OpenCode config declares Graphify MCP using a startup wrapper that makes graph available before serving.
- Root inherited guidance and Graphify-specific skill tell all lanes when to query, verify, update, and fall back.
- Validation proves CLI, graph query, MCP initialization, docs/agent/skill checks, config parse, and plan-depth compliance.
- Framework playbook docs absence is explicitly waived for this slice; no fabricated PROJECT_* docs claim remains.
- Quality gate passes or only non-plan residual risks remain explicitly listed.

## Final Planning Summary

This plan now reflects completed Graphify integration behavior already evidenced in repo artifacts. Plan scope stays narrow: remediate plan depth and handoff contract only, preserve existing implementation/config/docs/skills state, and record limited-scope waiver for missing framework playbook docs because this task does not create framework-managed artifacts. Future work starts at `G1` only if Graphify integration changes again; otherwise this artifact serves as execution-ready historical contract and replayable evidence map.

## Executor Handoff Prompt

Execute only assigned work. Preserve all invariants. Do not delegate, redesign scope, add hooks/HTTP/semantic extraction, or touch `commands/init-harness.md`. Report changed files, exact validation results, evidence paths, and residual risks.
