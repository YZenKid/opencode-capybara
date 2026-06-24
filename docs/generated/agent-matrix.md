# Generated: Agent Matrix

Generated summary of local agent metadata. This file is advisory and must not replace canonical policy in `.opencode/docs/`.

- Agent count: 22
- Source: `agents/*.md` frontmatter

| Agent | Mode | Model | Skills | Description |
| --- | --- | --- | --- | --- |
| architect | subagent | 9router/medium | opencode-architect | Unified read-only architect lane for product/SaaS, platform/runtime/release, AI, and UI-system boundaries |
| artifact-planner | primary | 9router/high | opencode-artifact-planner | Artifact-writing SDD/TDD planner using the standalone opencode-capybara plan flow without entering built-in read-only Plan Mode. |
| backend | subagent | 9router/low | opencode-backend | Backend API, services, validation, auth integration, jobs, queues, migrations, and data tests specialist |
| council | subagent | 9router/medium | opencode-council | Multi-LLM consensus engine for high-confidence answers |
| design-system-engineer | subagent | 9router/medium | opencode-design-system-engineer | Design-system implementation specialist for tokens, primitives, component APIs, theming, DESIGN.md alignment, and reusable UI foundations |
| designer | subagent | 9router/high | opencode-designer | UI/UX implementation and review lane for polished visuals, motion direction/reduced-motion review, accessibility, and visual polish |
| devops | subagent | 9router/low | opencode-devops | CI/CD, Docker, environment, deploy, monitoring, rollback, and infrastructure configuration specialist |
| explorer | subagent | 9router/low | opencode-explorer | Local codebase discovery and search specialist for unfamiliar or broad scopes |
| fixer | subagent | 9router/low | opencode-fixer | Bounded implementation and testing specialist for Red/Green/Refactor work |
| frontend | subagent | 9router/low | opencode-frontend | Web frontend implementation specialist for React/Next/Vue/Svelte UI after design direction exists |
| fullstack | subagent | 9router/low | opencode-fullstack | Narrow fullstack vertical-slice integrator for small tightly-coupled frontend/backend changes only |
| librarian | subagent | 9router/fast | opencode-librarian | Library/docs research plus document-centric read-only extraction and transformation support |
| mobile | subagent | 9router/low | opencode-mobile | Mobile app implementation specialist for React Native, Expo, Flutter, and native-capability workflows |
| oracle | subagent | 9router/medium | opencode-oracle | Read-only architecture and risk review advisor for complex decisions |
| orchestrator | primary | 9router/high | opencode-orchestrator | AI coding orchestrator that routes tasks to specialist agents |
| plan-reviewer | subagent | 9router/medium | opencode-plan-reviewer | Dedicated plan depth reviewer that validates plan meets minimum depth requirements before implementation |
| project-manager | subagent | 9router/low | opencode-project-manager | Read-only milestone, backlog, issue breakdown, dependency, risk register, release checklist, and handoff planner |
| quality-gate | subagent | 9router/medium | opencode-quality-gate | Final conformance and risk gate for non-trivial OpenCode work |
| skill-improver | subagent | 9router/fast | opencode-skill-improver | Bounded post-task skill improvement subagent for prompt, routing, and eval refinement. |
| system-analyst | subagent | 9router/low | opencode-system-analyst | Read-only requirements, user-flow, API contract, data-flow, edge-case, NFR, and acceptance-criteria analyst |
| visual-asset-generator | subagent | 9router/medium | opencode-visual-asset-generator | Plans and prepares style-equivalent fallback visual asset generation jobs for image-heavy UI, reference replication, hero art, icon badges, product mockups, thumbnails, avatars, and background textures. If image-generation tools are available in-session, it may execute generation; otherwise generation is executed by the orchestrator via an image generation tool/endpoint. |
| visual-context-extractor | subagent | 9router/vision | opencode-visual-context-extractor | Read-only extraction of observable visual context (layout, text, components, color, state, errors, flows) from images, screenshots, diagrams, and other visual files. Returns structured JSON for caller agents. Does not generate images, give design direction, or edit source. |
