# Skills Index

Routing and ownership source of truth: `AGENT_ROUTING.md`.

## Core working skills
- `opencode-orchestrator` — owned by `@orchestrator`; routes work, coordinates lanes, and integrates results
- `opencode-fixer` — owned by `@fixer`; handles bounded implementation and tests
- `opencode-oracle` — owned by `@oracle`; handles architecture, review, and simplification
- `opencode-quality-gate` — owned by `@quality-gate`; performs final read-only conformance/risk signoff
- `opencode-designer` — owned by `@designer`; handles UI/UX, reference, and design-system workflow
- `opencode-explorer` — owned by `@explorer`; discovers codebase structure and reuse

## Triggered planning lane
- `opencode-artifact-planner` — owned by `@artifact-planner`; used only for multi-phase, spec-heavy, materially ambiguous, or evidence-heavy planning.

## Supporting research lane
- `opencode-librarian` — owned by `@librarian`; a supporting docs-research helper, not a core routing lane in the simplified model.

## Specialist lanes (triggered)
- `opencode-document-specialist` — owned by `@document-specialist`; handles document-centric extraction/transformation/validation work
- `opencode-product-systems-architect` — owned by `@product-systems-architect`; handles MVP/flows plus SaaS tenancy/RBAC/billing boundaries
- `opencode-platform-architect` — owned by `@platform-architect`; handles platform runtime/release/ops plus mobile/offline constraints
- `opencode-ai-systems-architect` — owned by `@ai-systems-architect`; reviews AI/LLM/RAG/tooling architecture
- `opencode-security-risk-reviewer` — owned by `@security-risk-reviewer`; reviews auth, privacy, PII, and security/data-risk boundaries
- `opencode-skill-improver` — owned by `@skill-improver`; improves prompts/skills/routing after real evidence

Compatibility note: merged skill names are now canonical for routing.

## Contract expectations
Every skill should provide:
- frontmatter `name` and `description`,
- a clear workflow or usage contract,
- allowed/forbidden posture where relevant,
- evidence/output expectations when relevant,
- failure or limitation handling when relevant.
