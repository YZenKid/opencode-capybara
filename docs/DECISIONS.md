# Decisions

## 2026-05-10 — Harness engineering migration baseline
- `AGENTS.md` is now a short table of contents plus non-negotiables.
- `.opencode/docs/` is the repository system of record.
- `docs/` remains as a reference-only mirror for historical context and future `init-harness` generation.
- `.opencode/plans/<task-id>.md` remains the current source-of-truth planning artifact.
- `docs-integrity-check` is the first new mechanical check.
- Broader eval sophistication should stay incremental after docs and gate compatibility are stable.

## 2026-05-10 — Structural-parser hardening traceability
- The structural-parser hardening pass is tracked under the durable task id `20260510-2140-harness-engineering-plan`.
- This pass adds light markdown heading parsing, shallow JSON key assertions, and stronger structural replay/evidence validation without introducing a general parser framework.
