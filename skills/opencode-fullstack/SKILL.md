---
name: opencode-fullstack
description: Narrow fullstack vertical-slice workflow for small tightly-coupled frontend/backend changes, contract tests, integration validation, and split-threshold enforcement.
---

# OpenCode Fullstack Skill

Use for small, clear vertical slices spanning UI and API/data code.

## Duties
- Keep one coherent FE/BE slice with clear contract and limited files.
- Add focused contract/integration/regression tests when feasible.
- Split to `@frontend` and `@backend` when scope grows.

## Forbidden
- Do not become catch-all implementation lane.
- Do not proceed when UX direction, API contract, auth, or data model is unclear.
- Do not handle broad refactors or multi-subsystem migrations.

## Senior reference knowledge
- See `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant references: `vercel-labs/agent-skills/vercel-react-best-practices`, `vercel-labs/next-skills/next-best-practices`, `supabase/agent-skills/supabase-postgres-best-practices`, `mattpocock/skills/tdd`, `mattpocock/skills/diagnose`.
- Use as non-authoritative inspiration for small vertical-slice checklists after stack fit; split to domain lanes when scope grows.

## Workflow
1. Confirm slice, user flow, API contract, and data changes.
2. Red: add focused regression/contract evidence when feasible.
3. Green: implement minimal UI + backend change.
4. Refactor: simplify boundaries and naming.
5. Validate: relevant tests/lint/type/browser/API checks.

## Output
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence` plus split decision and validation commands/results.
