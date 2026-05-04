# Skill: opencode-product-architect

Read-only PRD-to-production product architecture workflow. Use this only when product docs, PRD, roadmap, MVP slicing, user-flow ambiguity, or acceptance criteria materially affect implementation.

## Trigger / skip

- Trigger for PRD/product overview analysis, MVP cut, roadmap-to-epics, user journeys, domain glossary, acceptance criteria, product risks, and production blueprint inputs.
- Skip for tiny UI polish, isolated bugfixes, already-scoped implementation, copy-only edits, or tasks where product behavior is already clear.
- If the PRD is a PDF/DOCX/XLSX or document transformation is needed, request `@document-specialist` first.

## Workflow

1. Identify product vision, target users, jobs-to-be-done, product layers, principles, and success metrics.
2. Separate MVP, v1, and future bets. Mark non-goals and deferred risks.
3. Produce user flows with actors, entry points, success states, empty/error states, and acceptance criteria.
4. Identify missing decisions that affect architecture, security, UX, cost, data, or release readiness.
5. Hand off to `@artifact-planner` as structured blueprint input; do not edit source files.

## Output contract

- Product summary and MVP slice.
- Epics/features with priorities.
- User flows and acceptance criteria.
- Domain glossary and assumptions/open questions.
- Product risks and validation metrics.
- Recommended specialist handoffs: SaaS, AI, mobile, security/privacy, release, designer.

## Quality bar

- Avoid inventing critical business rules; label assumptions.
- Prefer simple first, powerful later.
- Preserve user content and market context.
- Explicitly state readiness level: `ready-for-blueprint`, `needs-product-decisions`, or `blocked`.
