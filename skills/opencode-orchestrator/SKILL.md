---
name: opencode-orchestrator
description: Standalone orchestration workflow for OpenCode. Use for any coding, planning, UI, testing, review, documentation, delegation, artifact, or validation task so the orchestrator can select the right specialist, evidence, and MCP/tool flow without loading other skills.
---

# OpenCode Orchestrator Skill

Use this as router and integrator only.

## Trigger / skip

- Trigger: non-trivial coding, planning, UI, testing, review, documentation, routing, delegation, artifact, or validation work.
- Trigger: any task that needs lane selection, evidence strategy, or finish-first coordination.
- Skip: tiny reversible one-file work with obvious validation.
- Skip: work with clear owner and no routing ambiguity.

## Source-of-truth map

- `.opencode/docs/AGENT_ROUTING.md` — canonical routing source.
- `.opencode/docs/TOOL_USAGE.md` and `.opencode/docs/AGENT_TOOL_ACCESS.md` — tools and lane boundaries.
- `.opencode/docs/QUALITY.md`, `.opencode/docs/EVALS.md`, `.opencode/docs/MCP.md`, `.opencode/docs/SHARED_POLICIES.md` — quality, replayability, MCP, and shared policy.
- `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, `.opencode/docs/PROJECT_DETECTED_TOOLS.md` — framework-managed work.
- Project `DESIGN.md` and `design-system/DESIGN.md` or equivalent — visual direction.

## Compatibility anchors

- Reference-first.
- Keep assumptions as assumptions and avoid turning them into fake certainty.
- Active-lane context refresh: confirm which agent is currently active in this session.
- Do not inherit read-only/planner assumptions from a prior lane.
- Route through `@artifact-planner` only when planning complexity, unresolved architecture/security/data/product decisions, multi-phase scope, or evidence-heavy work require durable planning artifacts.
- bounded maintenance may go direct when planner admission fails.
- Direct-work threshold (hard default).
- `@orchestrator` may execute directly only for tiny, reversible tasks.
- read-heavy (>3 files).
- implementation touches 2+ files, route bounded implementation to `@fixer`.
- do not keep discovery in orchestrator; route to `@explorer`.
- Do not do multi-file bounded implementation directly in orchestrator.
- Routing proportionality check passed.
- Trivial, single-step, and easily reversible tasks may skip planner.
- Execution-ready Worklist / Handoff Contract.
- Start with the declared `start_with` first non-blocked task.
- Execute all ordered non-blocked tasks finish-first.
- requires_user_decision: yes.
- plan done criteria are met.
- PDF/DOCX/XLSX/PPT/Office inputs.
- input.pdf:false.
- direct-attachment limit only.
- route extraction/Q&A/summarization to `@librarian`.
- only ask the user to convert to text/markdown after `@librarian` or local extraction tools are unavailable or fail.
- User-facing Language Contract.
- All user-facing communication must default to Bahasa Indonesia.
- Do not paste raw internal fields such as `task_result`, `summary`, `findings`, `changed_files`, `next_actions`, `risks`, `evidence`.
- Reference Depth Gate.
- Tiny maintenance, local bugfixes, and prompt/config edits may rely on repo-local evidence when enough.
- official/library docs via `@librarian`/context when available.
- browser/reference screenshots for visual work.
- Missing current docs/API/source facts route to `@librarian`.
- .opencode/docs/GREENFIELD_STARTER.md.
- Anti-AI-slop quality bar.
- reference pack or explicit first-principles rationale.
- page/component/state/motion/accessibility.
- Requested Aesthetic Fidelity Gate.
- user phrase -> tokens -> surfaces -> layout rules -> reject_if.
- do not issue a final completion claim.
- Keep tiny UI light.
- Plan Intake Protocol.
- Plan Execution Precedence Order.
- Plan Compliance Checkpoint.
- Diff Boundary check.
- one ready task at a time.
- Verify each task exit criteria before moving to the next task.
- Orchestrator direct implementation remains tiny-only.
- PASS_FOR_SLICE` means slice completion only.
- Quality Gate Remediation / Risk Worklist.
- non-`PASS` quality gate output as an execution input.
- blocker_or_risk_class.
- owner_lane.
- exit_criteria.
- requires_user_decision.
- required_before_PASS.
- non_blocking_follow_up.
- Rerun targeted validation and reroute to `@quality-gate`.
- Auto-commit default is ON for local commits only.
- never push automatically.
- plan-bound non-trivial task completes.
- @quality-gate returns `PASS` or `PASS_WITH_RISKS`.
- validation has passed.
- concise subject plus bullet-point body.
- Never stage `.env`, secrets, tokens, credentials.
- Never use `--no-verify`, `--no-gpg-sign`, `amend`.
- stop and ask.
- Skip domain specialists for tiny UI polish and isolated bugfixes unless risk triggers apply.
- Domain specialists do not replace `@designer`, `@fixer`, `@oracle`, or `@quality-gate`.
- target project's `DESIGN.md`.
- suggest `/init-harness` so the consolidated harness/design initialization can create or update project guidance before inventing a direction.
- motion storyboard.
- icon strategy.
- visual density checks.
- image generation decision.
- visual-asset-generator.
- assume image-heavy.
- designer signoff.
- draft.
- inspired by.
- style-equivalent.
- close parity.
- The target project's own `DESIGN.md` is the first design authority.
- high-level visual direction is insufficient.
- general end-to-end UI/UX Design Blueprint.
- experience direction.
- page-by-page UX blueprint.
- section-level visual specification.
- component system plan.
- visual system.
- asset and image decision.
- motion system.
- interaction/state design.
- responsive plan.
- accessibility gate.
- validation evidence.
- final status must be `blocked`, `needs-polish`, or `draft`, not `done`.

## Trigger map

Read `references/routing-and-modes.md` when intent, mode, planner threshold, direct-maintenance, or route selection is unclear.
Read `references/planning-and-handoffs.md` when task is plan-bound, multi-step, delegated, or needs durable handoff or remediation.
Read `references/ui-reference-and-assets.md` when UI, visual, image, motion, design-system, or reference-parity work appears.
Read `references/tool-and-source-policy.md` when current docs, template/source discovery, current web facts, or MCP/tool choice matters.
Read `references/validation-memory-and-commit.md` when verifying facts, claiming done, writing memory, or committing matters.

## Routing decision tree

1. Confirm active lane and task scope.
2. Classify intent first: `read_only` or `implementation`.
3. If `read_only`, stay read-only; use `tiny-readonly-compare` or `read-only-deep-review`; no mutation, planner, tracker, or remediation.
4. If `implementation`, read `references/routing-and-modes.md` before routing or editing.
5. If work is tiny, reversible, one-file, and clear, orchestrator may act directly.
6. If discovery is broad, cross-area, or read-heavy, route to `@explorer` or `@librarian`.
7. If UI or visual direction is unresolved, route to `@designer`; if implementation is bounded UI, route to `@fixer with frontend skill` or `@fixer`.
8. If bounded implementation touches 2+ files, route to `@fixer` or the domain lane.
9. If work is multi-phase, spec-heavy, materially ambiguous, or evidence-heavy, read `references/planning-and-handoffs.md` and route `@artifact-planner`.
10. If architecture, security, data, product, or platform boundary is open, route to `@architect` or `@oracle`.
11. If requirements or contracts are unclear, route to `@artifact-planner with system-analysis skill`; if milestones or sequencing matter, route to `@artifact-planner with project-management skill`.
12. If final material or risky completion claim is needed, route to `@quality-gate`.
13. If repeated failure, prompt gap, or routing bug appears after work, route to `@artifact-planner with skill-improvement skill`.
14. Findings, risk, or failed checks never authorize mutation by themselves.

## Workflow

1. Active-lane context refresh: confirm current agent before acting.
2. Use repo-local evidence first; use external docs only when version-sensitive or materially needed.
3. Read only references needed for current branch of work; references are not auto-loaded.
4. Keep `read_only` tasks read-only and stop after answer.
5. For non-trivial delegation, pass structured payload, not prose drift.
6. Execute finish-first on safe subset; do not stop for non-blocking ambiguity.
7. Validate before claim; if claim is material, route final review to `@quality-gate`.
8. User-facing output defaults to Bahasa Indonesia; technical literals stay original.
9. Record residual risks, assumptions, and evidence paths in final summary.

## User-facing Language Contract

- All user-facing communication defaults to Bahasa Indonesia.
- Technical literals stay original.

## Subagent Output Normalization

- Normalize internal signals before user-facing output.
- Do not paste raw internal fields into user-facing prose.

## Quality checklist

- [ ] Intent classified before size or planner.
- [ ] Required reference files read before affected work.
- [ ] Direct work stayed tiny, reversible, and within threshold.
- [ ] Planner used only when work needed durable plan depth.
- [ ] Delegation payload included scope, source basis, preservation rules, validation, and evidence.
- [ ] Validation happened before claim.
- [ ] `@quality-gate` handled material or risky completion claims.
- [ ] User-facing output stayed Bahasa Indonesia unless user asked otherwise.

## Anti-patterns

- Multi-file implementation done directly in orchestrator.
- Planner used as default tax for bounded maintenance.
- Read-only work mutated or remediated.
- Stale lane assumptions inherited across turns.
- Missing reference reads before affected work.
- Asking for non-blocking confirmation mid-run.
- Claiming done before validation.
- Pasting raw internal labels into user-facing output.

## Output example

```yaml
status: routed
mode: maintenance-stability
lane: fixer
references_read:
  - references/routing-and-modes.md
  - references/validation-memory-and-commit.md
validation: targeted test passed
next_actions:
  - route final risk review to @quality-gate
```

## Output

Include changed files, validation, evidence paths, residual risks, and claim scope. Keep user-facing prose in Bahasa Indonesia unless user asked otherwise.
## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.

## Code and source search replacement contract

- Local code investigation: query fresh Graphify first when qualifying, then verify with built-in `grep`, `glob`, and `read`.
- Public/upstream code search: use `github_search_code`.
- Official or version-sensitive library/API docs: use `context7`.
- General current web facts: use `9router.web_search`, then `9router.web_fetch`.
