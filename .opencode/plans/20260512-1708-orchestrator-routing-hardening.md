# Plan — Orchestrator Routing Hardening

Task id: `20260512-1708-orchestrator-routing-hardening`

## Goal
Harden orchestrator routing discipline so material work is plan-bound, delegated appropriately, and reviewed by `@quality-gate`.

## Validation Commands
- `npm run test:prompt-gates`
- `npm run check:harness`

## Evidence Requirements
- Plan artifact reviewed by `@artifact-planner`.
- Routing decisions recorded before implementation.
- Verification includes `@quality-gate` outcome.

## Final Planning Summary
Use `@artifact-planner` for non-trivial plan artifacts and `@quality-gate` for final conformance.
