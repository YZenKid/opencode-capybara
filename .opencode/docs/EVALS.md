# Evals

## Goal
Measure harness quality with task suites that resemble real work, not only static rule assertions.

## Minimum suite types
1. **Core behavioral evals** — task-level work such as docs migration, policy update, or bounded implementation.
2. **Constraint evals** — attempts to violate secrets, boundaries, or routing rules.
3. **Replay/regression evals** — cases derived from real failures.
4. **Drift watch evals** — checks that quality is not degrading over time.

## Grader layers
1. Deterministic checks
2. Structural/constraint checks
3. Semantic review
4. Human/LLM adjudication only when ambiguity remains

Use pass/fail + reason codes wherever possible.

## Replay bundle minimum
- `task_id`
- harness version metadata
- prompt or task summary
- tool trace summary
- files changed
- validation commands and outputs
- verdict
- reason codes

## Failure taxonomy
- instruction-following failure
- tool-selection failure
- constraint violation
- missing evidence
- over-editing
- under-editing
- validation omission
- harness bug
- flaky / nondeterministic failure

Use [TOOL_USAGE.md](./TOOL_USAGE.md) and [AGENT_TOOL_ACCESS.md](./AGENT_TOOL_ACCESS.md) as canonical references when triaging tool-selection failures.

## Improvement loop
failure → taxonomy → remediation → new regression/eval case → rerun

## Runnable fixtures in this repo
- `npm run eval:harness`
- fixtures live in `scripts/evals/fixtures/`
- current lightweight executable fixtures:
  - `docs-system-of-record`
  - `runtime-plugin-removal`
  - `agents-policy-bloat-negative`
  - `evidence-verification-negative`
  - `readonly-boundary-negative`

- current task-shaped behavioral fixtures:
  - `docs-policy-migration-roundtrip`
  - `evidence-bundle-completion`
  - `reviewer-boundary-routing`
  - `planner-and-mcp-state-contract`
  - `orchestrator-routing-discipline-20260512-1708`

- current transcript-shaped routing fixtures:
  - `routing-overreach-negative`
  - `routing-compliant-positive`
  - `routing-raw-overreach-negative`
  - `routing-raw-compliant-positive`

## Strict validation lane
- `npm run check:harness:strict`
- runs deterministic harness checks and the lightweight runnable eval suite together

## Replay evidence output
`npm run eval:harness` writes replayable evidence to:
- `.opencode/evidence/harness-evals/latest/report.json`
- `.opencode/evidence/harness-evals/latest/report.md`

These fixtures are intentionally lightweight for the current phase. They provide executable examples of harness expectations without introducing a heavy eval framework.

Behavioral task fixtures live in:
- `scripts/evals/task-fixtures/`

They remain deterministic and structural. They are meant to simulate real harness maintenance flows without introducing a judge-heavy eval platform.

Transcript sequence fixtures live in:
- `scripts/evals/transcript-fixtures/`

They add replayable sequence-level routing checks for orchestrator overreach without requiring a heavy semantic judge.
Transcript fixtures may use either explicit normalized `events`, `rawTranscript`, or `rawToolTrace` inputs. Each transcript eval emits `transcript_source_mode` plus a deterministic `routing_score` from 0–5 across lane fit, threshold compliance, planner-first, evidence legibility proxy, and final-gate presence.
