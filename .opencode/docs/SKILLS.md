# Skills Index

## Core working skills
- `opencode-orchestrator` — owned by `@orchestrator`; routes work, coordinates lanes, and integrates results
- `opencode-artifact-planner` — owned by `@artifact-planner`; writes planning artifacts and evidence under `.opencode/`
- `opencode-fixer` — owned by `@fixer`; handles bounded implementation and tests
- `opencode-oracle` — owned by `@oracle`; handles architecture, review, and simplification
- `opencode-quality-gate` — owned by `@quality-gate`; performs final read-only conformance/risk signoff
- `opencode-designer` — owned by `@designer`; handles UI/UX, reference, and design-system workflow

## Discovery and references
- `opencode-explorer` — owned by `@explorer`; discovers codebase structure and reuse
- `opencode-librarian` — owned by `@librarian`; checks official/current docs and API behavior
- `opencode-document-specialist` — owned by `@document-specialist`; handles document-centric extraction/transformation/validation work

## Conditional specialist skills
- `opencode-product-architect` — owned by `@product-architect`; clarifies MVP, flows, and acceptance criteria
- `opencode-saas-architect` — owned by `@saas-architect`; reviews tenancy, RBAC, billing, and workspace architecture
- `opencode-ai-systems-architect` — owned by `@ai-systems-architect`; reviews AI/LLM/RAG/tooling architecture
- `opencode-security-privacy-reviewer` — owned by `@security-privacy-reviewer`; reviews auth, privacy, PII, and data/security boundaries
- `opencode-release-engineer` — owned by `@release-engineer`; reviews deployment, CI/CD, migrations, and operational readiness
- `opencode-mobile-architect` — owned by `@mobile-architect`; reviews native/hybrid/mobile constraints
- `opencode-skill-improver` — owned by `@skill-improver`; improves prompts/skills/routing after real evidence

## Contract expectations
Every skill should provide:
- frontmatter `name` and `description`,
- a clear workflow or usage contract,
- allowed/forbidden posture where relevant,
- evidence/output expectations when relevant,
- failure or limitation handling when relevant.
