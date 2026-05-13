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
| `OPENCODE_MODEL_DEFAULT` | `cliproxyapi/gpt-5.3-codex` | Top-level default model and general fallback | Use Codex lane as balanced default for coding-heavy work while keeping specialist high-risk lanes stronger. |
| `OPENCODE_MODEL_ORCHESTRATOR` | `cliproxyapi/gpt-5.4` | `@orchestrator` primary routing/integration | Keep high quality for delegation, coordination, and final synthesis. |
| `OPENCODE_MODEL_PLANNER` | `cliproxyapi/gpt-5.3-codex` | `@artifact-planner`, `modes/plan.md`, `agents-disabled/plan.md` | Planning is codebase-heavy and can use Codex to reduce cost while keeping structure strong. |
| `OPENCODE_MODEL_DESIGN` | `cliproxyapi/gpt-5.4` | `@designer` | UI and visual reasoning are higher-value, so keep quality high. |
| `OPENCODE_MODEL_REVIEW` | `cliproxyapi/gpt-5.4` | `@oracle`, `@quality-gate`, `@council` | Review lanes should stay strict and high quality; optimize for correctness over cost. |
| `OPENCODE_MODEL_ADVISORY` | `cliproxyapi/gpt-5.4` | `@architect` | Advisory work is often high-stakes; keep the stronger model unless cost pressure is extreme. |
| `OPENCODE_MODEL_EXECUTION` | `cliproxyapi/gpt-5.3-codex` | `@fixer` | Use Codex for bounded implementation/testing because this lane is code-edit heavy. |
| `OPENCODE_MODEL_DISCOVERY` | `cliproxyapi/gpt-5.4-mini` | `@explorer`, `@librarian` | Discovery and read-only analysis can usually use the lower-cost model. |
| `OPENCODE_MODEL_DOCUMENTS` | `cliproxyapi/gpt-5.4-mini` | Reserved compatibility lane (document-centric work now routes via `@librarian`) | Keep for env compatibility; active document support is merged into librarian. |
| `OPENCODE_MODEL_IMPROVEMENT` | `cliproxyapi/gpt-5.4-mini` | `@skill-improver` | Small prompt/skill refinements should stay on the cheaper lane. |

## Hubungan dengan OpenChamber

`npm run post:update` akan:

1. sync model agent dari `.env`
2. sync OpenChamber
3. menjalankan `doctor`
