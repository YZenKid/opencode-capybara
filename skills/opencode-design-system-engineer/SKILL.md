---
name: opencode-design-system-engineer
description: Reusable design-system implementation workflow for tokens, primitives, theming, component APIs, icon systems, and DESIGN.md-aligned UI foundations.
---

# OpenCode Design System Engineer

Use for shared UI foundations. This lane sits between `@designer` and `@frontend`/`@mobile`.

## Trigger / skip
- Trigger: design tokens, theme variables, shared primitives, component APIs, typography/spacing scales, icon systems, dark/light modes, cross-screen reusable building blocks.
- Skip: page-level UX direction -> `@designer`; bounded screen implementation -> `@frontend`/`@mobile`; final gate -> `@quality-gate`.

## Core rule
This lane builds reusable foundations, not page composition. If work is not shared across surfaces, it likely belongs elsewhere.

## Workflow
1. Read stack docs + `DESIGN.md` first.
2. Detect token/component architecture from repo evidence.
3. Map requested design grammar into tokens -> primitives -> variants -> usage rules.
4. Reuse existing architecture first; do not fork system patterns casually.
5. Validate impacted consumers and document migration/use sites.

## Open Design bits worth adopting here
- Treat `DESIGN.md` as source of truth.
- Keep artifact/system thinking, but do not copy upstream tooling assumptions.
- Prefer reusable system contracts over prompt-only taste.

## Output contract
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`.
Include: translated design grammar, affected consumers, migration notes if any.

## Quality checklist
- [ ] Shared-system scope is real.
- [ ] `DESIGN.md` or approved source grammar translated into code.
- [ ] Existing architecture reused where possible.
- [ ] Tokens/primitives/variants documented by usage.
- [ ] Validation includes impacted surfaces or screenshots when material.

## Anti-patterns
- Using this lane for one-off page polish.
- Adding tokens with no consumers.
- Replacing settled project patterns with personal taste.
- Smuggling product-flow or backend work into system changes.

## Escalation
- `@designer` for missing grammar.
- `@frontend` / `@mobile` for screen consumption.
- `@quality-gate` for broad risk signoff.
