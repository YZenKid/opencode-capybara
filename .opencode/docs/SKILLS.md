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
- `opencode-designer` — owned by `@designer`; handles UI/UX direction, reference parity, `DESIGN.md`-driven blueprint handoff, polish-mode audit evidence, and motion direction/reduced-motion review
- `opencode-design-system-engineer` — owned by `@design-system-engineer`; handles shared tokens, primitives, component APIs, design-system registry upkeep, and generated token/spec/docs artifacts
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

## UI/UX design system source of truth (Open Design integration)

Substantial UI work (greenfield, design revamp, reference parity, image-heavy, or taste-sensitive surfaces) **must anchor to the Open Design catalog** (`https://open-design.ai`):

- 150 design systems: `https://open-design.ai/plugins/systems/`
- 290 templates: `https://open-design.ai/plugins/templates/`
- Format: single-file `DESIGN.md` (Apache-2.0) per system — adopted as the project's `DESIGN.md` v2 schema.

Local cache: `.opencode/catalog/INDEX.md` (≥150 entries with license per entry). Index is seeded by `python3 ~/.config/opencode/scripts/design-source-importer.py --init`.

Lane obligations under this policy:

- `@designer` — pick from the catalog (1 system + 1 template minimum) before producing any substantial UI artifact. Cite in `.opencode/evidence/<task-id>/catalog-decision.md` and in the visual contract's `catalog_citation` block. Deviation from the cited system requires a `deviation_audit` entry.
- `@frontend` / `@mobile` — implement from the cited catalog. Load tokens from `.opencode/catalog/<active-system>/tokens.{css,json}` (do not re-derive from memory). Cite catalog source in PR/evidence.
- `@design-system-engineer` — when adding new shared tokens/primitives, search the catalog first via `python3 ~/.config/opencode/scripts/catalog-search.py`. Use `design-system-fork.py` when extending a catalog system.
- `@quality-gate` — for substantial UI, `visual-quality-contract.md` must contain `catalog_citation`. Missing → `NEEDS_FIX` (mechanical, not taste). Token parity and deviation count rows in `visual-rubric.md` are mechanical checks.
- `@orchestrator` — on `greenfield` or `substance=substantial UI` tasks, verify `catalog-decision.md` exists before routing to `@frontend`/`@mobile`.

Exemptions: tiny/reversible UI tweaks, non-visual changes, and projects with their own private brand kit (private kits extend catalog, never replace).

Meta-skill: `ui-ux-pro-max` is auto-loaded for substantial UI work and contains the cross-lane UI/UX playbook + catalog index pointer.

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
