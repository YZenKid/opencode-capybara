# Environment

## Apa itu CLIProxyAPI di repo ini?

Di repo ini, **CLIProxyAPI** adalah provider model utama yang dipakai OpenCode untuk menjalankan agent-agent lokal.

Variabel utamanya:

- `CLIPROXYAPI_BASE_URL` → base URL endpoint OpenAI-compatible
- `CLIPROXYAPI_API_KEY` → API key untuk autentikasi ke provider tersebut

Variabel ini dipakai oleh:

- `opencode.json` untuk provider model utama OpenCode
- MCP image asset generator sebagai fallback/default endpoint image generation

Kalau dua nilai ini salah atau kosong, agent bisa gagal memanggil model meskipun konfigurasi lain terlihat benar.

## Minimal env dari `.env.example`

```bash
CLIPROXYAPI_BASE_URL="https://your-openai-compatible-endpoint/v1"
CLIPROXYAPI_API_KEY="your_cliproxyapi_api_key"
BRAVE_API_KEY="your_brave_search_api_key"
CONTEXT7_API_KEY="your_context7_api_key"
GITHUB_PERSONAL_ACCESS_TOKEN="your_github_pat"
GITHUB_TOOLSETS="context,repos,issues,pull_requests,actions,code_security"
OPENCODE_MODEL_DEFAULT="cliproxyapi/gpt-5.3-codex"
OPENCODE_MODEL_ORCHESTRATOR="cliproxyapi/gpt-5.4"
OPENCODE_MODEL_PLANNER="cliproxyapi/gpt-5.3-codex"
OPENCODE_MODEL_DESIGN="cliproxyapi/gpt-5.4"
OPENCODE_MODEL_REVIEW="cliproxyapi/gpt-5.4"
OPENCODE_MODEL_ADVISORY="cliproxyapi/gpt-5.4"
OPENCODE_MODEL_EXECUTION="cliproxyapi/gpt-5.3-codex"
OPENCODE_MODEL_DISCOVERY="cliproxyapi/gpt-5.4-mini"
OPENCODE_MODEL_DOCUMENTS="cliproxyapi/gpt-5.4-mini"
OPENCODE_MODEL_IMPROVEMENT="cliproxyapi/gpt-5.4-mini"
IMAGE_ASSET_MODEL="gpt-image-2"
IMAGE_ASSET_DEFAULT_SIZE="1024x1024"
IMAGE_ASSET_DEFAULT_BACKGROUND="auto"
```

Copy `.env.example` to `.env` and set every `OPENCODE_MODEL_*` value before launching OpenCode. Missing env vars resolve to an empty string, which can break OpenCode model routing.

## Wajib vs opsional

### Wajib

- `CLIPROXYAPI_BASE_URL`
- `CLIPROXYAPI_API_KEY`
- `OPENCODE_MODEL_*`

### Biasanya diperlukan tergantung tool

- `BRAVE_API_KEY`
- `CONTEXT7_API_KEY`
- `GITHUB_PERSONAL_ACCESS_TOKEN`
- `GITHUB_TOOLSETS`

### Figma MCP (remote)

- `figma` MCP pada `opencode.json` memakai remote URL `https://mcp.figma.com/mcp`.
- Gunakan posture OAuth client/host (bukan API-key header custom) sesuai dukungan server/client resmi.
- Capability Figma MCP bisa berbeda tergantung support client, mode remote/desktop, dan seat/plan (misalnya write-to-canvas atau live UI sync).

### Image asset

- `IMAGE_ASSET_MODEL`
- `IMAGE_ASSET_DEFAULT_SIZE`
- `IMAGE_ASSET_DEFAULT_BACKGROUND`
