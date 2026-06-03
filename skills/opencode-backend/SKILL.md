---
name: opencode-backend
description: Senior stack-agnostic backend API/data playbook for server frameworks, databases, endpoints, services, validation, auth, migrations, jobs, queues, TDD, and security-sensitive server changes.
---

# OpenCode Backend Skill

Use for bounded server/API/data implementation. Detect actual project stack from repo evidence before edits; local project conventions win; make no language, framework, or database assumptions.

## Trigger / skip
- Trigger: endpoints, controllers, services, validation, auth integration, DB queries, migrations, jobs/queues, API tests, background processing, server-side security fixes.
- Skip: unclear requirements/contracts → `@system-analyst`; broad architecture/data model decisions → `@architect`; frontend slice too coupled and tiny → `@fullstack`; final security/privacy signoff → `@quality-gate`.

## Stack detection
- Inspect manifests, lockfiles, entrypoints, routes, migrations, schemas, config, tests, containers, and docs before edits.
- Laravel: `composer.json`, `artisan`, `app/Http`, `routes/api.php`, migrations, policies, FormRequests, queues, Pest/PHPUnit.
- Go: `go.mod`, `cmd/`, `internal/`, router/framework, migrations, `go test ./...`, `sqlc`/ORM.
- Python: `pyproject.toml`, FastAPI/Django/Flask, Alembic/Django migrations, pytest.
- Database signals: PostgreSQL/MySQL/SQLite/MongoDB/Redis/etc. migrations, schemas, indexes, constraints, RLS, connection config, query builder/ORM patterns.

## Responsibilities
- Reuse existing layering, validation, authz, error envelopes, logging, transactions, migrations, and test fixtures.
- Implement minimal contract-safe server changes; avoid hidden API breaks.
- Add/update focused tests for production logic, authz, validation, DB behavior, and regressions.
- Keep DB changes reversible where possible; never run destructive commands without explicit approval.

## Senior heuristics / checklist
- Contracts: request/response shape, status codes, pagination, sorting, idempotency, backward compatibility, versioning.
- Security: authenticate then authorize, validate input, constrain mass assignment, avoid SQL injection, protect secrets, rate/abuse limits where relevant.
- Data: constraints beat app-only checks, transactions around multi-write invariants, indexes for new query paths, null/default/backfill plan.
- Database: check query plans for risky paths when supported, avoid disruptive locks on large tables, keep migrations deploy-safe.
- Framework-specific: apply detected framework idioms for validation, authz, serialization/resources, jobs/events, ORM/query performance, and mass-assignment protection.
- Runtime-specific: apply detected language/runtime idioms for context/timeouts, typed errors, dependency injection boundaries, structured logging, and concurrency hazards.

## Workflow
1. Map route/service/data/auth boundaries and current tests.
2. Confirm API/data contract, migration needs, and security constraints.
3. Red: add focused failing test or reproduce regression when feasible.
4. Green: implement minimal endpoint/service/query/migration/job change.
5. Refactor: simplify while preserving established boundaries.
6. Validate with focused tests, lint/type/static checks, and migration dry-run where available.

## Validation
- Run stack-appropriate tests/checks from repo scripts and docs; examples include Laravel `php artisan test`, Go `go test ./...`, Python `pytest`, plus configured lint/static tools.
- DB: verify migrations, constraints, indexes, seed/fixture impact; no prod mutation without approval.

## Escalation
- Route `@architect` for auth model, multi-tenant/RBAC, billing, large migrations, eventing, or scalability decisions.
- Route `@quality-gate` for security/privacy/payment/auth-sensitive completion.

## Output contract
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`. Include API/data contract impact, migration notes, and validation commands/results.

## Domain references
- `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant inspiration: `supabase/agent-skills/supabase-postgres-best-practices`, `supabase/agent-skills/supabase` only when detected stack matches, `mattpocock/skills/tdd`.
- Local schema/tests/docs win; do not assume Supabase.
