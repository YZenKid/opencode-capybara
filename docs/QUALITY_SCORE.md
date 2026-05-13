# Quality Score

| Area | Score | Evidence | Gap | Owner Agent |
|---|---:|---|---|---|
| Agent boundaries | 8/10 | `npm run check:agents` | Tighten read-only heuristics over time | `@quality-gate` |
| Prompt gates | 8/10 | `npm run test:prompt-gates` | Keep docs/gates in lockstep | `@skill-improver` |
| Docs integrity | 7/10 | `npm run check:docs` | Add stale-doc detection later | `@librarian` |
| Security policy | 8/10 | `.opencode/docs/SECURITY.md`, `npm run doctor` | Add secret-scan fixtures later | `@quality-gate` |
| Evidence contract | 7/10 | `npm run check:evidence` | Expand replay bundle validation later | `@quality-gate` |
| Harness evals | 6/10 | `.opencode/docs/EVALS.md` | Add runnable task suites/replay fixtures | `@oracle` |

## Usage
- Update after material harness changes.
- Treat low scores as backlog seeds.
- Repeated failures should increase evidence depth or mechanical enforcement.
