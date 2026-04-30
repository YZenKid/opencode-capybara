# OpenCode + oh-my-opencode-slim Preset

Preset konfigurasi OpenCode personal dengan plugin `oh-my-opencode-slim`, multi-agent workflow, skill anti-AI-slop, dan MCP untuk grounding lewat dokumentasi, kode nyata, browser validation, UI registry, security scan, serta GitHub context.

## Isi Preset

- `opencode.json` — konfigurasi provider, model, MCP, plugin, dan agent bawaan yang dinonaktifkan.
- `oh-my-opencode-slim.json` — mapping model, skill, MCP, dan council preset untuk agent `oh-my-opencode-slim`.
- `.env.example` — template environment variable tanpa secret.
- `.gitignore` — melindungi `.env` dan file lokal/generated.
- `skills/` dan `.agents/skills/` — skill tambahan untuk OpenCode/agent.

## Prasyarat

Install tools berikut:

- Node.js + npm
- OpenCode CLI
- Docker, untuk GitHub MCP official server
- `uv`/`uvx`, untuk MCP berbasis Python seperti `semgrep` dan `time`

Cek cepat:

```bash
node --version
npm --version
opencode --version
docker --version
uvx --version
```

## Clone / Pasang Preset

Backup config lama lebih dulu jika ada:

```bash
mv ~/.config/opencode ~/.config/opencode.backup.$(date +%Y%m%d-%H%M%S)
```

Clone repo preset ini ke lokasi config OpenCode:

```bash
git clone <REPO_URL> ~/.config/opencode
cd ~/.config/opencode
```

Install dependency plugin:

```bash
npm install
```

Jika kamu tidak memakai npm install karena `package.json` sengaja tidak di-track, install paket minimal:

```bash
npm install @opencode-ai/plugin@1.4.10 oh-my-opencode-slim@^1.0.3
```

## Setup Environment Variable

Buat `.env` dari contoh:

```bash
cp .env.example .env
```

Isi nilai berikut di `.env`:

```bash
CLIPROXYAPI_BASE_URL="https://your-openai-compatible-endpoint/v1"
CLIPROXYAPI_API_KEY="your_cliproxyapi_api_key"
BRAVE_API_KEY="your_brave_search_api_key"
CONTEXT7_API_KEY="your_context7_api_key"
GITHUB_PERSONAL_ACCESS_TOKEN="your_github_pat"
GITHUB_TOOLSETS="context,repos,issues,pull_requests,actions,code_security"
```

Jangan commit `.env`. File ini sudah di-ignore.

Load env sebelum menjalankan OpenCode:

```bash
set -a
source ~/.config/opencode/.env
set +a
opencode
```

Untuk membuat env otomatis tersedia di shell baru, tambahkan ke `~/.zshrc`:

```bash
cat >> ~/.zshrc <<'EOF'

# OpenCode preset env
if [ -f "$HOME/.config/opencode/.env" ]; then
  set -a
  source "$HOME/.config/opencode/.env"
  set +a
fi
EOF
```

Lalu reload:

```bash
source ~/.zshrc
```

## Setup OpenChamber

Jika OpenCode dibuka lewat OpenChamber, `.env` OpenCode tidak otomatis terbaca saat OpenChamber dijalankan dari Dock/app launcher. Gunakan wrapper agar OpenChamber selalu menjalankan OpenCode dengan env yang benar.

Buat wrapper:

```bash
mkdir -p ~/.config/opencode/bin
cat > ~/.config/opencode/bin/opencode-with-env <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${OPENCODE_ENV_FILE:-$HOME/.config/opencode/.env}"

if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

exec opencode "$@"
EOF
chmod +x ~/.config/opencode/bin/opencode-with-env
```

Set OpenChamber agar memakai wrapper ini sebagai binary OpenCode:

```bash
launchctl setenv OPENCHAMBER_OPENCODE_PATH "$HOME/.config/opencode/bin/opencode-with-env"
```

Cek:

```bash
launchctl getenv OPENCHAMBER_OPENCODE_PATH
```

Expected:

```text
/Users/<username>/.config/opencode/bin/opencode-with-env
```

Setelah itu quit OpenChamber sepenuhnya lalu buka lagi.

Jika menjalankan OpenChamber dari terminal, kamu juga bisa pakai:

```bash
export OPENCHAMBER_OPENCODE_PATH="$HOME/.config/opencode/bin/opencode-with-env"
openchamber
```

Untuk membuat env OpenChamber permanen di shell:

```bash
cat >> ~/.zshrc <<'EOF'

# OpenChamber should launch OpenCode through the env wrapper
export OPENCHAMBER_OPENCODE_PATH="$HOME/.config/opencode/bin/opencode-with-env"
EOF
source ~/.zshrc
```

OpenChamber membaca `OPENCHAMBER_OPENCODE_PATH` dari environment prosesnya dan meneruskannya ke wrapper OpenCode. Wrapper ini akan source `~/.config/opencode/.env`, sehingga MCP seperti `brave-search`, `context7`, dan `github` mendapat token yang dibutuhkan.

## Cara Mendapatkan Token

### 1. CliProxyAPI / OpenAI-Compatible Provider

Preset ini memakai provider custom `cliproxyapi` di `opencode.json`:

```json
"model": "cliproxyapi/gpt-5.5"
```

Kamu perlu endpoint dan API key OpenAI-compatible:

- `CLIPROXYAPI_BASE_URL` — URL endpoint API, biasanya berakhir dengan `/v1`.
- `CLIPROXYAPI_API_KEY` — API key provider tersebut.

Masukkan keduanya ke `.env`.

### 2. Brave Search API Key

Dipakai oleh MCP `brave-search` untuk web search.

Langkah:

1. Buka `https://brave.com/search/api/`.
2. Buat akun / login.
3. Buat API key untuk Brave Search API.
4. Isi ke `.env`:

```bash
BRAVE_API_KEY="your_brave_search_api_key"
```

### 3. Context7 API Key

Dipakai oleh MCP `context7` untuk dokumentasi library yang up-to-date.

Langkah:

1. Buka `https://context7.com/`.
2. Login / buat akun.
3. Ambil API key dari dashboard/account settings.
4. Isi ke `.env`:

```bash
CONTEXT7_API_KEY="your_context7_api_key"
```

### 4. GitHub Personal Access Token

Dipakai oleh GitHub MCP official server untuk repo, issues, pull requests, actions, dan code security context.

Buat token di:

```text
https://github.com/settings/personal-access-tokens/new
```

Rekomendasi: gunakan **Fine-grained personal access token**.

Setelan aman:

- Token name: `opencode-mcp`
- Expiration: 30/60/90 hari
- Repository access: pilih repository tertentu jika memungkinkan

Permission minimum read-only:

- Contents: `Read-only`
- Issues: `Read-only`
- Pull requests: `Read-only`
- Actions: `Read-only`
- Metadata: otomatis required

Jika ingin agent bisa membuat/mengubah issue atau PR:

- Issues: `Read and write`
- Pull requests: `Read and write`

Jika ingin code security context:

- Code scanning alerts: `Read-only`, jika tersedia

Isi ke `.env`:

```bash
GITHUB_PERSONAL_ACCESS_TOKEN="your_github_personal_access_token"
```

Jangan paste token ke chat atau commit ke repo.

## Install / Update Skills

Skill utama yang direkomendasikan untuk preset ini:

```bash
npx -y skills add https://github.com/anthropics/skills --skill frontend-design -y
npx -y skills add https://github.com/microsoft/agent-skills --skill frontend-design-review -y
npx -y skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices -y
npx -y skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines -y
npx -y skills add https://github.com/vercel-labs/skills --skill find-skills -y
npx -y skills add https://github.com/getsentry/skills --skill agents-md -y
npx -y skills add https://github.com/devinschumacher/skills --skill playwright -y
```

Cek skill:

```bash
npx -y skills list
```

Update skill yang punya metadata update:

```bash
npx -y skills update -p -y
```

Catatan: beberapa skill lokal mungkin tidak punya metadata update yang dikenali CLI. Untuk skill seperti `web-design-guidelines`, reinstall eksplisit dari sumber resmi jika perlu.

## MCP Yang Digunakan

MCP global di preset:

- `time` — waktu/timezone utility.
- `brave-search` — web search.
- `context7` — dokumentasi library/framework terbaru.
- `grep_app` — search contoh kode nyata dari GitHub via Grep.app.
- `playwright` — browser automation/validation.
- `shadcn` — shadcn/ui registry dan component context.
- `semgrep` — static/security analysis.
- `github` — repository, issues, PR, actions, dan code security context.

Cek status MCP:

```bash
set -a
source ~/.config/opencode/.env
set +a
opencode mcp list
```

Expected setelah semua token valid:

```text
✓ time
✓ brave-search
✓ context7
✓ grep_app
✓ playwright
✓ shadcn
✓ semgrep
✓ github
```

Jika `github` gagal, biasanya `GITHUB_PERSONAL_ACCESS_TOKEN` belum diisi atau Docker belum berjalan.

## Agent Mapping

Preset `oh-my-opencode-slim` memakai agent berikut:

| Agent | Fungsi | Skill/MCP Penting |
|---|---|---|
| `orchestrator` | Koordinasi, routing, verifikasi | Semua skill, semua MCP kecuali `context7` |
| `explorer` | Search/read-only codebase exploration | `semgrep`, `grep_app` |
| `librarian` | Dokumentasi dan library research | `context7`, `grep_app`, `github`, `brave-search`, `find-skills` |
| `oracle` | Architecture/review/simplification | `simplify`, React best practices, design review, `semgrep`, `playwright` |
| `designer` | UI/UX implementation/review | `frontend-design`, `frontend-design-review`, `web-design-guidelines`, `playwright`, `shadcn` |
| `fixer` | Bounded implementation/testing | `playwright`, `semgrep`, `shadcn`, `github` |
| `council` | Multi-model consensus | `github`, `grep_app` |

Tujuannya bukan memberi semua tool ke semua agent, tapi memberi tool yang relevan agar output lebih grounded dan tidak AI slop.

## Verifikasi Agent

Jalankan OpenCode:

```bash
set -a
source ~/.config/opencode/.env
set +a
opencode
```

Di OpenCode, jalankan:

```text
ping all agents
```

Expected untuk agent utama:

```text
@explorer ✓
@librarian ✓
@oracle ✓
@designer ✓
@fixer ✓
```

Jika konfigurasi baru belum terbaca, restart OpenCode.

## Troubleshooting

### MCP GitHub gagal connect

Cek token:

```bash
test -n "$GITHUB_PERSONAL_ACCESS_TOKEN" && printf present || printf missing
```

Cek Docker:

```bash
docker --version
docker run --rm ghcr.io/github/github-mcp-server --help
```

Pastikan `.env` sudah diload sebelum `opencode mcp list` atau `opencode`.

### Context7 / Brave gagal

Pastikan API key valid dan `.env` sudah diload:

```bash
test -n "$CONTEXT7_API_KEY" && printf context7-present || printf context7-missing
test -n "$BRAVE_API_KEY" && printf brave-present || printf brave-missing
```

### Semgrep pertama kali lambat

`uvx semgrep mcp -t stdio` bisa butuh waktu saat pertama kali download package. Jalankan ulang `opencode mcp list` setelah selesai.

### OpenCode tidak otomatis membaca `.env`

Gunakan wrapper manual:

```bash
set -a
source ~/.config/opencode/.env
set +a
opencode
```

Atau simpan auto-load di `~/.zshrc` seperti bagian setup environment.

## Security Notes

- Jangan commit `.env`.
- Rotasi token secara berkala.
- Pakai fine-grained GitHub token dan batasi repository access.
- Jangan memberi write permission GitHub jika hanya butuh read-only context.
- Jika secret pernah ter-commit, anggap bocor dan revoke/regenerate token.
