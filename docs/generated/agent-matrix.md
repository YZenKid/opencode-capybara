# Generated: Agent Matrix

Generated summary of local agent metadata. This file is advisory and must not replace canonical policy in `.opencode/docs/`.

- Agent count: historical snapshot; regenerate from current `agents/*.md` when needed
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
| platform-architect | subagent | cliproxyapi/gpt-5.4 | none | Merged platform architect for runtime, release, and mobile platform constraints |
| motion-specialist | subagent | cliproxyapi/gpt-5.4-mini | none | Read-only motion specialist for animation systems and reduced-motion checks |
| oracle | subagent | cliproxyapi/gpt-5.4 | none | Architecture and risk review specialist for complex decisions |
| orchestrator | primary | cliproxyapi/gpt-5.4 | none | AI coding orchestrator that routes tasks to specialist agents |
| product-systems-architect | subagent | cliproxyapi/gpt-5.4 | none | Merged product systems architect for PRD-to-production planning and SaaS system boundaries |
| quality-gate | subagent | cliproxyapi/gpt-5.4 | none | Final conformance and risk gate for non-trivial OpenCode work |
| security-risk-reviewer | subagent | cliproxyapi/gpt-5.4 | none | Merged security risk reviewer for auth, privacy, data-risk, and compliance-sensitive boundaries |
| skill-improver | subagent | cliproxyapi/gpt-5.4-mini | none | Bounded post-task skill improvement subagent for prompt, routing, and eval refinement. |
| ui-system-architect | subagent | cliproxyapi/gpt-5.4 | none | Read-only UI system architect for tokens, component anatomy, and Figma/design-system handoff |
| visual-asset-generator | subagent | unknown | none | Plans and prepares legal style-equivalent visual asset generation jobs for image-heavy UI, reference replication, hero art, icon badges, product mockups, thumbnails, avatars, and background textures. This subagent must use a chat-capable model; actual image generation is executed by the orchestrator through an image generation tool/endpoint. |
| visual-parity-auditor | subagent | cliproxyapi/gpt-5.4 | none | Read-only visual parity auditor for screenshots and section-by-section comparison |
