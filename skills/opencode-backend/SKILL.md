---
name: opencode-backend
description: Backend API/data workflow for endpoints, services, validation, auth integration, DB queries, migrations, jobs, queues, TDD, and security-sensitive server changes.
---

# OpenCode Backend Skill

Use for bounded server/API/data implementation.

## Duties
- Reuse existing endpoint, service, validation, auth, migration, error, and test patterns.
- Use TDD for production logic and security-sensitive behavior.
- Keep DB operations safe; prefer migrations/tests over ad hoc mutation.

## Forbidden
- Do not invent secrets or commit `.env` values.
- Do not run destructive DB commands without explicit approval.
- Do not proceed when API/data contract is unclear; route `@system-analyst`.

## Senior reference knowledge
- See `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant references: `supabase/agent-skills/supabase`, `supabase/agent-skills/supabase-postgres-best-practices`, `mattpocock/skills/tdd`.
- Use as non-authoritative inspiration for DB/API/TDD checklists; do not assume Supabase unless repo evidence proves it.

## Workflow
1. Map contracts, data model, auth, and existing patterns.
2. Red: add focused failing/regression test where feasible.
3. Green: implement minimal backend change.
4. Refactor: simplify and align with service boundaries.
5. Validate: focused tests/lint/type/security checks.

## Output
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence` plus validation commands/results.
