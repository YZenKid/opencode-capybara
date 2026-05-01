# OpenCode + oh-my-opencode-slim Preset

Preset konfigurasi OpenCode personal dengan plugin `oh-my-opencode-slim`, multi-agent workflow, skill anti-AI-slop, dan MCP untuk grounding lewat dokumentasi, kode nyata, browser validation, UI registry, security scan, serta GitHub context.

## Isi Preset

- `opencode.json` — konfigurasi provider, model, MCP, plugin, agent bawaan yang dinonaktifkan, dan override eksplisit `council` sebagai subagent.
- `oh-my-opencode-slim.json` — mapping model, skill, MCP, dan council preset untuk agent `oh-my-opencode-slim`, termasuk `disabled_agents` agar council bawaan plugin tidak digenerasi.
- `.env.example` — template environment variable tanpa secret.
- `.gitignore` — melindungi `.env` dan file lokal/generated.
- `skills/` dan `.agents/skills/` — skill tambahan untuk OpenCode/agent.
- `scripts/prompt-gate-regression.mjs` — regression check untuk prompt/agent gates, path portability, dan boundary planner.

## Verifikasi Konfigurasi

Jalankan regression check setelah mengubah `AGENTS.md`, `agents/`, `skills/`, `opencode.json`, atau script gate:

```bash
npm run test:prompt-gates
```

Script ini memvalidasi:

- anti-AI-slop UI gates,
- image-heavy/reference UI asset generation gates,
- motion/icon/visual-density gates,
- portability/path rules,
- agent architecture rules: primary agents via `mode: primary`, subagents via `mode: subagent`, `disable: true`, dan `hidden: true` untuk autocomplete bila didukung,
- current architecture summary: plugin `oh-my-opencode-slim` hardcodes council menjadi `mode: all` setelah override; fix-nya adalah mematikan council bawaan lewat `disabled_agents` dan memakai `agents/council.md` sebagai subagent lokal sehingga council tidak muncul di primary agent switcher; built-in `build` dan `plan` dimatikan/di-hide sejauh didukung,
- MCP `image-asset-generator` tidak memakai path relatif rapuh,
- `artifact-planner` dapat memanggil subagent informasi/read-only/research/dokumentasi yang diizinkan: `explorer`, `librarian`, `oracle`, `council`, `observer`, `document-specialist`,
- `artifact-planner` tidak bisa memanggil subagent implementasi/source-edit/generation seperti `fixer`, `build`, `designer`, atau `visual-asset-generator`,
- `artifact-planner` tetap bisa menulis artefak `.opencode/plans`, `.opencode/draft`, dan `.opencode/evidence`.

Expected:

```text
Prompt gate regression passed.
```

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

## Portability dan Path Policy

Preset ini tidak boleh bergantung pada path device-specific seperti `/home/<user>` atau `/Users/<user>` di active agent/config/script. Gunakan:

- path relatif project/workspace untuk rencana dan dokumentasi,
- `{env:HOME}` untuk config-level path di `opencode.json` atau permission rules,
- absolute path yang diturunkan dari active workspace/project root hanya saat tool memang membutuhkannya.

Bedakan dua root berikut:

- **OpenCode config root**: lokasi preset ini, biasanya `$HOME/.config/opencode`.
- **Target app/project root**: aplikasi yang sedang dikerjakan agent.

Untuk image asset jobs:

- `project_root` harus menunjuk ke target app/project root, bukan config root OpenCode.
- `target_path` harus relatif terhadap `project_root`.
- Jangan hardcode absolute output path di manifest asset.

Regression check akan fail jika active prompt/config/script mengandung concrete `/home/ujang`, `/Users/ujang`, atau MCP image lama `./bin/image-asset-mcp.mjs`.

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

## TDD Workflow

Preset ini menerapkan Test-Driven Development untuk coding task yang mengubah behavior production code.

Siklus wajib:

- Red: tulis failing test dulu untuk behavior yang diinginkan.
- Green: implementasi perubahan terkecil agar test pass.
- Refactor: bersihkan struktur/readability setelah test green.
- Ulangi dalam behavior slice kecil, bukan feature drop besar.

TDD mandatory untuk:

- production logic
- bug fix
- API behavior
- service/use-case behavior
- UI interaction behavior
- validation logic
- security-sensitive logic

TDD tidak wajib untuk:

- docs-only changes
- prompt-only changes
- config-only changes
- `.gitignore`
- command documentation
- pure formatting

Untuk bug fix, agent harus mulai dari regression test yang gagal dan mereproduksi bug. Jika test tidak bisa ditulis atau dijalankan karena tooling, environment, dependency, atau requirement belum jelas, agent harus berhenti dan menjelaskan blocker sebelum mengubah production logic.

Gunakan command khusus untuk task TDD:

```text
/tdd <task description>
```

Contoh:

```text
/tdd fix validation so empty email is rejected
```

Ringkasan task coding harus memakai istilah:

- Red: test yang ditambahkan/diubah
- Green: production code yang diubah
- Refactor: cleanup yang dilakukan
- Verification: test/check yang dijalankan

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

## Agent Mapping dan Boundary

Menurut dokumentasi OpenCode:

- `mode: primary` membuat agent bisa dipilih langsung dengan Tab/switch-agent.
- `mode: subagent` membuat agent hanya dipakai sebagai child/specialist agent.
- `disable: true` menonaktifkan agent, termasuk built-in agent.
- `hidden: true` menyembunyikan subagent dari `@` autocomplete, tetapi agent masih bisa dipanggil programmatically jika permission mengizinkan.
- `default_agent` harus menunjuk ke primary agent.

Arsitektur preset saat ini:

- Primary/selectable agents hanya `orchestrator` dan `artifact-planner`.
- `default_agent` adalah `orchestrator`.
- Built-in `build` dan `plan` dinonaktifkan di `opencode.json`.
- Built-in `general` dan `explore` juga dinonaktifkan.
- `build` custom masih ada sebagai hidden subagent untuk bounded implementation jika benar-benar diroute oleh orchestrator.
- `council` adalah subagent untuk multi-model consensus, bukan primary agent.

Preset `oh-my-opencode-slim` memakai agent/subagent berikut:

| Agent | Fungsi | Skill/MCP Penting |
|---|---|---|
| `orchestrator` | Koordinasi, routing, verifikasi | Semua skill, semua MCP kecuali `context7` |
| `explorer` | Search/read-only codebase exploration | `semgrep`, `grep_app` |
| `librarian` | Dokumentasi dan library research | `context7`, `grep_app`, `github`, `brave-search`, `find-skills` |
| `oracle` | Architecture/review/simplification | `simplify`, React best practices, design review, `semgrep`, `playwright` |
| `designer` | UI/UX implementation/review | `frontend-design`, `frontend-design-review`, `web-design-guidelines`, `playwright`, `shadcn` |
| `artifact-planner` | Artifact-writing SDD/TDD planner | Hanya plan/draft/evidence `.opencode`; tidak boleh spawn subagent atau edit source |
| `visual-asset-generator` | Image-heavy UI asset generation | Chat-capable model + MCP `image-asset-generator`; no layout implementation |
| `fixer` | Bounded implementation/testing | `playwright`, `semgrep`, `shadcn`, `github` |
| `council` | Multi-model consensus | `github`, `grep_app` |

Tujuannya bukan memberi semua tool ke semua agent, tapi memberi tool yang relevan agar output lebih grounded dan tidak AI slop.

### Boundary `artifact-planner`

`artifact-planner` adalah agent untuk membuat artefak rencana, bukan implementasi. Boundary saat ini:

- `task` default deny (`"*": deny`) dengan allowlist subagent informasi/read-only/research/dokumentasi: `explorer`, `librarian`, `oracle`, `council`, `observer`, dan `document-specialist`.
- Subagent implementasi/source-edit/generation seperti `fixer`, `build`, `designer`, dan `visual-asset-generator` tetap dilarang.
- `bash: deny` — tidak boleh menjalankan command implementasi.
- `apply_patch: deny` — tidak boleh patch source/config.
- `edit` dan `write` hanya scoped ke:
  - `.opencode/plans/`
  - `.opencode/draft/`
  - `.opencode/evidence/`

Jadi planner tetap bisa membuat folder/file plan, draft, dan evidence di `.opencode/`, tetapi tidak bisa mengubah app source, package files, assets, tests, atau memulai implementasi lewat subagent.

## Visual Asset Generation Pipeline

Untuk pekerjaan UI yang image-heavy seperti portfolio, landing page, reference replication, hero portrait, icon badge set, project/product mockup, testimonial avatar, blog/news thumbnail, atau background texture, gunakan pipeline berikut:

1. Untuk portfolio/reference/template work dengan hero art, portrait, project cards, thumbnail, testimonial/avatar cluster, blog cards, icon badges, atau rich background, anggap image-heavy sampai `designer` membuktikan sebaliknya.
2. `planner`/`designer` harus membuat **Image Generation Decision** per section:
   - `generate`
   - `use-provided-assets`
   - `licensed-existing-assets`
   - `no-generation-needed`
3. Jika reference punya imagery bermakna dan tidak ada asset user/licensed, default yang benar adalah **generate legal style-equivalent assets**, bukan CSS-only placeholder, generic gradient, blank frame, atau omit imagery.
4. Jika image `required`, `designer` harus membuat **asset manifest** terlebih dulu, bukan langsung final dengan placeholder CSS/SVG. Manifest minimal berisi:
   - `id`
   - `type`
   - `priority` (`required`/`optional`)
   - `target_path`
   - `dimensions` atau `aspect_ratio`
   - `prompt`
   - `negative_prompt` jika perlu
   - `alt`
   - image generation decision
   - placement notes
   - legal notes
5. `orchestrator` melakukan capability gate:
   - preset ini menyediakan custom subagent `visual-asset-generator` sebagai titik konfigurasi image generation,
   - jika runtime/tool aktif mengekspos image generation, orchestrator menjalankan generation melalui `visual-asset-generator` atau workflow/tool image yang tersedia,
   - jika `visual-asset-generator` belum muncul di active subagent/tool list setelah restart OpenCode, anggap unavailable meskipun sudah ada di config,
   - jika runtime tidak mengekspos image generation, jangan panggil subagent image dan jangan klaim visual parity; tanyakan apakah user mau menyediakan asset, berhenti di manifest, atau lanjut dengan placeholder sementara.
6. Setelah asset generated/provided tersedia, integrasi dilakukan oleh `designer` atau `fixer`:
   - simpan di asset directory project,
   - gunakan `<img>`/framework image component,
   - set explicit `width`/`height`,
   - gunakan `alt` bermakna untuk content image dan `alt=""`/`aria-hidden` untuk dekoratif,
   - hero above-fold memakai loading priority yang sesuai; below-fold memakai lazy loading.
7. Validasi wajib:
    - run lint/build/checks,
    - capture viewport yang sama dengan referensi,
    - bandingkan image density, crop, colorfulness, shadow, placement, responsive behavior, dan legal limitations.

#### Professional art direction gate

Sebelum membuat asset manifest untuk image-heavy work, `designer` harus menyusun art direction brief atau style board agar hasil generasi tidak terlihat seperti generic AI slop. Brief tersebut harus menetapkan visual thesis, reference traits yang dijaga, composition notes, subject/props/environment, medium/style constraints, palette dan lighting, camera/crop/perspective, texture/material detail, negative style constraints, brand/domain specificity, serta acceptance/rejection criteria.

Gate ini menolak prompt yang terlalu generik seperti "modern tech dashboard", "futuristic", "cyberpunk", atau "abstract UI" tanpa objek, komposisi, dan makna domain yang jelas. Ia juga menolak glossy cyberpunk dashboards, random neon blobs, floating UI cards tanpa domain meaning, cloned reference assets, fake logos/text, uncanny portraits/hands, inconsistent style sets, over-saturated stock-ish art, dan same-looking thumbnails.

Rule penting: CSS/SVG placeholder boleh dipakai sebagai scaffolding sementara, tetapi bukan final untuk image-heavy visual parity kecuali user eksplisit menerima vector-only/placeholder output atau reference memang geometrik/vector. Jika asset generation unavailable dan user tidak menyetujui placeholder, status harus `blocked` atau `draft`.

### Konfigurasi `visual-asset-generator`

Subagent khusus image didefinisikan di:

```text
agents/visual-asset-generator.md
```

Model aktualnya dikonfigurasi terpusat di:

```text
oh-my-opencode-slim.json
```

Contoh entry:

```json
"visual-asset-generator": {
  "model": "<provider/image-generation-model>",
  "skills": [],
  "mcps": []
}
```

Jika provider/model image berubah, update hanya entry config tersebut. Prompt/rules tidak perlu menyebut nama model spesifik. Setelah mengubah agent config, restart OpenCode lalu verifikasi agent/subagent tersedia. Jika belum tersedia, gunakan fallback orchestrator image tool atau manifest-only flow.

### MCP `image-asset-generator`

Actual image generation untuk subagent dilakukan lewat MCP lokal:

```text
bin/image-asset-mcp.mjs
```

MCP ini terdaftar di `opencode.json` sebagai:

```json
"image-asset-generator": {
  "type": "local",
  "command": ["node", "{env:HOME}/.config/opencode/bin/image-asset-mcp.mjs"],
  "environment": {
    "IMAGE_ASSET_BASE_URL": "{env:CLIPROXYAPI_BASE_URL}",
    "IMAGE_ASSET_API_KEY": "{env:CLIPROXYAPI_API_KEY}",
    "IMAGE_ASSET_MODEL": "{env:IMAGE_ASSET_MODEL}"
  }
}
```

Gunakan path `{env:HOME}/.config/opencode/bin/image-asset-mcp.mjs`, bukan `./bin/image-asset-mcp.mjs`, agar MCP tetap bisa dibuka saat OpenCode dijalankan dari target project/folder lain.

`visual-asset-generator` tetap memakai chat-capable model untuk planning, tetapi diberi MCP `image-asset-generator` agar bisa memanggil tool:

```text
generate_image_asset
generate_image_assets_batch
```

Set `IMAGE_ASSET_MODEL` ke model image endpoint yang aktif di provider. Jika kosong, wrapper mencoba default `gpt-image-2`. Model image tidak boleh dijadikan model chat subagent; ia hanya dipakai oleh MCP wrapper untuk endpoint image generation.

Untuk asset yang perlu alpha channel seperti portrait cutout, floating icon badge, decorative overlay, atau avatar mark, request:

```json
{
  "format": "png",
  "output_format": "png",
  "background": "transparent"
}
```

`background: "transparent"` hanya valid untuk format yang mendukung alpha seperti PNG/WebP. Jangan gunakan untuk JPEG/JPG.

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

Default config memakai **Remote GitHub MCP** sehingga tidak perlu Docker:

```json
"github": {
  "type": "remote",
  "url": "https://api.githubcopilot.com/mcp/",
  "headers": {
    "Authorization": "Bearer {env:GITHUB_PERSONAL_ACCESS_TOKEN}",
    "X-MCP-Toolsets": "{env:GITHUB_TOOLSETS}"
  },
  "oauth": false
}
```

Jika remote MCP tidak bisa dipakai oleh runtime, fallback ke Docker/local server dan cek Docker:

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
