---
name: opencode-skill-improver
description: Skill improvement workflow for OpenCode agents and skills. Use after non-trivial tasks, repeated failures, policy gaps, or explicit user request to capture evidence, refine prompts, and validate bounded improvements without bloat or secret access.
---

# OpenCode Skill Improver

Use this skill for small, evidence-based improvements to agents, skills, routing, and evals.

## Trigger / skip

- Trigger: repeated failures, routing friction, policy gaps, stale prompts, unclear instructions, eval drift, or explicit user request to improve skill/agent behavior.
- Skip: trivial one-off tasks, speculative improvements with no evidence, or broad rewrites that should become a proposal first.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Pre-flight Skill & MCP Discovery
Before the first substantial answer, diagnosis, route, or implementation step on non-trivial work:
- Name the skill explicitly (`Skill I'm using: ...`).
- Decide MCP applicability explicitly (`MCPs I'm using: ...`, `What I'm checking first: ...`).
- If an MCP is obviously applicable, use it or record a concrete skip reason. Silent skip is a defect.
- At final summary time, name one concrete thing this skill changed about execution. Loaded-but-unused skill is a process defect.

ponytail: This is a behavioral contract. Use `scripts/session-trace-audit.py` as the advisory checker until transcript hooks become first-class.

## Workflow

1. **Capture intent** — summarize the last task, the problems that appeared, and the smallest valuable improvement opportunity.
2. **Research / interview** — read relevant local files, ask only when context is still insufficient, and gather verifiable evidence.
3. **Draft update** — propose the minimum change to `SKILL.md`, agent routing, references, or evals.
4. **Validate with-skill vs baseline** — compare old and new behavior through 2–3 realistic evaluation prompts.
5. **Feedback loop** — if the result is still unstable, revise once more with focus on the most ambiguous or failure-prone instruction.
6. **Trigger description optimization** — clarify when this skill should be called, but do not make the trigger too aggressive or duplicate existing rules.
7. **Post-task improvement checkpoint** — after non-trivial work, check whether recurring patterns, prompt bugs, policy gaps, or compressible instructions emerged.

The trigger description optimization step should stay conservative and evidence-based.

Short reference: `skill-creator` is used as a working pattern, not as a source of truth that must be reinstalled.

## Safety gates

- Do not read or write `.env`, secrets, tokens, or credentials.
- Do not make blind external updates; update `skills.sh` or an external registry only when explicitly requested and backed by context.
- Do not add prompt bloat; prefer replace or consolidate over endless append.
- Do not create instructions that conflict with `AGENTS.md`, an agent file, or another skill; if a conflict appears, record it and escalate.
- Do not allow instruction conflicts to remain hidden in frontmatter, references, or evals.
- Keep the post-task improvement checkpoint as an explicit step, not a hidden assumption.
- Do not expand access permissions beyond what the bounded improvement requires.
- Do not change many files at once if one small change already solves the problem.
- Do not assume every task needs improvement; skip trivial tasks.

## Bounded update rules

- Evidence must come from the last task, evaluation prompts, or relevant configuration files.
- Changes must be specific, testable, and easy to roll back.
- If a large rewrite is needed, write a short proposal first and ask for approval.
- Prioritize reuse of existing local patterns and references before inventing new instructions.
- Keep long details in references rather than frontmatter or the main body.

## Eval contract

- Prepare 2–3 prompts that mirror real cases: improvement after a bug fix, an external skill update with permission, and rejection of a risky change without evidence.
- Run the baseline first, then the with-skill evaluation.
- Record the visible differences: quality, safety, routing accuracy, and bloat risk.
- If results get worse, revert the change or narrow the instruction.

## References usage

- Use `references/skill-creator.md` for extra detail that does not belong in the main body.
- Keep the main body concise, actionable, and easy to scan.

## Output

Provide a short summary: intent, evidence, changed/proposed files, baseline vs with-skill evaluation results, and any remaining follow-up.

## Quality checklist
- [ ] Improvement is tied to concrete evidence, not speculation.
- [ ] Scope is bounded and reversible.
- [ ] Trigger description stays conservative, not over-eager.
- [ ] Validation compares baseline vs changed behavior when possible.
- [ ] No hidden cross-lane policy drift introduced.
- [ ] Rollback path is clear.
- [ ] Secrets/credentials were not touched.

## Anti-patterns
- Broad prompt rewrites for one isolated incident.
- Speculative improvements with no measured pain point.
- Silent policy changes affecting multiple lanes.
- Expanding permissions beyond what the fix needs.
- Rewriting many files when one small change solves the problem.

## Output example

```yaml
intent: reduce repeated auth-check omissions in backend tasks
evidence:
  - "3 recent backend tasks missed auth edge-case coverage"
changed_files:
  - "agents/backend.md"
  - "skills/opencode-backend/SKILL.md"
baseline_vs_with_skill:
  - "before: auth middleware often omitted from checklist"
  - "after: auth checklist item is explicit"
expected_effect:
  - "fewer auth-related rework loops"
follow_up:
  - "monitor next 10 backend tasks for auth completeness"
```

## Escalation

- Escalate to `@architect` / `@oracle` when a proposed improvement changes lane boundaries or policy meaning.
- Escalate to `user` when improvement would rewrite behavior broadly instead of applying a bounded correction.
- Escalate to `@quality-gate` only when the improvement itself changes signoff/governance expectations.
## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

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

