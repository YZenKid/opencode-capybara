# Agent Legibility

This repository optimizes for agent readability and safe autonomy.

Agents perform better when:
- entrypoints are short,
- docs are indexed,
- decisions are versioned,
- skills have contracts,
- validation is executable,
- errors include remediation steps,
- evidence is required,
- boundaries are enforced mechanically.

## Repository-local knowledge rule
If important knowledge cannot be found in the repo while an agent is running, that knowledge is practically unavailable.

## Legibility goals
- `AGENTS.md` should remain a short map.
- `docs/` should remain the reference-only mirror layer in this repository.
- `.opencode/plans/` should remain the durable plan location.
- `scripts/*check*.mjs` should remain the mechanical guardrails.
- Error messages should provide clear remediation steps.
- Work division across agents and subagents should be easy to read so execution does not default back to `@orchestrator`.

## Improvement order after repeated failures
If an agent fails repeatedly, improve the harness in this order:
1. clarify docs,
2. tighten skill contract,
3. add prompt regression,
4. add mechanical check,
5. improve tool wrapper,
6. update quality score.
