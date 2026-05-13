# Generated: Agent Matrix

Generated summary of local agent metadata. This file is advisory and must not replace canonical policy in `.opencode/docs/`.

- Agent count: 12
- Source: `agents/*.md` frontmatter

| Agent | Mode | Model | Skills | Description |
| --- | --- | --- | --- | --- |
| architect | subagent | cliproxyapi/gpt-5.4 | none | Unified read-only architect lane for product, platform, AI, and UI-system boundaries |
| artifact-planner | primary | cliproxyapi/gpt-5.3-codex | none | Artifact-writing SDD/TDD planner using the standalone opencode-capybara plan flow without entering built-in read-only Plan Mode. |
| council | subagent | cliproxyapi/gpt-5.4 | none | Multi-LLM consensus engine for high-confidence answers |
| designer | subagent | cliproxyapi/gpt-5.4 | none | UI/UX owner for polished implementation, motion direction/reduced-motion review, accessibility, and visual polish |
| explorer | subagent | cliproxyapi/gpt-5.4-mini | none | Local codebase discovery and search specialist for unfamiliar or broad scopes |
| fixer | subagent | cliproxyapi/gpt-5.3-codex | none | Bounded implementation and testing specialist for Red/Green/Refactor work |
| librarian | subagent | cliproxyapi/gpt-5.4-mini | none | Library/docs research plus document-centric read-only extraction and transformation support |
| oracle | subagent | cliproxyapi/gpt-5.4 | none | Architecture and risk review specialist for complex decisions |
| orchestrator | primary | cliproxyapi/gpt-5.4 | none | AI coding orchestrator that routes tasks to specialist agents |
| quality-gate | subagent | cliproxyapi/gpt-5.4 | none | Final conformance and risk gate for non-trivial OpenCode work |
| skill-improver | subagent | cliproxyapi/gpt-5.4-mini | none | Bounded post-task skill improvement subagent for prompt, routing, and eval refinement. |
| visual-asset-generator | subagent | unknown | none | Plans and prepares legal style-equivalent visual asset generation jobs for image-heavy UI, reference replication, hero art, icon badges, product mockups, thumbnails, avatars, and background textures. This subagent must use a chat-capable model; actual image generation is executed by the orchestrator through an image generation tool/endpoint. |
