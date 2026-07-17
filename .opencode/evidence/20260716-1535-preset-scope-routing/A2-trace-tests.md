# A2 trace tests

Red: strict mode treated every WARN as failure, conflicting with unknown-schema semantics.

Green: `--strict` ignores only `unknown_trace_schema` for exit status. JSON still reports `status: WARN` and finding `unknown_trace_schema`.

Fixture semantics:

- planner in read-only: WARN `planner_on_read_only`; strict non-zero
- mutation after audit: WARN `mutation_after_read_only`; strict non-zero
- security audit no edit: PASS; strict zero
- explicit `fix P0 #1`: PASS; strict zero
- tiny budget excess: WARN `tiny_budget_exceeded`; strict non-zero
- deep checkpoint: PASS; strict zero
- unknown schema: WARN/unverified `unknown_trace_schema`; strict zero
- repeated orientation: WARN `repeated_orientation`; strict non-zero

Validation:

- `npm run test:session-trace` — PASS, 5 tests
- `npm run test:session-trace-strict` — PASS, 5 tests
- `python3 scripts/session-trace-audit.py --strict scripts/tests/fixtures/session-trace/unknown_schema.md` — exit 0
- JSON unknown-schema output — `status: WARN`, finding `unknown_trace_schema`

Limits: explicit markers only. Live OpenCode structured trace emission remains unverified.
