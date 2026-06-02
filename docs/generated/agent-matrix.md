# Generated: Agent Matrix

Generated summary of local agent metadata. This file is advisory and must not replace canonical policy in `.opencode/docs/`.

- Agent count: 12
- Source: `agents/*.md` frontmatter

| Agent | Mode | Model | Skills | Description |
| --- | --- | --- | --- | --- |
| architect | subagent | 9router/medium | opencode-architect | Unified read-only architect lane for product/SaaS, platform/runtime/release, AI, and UI-system boundaries |
| artifact-planner | primary | 9router/high | opencode-artifact-planner | Artifact-writing SDD/TDD planner using the standalone opencode-capybara plan flow without entering built-in read-only Plan Mode. |
| council | subagent | 9router/medium | opencode-council | Multi-LLM consensus engine for high-confidence answers |
| designer | subagent | 9router/high | opencode-designer | UI/UX implementation and review lane for polished visuals, motion direction/reduced-motion review, accessibility, and visual polish |
| explorer | subagent | 9router/low | opencode-explorer | Local codebase discovery and search specialist for unfamiliar or broad scopes |
| fixer | subagent | 9router/low | opencode-fixer | Bounded implementation and testing specialist for Red/Green/Refactor work |
| librarian | subagent | 9router/fast | opencode-librarian | Library/docs research plus document-centric read-only extraction and transformation support |
| oracle | subagent | 9router/medium | opencode-oracle | Read-only architecture and risk review advisor for complex decisions |
| orchestrator | primary | 9router/medium | opencode-orchestrator | AI coding orchestrator that routes tasks to specialist agents |
| quality-gate | subagent | 9router/low | opencode-quality-gate | Final conformance and risk gate for non-trivial OpenCode work |
| skill-improver | subagent | 9router/fast | opencode-skill-improver | Bounded post-task skill improvement subagent for prompt, routing, and eval refinement. |
| visual-asset-generator | subagent | 9router/medium | opencode-visual-asset-generator | Plans and prepares legal style-equivalent visual asset generation jobs for image-heavy UI, reference replication, hero art, icon badges, product mockups, thumbnails, avatars, and background textures. If image-generation tools are available in-session, it may execute generation; otherwise generation is executed by the orchestrator via an image generation tool/endpoint. |
