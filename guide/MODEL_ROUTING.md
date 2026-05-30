# Model Routing

## Kenapa model agent tidak langsung membaca `.env`?

`opencode.json` jelas mendukung `{env:...}`.

Namun untuk frontmatter `model:` di `agents/*.md`, dukungan env placeholder tidak cukup aman untuk diandalkan. Karena itu repo ini memakai jalur sinkronisasi yang eksplisit.

## Model routing sekarang diterapkan lewat dua jalur

- `opencode.json` memakai `OPENCODE_MODEL_DEFAULT` untuk model default runtime
- `scripts/sync-agent-models.mjs` menyamakan `model:` literal di `agents/*.md` dengan nilai `OPENCODE_MODEL_*` dari `.env`

## Cara pakai

Kalau kamu mengubah `OPENCODE_MODEL_*`, jalankan:

```bash
npm run sync:agent-models
```

Untuk check-only:

```bash
npm run sync:agent-models:check
```

Atau gunakan refresh lengkap:

```bash
npm run post:update
```

## Model routing table

| Env var | Default / recommended model | Used by / capability | Cost guidance |
|---|---|---|---|
| `OPENCODE_MODEL_DEFAULT` | `9router/low` | Top-level default model and general fallback | Keep the baseline lane low-cost for broad default routing. |
| `OPENCODE_MODEL_ORCHESTRATOR` | `9router/medium` | `@orchestrator` primary routing/integration | Use a balanced lane for delegation, coordination, and synthesis. |
| `OPENCODE_MODEL_PLANNER` | `9router/high` | `@artifact-planner`, `modes/plan.md`, `agents-disabled/plan.md` | Keep planning on the strongest lane for higher-accuracy specs and execution handoffs. |
| `OPENCODE_MODEL_DESIGN` | `9router/high` | `@designer` | Keep substantial UI/design reasoning, motion, and accessibility work on the high lane. |
| `OPENCODE_MODEL_VISUAL_ASSET` | `9router/medium` | `@visual-asset-generator` | Keep visual asset manifest prep and legal style-equivalent generation routing on medium while leaving designer on high. |
| `OPENCODE_MODEL_REVIEW` | `9router/medium` | `@oracle`, `@council` | Keep advisory/review reasoning on a balanced lane without degrading high-confidence review paths. |
| `OPENCODE_MODEL_QUALITY_GATE` | `9router/low` | `@quality-gate` | Final conformance gate stays cheap and explicit without forcing `@oracle`/`@council` down. |
| `OPENCODE_MODEL_ADVISORY` | `9router/medium` | `@architect` | Use a balanced lane for advisory and architecture guidance. |
| `OPENCODE_MODEL_EXECUTION` | `9router/low` | `@fixer` | Keep bounded implementation and testing on lower-cost lane. |
| `OPENCODE_MODEL_DISCOVERY` | `9router/low` | `@explorer` | Local discovery and read-only pattern analysis stay on the cheaper lane. |
| `OPENCODE_MODEL_DOCUMENTS` | `9router/low` | Reserved compatibility lane (document-centric work now routes via `@librarian`) | Keep for env compatibility on the cheaper lane. |
| `OPENCODE_MODEL_IMPROVEMENT` | `9router/fast` | Compatibility alias (agent mapping now uses `OPENCODE_MODEL_FAST`) | Kept for env compatibility; recommended default aligned to fast. |
| `OPENCODE_MODEL_FAST` | `9router/fast` | `@librarian`, `@skill-improver` | Docs/API lookup, summarization, and bounded prompt refinements are latency-sensitive and low-risk; use the fast lane. |

## Fast vs low

- `fast` (`9router/fast`) — latency-optimised, backed by `cx/gpt-5.4-mini` and `kr/claude-haiku-4.5`. Best for high-volume, low-risk, lookup-heavy work: docs research, API summarisation, and bounded post-task prompt refinements.
- `low` (`9router/low`) — cheaper baseline. Best for local pattern/reuse discovery where reasoning depth matters more than latency (`@explorer`).

## Hubungan dengan OpenChamber

`npm run post:update` akan:

1. sync model agent dari `.env`
2. sync OpenChamber
3. menjalankan `doctor`
