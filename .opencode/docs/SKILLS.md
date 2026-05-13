# Skills Index

Routing and ownership source of truth: `AGENT_ROUTING.md`.

## Active skills (1:1 with active agents)
- `opencode-orchestrator` — owned by `@orchestrator`; routes work, coordinates lanes, and integrates results
- `opencode-fixer` — owned by `@fixer`; handles bounded implementation and tests
- `opencode-oracle` — owned by `@oracle`; handles architecture, review, and simplification
- `opencode-quality-gate` — owned by `@quality-gate`; performs final read-only conformance/risk signoff
- `opencode-designer` — owned by `@designer`; handles UI/UX, reference, design-system workflow, and motion direction/reduced-motion review
- `opencode-explorer` — owned by `@explorer`; discovers codebase structure and reuse
- `opencode-council` — owned by `@council`; provides multi-LLM consensus for high-stakes or ambiguous decisions
- `opencode-visual-asset-generator` — owned by `@visual-asset-generator`; plans legal style-equivalent visual asset generation jobs

## Triggered planning lane
- `opencode-artifact-planner` — owned by `@artifact-planner`; used only for multi-phase, spec-heavy, materially ambiguous, or evidence-heavy planning.

## Supporting research lane
- `opencode-librarian` — owned by `@librarian`; a supporting docs-research helper plus document-centric read-only extraction/research/transformation support, not a core routing lane in the simplified model.

## Helper/specialist lanes (triggered)
- `opencode-architect` — owned by `@architect`; unified read-only advisory lane for product/SaaS, platform/runtime/release/mobile, AI systems, and UI-system architecture boundaries
- `opencode-skill-improver` — owned by `@skill-improver`; improves prompts/skills/routing after real evidence

Compatibility note: merged skill names are now canonical for routing. Legacy merged-away skills (accessibility/platform/product/AI/security/UI-system/visual-parity reviewer variants plus build/general) are intentionally removed from active routing.

## Contract expectations
Every skill should provide:
- frontmatter `name` and `description`,
- a clear workflow or usage contract,
- allowed/forbidden posture where relevant,
- evidence/output expectations when relevant,
- failure or limitation handling when relevant.
