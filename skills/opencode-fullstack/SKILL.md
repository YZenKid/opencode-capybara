---
name: opencode-fullstack
description: Senior narrow fullstack vertical-slice playbook for small tightly-coupled frontend/backend changes, contracts, integration tests, and split-threshold enforcement.
---

# OpenCode Fullstack Skill

Use for small clear vertical slices spanning UI and API/data code where one agent can keep contract coherence. Detect actual frontend, backend, and data stacks from repo evidence first; local project conventions win; make no stack assumptions.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Trigger / skip
- Trigger: tiny UI + endpoint change, form + validation + persistence, API contract test, integration regression, frontend route consuming backend data.
- Skip: broad feature, unclear UX/API/data model, multi-service change, big migration, auth model redesign, devops/release work; split to domain lanes or `@architect`.

## Stack detection
- Frontend: package scripts, framework/router dirs, components, form/state/data libs, browser tests.
- Backend: language/framework manifests, routes/services/tests, migrations, queues/jobs, authz patterns.
- Data: detected database schemas/migrations/indexes/fixtures.
- Integration: API clients, generated types, OpenAPI, contract tests, E2E tests, Docker/Compose dev env.

## Responsibilities
- Keep one coherent user-facing slice with explicit contract, limited files, and focused tests.
- Greenfield App Accelerator: may own one bounded first vertical slice when FE/BE coupling is high, contracts are clear enough, and the plan is `PASS` or `PASS_FOR_SLICE`.
- Maintenance Stability Mode: keep FE/BE diff minimal and regression-first.
- Update both sides only when coupling is direct and small.
- Preserve API compatibility or document intentional change.
- Split early when independent workstreams, architecture decisions, or release risk appear.

## Senior heuristics / checklist
- Contract first: request/response, validation, authz, error mapping, loading/error UI, idempotency.
- Data first enough: migration safety, constraints, indexes, rollback/backfill notes.
- UI first enough: a11y, responsive state, slow/error/empty handling, no secret leakage.
- Tests: unit where logic lives, contract/integration for boundary, browser/E2E for critical flow.
- Split threshold: more than one route + one backend area, broad schema change, cross-cutting auth, async jobs, CI/deploy impact, or unclear ownership.

## Workflow
1. Confirm slice, user flow, UX states, API contract, data changes, and auth rules.
2. Detect stack and reuse existing FE/BE/integration patterns.
3. Red: add failing contract/regression/integration test or capture repro evidence.
4. Green: implement minimal UI + API/data change.
5. Refactor: keep names/contracts aligned; avoid opportunistic broad cleanup.
6. Validate focused frontend, backend, and integration checks.
7. Record split decision and remaining domain risks.

## Validation
- Run targeted frontend lint/type/test and backend tests for touched code.
- Run migration checks or test DB setup when schema changed.
- Run browser/API integration check when user flow changed and tooling exists.
- Document skipped checks with reason and risk.

## Output example

```yaml
status: PASS
files_changed:
  - src/api/users.ts
  - src/components/UserList.tsx
validation:
  commands:
    - "npm run test -- users"
    - "npm run test -- UserList"
  results: "integration + component tests pass"
evidence:
  contract_test: "tests/api/users.integration.test.ts validates request/response shape"
  ui_test: "tests/components/UserList.test.tsx validates empty/error/success states"
```

## Escalation
- Route `@frontend`, `@backend`, `@mobile`, or `@devops` when scope exceeds narrow slice.
- Route `@system-analyst` for unclear contract/acceptance criteria.
- Route `@architect` for auth/RBAC/multi-tenant/billing/migration/platform tradeoffs.
- Route `@quality-gate` for material security/privacy/accessibility/release-sensitive completion.

## Output contract
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`. Include split decision, contract impact, validation commands/results, and skipped checks.

## Domain references
- `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant inspiration: framework/database best practices, TDD/diagnose references listed there, only when detected stack matches.
- References guide checklists only; local docs/tests/contracts win.

## Quality checklist
- [ ] Slice is truly small and tightly coupled.
- [ ] Contract boundary is clear and preserved or explicitly changed.
- [ ] Frontend and backend stack docs / best practices checked.
- [ ] Frontend and backend validations both covered.
- [ ] Shared types/contracts updated once, not drifted in two places.
- [ ] Split recommendation made if complexity grew mid-task.
- [ ] Residual cross-boundary risk documented.

## Anti-patterns
- Using fullstack as default lane for unrelated mixed work.
- Letting one side change silently force risky changes on the other.
- Skipping contract validation because both sides were edited together.
- Holding work that should split to specialized lanes.
- Editing FE and BE independently without shared contract evidence.
- Allowing slice scope to expand into multi-subsystem implementation.


## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
