---
name: opencode-frontend
description: Senior stack-agnostic frontend implementation playbook for web UI frameworks, forms, state, routing, accessibility, browser validation, and design-system compliant UI after design direction exists.
---

# OpenCode Frontend Skill

Use for bounded web UI implementation where visual direction, route intent, and data contract are known. Detect actual project stack from repo evidence before acting; local project conventions win; make no framework defaults.

Lane contract:
- consumes design handoff from `@designer`
- consumes shared primitives/themes from `@design-system-engineer` when present
- does not invent visual language when design basis is missing

Adopted from Open Design: source-pack discipline, `DESIGN.md` authority, screenshot evidence, and reuse-first implementation. Not adopted: upstream plugin/export assumptions.

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
- shadcn/ui signals: `components.json`, `components/ui/*`, registry config, Tailwind aliases, and local package-manager files.
- Identify validation/forms/state: React Hook Form, Zod/Yup, TanStack Query, SWR, Redux/Zustand/Jotai, server actions.

## Responsibilities
- Reuse project components, tokens, layouts, hooks, error/loading/empty patterns, and test fixtures.
- Greenfield App Accelerator: implement from `MVP design enough` or stronger handoff and focus on first usable UI slice; full visual parity only when reference/image-heavy.
- Maintenance Stability Mode: preserve existing UX and fix the smallest reproducible UI surface.
- Frontend is implementation, not product taste invention, for substantial UI. Major layout/composition/imagery/state choices must come from `DESIGN.md`, designer blueprint/handoff, reference pack, or explicit existing-product patterns.
- If the implementation basis is missing for a material UI choice, stop and route back to `@designer` instead of defaulting to generic hero sections, card grids, glassmorphism, or placeholder polish.
- For explicit aesthetics, implementation must follow style grammar/blueprint: user phrase -> tokens -> surfaces -> layout rules -> reject_if. If missing or mismatched, route back to `@designer`; do not invent generic cards/glass/neon/clay fallback.
- **Source-approved 1:1 Porting / Literal Porting Contract**: when the user explicitly approves a source and asks for `1:1`, `clone`, `port`, `copy`, `copy from`, or `make exactly like`, port upstream structure, class anatomy, component names, and file organization first. Do not generate replacement UI from prose unless direct copy/adapt is unsafe, unavailable, legally blocked, or the plan explicitly says `create`. Any deviation must be evidence-backed and labeled `scope-preserving deviation` or `remaining parity debt`.
- **Open Source Reuse Policy**: when the user provides an open source reference (repo, package, component, pattern), do not reject it and generate a replacement from scratch. Verify the license first:
  - **Permissive (MIT, BSD, Apache-2.0, ISC, Unlicense, CC0, MPL-2.0)**: reuse and adapt freely. Prefer source anatomy/components/code over reinventing. Record source URL + license in evidence.
  - **Copyleft / caution (LGPL, GPL, AGPL, SSPL, custom/nonstandard)**: escalate to user with license class and risk note before reuse. Do not auto-generate replacement either — ask.
  - **No license / unclear**: ask user for direction. Do not assume blocked.
  - Fallback to self-generate only when: license is genuinely unclear AND user cannot clarify, scope genuinely diverges, or reuse would introduce incompatible dependencies. Record why reuse was skipped.
- User-facing debug/internal copy, fake metrics, arbitrary KPI/dashboard numbers, port/server labels, placeholder claims, and local dev artifacts are not allowed unless the surface is explicitly demo/dev and labeled.
- Implement minimal UI changes with stable contracts, accessible semantics, and predictable render/data boundaries.
- Generator-first for new UI framework artifacts when detected tooling supports it. For shadcn/ui, prefer shadcn MCP or detected package manager CLI for `shadcn init`/`shadcn add`; do not manually copy new `components/ui/*` from docs when CLI/MCP is usable.
- Detect package manager from lockfiles/scripts before shadcn CLI examples (`bunx`, `pnpm dlx`, `npx`, or repo script). Use `components.json` to confirm configured shadcn projects; use `shadcn init` only for setup tasks, and `shadcn add` for new components/blocks.
- Manual shadcn component creation requires evidence: MCP/CLI unavailable or failed, repo intentionally uses custom local components, or task customizes existing generated files.
- Keep client components small; keep server-only logic out of browser bundles.
- Add/update tests when behavior changes; capture browser evidence for interaction/regression work.

## Senior heuristics / checklist
- Basis check: for each material UI decision, know whether it comes from `DESIGN.md`, blueprint, reference screen, or existing pattern. If you cannot name the basis, the decision is under-specified.
- Style grammar check: for explicit aesthetics, name the user phrase, tokens, surfaces, layout rules, and reject_if before coding; visible mismatch is not acceptable as “taste”.
- UX: loading, empty, error, disabled, success, optimistic, slow-network, mobile, keyboard, reduced motion.
- A11y: semantic elements, labels, focus order, visible focus, ARIA only when needed, color contrast, announcement for async status.
- Framework-specific boundaries: follow detected framework conventions for server/client rendering, routing, data loading, caching, and secrets; for Next.js projects, prefer Server Components for data/read-only UI and use `use client` only at interaction boundaries.
- Forms: validate client for UX and server for trust; preserve submitted values; map field errors predictably.
- State: colocate local state; avoid global state unless shared cross-route/session need exists.
- Performance: avoid needless client bundles, waterfalls, layout shift, unbounded lists, heavy sync work in render.
- Security: escape/sanitize untrusted HTML, avoid token exposure, preserve auth/CSRF assumptions.

## Pre-flight Skill & MCP Discovery
Before the first substantial answer, diagnosis, route, or implementation step on non-trivial work:
- Name the skill explicitly (`Skill I'm using: ...`).
- Decide MCP applicability explicitly (`MCPs I'm using: ...`, `What I'm checking first: ...`).
- If an MCP is obviously applicable, use it or record a concrete skip reason. Silent skip is a defect.
- At final summary time, name one concrete thing this skill changed about execution. Loaded-but-unused skill is a process defect.

ponytail: This is a behavioral contract. Use `scripts/session-trace-audit.py` as the advisory checker until transcript hooks become first-class.

## Workflow
1. **MANDATORY stack read**: Read `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` before any non-trivial implementation. If missing or stale, run `/init-harness` (single entrypoint for harness + design init per `commands/init-harness.md`) or route to `@librarian` for current stack docs — do not implement blind.
2. Read local docs: `AGENTS.md`, `.opencode/docs/`, `DESIGN.md` when present.
3. Detect stack and reuse paths: components, routes, hooks, tests, fixtures.
4. Confirm UX states, API/data contract, and implementation basis for each material UI decision.
5. For new framework/UI artifacts, use official generator/CLI/MCP first when usable, including existing apps; record the exact fallback reason and skipped/attempted command if manual. **This is mandatory — do not manually create components that a generator can produce (e.g. hand-building shadcn components instead of `shadcn add`).**
6. If generator behavior is version-sensitive and project docs do not already settle it, route to `@librarian` for official docs/context7 before coding. **This is mandatory — do not rely on memory for version-sensitive behavior.**
7. TDD where relevant: Red by adding/adjusting focused failing test or capturing current bug/browser evidence when feasible.
8. Green: implement smallest component/page/form/routing change that matches the existing basis.
9. Refactor: align names, boundaries, styling, and a11y without broad cleanup.
10. **Anti-AI-slop gate** (mandatory before returning output):
    - No card spam / repeated grid anatomy across sections
    - No fake metrics, arbitrary KPIs, debug copy, server labels, or port numbers in UI
    - No placeholder imagery, lorem text, or blank image frames
    - No generic "modern clean" without source-backed specifics
    - No centered gradient hero without product/domain composition
    - Section anatomy varies by purpose, not copy-pasted layout
    - States covered: empty/loading/error/success where relevant
    - If any slop pattern present, fix before returning
11. Validate with focused lint/type/test/browser commands available in repo, plus screenshots for changed screens when the UI is material.
12. **Comment Verbosity Gate**: Keep comments minimal. Doc comments above exported/public functions, components, and types are OK. Inline comments must be 1-3 lines max, only for truly non-obvious logic. Do not add long multi-line comments explaining UI behavior, state transitions, API flows, or component purpose inside component function bodies. If verbose comments exist, summarize or delete them before claiming done.

## Validation
- Prefer existing commands: `npm|pnpm|yarn test`, `test:unit`, `test:e2e`, `lint`, `typecheck`, Storybook checks.
- Browser-test interactive flows when UI behavior changes; include viewport and console/network evidence when relevant.
- Include framework-appropriate build/type checks if routing/server-client boundaries changed and cost acceptable.

## Output example

```yaml
status: PASS
files_changed:
  - src/components/Dashboard.tsx
  - src/styles/dashboard.module.css
validation:
  commands:
    - "npm run typecheck"
    - "npm run test -- Dashboard"
  results: "typecheck pass, all tests pass"
visual_evidence:
  screenshots:
    - "dashboard-desktop.png"
    - "dashboard-mobile.png"
  accessibility: "axe-core scan: 0 violations"
```

## Escalation
- Route `@designer` for visual language, animation systems, reference parity, or design ambiguity.
- Route `@design-system-engineer` for shared primitives, theme variables, or component API changes.
- Route `@backend` for API/schema/auth changes; `@fullstack` for tiny clear vertical slices.
- Route `@quality-gate` for material UI/accessibility/security-sensitive changes.

## Output contract
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`. Include validation commands/results, implementation basis for material UI decisions, and any skipped checks with reason.

## Domain references
- `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant inspiration: `vercel-labs/agent-skills/vercel-react-best-practices`, `vercel-labs/next-skills/next-best-practices`, `anthropics/skills/webapp-testing`, `vercel-labs/agent-skills/web-design-guidelines`.
- Use references only when detected stack matches; local docs/tests/design win.

## Quality checklist
- [ ] UI basis identified before coding.
- [ ] Stack docs read and current best practice verified.
- [ ] Generator/CLI used for new components — no manual creation of generator-available components.
- [ ] Anti-AI-slop gate passed: no card spam, fake metrics, generic hero, placeholder imagery, or debug copy.
- [ ] Existing components/tokens reused where possible.
- [ ] States covered: empty/loading/error/success where relevant.
- [ ] Accessibility and responsive implications checked.
- [ ] Validation includes screenshots or equivalent evidence for material UI changes.
- [ ] Framework/library version-sensitive behavior verified via `@librarian`/context7 when non-trivial.

## Token-First Implementation (v2 — Open Design integration)

For substantial UI work, `@frontend` implements from the **cited catalog system**'s tokens, not from memory or ad-hoc decisions. Reference: `.opencode/docs/SKILLS.md` §"UI/UX design system source of truth".

**Token source-of-truth:**

1. The canonical token file is `.opencode/catalog/<active-system>/tokens.json` (or its generated equivalent at `.opencode/generated-design/tokens.{json,css,tailwind.config.js}`).
2. Components reference these via:
   - Tailwind: `tailwind.config.js` extends `theme.colors` from the token generator output.
   - CSS: `:root { --color-ink: #...; ... }` from `tokens.css`.
   - CSS-in-JS: import the JSON.
3. **No inline `#hex` in component code.** If you need a color, it's a token, and tokens come from the cited system. Exception: one-off values that are clearly labeled `/* one-off */` and reviewed by `@designer`.

**Catalog citation in evidence:**

- Every material UI change must cite the catalog template the section anatomy came from (e.g. `Following example-aerocore hero anatomy with one deviation per deviation_audit`).
- Token usage is mechanically checked: `python3 ~/.config/opencode/scripts/visual-audit-check.py --contract <contract.md> --token-parity` reports parity percentage.

**Pattern-aware component selection:**

Instead of "use shadcn Card", the instruction becomes "use `<CatalogTemplate>/components/Card.tsx` (adapted from `example-aerocore` if a Bento-style is needed)". Prefer catalog-template-derived component anatomy over generic primitives.

**Push-back authority for catalog gaps:** if `DESIGN.md` exists for a substantial-UI project but does not cite an Open Design source (no `Source & Provenance` block, no `open-design.ai` URL), `@frontend` MUST write `design_pushback.md` asking `@designer` to add a catalog citation. Do not silently implement a template-feeling design.

**Workflow (v2 amendments):**

1. Read `DESIGN.md` and verify it cites the catalog (v2 schema).
2. If not, push back via `design_pushback.md` and stop.
3. Load tokens from `.opencode/catalog/<active-system>/tokens.{json,css}` (or generated equivalent).
4. Implement from the cited template's section anatomy; cite the template in PR/evidence.
5. Run `visual-audit-check.py --contract <contract> --token-parity` before claiming done; if parity < 80% or any `must_avoid_token` is found, fix or push back.

## Anti-patterns
- Manually creating components that a generator/CLI can produce.
- Shipping UI with AI-slop patterns.
- Inventing design language instead of implementing provided direction.
- Adding generic placeholder UI to fill unclear gaps.
- Changing interaction/state behavior without validation evidence.
- Ignoring responsive/accessibility impact of visual changes.
- **Verbose inline comments**: Do not add multi-line comments inside component function bodies, hooks, or render logic explaining UI behavior, state, or data flow. Doc comments above exported/public functions/components are OK. Inline comments must be 1-3 lines max, only for truly non-obvious logic. Move long explanations to PR description, tests, or docs.


## Sequential Thinking MCP Gate

After loading this skill, call `sequential_thinking` before material planning, routing, implementation, review, or final claims. For non-trivial, ambiguous, or risky work, use at most 3 thought steps total—enough to frame scope, constraints, approach, and validation—and set or keep `totalThoughts` no higher than `3` when invoking `sequential_thinking`. For tiny fast-path work, keep it to one brief thought. If the MCP tool is unavailable, record the fallback and continue with this role's normal evidence-first workflow. Do not expose raw thoughts to the user; summarize decisions/evidence only. This tool does not change permissions, role boundaries, or read-only constraints.

## skills.sh inspirations

This skill folder absorbs selected practices from `skills.sh` while staying a single local skill folder for this agent. Do not split these inspirations into separate local skills here. Use curated notes in `references/skills-sh-curated.md` and adapt them through this lane's own contracts, boundaries, and evidence rules.
