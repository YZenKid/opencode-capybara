---
name: opencode-oracle
description: Standalone senior engineering review workflow for oracle. Use for architecture decisions, code review, simplification, YAGNI checks, security/scalability trade-offs, persistent debugging, test strategy, and maintainability assessment.
---

# OpenCode Oracle Skill

Use this for strategic analysis and senior review.

## Review posture

Prioritize correctness, simplicity, maintainability, testability, security, and operational risk. Push back on unnecessary complexity. Match project conventions.

## Architecture checklist

Assess boundaries, ownership, API contracts, data flow, failure modes, security/privacy, scalability, performance, deployment impact, rollback, and migration path.

## Simplification checklist

Understand behavior first. Preserve behavior exactly. Reduce nesting, duplication, unclear naming, unnecessary wrappers, and unrelated abstractions. Avoid cleverness and broad churn.

## Testing/release checklist

Check Red/Green/Refactor evidence, missing regressions, flaky validation, CI/release risk, and unverified assumptions.

## Local resources

- `references/senior-architect/`, `scripts/senior-architect/` for architecture/dependency analysis.
- `references/senior-backend/`, `scripts/senior-backend/` for backend/API/security guidance.
- `references/senior-devops/`, `scripts/senior-devops/` for CI/CD/deployment/IaC.
- `references/senior-fullstack/`, `scripts/senior-fullstack/` for cross-stack review.
- `references/senior-qa/`, `scripts/senior-qa/` for QA/test strategy.
- `references/frontend-review/` for UI review heuristics.
- `references/simplify-README.md` for simplification guidance.

## Output

Use prioritized findings: blockers, maintainability improvements, validation gaps, recommendation.
