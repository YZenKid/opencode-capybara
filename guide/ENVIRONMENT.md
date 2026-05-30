# Environment

## Apa itu 9Router di repo ini?

Di repo ini, **9Router** adalah gateway AI/web/image utama yang dipakai OpenCode untuk menjalankan agent-agent lokal.

Variabel utamanya:

- `NINEROUTER_URL` → base URL endpoint 9Router
- `NINEROUTER_KEY` → API key untuk autentikasi ke 9Router

Variabel ini dipakai oleh:

- `opencode.json` untuk provider model utama OpenCode
- MCP `9router` untuk web search, web fetch, image generation, dan image asset generation

Kalau dua nilai ini salah atau kosong, agent bisa gagal memanggil model atau tool 9Router meskipun konfigurasi lain terlihat benar.

## Minimal env dari `.env.example`

```bash
NINEROUTER_URL="http://localhost:20128"
NINEROUTER_KEY="your_9router_api_key"
NINEROUTER_SEARCH_MODEL="search-combo"
NINEROUTER_FETCH_MODEL="fetch-combo"
NINEROUTER_IMAGE_MODEL="gemini/gemini-3-pro-image-preview"
NINEROUTER_IMAGE_DEFAULT_SIZE="1024x1024"
NINEROUTER_IMAGE_DEFAULT_QUALITY="medium"
NINEROUTER_IMAGE_DEFAULT_BACKGROUND="auto"
NINEROUTER_IMAGE_MAX_BYTES="25000000"
CONTEXT7_API_KEY="your_context7_api_key"
GITHUB_PERSONAL_ACCESS_TOKEN="your_github_pat"
GITHUB_TOOLSETS="context,repos,issues,pull_requests,actions,code_security"
OPENCODE_MODEL_DEFAULT="9router/low"
OPENCODE_MODEL_ORCHESTRATOR="9router/medium"
OPENCODE_MODEL_PLANNER="9router/high"
OPENCODE_MODEL_DESIGN="9router/high"
OPENCODE_MODEL_VISUAL_ASSET="9router/medium"
OPENCODE_MODEL_REVIEW="9router/medium"
OPENCODE_MODEL_QUALITY_GATE="9router/low"
OPENCODE_MODEL_ADVISORY="9router/medium"
OPENCODE_MODEL_EXECUTION="9router/low"
OPENCODE_MODEL_DISCOVERY="9router/low"
OPENCODE_MODEL_DOCUMENTS="9router/low"
OPENCODE_MODEL_IMPROVEMENT="9router/fast"
OPENCODE_MODEL_FAST="9router/fast"
```

Copy `.env.example` to `.env` and set every `OPENCODE_MODEL_*` value before launching OpenCode. Missing env vars resolve to an empty string, which can break OpenCode model routing.

Agent frontmatter still keeps literal `model:` values. `scripts/sync-agent-models.mjs` is source that syncs those literals from `.env`, so after changing `OPENCODE_MODEL_*` you should run:

```bash
npm run sync:agent-models
```

Current routing notes:

- `OPENCODE_MODEL_DESIGN` now drives `@designer` and recommended default is `9router/high`.
- `OPENCODE_MODEL_VISUAL_ASSET` now drives `@visual-asset-generator` and recommended default is `9router/medium`.
- `OPENCODE_MODEL_REVIEW` now stays scoped to `@oracle` and `@council`.
- `OPENCODE_MODEL_QUALITY_GATE` now drives `@quality-gate` and recommended default is `9router/low`.
- `OPENCODE_MODEL_EXECUTION` now drives `@fixer` and recommended default is `9router/low`.
- `OPENCODE_MODEL_DISCOVERY` now only drives `@explorer`.
- `OPENCODE_MODEL_FAST` now drives `@librarian` and `@skill-improver`.
- `OPENCODE_MODEL_IMPROVEMENT` remains as compatibility alias and recommended default is also `9router/fast`.

## Wajib vs opsional

### Wajib

- `NINEROUTER_URL`
- `NINEROUTER_KEY`
- `OPENCODE_MODEL_*`

### Biasanya diperlukan tergantung tool

- `CONTEXT7_API_KEY`
- `GITHUB_PERSONAL_ACCESS_TOKEN`
- `GITHUB_TOOLSETS`

### 9Router tool defaults

- `NINEROUTER_SEARCH_MODEL`
- `NINEROUTER_FETCH_MODEL`
- `NINEROUTER_IMAGE_MODEL`
- `NINEROUTER_IMAGE_DEFAULT_SIZE`
- `NINEROUTER_IMAGE_DEFAULT_QUALITY`
- `NINEROUTER_IMAGE_DEFAULT_BACKGROUND`
- `NINEROUTER_IMAGE_MAX_BYTES`
