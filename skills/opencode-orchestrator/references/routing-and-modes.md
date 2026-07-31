# Routing and Mode Contracts

Read this before routing when intent, mode, or direct-maintenance boundary is unclear.

## Intent and mode

- `read_only` means inspection only. No mutation, planner, tracker, remediation, or commit.
- `implementation` means explicit user change intent or approved plan. Findings, risk, and failed checks do not authorize edits.
- Use `tiny-readonly-compare` for narrow local evidence and `read-only-deep-review` for broad or risk-sensitive review.

## Mode contracts

### Greenfield App Accelerator

- Use for new apps, blank repos, MVPs, SaaS/product builds, or major product revamps.
- Route to `@artifact-planner` before implementation unless work is explicitly tiny prototype-only.
- Explore 2-3 credible options when it helps quality.
- Keep slice decisions reversible.
- Final claim should be `MVP slice complete` unless whole app is actually finished.

### Maintenance Stability Mode

- Use for bugfixes, regressions, refactors, dependency updates, small features in existing apps, and incident follow-up.
- Start from repro, failing behavior, regression test, or targeted evidence.
- Prefer smallest safe diff and preserve existing architecture/UX unless evidence says otherwise.

### Creativity Fast Path

- Use only for explicit natural-language requests to brainstorm, explore, generate, sketch, or prototype.
- Keep output labeled `draft`, `prototype`, or `exploration`.
- Promotion Gate applies when the user asks for permanent implementation, commit, deploy, or strong completion claim.

## Direct maintenance

- Maintenance Direct Fix: bounded existing-code bugfix with one known subsystem and one worker, no unresolved architecture/security/data/product decision, and no need for durable plan artifacts.
- Planner admission test: if the request can be safely executed with one worker, one known subsystem, and existing acceptance/regression evidence, prefer direct maintenance routing.
- If planner admission fails for bounded maintenance, reply `ROUTE_DIRECT` and stop planning instead of writing artifacts.
- Bounded maintenance may go direct when planner admission fails.
- bounded maintenance may go direct when planner admission fails.

## Trigger phrases to preserve

- Greenfield App Accelerator
- Maintenance Stability Mode
- Creativity Fast Path
- Best Practice Readiness Contract
- Creative Depth Contract
- Plan Quality Gate
- PASS_FOR_SLICE
- user journey → data model → API/contracts → UI screens → tests
- Maintenance work should not be forced through greenfield product thesis
- natural-language
- Promotion Gate
- Maintenance Direct Fix
- Planner admission test
- ROUTE_DIRECT
