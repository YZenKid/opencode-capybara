# A3 candidate samples

Static fixture samples. These validate checker policy markers, not live OpenCode telemetry.

| Scenario | Class / route marker | Result | Planner | Mutation | Notes |
| --- | --- | --- | --- | --- | --- |
| `planner_read_only.md` | read-only | `WARN` `planner_on_read_only` | present | absent | Correct negative guard. |
| `mutation_after_audit.md` | read-only | `WARN` `mutation_after_read_only` | absent | present | Correct negative guard. |
| `security_audit_stays_read_only.md` | security audit, no edit | `PASS` | absent | absent | Risk did not grant implementation. |
| `explicit_fix_promotion.md` | explicit `fix P0 #1` | `PASS` | allowed by promotion semantics | permitted after promotion | Explicit scope promotion accepted. |
| `tiny_budget_excess.md` | `tiny-readonly-compare` | `WARN` `tiny_budget_exceeded` | absent | absent | Fixture signals 4 reads and 11 calls. |
| `deep_checkpoint_allowed.md` | `read-only-deep-review` | `PASS` | absent | absent | Deep review not forced into lite budget. |

Measured scope: fixture audit outcomes only. Tool/read counters are fixture markers, not live session metrics. Structured live transcript schema remains `unverified`.
