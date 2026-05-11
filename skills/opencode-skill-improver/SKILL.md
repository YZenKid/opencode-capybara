---
name: opencode-skill-improver
description: Skill improvement workflow for OpenCode agents and skills. Use after non-trivial tasks, repeated failures, policy gaps, or explicit user request to capture evidence, refine prompts, and validate bounded improvements without bloat or secret access.
---

# OpenCode Skill Improver

Use this skill for small, evidence-based improvements to agents, skills, routing, and evals.

## Progressive workflow

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
