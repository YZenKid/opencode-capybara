---
name: opencode-council
description: Standalone consensus workflow for council. Use for high-stakes architecture, security, ambiguous, or expensive decisions where multiple perspectives reduce risk.
---

# OpenCode Council Skill

Use this for consensus on costly, ambiguous, or high-blast-radius decisions where one advisor is not enough. Council is Read-only and expensive; do not use for normal implementation, routine review, or final release signoff.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Trigger threshold

Use council only when at least one condition holds:
- irreversible or hard-to-rollback architecture/product/security decision,
- multiple viable approaches with materially different cost/risk profiles,
- disagreement between advisory lanes or unresolved high-stakes ambiguity,
- security/privacy/compliance/data-loss risk needs multi-perspective review,
- major migration, dependency replacement, billing/RBAC/tenancy, AI safety/evals, or deployment model choice.

Do not use when `@architect` or `@oracle` can answer cheaply, when code discovery is missing (`@explorer` first), or when final evidence gate is needed (`@quality-gate`).

## Trigger / skip

- Trigger: irreversible architecture/security/product decisions, unresolved disagreement between advisory lanes, high-blast-radius migration choices, or multi-option decisions with materially different risk/cost profiles.
- Skip: routine review, ordinary implementation, local debugging with clear evidence, repo discovery without facts, or final release signoff.
- Use only when extra deliberation is worth the coordination cost.

## Evaluate

Correctness, risk, maintainability, simplicity, performance, scalability, security, privacy, data integrity, testability, migration, rollback, cost, and operational burden.

## Workflow

1. Frame decision, non-goals, constraints, and success criteria.
2. Summarize known evidence and gaps; request more discovery if core facts are missing.
3. Evaluate 2-4 options, including “do nothing/smallest reversible step” when valid.
4. Score options on risk, reversibility, delivery cost, operational burden, and long-term maintainability.
5. Identify where perspectives agree, disagree, or depend on unknowns.
6. Recommend one path, fallback path, and rollback/validation plan.

## Boundary table

| Lane | Owns |
| --- | --- |
| `@architect` | single-lane architecture advisory and option design |
| `@oracle` | senior review, simplification, risk critique |
| `@council` | multi-perspective consensus for expensive/high-stakes decisions |
| `@quality-gate` | final conformance/risk status after changes/evidence |
| `@fixer`/domain agents | implementation after decision is clear |

## Local resources

- `references/senior-architect/`, `scripts/senior-architect/` for architecture and dependency analysis.

## Output

Return `summary`, `decision`, `rationale`, `alternatives`, `consensus`, `dissent`, `risks`, `mitigations`, `validation_plan`, `rollback_plan`, `open_questions`, `evidence`. Do not implement. Mark whether recommendation is `strong`, `conditional`, or `defer`.

## Quality checklist
- [ ] Decision is expensive/high-risk enough to justify council overhead.
- [ ] Convergence and divergence are both summarized.
- [ ] Minority concerns are preserved when they materially affect risk.
- [ ] Recommendation is actionable, not just a debate summary.
- [ ] Validation and rollback plans are concrete.
- [ ] Remaining owner/user decisions are explicit.
- [ ] Evidence basis is named for material claims.

## Anti-patterns
- Using council for routine low-risk choices.
- Returning raw conflicting opinions without synthesis.
- Hiding disagreement that materially affects risk.
- Producing a vague compromise with no validation path.
- Treating council output as final release signoff.

## Output example

```yaml
summary: Multi-perspective review favors event-driven order processing with staged rollout
decision: adopt async event-driven path with synchronous fallback
rationale:
  - "better blast-radius isolation than sync chain"
  - "keeps rollback path open during rollout"
alternatives:
  - option: synchronous REST chain
    verdict: rejected
    reason: tighter coupling and cascading failure risk
consensus:
  - "async decoupling is worth the operational cost"
dissent:
  - "team onboarding cost for event tooling is non-trivial"
risks:
  - "ordering guarantees"
mitigations:
  - "partition by order id"
validation_plan:
  - "staging load test"
rollback_plan:
  - "feature flag + sync fallback"
open_questions:
  - "schema registry owner decision"
evidence:
  - "repo: services/order"
  - "docs: queue best practices"
```

## Escalation

- Escalate back to `@explorer` / `@librarian` when core facts are still missing.
- Escalate to `@quality-gate` after implementation when the decision needs real-world conformance/risk proof.
- Escalate to `user` when the remaining choice is a policy/product-owner call rather than an engineering judgment call.
## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
