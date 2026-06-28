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
- `npm run check:rules-source` → `scripts/rules-source-scanner.py` (advisory; scan project for agent-rules files from OpenCode, Claude Code, Codex, Cursor, Windsurf, Continue, Cline, Cody, Roo, Aider, GitHub Copilot, GitLab Duo)
- `npm run init:rules-harmonize` → `scripts/rules-harmonizer.py --apply` (import external rules into `.opencode/docs/SOURCE_RULES.md`; append `## Source Rules` to root `AGENTS.md`; idempotent)
- `npm run init:rules-harmonize:forward-all` → same, with `--forward-to claude,codex,cursor,windsurf` to write mirror files
- `npm run init:stack-suggest` → `scripts/stack-resource-suggester.py` (soft recommender; matches project signals against `scripts/data/stack_resources.json` to surface idiomatic skills, MCP servers, and best practices; never auto-installs)
- `npm run check:session-trace <transcript>` → `scripts/session-trace-audit.py` (advisory heuristic audit for the failure mode: no skill/MCP orientation, loaded-but-unused skill, obvious MCP silently skipped, no sequential-thinking on multi-issue debugging)
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
- Multi-source rules compatibility: when a target project has rules files from other agent tools (Claude Code `CLAUDE.md`, Codex `AGENTS.md`/`.codex/`, Cursor `.cursorrules`/`.cursor/rules/`, Windsurf `.windsurfrules`, Continue, Cline, Cody, Roo, Aider, GitHub Copilot, GitLab Duo), orchestrator MUST run `npm run check:rules-source` then `npm run init:rules-harmonize` to capture the audit trail at `.opencode/docs/SOURCE_RULES.md` before non-trivial work. OpenCode-native rules (`AGENTS.md` + `.opencode/docs/`) win on conflict; user is surfaced before any silent override.
- Stack-aware resource discovery: when working in any stack covered by `scripts/data/stack_resources.json` (Laravel, Next.js, React Native/Expo, Flutter, Supabase, Rails, Go, Python/FastAPI, Django, Vue/Nuxt, Svelte/SvelteKit, Tailwind+shadcn, Rust, Postgres), orchestrator MUST run `npm run init:stack-suggest -- --write-evidence .opencode/evidence/<task>/stack-suggestion.md` and confirm the idiomatic patterns with the user before non-trivial implementation. The registry's idiomatic guidance (e.g. "use `php artisan make:*` for all scaffolding") overrides ad-hoc habits.
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
