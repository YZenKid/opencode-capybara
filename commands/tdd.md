---
description: Plan and execute a coding task using TDD
agent: build
model: cliproxyapi/gpt-5.5
---

Use strict TDD for this task:

```text
$ARGUMENTS
```

Workflow:

1. Create or reuse SDD/TDD artifacts in the active project root using `.opencode/plans`, `.opencode/draft`, and `.opencode/evidence`.
2. Use a stable task id: `YYYYMMDD-HHMM-<slug>`.
3. Inspect existing tests, helpers, fixtures, mocks, and KiloCode/project patterns.
4. Write discovery evidence to `.opencode/evidence/<task-id>/discovery.md`.
5. Create or update exactly one primary plan file: `.opencode/plans/<task-id>.md`. Include SDD spec, TDD/test plan, implementation plan, validation commands, evidence requirements, and done criteria as sections in this single file. Use `.opencode/draft/` for expanded notes and `.opencode/evidence/<task-id>/` for run evidence.
6. Identify the smallest behavior slice.
7. Red: write or update a failing test first and record the failing command/output in `.opencode/evidence/<task-id>/red.md`.
8. Green: implement the smallest production change needed to pass the test and record evidence in `.opencode/evidence/<task-id>/green.md`.
9. Refactor: clean up while keeping tests green and record evidence in `.opencode/evidence/<task-id>/refactor.md`.
10. Run relevant tests/checks and record commands/results in `.opencode/evidence/<task-id>/verification.md`.
11. Summarize artifact paths plus Red, Green, Refactor, and Verification.

Rules:

- Apply TDD to production logic, bug fixes, API behavior, service/use-case behavior, UI interaction behavior, validation logic, and security-sensitive logic.
- Do not write production logic before a failing test exists for that behavior.
- If bug fixing, first add a failing regression test that reproduces the bug.
- Reuse existing project/KiloCode test helpers, fixtures, factories, mocks, components, and utilities before creating new ones.
- Prefer table-driven tests for multiple scenarios in Go code.
- Cover success path, validation failure, and critical edge cases for each behavior slice.
- If tests cannot be written or run, stop and explain the blocker before production changes; record the blocker in `.opencode/evidence/<task-id>/red.md` and `.opencode/evidence/<task-id>/verification.md`.
- Ask before architectural, API-contract, data-model, security, permission, or UX-direction decisions.
- If the task is docs-only, prompt-only, config-only, `.gitignore`, command documentation, or pure formatting, TDD is not required; document the exemption in the TDD/Test Plan section of `.opencode/plans/<task-id>.md`, record useful validation in `.opencode/evidence/<task-id>/verification.md`, and do not fabricate Red/Green evidence.
- Do not intentionally deviate from `.opencode/plans/<task-id>.md` without recording the deviation and reason in `.opencode/evidence/<task-id>/verification.md`.
