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

## OMP alignment checks (docs/contract phase)
- Verify typed output schema fields present in active lane contracts.
- Verify validation ladder language present in orchestrator/fixer/quality contracts.
- Verify LSP-first + fallback evidence language present where implementation/routing owns edits.
- Verify built-ins remain opt-in/comparator and not default canonical routing.

## Deterministic edit helper MVP checks
- `npm run test:deterministic-edit-helper`
- Scope: proposal-only, zero-write, exact unique block match, expected file sha256, fail-closed reason codes, JSON + unified diff output.
- Exit code contract:
  - `10` stale hash
  - `11` anchor not found
  - `12` ambiguous anchor
  - `13` no change
  - `14` path out of scope
  - `15` unsupported file
  - `16` write forbidden

## Runnable fixtures in this repo
- `npm run eval:harness`
- fixtures live in `scripts/evals/fixtures/`
- current lightweight executable fixtures:
  - `docs-system-of-record`
  - `runtime-plugin-removal`
  - `agents-policy-bloat-negative`
  - `evidence-verification-negative`
  - `readonly-boundary-negative`
  - `creativity-fast-path-routing`

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
  - `routing-borderline-direct-tiny-task`
  - `routing-fallback-valid-specialist-unavailable`
  - `creativity-fast-path-positive`
  - `prototype-promotion-required-positive`
  - `creativity-fast-path-risky-negative`

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
Transcript fixtures may use either explicit normalized `events`, `rawTranscript`, `rawToolTrace`, or `shareExport` inputs. Each transcript eval emits `transcript_source_mode` plus a deterministic `routing_score` from 0–5 across lane fit, threshold compliance, planner-first, evidence legibility proxy, and final-gate presence.

Maintainer workflow for transcript fixtures:
- Prefer adding a new fixture whenever a real workflow failure or ambiguity is discovered.
- Label fixtures as `good`, `bad`, `borderline`, `fallback-valid`, `source-strategy`, `domain-boundary`, `quality-gate`, or `planner-boundary` via `classification`.
- Mark fixtures with `releaseCritical: true` only when they should count toward release readiness.
- Provide `expectedReasonCodes` and, when useful, `expectedScoreRange` so regressions stay explicit.
- If the source is not already normalized, prefer `rawToolTrace` over free-form text when structured data is available.
- Use `shareExport` for saved OpenCode share/session HTML or embedded payload snippets when the source is real but not already normalized. The adapter is intentionally heuristic: it extracts transcript-like quoted strings from script payloads, decodes common JS escapes, and only keeps candidates that look structurally like transcript lines (agent/action cues with transcript-style ordering) before normalizing them into replayable events.
- For `Creativity Fast Path`, keep at least four coverage shapes live: creative-positive, prototype-positive, risky-negative, and promotion-required behavior. Positive fixtures must stay labeled `draft`/`prototype`/`exploration`; risky negatives must prove the mode exits when hard rails are touched.

## Drift sentinel release suite

`npm run check:routing-release` hardens transcript release readiness. It fails when critical drift coverage disappears, even if ordinary fixture averages still look healthy.

Required drift sentinel ids:
- `drift-planner-default-tax-negative` → `routing-drift-planner-overuse-tiny-task` (`planner-boundary`, release-critical)
- `drift-maintenance-overgated-negative` → `routing-drift-maintenance-overgated` (`bad`, staged non-critical)
- `drift-designer-frontend-boundary-negative` → `routing-drift-missing-designer-direction` (`domain-boundary`, release-critical)
- `drift-fullstack-catchall-negative` → `routing-drift-fullstack-catchall` (`domain-boundary`, release-critical)
- `drift-source-strategy-skip-negative` → `source-strategy-missing-for-version-sensitive-work` (`source-strategy`, staged non-critical)
- `drift-quality-gate-remediation-positive` → no violation reason codes expected (`quality-gate`, release-critical)
- `drift-visual-asset-boundary-negative` → `visual-asset-boundary-violation` (`domain-boundary`, staged non-critical)
- `drift-readonly-advisor-write-negative` → `readonly-advisor-write-violation` (`bad`, release-critical)

Option B staged rollout keeps core routing, domain split, read-only, and quality-gate remediation sentinels release-critical now. Source-style and visual-asset sentinels remain required but staged non-critical until more real transcripts exist.

Release gate expectations:
- minimum transcript fixture count covers current suite plus drift sentinels;
- required sentinel ids all present;
- required classifications all present: `good`, `bad`, `borderline`, `fallback-valid`, `source-strategy`, `domain-boundary`, `quality-gate`, `planner-boundary`;
- source-mode diversity includes normalized events and raw tool trace coverage;
- all transcript fixtures pass expected reason-code matching;
- release-critical fixtures all pass;
- transcript average and release-critical average stay at or above `4.5`.

Task fixture `drift-planner-visual-asset-boundary` also guards that visual-asset boundary coverage remains connected to a legal-style-equivalent handoff sentinel.
