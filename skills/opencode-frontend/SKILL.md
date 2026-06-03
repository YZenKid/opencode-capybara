---
name: opencode-frontend
description: Frontend implementation workflow for web UI. Use for React, Next.js, Vue, Svelte, forms, state, routing, component tests, accessibility implementation, and browser validation after design direction exists.
---

# OpenCode Frontend Skill

Use for bounded web frontend implementation after design direction or project design guidance exists.

## Duties
- Reuse `DESIGN.md`, design-system docs, components, tokens, routes, data hooks, and test patterns.
- Implement components/pages/forms/state/API integration with minimal blast radius.
- Add or update component/unit/browser tests when behavior changes.

## Forbidden
- Do not invent visual direction for substantial UI; route `@designer` first.
- Do not change backend contracts without `@backend` or explicit contract evidence.
- Do not add UI libraries before checking existing stack.

## Senior reference knowledge
- See `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant references: `vercel-labs/agent-skills/vercel-react-best-practices`, `vercel-labs/next-skills/next-best-practices`, `anthropics/skills/webapp-testing`, `vercel-labs/agent-skills/web-design-guidelines`.
- Use as non-authoritative inspiration for React/Next/browser-test checklists only after stack fit; local docs, design guidance, and tests win.

## Workflow
1. Inspect stack, project design guidance, and existing component patterns.
2. Confirm data/API contract and accessibility requirements.
3. Red: capture failing test, regression, or browser evidence when feasible.
4. Green: implement minimal UI change.
5. Refactor: simplify and align with project conventions.
6. Validate: run focused tests/lint/type/browser checks when available.

## Output
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence` plus validation commands/results.
