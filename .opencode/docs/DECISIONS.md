# Decisions

## 2026-05-10 — Harness engineering migration baseline
- `AGENTS.md` is now a short table of contents plus non-negotiables.
- `.opencode/docs/` is the repository system of record.
- `.opencode/plans/<task-id>.md` remains the current source-of-truth planning artifact.
- `docs-integrity-check` is the first new mechanical check.
- Broader eval sophistication should stay incremental after docs and gate compatibility are stable.

## 2026-05-10 — Structural-parser hardening traceability
- The structural-parser hardening pass is tracked under the durable task id `20260510-2140-harness-engineering-plan`.
- This pass adds light markdown heading parsing, shallow JSON key assertions, and stronger structural replay/evidence validation without introducing a general parser framework.

## 2026-05-11 — Orchestrator finish-first execution default
- For implementation and plan-execution requests, the orchestrator should finish as much work as safely possible before asking the user follow-up questions.
- Plan gates, phases, and work packages are internal execution checkpoints by default, not user approval checkpoints, unless explicitly marked otherwise.
- Non-blocking questions should be deferred and accumulated for the end-of-run summary together with assumptions and residual decisions.
- Mid-run interruption is reserved for destructive/irreversible actions, security/privacy boundaries, missing mandatory access, or material non-reversible ambiguity.

## 2026-05-12 — Operational proof density hardening
- The repo now keeps curated exemplar task bundles under `.opencode/plans/` and `.opencode/evidence/` to prove the evidence contract with real artifacts, not placeholders.
- Advisory generated summaries under `docs/generated/` are refreshed via `npm run docs:generate` rather than remaining static placeholders.
- The strict golden path for proof-of-use is documented in `.opencode/docs/QUALITY.md` so maintainers can replay a small end-to-end harness success path.
- Generated-doc freshness is now mechanically enforced through `npm run docs:generate:check` and included in docs-integrity validation to reduce silent drift.
- The generated-doc parser remains intentionally lightweight but now relies on simpler structure-aware extraction instead of a single broad regex pass.
