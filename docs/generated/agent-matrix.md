# Generated: Agent Matrix

Generated summary of local agent metadata. This file is advisory and must not replace canonical policy in `.opencode/docs/`.

- Agent count: 22
- Source: `agents/*.md` frontmatter

| Agent | Mode | Model | Skills | Description |
| --- | --- | --- | --- | --- |
| accessibility-reviewer | subagent | cliproxyapi/gpt-5.4-mini | none | Read-only accessibility reviewer for semantics, keyboard, focus, contrast, and motion |
| ai-systems-architect | subagent | cliproxyapi/gpt-5.4 | none | AI systems specialist for LLM features, RAG, evals, safety, cost, and reliability boundaries |
| artifact-planner | primary | cliproxyapi/gpt-5.3-codex | none | Artifact-writing SDD/TDD planner using the standalone opencode-capybara plan flow without entering built-in read-only Plan Mode. |
| council | subagent | cliproxyapi/gpt-5.4 | none | Multi-LLM consensus engine for high-confidence answers |
| designer | subagent | cliproxyapi/gpt-5.4 | none | UI/UX owner for polished implementation, accessibility, and visual polish |
| document-specialist | subagent | cliproxyapi/gpt-5.4-mini | none | Document processing specialist for PDF, Office, spreadsheets, presentations, and text document files |
| explorer | subagent | cliproxyapi/gpt-5.4-mini | none | Local codebase discovery and search specialist for unfamiliar or broad scopes |
| fixer | subagent | cliproxyapi/gpt-5.3-codex | none | Bounded implementation and testing specialist for Red/Green/Refactor work |
| librarian | subagent | cliproxyapi/gpt-5.4-mini | none | Library and docs research specialist for version-sensitive behavior |
| mobile-architect | subagent | cliproxyapi/gpt-5.4 | none | Mobile and hybrid app architecture specialist for native constraints, offline behavior, push, deep links, camera, QR, and app-store readiness |
| motion-specialist | subagent | cliproxyapi/gpt-5.4-mini | none | Read-only motion specialist for animation systems and reduced-motion checks |
| oracle | subagent | cliproxyapi/gpt-5.4 | none | Architecture and risk review specialist for complex decisions |
| orchestrator | primary | cliproxyapi/gpt-5.4 | none | AI coding orchestrator that routes tasks to specialist agents |
| product-architect | subagent | cliproxyapi/gpt-5.4 | none | PRD-to-production product architecture specialist for MVP slicing, user flows, and acceptance criteria |
| quality-gate | subagent | cliproxyapi/gpt-5.4 | none | Final conformance and risk gate for non-trivial OpenCode work |
| release-engineer | subagent | cliproxyapi/gpt-5.4 | none | Release engineering specialist for CI/CD, deployment readiness, monitoring, rollback, migrations, and production operations |
| saas-architect | subagent | cliproxyapi/gpt-5.4 | none | SaaS architecture specialist for tenancy, RBAC, billing, audit, and workspace systems |
| security-privacy-reviewer | subagent | cliproxyapi/gpt-5.4 | none | Read-only security and privacy reviewer for PII, RBAC, tenant isolation, uploads, payments, and AI data risks |
| skill-improver | subagent | cliproxyapi/gpt-5.4-mini | none | Bounded post-task skill improvement subagent for prompt, routing, and eval refinement. |
| ui-system-architect | subagent | cliproxyapi/gpt-5.4 | none | Read-only UI system architect for tokens, component anatomy, and Figma/design-system handoff |
| visual-asset-generator | subagent | unknown | none | Plans and prepares legal style-equivalent visual asset generation jobs for image-heavy UI, reference replication, hero art, icon badges, product mockups, thumbnails, avatars, and background textures. This subagent must use a chat-capable model; actual image generation is executed by the orchestrator through an image generation tool/endpoint. |
| visual-parity-auditor | subagent | cliproxyapi/gpt-5.4 | none | Read-only visual parity auditor for screenshots and section-by-section comparison |
