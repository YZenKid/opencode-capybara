# Prompt Gates

## Purpose
Prompt gates convert important repository invariants into deterministic checks.

## Existing gate
- `npm run test:prompt-gates`
- implementation: `scripts/prompt-gate-regression.mjs`

## Mechanical checks
- `npm run check:docs` → `scripts/docs-integrity-check.mjs`
- `npm run check:agents` → `scripts/agent-boundary-check.mjs`
- `npm run check:skills` → `scripts/skill-contract-check.mjs`
- `npm run check:evidence` → `scripts/evidence-contract-check.mjs`
- `npm run check:verify-claim` → `scripts/verify-before-claim-check.py` (soft helper; orchestrator-facing audit for confident claims without a matching tool call or `confirmed_*` / `assumption` / `unverified` label)
- `npm run check:verify-claim:strict` → same script with `--strict` (exit 1 on any flagged claim; use in CI to enforce)
- `npm run docs:generate:check` → generated docs freshness validation
- `npm run check:harness` → aggregate harness check

## Invariant categories
- Routing and skill posture
- Orchestrator direct-vs-delegate thresholds
- Read-only vs write-capable boundaries
- Docs as system of record
- Evidence contract
- Portability rules
- Setup safety / no hidden install hooks
- Auto-commit safety
- Finish-first execution with explicit blocker taxonomy and deferred non-blocking questions
- Advisory non-veto behavior (must reclassify advisory status via taxonomy + evidence)
- Document fallback routing: unsupported model attachment input (for example `input.pdf:false`) must trigger workspace-file check plus `@librarian` extraction before asking the user to convert PDF/DOCX/XLSX/PPT/Office files.
- Indonesian-first user-facing orchestrator language with technical-literal exceptions
- Subagent internal-schema normalization before user-facing final output
- Verify-before-claim for orchestrator: confident claims about user code/runtime/environment/configuration MUST be backed by a tool call (`read_file`, `terminal`, `web_search`, `web_extract`, `grep`, `search_files`, `session_search`, or delegated subagent) in the same response or carry an explicit `confirmed_repo` / `confirmed_runtime` / `confirmed_docs` / `user_confirmed` / `assumption` / `unverified` label. Forwarded subagent prose is `assumption` until independently verified. Mechanical helper: `npm run check:verify-claim` (soft) / `:strict` (CI).
- Mode-aware execution: Greenfield App Accelerator for new app/MVP/product builds, Maintenance Stability Mode for bugfix/maintenance work, and Creativity Fast Path for explicit ideation/generate/prototype/draft requests.
- Creative Depth Contract for greenfield plans: alternatives, tradeoff scoring, first-slice rationale, journey-to-contract mapping, readiness status, and `PASS_FOR_SLICE` support.
- Creativity Fast Path invariant: natural-language opt-in only, exploratory/reversible only, must label outputs `draft`/`prototype`/`exploration`, and must use a Promotion Gate before any strong completion claim.
- Plan Quality Gate before non-trivial implementation with `PASS`, `PASS_FOR_SLICE`, `NEEDS_DEPTH`, and `BLOCKED`.
- Over-gating prevention: maintenance/bugfix work must not require greenfield product thesis or 2-3 creative alternatives by default.
- Non-bypass rule: Creativity Fast Path must not bypass hard security/privacy/destructive/release rails, planner triggers for material ambiguity, or `@quality-gate` on material/risky/prompt/config/security/UI completion claims.

## Change adjacency rule
If you change policy or docs guarded by a gate:
1. update canonical doc,
2. update the related gate/check,
3. rerun validation,
4. record decision/evidence.

Routing hardening minimum:
- Ensure `.opencode/docs/AGENT_ROUTING.md` keeps explicit orchestrator direct-work thresholds, anti-pattern examples, and compact routing checklist/rubric.
- Ensure `skills/opencode-orchestrator/SKILL.md` keeps hard defaults that route read-heavy discovery to `@explorer` and multi-file bounded implementation to `@fixer`.
- Ensure greenfield work cannot be executed from a shallow plan lacking creative alternatives, tradeoff scoring, journey-to-contract mapping, readiness status, and Plan Quality Gate.
- Ensure maintenance work remains lightweight and regression-first rather than being forced through greenfield-heavy gates.
- Enforce via `npm run test:prompt-gates` (and `npm run doctor` as a quick local policy sanity check).

Drift sentinel adjacency minimum:
- Routing/boundary changes must update transcript fixtures when they alter planner default-tax, maintenance over-gating, designer/frontend split, fullstack catch-all, read-only advisor, source-strategy, visual-asset, or quality-gate remediation behavior.
- Release-critical sentinel fixtures use Option B staged rollout: core routing/domain/read-only/quality remediation blockers are critical now; source-style and visual-asset style-equivalent checks are required but staged non-critical until fixture history stabilizes.
- Source-strategy changes must keep reference-first lookup or skipped-source rationale for version-sensitive/material work.
- Creative-depth changes must not apply greenfield thesis/options burden to ordinary maintenance bugfixes.
- Creativity Fast Path changes must add or update both positive and negative coverage: creative-positive, prototype-positive, risky-negative, and promotion-required behavior.
- Harness evidence changes must preserve fixture ids, classifications, source modes, release-critical flags, reason codes, and latest report paths in `.opencode/evidence/harness-evals/latest/`.

## Generated reports
- Refresh advisory generated summaries with `npm run docs:generate`.
- Validate freshness with `npm run docs:generate:check` or indirectly through `npm run check:docs`.
- Generated outputs live in `docs/generated/` and help maintainers inspect current agent metadata, prompt-gate coverage, and docs-integrity coverage.
- Generated reports are evidence helpers only; canonical policy remains in `.opencode/docs/` and the implementing scripts.
