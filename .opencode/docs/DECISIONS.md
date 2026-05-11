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
