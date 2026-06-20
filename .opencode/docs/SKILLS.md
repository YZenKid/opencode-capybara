# Skills Index

Routing and ownership source of truth: `AGENT_ROUTING.md`.
Capability registry: `.opencode/capabilities/registry.json`. Generated advisory view: `docs/generated/capability-matrix.md`.
Senior external reference map: `SENIOR_SKILLS_REFERENCES.md`. Marketplace skills from `skills.sh` are reference material, not default runtime installs; no mass installing external skills without explicit user approval and stack-fit review.

## Active skills (1:1 with active agents)
- `opencode-orchestrator` — owned by `@orchestrator`; routes work, coordinates lanes, and integrates results
- `opencode-fixer` — owned by `@fixer`; handles bounded implementation and tests
- `opencode-frontend` — owned by `@frontend`; handles web UI implementation, component tests, accessibility implementation, and browser validation after design direction exists
- `opencode-backend` — owned by `@backend`; handles APIs, services, validation, auth integration, migrations, jobs, queues, and TDD for server/data changes
- `opencode-mobile` — owned by `@mobile`; handles React Native, Expo, Flutter, native permissions, navigation, offline, push, camera, deep links, and mobile validation
- `opencode-devops` — owned by `@devops`; handles CI/CD, Docker, env config, deploy, monitoring, rollback, and destructive-action gates
- `opencode-fullstack` — owned by `@fullstack`; handles small tightly-coupled FE/BE vertical slices and split thresholds
- `opencode-oracle` — owned by `@oracle`; handles architecture, review, and simplification
- `opencode-quality-gate` — owned by `@quality-gate`; performs final read-only conformance/risk signoff
- `opencode-designer` — owned by `@designer`; handles UI/UX, reference, design-system workflow, and motion direction/reduced-motion review
- `opencode-explorer` — owned by `@explorer`; discovers codebase structure and reuse
- `opencode-council` — owned by `@council`; provides multi-LLM consensus for high-stakes or ambiguous decisions
- `opencode-visual-asset-generator` — owned by `@visual-asset-generator`; plans style-equivalent fallback visual asset generation jobs

## Triggered planning lane
- `opencode-artifact-planner` — owned by `@artifact-planner`; used only for multi-phase, spec-heavy, materially ambiguous, or evidence-heavy planning.

## Supporting research lane
- `opencode-librarian` — owned by `@librarian`; a supporting docs-research helper plus document-centric read-only extraction/research/transformation support, not a core routing lane in the simplified model.

## Helper/specialist lanes (triggered)
- `opencode-architect` — owned by `@architect`; unified read-only advisory lane for product/SaaS, platform/runtime/release/mobile, AI systems, and UI-system architecture boundaries
- `opencode-system-analyst` — owned by `@system-analyst`; read-only requirements, PRD, user-flow, API contract, data-flow, edge-case, NFR, and acceptance-criteria analysis
- `opencode-project-manager` — owned by `@project-manager`; read-only milestones, backlog, issue breakdown, dependency/risk register, release checklist, and handoff planning
- `opencode-skill-improver` — owned by `@skill-improver`; improves prompts/skills/routing after real evidence
- `opencode-visual-context-extractor` — owned by `@visual-context-extractor`; mandatory first lane for visual understanding from image, screenshot, mockup, and diagram inputs. No other agent may self-infer from visual input; all agents needing visual context must route here first (returns `visual_context_extractor.v1` JSON; no design critique, no parity claim, no image generation). Downstream decisions remain with the receiving lane.

## Domain skill trigger notes
- All active skills follow mode-aware execution: `Greenfield App Accelerator` for new app/MVP/product builds and `Maintenance Stability Mode` for bugfix/refactor/maintenance work.
- Greenfield skills use the Creative Depth Contract, Plan Quality Gate, and [GREENFIELD_STARTER.md](./GREENFIELD_STARTER.md); maintenance skills stay regression-first and minimal.
- Framework/generator best-practice enforcement applies to existing app development too, not only from-scratch work. Before framework-managed edits, implementation skills should read `.opencode/docs/PROJECT_STACK.md`, `.opencode/docs/PROJECT_COMMANDS.md`, `.opencode/docs/FRAMEWORK_PLAYBOOK.md`, and `.opencode/docs/PROJECT_DETECTED_TOOLS.md` when present.
- If those project docs are missing or stale for non-trivial work, implementation/routing skills should run or suggest `/init-harness`, then use `@librarian` for version-sensitive official docs when project docs do not already settle command behavior.
- Use `opencode-frontend` only after `@designer` direction or project-local design guidance exists for substantial UI.
- Use `opencode-mobile` for app implementation; escalate privacy/native permission/store/runtime boundaries.
- Use `opencode-backend` for API/data code; require TDD for production/security-sensitive behavior.
- Use `opencode-devops` for ops config; deploy/destructive/credential actions require explicit approval.
- Use `opencode-system-analyst` before implementation when requirements/contracts are unclear.
- Use `opencode-project-manager` after scope is understood and delivery breakdown is needed.
- Use `opencode-fullstack` only for small vertical slices; split broad work to frontend/backend lanes.

Compatibility note: merged skill names are now canonical for routing. Legacy merged-away skills (accessibility/platform/product/AI/security/UI-system/visual-parity reviewer variants plus build/general) are intentionally removed from active routing.

## Contract expectations
Every skill should provide:
- frontmatter `name` and `description`,
- a clear workflow or usage contract,
- allowed/forbidden posture where relevant,
- evidence/output expectations when relevant,
- failure or limitation handling when relevant,
- source strategy: when to rely on repo evidence, official docs, upstream source/examples, browser/screenshots, or current web research,
- anti-assumption posture: how to mark assumptions, when to ask, and when to stop instead of guessing,
- grounded creativity posture for greenfield or taste-sensitive work: when to generate 2-3 bounded options and how to justify the chosen path.

Active-lane schema baseline (non-trivial work):
- `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence`.
- Validation ladder and LSP-first posture must be explicit where lane owns implementation, routing, review, or quality gate.
- Mode, readiness status, and claim level must be explicit for greenfield/product work and material maintenance work.
