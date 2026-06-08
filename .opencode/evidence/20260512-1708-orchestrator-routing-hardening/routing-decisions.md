# Routing Decisions — 20260512-1708-orchestrator-routing-hardening

## Routing Decision Summary
- `@artifact-planner` owns plan artifact depth for non-trivial work.
- `@fixer` owns bounded implementation after the plan is ready.
- `@quality-gate` owns final conformance and risk signoff.

### Validation lane
- Use targeted prompt-gate and harness checks before completion claims.
