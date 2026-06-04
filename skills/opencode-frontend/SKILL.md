---
name: opencode-frontend
description: Senior stack-agnostic frontend implementation playbook for web UI frameworks, forms, state, routing, accessibility, browser validation, and design-system compliant UI after design direction exists.
---

# OpenCode Frontend Skill

Use for bounded web UI implementation where visual direction, route intent, and data contract are known. Detect actual project stack from repo evidence before acting; local project conventions win; make no framework defaults.

## Reference-first creativity contract
- Use this lane creatively, but never fictionally: better options, sharper synthesis, and stronger tradeoffs are good; invented facts, APIs, assets, or requirements are not.
- Prefer local repo evidence first, then official docs, upstream source/examples, screenshots/references, and current web evidence when materially relevant.
- If a reasonable source exists, use it or state why it was skipped.
- For greenfield, ambiguous, or taste-sensitive work, generate 2-3 bounded options when that improves quality, then choose with explicit rationale.
- Mark assumptions as assumptions, keep them reversible, and avoid turning them into fake certainty.
- In output/evidence, include the key references or repo artifacts that materially shaped the result.

## Trigger / skip
- Trigger: pages, components, forms, state, client/server rendering, routing, data hooks, API integration, component tests, Playwright/browser checks, accessibility implementation.
- Skip: major visual direction or reference parity → `@designer`; unclear product flow/API contract → `@system-analyst`; backend contract/data change → `@backend` or `@fullstack`; final a11y/security signoff → `@quality-gate`.

## Stack detection
- Inspect `package.json`, lockfile, app/router dirs, config, test setup, Storybook, design docs, and existing components before edits.
- Common framework signals: React/Next.js (`next.config.*`, `app/`, `pages/`, route handlers, server actions, RSC boundaries, `use client`), Vue/Nuxt, Svelte/SvelteKit, Angular, Astro, Vite, or other repo-specific setup.
- Identify styling system: Tailwind, CSS modules, shadcn/ui, MUI, Chakra, CSS-in-JS, tokens, `DESIGN.md`.
- Identify validation/forms/state: React Hook Form, Zod/Yup, TanStack Query, SWR, Redux/Zustand/Jotai, server actions.

## Responsibilities
- Reuse project components, tokens, layouts, hooks, error/loading/empty patterns, and test fixtures.
- Greenfield App Accelerator: implement from `MVP design enough` or stronger handoff and focus on first usable UI slice; full visual parity only when reference/image-heavy.
- Maintenance Stability Mode: preserve existing UX and fix the smallest reproducible UI surface.
- Frontend is implementation, not product taste invention, for substantial UI. Major layout/composition/imagery/state choices must come from `DESIGN.md`, designer blueprint/handoff, reference pack, or explicit existing-product patterns.
- If the implementation basis is missing for a material UI choice, stop and route back to `@designer` instead of defaulting to generic hero sections, card grids, glassmorphism, or placeholder polish.
- Implement minimal UI changes with stable contracts, accessible semantics, and predictable render/data boundaries.
- Keep client components small; keep server-only logic out of browser bundles.
- Add/update tests when behavior changes; capture browser evidence for interaction/regression work.

## Senior heuristics / checklist
- Basis check: for each material UI decision, know whether it comes from `DESIGN.md`, blueprint, reference screen, or existing pattern. If you cannot name the basis, the decision is under-specified.
- UX: loading, empty, error, disabled, success, optimistic, slow-network, mobile, keyboard, reduced motion.
- A11y: semantic elements, labels, focus order, visible focus, ARIA only when needed, color contrast, announcement for async status.
- Framework-specific boundaries: follow detected framework conventions for server/client rendering, routing, data loading, caching, and secrets; for Next.js projects, prefer Server Components for data/read-only UI and use `use client` only at interaction boundaries.
- Forms: validate client for UX and server for trust; preserve submitted values; map field errors predictably.
- State: colocate local state; avoid global state unless shared cross-route/session need exists.
- Performance: avoid needless client bundles, waterfalls, layout shift, unbounded lists, heavy sync work in render.
- Security: escape/sanitize untrusted HTML, avoid token exposure, preserve auth/CSRF assumptions.

## Workflow
1. Read local docs: `AGENTS.md`, `.opencode/docs/`, `DESIGN.md` when present.
2. Detect stack and reuse paths: components, routes, hooks, tests, fixtures.
3. Confirm UX states, API/data contract, and implementation basis for each material UI decision.
4. Red: add/adjust focused failing test or capture current bug/browser evidence when feasible.
5. Green: implement smallest component/page/form/routing change that matches the existing basis.
6. Refactor: align names, boundaries, styling, and a11y without broad cleanup.
7. Validate with focused lint/type/test/browser commands available in repo, plus screenshots for changed screens when the UI is material.

## Validation
- Prefer existing commands: `npm|pnpm|yarn test`, `test:unit`, `test:e2e`, `lint`, `typecheck`, Storybook checks.
- Browser-test interactive flows when UI behavior changes; include viewport and console/network evidence when relevant.
- Include framework-appropriate build/type checks if routing/server-client boundaries changed and cost acceptable.

## Escalation
- Route `@designer` for visual language, animation systems, reference parity, or design ambiguity.
- Route `@backend` for API/schema/auth changes; `@fullstack` for tiny clear vertical slices.
- Route `@quality-gate` for material UI/accessibility/security-sensitive changes.

## Output contract
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`. Include validation commands/results, implementation basis for material UI decisions, and any skipped checks with reason.

## Domain references
- `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant inspiration: `vercel-labs/agent-skills/vercel-react-best-practices`, `vercel-labs/next-skills/next-best-practices`, `anthropics/skills/webapp-testing`, `vercel-labs/agent-skills/web-design-guidelines`.
- Use references only when detected stack matches; local docs/tests/design win.
## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
