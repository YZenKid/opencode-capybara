---
name: opencode-backend
description: Senior stack-agnostic backend API/data playbook for server frameworks, databases, endpoints, services, validation, auth, migrations, jobs, queues, TDD, and security-sensitive server changes.
---

# OpenCode Backend Skill

Use for bounded server/API/data implementation. Detect actual project stack from repo evidence before edits; local project conventions win; make no language, framework, or database assumptions.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

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
- Generator-first for new backend framework artifacts when detected stack/tooling supports it; edit existing generated/customized files directly when task is app-specific customization.
- Laravel: when `artisan`/Laravel structure is detected, prefer `php artisan make:*` for controllers, models, migrations, FormRequests, policies, jobs, events/listeners, mail/notifications, resources, factories, seeders, and tests where appropriate before manual file creation.
- Manual Laravel artifact creation requires evidence: `php artisan make:*` unavailable/not permitted, command failed, repo convention intentionally avoids generator, or only existing generated files are being customized.
- Greenfield App Accelerator: implement/propose only the data/API portion of a ready slice with explicit contract and migration path.
- Maintenance Stability Mode: keep changes regression-first, minimal, and backward-compatible unless approved.
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

## Pre-flight Skill & MCP Discovery
Before the first substantial answer, diagnosis, route, or implementation step on non-trivial work:
- Name the skill explicitly (`Skill I'm using: ...`).
- Decide MCP applicability explicitly (`MCPs I'm using: ...`, `What I'm checking first: ...`).
- If an MCP is obviously applicable, use it or record a concrete skip reason. Silent skip is a defect.
- At final summary time, name one concrete thing this skill changed about execution. Loaded-but-unused skill is a process defect.

ponytail: This is a behavioral contract. Use `scripts/session-trace-audit.py` as the advisory checker until transcript hooks become first-class.

## Workflow
1. Read `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present.
2. Map route/service/data/auth boundaries and current tests.
3. Confirm API/data contract, migration needs, and security constraints.
4. For new framework artifacts, detect and use the documented official generator command/tool first; record the exact fallback reason and skipped/attempted command if manual.
5. If generator, migration, or codegen behavior is version-sensitive and project docs do not already settle it, route to `@librarian` for official docs/context7 before coding.
6. Red: add focused failing test or reproduce regression when feasible.
7. Green: implement minimal endpoint/service/query/migration/job change.
8. Refactor: simplify while preserving established boundaries.
9. **Comment Verbosity Gate**: Keep comments minimal. Doc comments (GoDoc/phpdoc/JSDoc) above exported functions, types, and public interfaces are OK. Inline comments must be 1-3 lines max, only for truly non-obvious logic. Do not embed long multi-line comments explaining business rules, validation contracts, state-machine transitions, or API flows inside struct fields, function bodies, or endpoint handlers. If verbose comments exist, summarize or delete them before claiming done.
10. Validate with focused tests, lint/type/static checks, and migration dry-run where available.

## Validation
- Run stack-appropriate tests/checks from repo scripts and docs; examples include Laravel `php artisan test`, Go `go test ./...`, Python `pytest`, plus configured lint/static tools.
- DB: verify migrations, constraints, indexes, seed/fixture impact; no prod mutation without approval.

## Output example

```yaml
status: PASS
files_changed:
  - src/services/auth.service.ts
  - src/controllers/auth.controller.ts
validation:
  commands:
    - "npm run test -- auth"
    - "npm run lint"
  results: "all tests pass, no lint errors"
evidence:
  plan_reference: ".opencode/plans/20260623-auth-hardening.md"
  tests_added: 3
```

## Escalation
- Route `@architect` for auth model, multi-tenant/RBAC, billing, large migrations, eventing, or scalability decisions.
- Route `@quality-gate` for security/privacy/payment/auth-sensitive completion.

## Output contract
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`. Include API/data contract impact, migration notes, and validation commands/results.

## Domain references
- `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant inspiration: `supabase/agent-skills/supabase-postgres-best-practices`, `supabase/agent-skills/supabase` only when detected stack matches, `mattpocock/skills/tdd`.
- Local schema/tests/docs win; do not assume Supabase.

## Quality checklist
- [ ] Existing contracts and invariants identified before edit.
- [ ] Stack docs read and current backend best practice verified.
- [ ] Validation/business-rule changes covered by tests or explicit evidence.
- [ ] Data/queue/job side effects reviewed.
- [ ] Migration, backfill, and rollback implications documented.
- [ ] Secrets/destructive actions avoided or explicitly approved.
- [ ] Generator/codegen fallback reason recorded when not using official tooling.

## Anti-patterns
- Silent contract changes without evidence.
- New abstractions without reuse or simplification rationale.
- Changing validation/business rules without test coverage or explicit proof.
- Leaving migration, data backfill, or rollback implications undocumented.
- Relying on memory for version-sensitive ORM/framework behavior.
- Skipping queue/job/idempotency failure-state review.
- **Verbose inline comments**: Do not add multi-line comments inside function bodies, struct fields, endpoint handlers, or service methods explaining business rules, validation contracts, or API flows. Doc comments above exported/public functions/types are OK. Inline comments must be 1-3 lines max, only for truly non-obvious logic. Move long explanations to PR description, tests, or docs.


## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
