# Skills Index

Routing and ownership source of truth: `AGENT_ROUTING.md`.
Capability registry: `.opencode/capabilities/registry.json`. Generated advisory view: `docs/generated/capability-matrix.md`.
Senior external reference map: `SENIOR_SKILLS_REFERENCES.md`. Marketplace skills from `skills.sh` are reference material, not default runtime installs; no mass installing external skills without explicit user approval and stack-fit review.

## Graphify discovery skill
- `graphify-discovery` — mandatory query-first local code-only graph context for code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes when fresh; direct source reading, tests, and runtime checks remain mandatory. If missing, stale, or unsupported, record fallback and use normal discovery.

## Active skills (1:1 with active agents)
- `opencode-orchestrator` — owned by `@orchestrator`; routes work, coordinates lanes, and integrates results
- `opencode-fixer` — owned by `@fixer`; handles bounded implementation and tests
- `opencode-designer` — owned by `@designer`; handles UI/UX direction and visual contracts
- `opencode-explorer` — owned by `@explorer`; discovers codebase structure and reuse
- `opencode-librarian` — owned by `@librarian`; supports docs research and extraction
- `opencode-oracle` — owned by `@oracle`; handles architecture and review
- `opencode-quality-gate` — owned by `@quality-gate`; performs final read-only conformance and risk signoff
- `opencode-architect` — owned by `@architect`; handles architecture advisory boundaries
- `opencode-artifact-planner` — owned by `@artifact-planner`; handles multi-phase or evidence-heavy planning
- `opencode-visual-context-extractor` — owned by `@visual-context-extractor`; extracts visual context before downstream decisions

## On-demand domain skills
- Backend, frontend, mobile, fullstack, devops, design-system, planning-review, project-management, consensus, skill-improvement, and visual-asset work remain skills invoked by retained lanes.

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
- `@fixer with frontend skill` / `@fixer with mobile skill` — implement from the cited catalog. Load tokens from `.opencode/catalog/<active-system>/tokens.{css,json}` (do not re-derive from memory). Cite catalog source in PR/evidence.
- `@designer with design-system skill` — when adding new shared tokens/primitives, search the catalog first via `python3 ~/.config/opencode/scripts/catalog-search.py`. Use `design-system-fork.py` when extending a catalog system.
- `@quality-gate` — for substantial UI, `visual-quality-contract.md` must contain `catalog_citation`. Missing → `NEEDS_FIX` (mechanical, not taste). Token parity and deviation count rows in `visual-rubric.md` are mechanical checks.
- `@orchestrator` — on `greenfield` or `substance=substantial UI` tasks, verify `catalog-decision.md` exists before routing to `@fixer with frontend skill`/`@fixer with mobile skill`.

Exemptions: tiny/reversible UI tweaks, non-visual changes, and projects with their own private brand kit (private kits extend catalog, never replace).

Meta-skill: `ui-ux-pro-max` is auto-loaded for substantial UI work and contains the cross-lane UI/UX playbook + catalog index pointer.

Controlled external overlays: canonical authority, activation/skip/reject, adoption, and evidence rules live in `skills/ui-ux-pro-max/SKILL.md` §"Canonical Taste / 21st bridge".
- `taste-overlay` — local MIT adaptation of Taste `gpt-taste`; bounded craft dials and anti-slop preflight only after catalog/design authority selection. Never token/layout authority. Source/revision/adaptation record: `skills/taste-overlay/SOURCE.md`.
- `21st-discovery-overlay` — local Apache-2.0 adaptation of 21st `21st-cli-use`; candidate metadata only after explicit design direction, stack, and component gap. It does not authorize auth, retrieval, install, generation, publish, team access, source adoption, or target-app mutation. Per-item license remains required. Source/revision/adaptation record: `skills/21st-discovery-overlay/SOURCE.md`.

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
## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.
