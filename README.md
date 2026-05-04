# opencode-capybara

<p align="center">
  <img src="assets/opencode-capybara-icon.png" alt="opencode-capybara capybara mascot icon" width="128" height="128" />
</p>

Standalone OpenCode multi-agent configuration yang tenang, terarah, dan safety-gated untuk coding, dokumentasi, UI, browser validation, security scan, GitHub context, dan visual asset workflow.

`opencode-capybara` adalah konfigurasi OpenCode standalone berbasis local Markdown agents, standalone `opencode-*` skills, prompt gates, dan MCP. Fokusnya bukan membuat satu agent serba bisa, tetapi mengoordinasikan specialist agents dengan boundary yang jelas, evidence yang dapat diverifikasi, dan commit policy yang aman.

## Kenapa capybara?

`opencode-capybara` memilih capybara sebagai simbol karena capybara adalah hewan yang tenang, sosial, adaptif, dan bisa berdampingan dengan banyak spesies. Itu menggambarkan tujuan project ini: menjadi lapisan orkestrasi OpenCode yang tidak agresif, tidak berisik, tetapi mampu mengoordinasikan banyak agent, skill, MCP, dan safety gate dengan stabil.

Filosofinya:

- **Calm orchestration** — capybara tenang; `@orchestrator` juga harus meredam chaos multi-tool/multi-agent, bukan menambah noise.
- **Coexistence** — capybara bisa hidup berdampingan dengan banyak hewan; project ini menyatukan agents, skills, MCP, docs, browser, security, GitHub, document tooling, dan image generation.
- **Social coordination** — capybara hidup berkelompok; cocok untuk multi-agent collaboration dengan role yang spesifik.
- **Low drama, high utility** — bukan mascot agresif; project ini mengutamakan safety gates, validation, prompt discipline, dan grounded execution.
- **Adaptability** — capybara semi-aquatic; analoginya, agent di sini adaptif di code, docs, browser, design, security, dan documents.

Capybara bukan simbol “cepat sendiri”; ia simbol “tenang bersama-sama sampai hasilnya benar”.

## Apa yang ada di dalamnya?

| Area | Isi |
|---|---|
| Core config | `opencode.json`, `tui.json`, `AGENTS.md` |
| Local agents | `agents/*.md` untuk primary/subagent routing standalone |
| Standalone skills | `skills/opencode-*/SKILL.md` sebagai workflow contract per agent |
| Slash commands | `commands/tdd.md`, `replicate-ui.md`, `revamp-like.md`, `commit-message.md` |
| Prompt gates | `scripts/prompt-gate-regression.mjs` |
| Local tooling package | `package.json` / `package-lock.json` untuk prompt gates dan MCP helpers |
| Visual asset tooling | `bin/image-asset-mcp.mjs` + MCP `image-asset-generator` |

## Quick start

```bash
git clone <REPO_URL> ~/.config/opencode
cd ~/.config/opencode
npm install
npm run test:prompt-gates
```

Buat environment file dari contoh, lalu isi token yang dibutuhkan:

```bash
cp .env.example .env
```

Jangan commit `.env`. File secrets sudah di-ignore.

Load env sebelum menjalankan OpenCode:

```bash
set -a
source ~/.config/opencode/.env
set +a
opencode
```

## Architecture overview

Project ini memakai pendekatan **standalone-first**:

1. OpenCode membaca config dan local Markdown agents dari repo ini.
2. `@orchestrator` menjadi default primary agent dan router/integrator utama.
3. Specialist subagents menangani discovery, docs, implementation, UI, architecture review, document processing, image assets, consensus, dan quality gate.
4. Prompt gates menjaga invariants agar config, docs, dan prompt tidak drift.
5. Quality gate menjadi review final untuk perubahan non-trivial, prompt/config changes, security-sensitive work, atau sebelum commit/PR.

Primary/selectable agents:

- `orchestrator` — default router/integrator.
- `artifact-planner` — pembuat artifact plan SDD/TDD; bukan implementer.

Retired/disabled:

- `build` — retired; build retired berarti implementation/testing baru diarahkan ke `@fixer`.
- `general` — retired/disabled; general retired berarti jangan diaktifkan tanpa use case dan model valid.
- built-in `plan` dan `explore` — disabled agar workflow tetap lewat local agents.

## Agent matrix

| Agent | Mode | Fungsi | Skill utama |
|---|---:|---|---|
| `@orchestrator` | primary | Router/integrator, delegation, validation, final summary | `opencode-orchestrator` |
| `@artifact-planner` | primary | Menulis plan/draft/evidence di `.opencode/` saja | `opencode-artifact-planner` |
| `@explorer` | subagent | Local codebase discovery, search, symbol map, reuse candidates | `opencode-explorer` |
| `@librarian` | subagent | Official docs/library/API research | `opencode-librarian` |
| `@oracle` | subagent | Architecture review, simplification, maintainability/risk review | `opencode-oracle` |
| `@fixer` | subagent | Bounded implementation, tests, fixtures, Red/Green/Refactor | `opencode-fixer` |
| `@designer` | subagent | UI/UX implementation/review, visual polish, Stitch-aware design gate | `opencode-designer` |
| `@visual-parity-auditor` | subagent | Read-only screenshot/section parity review | `opencode-visual-parity-auditor` |
| `@motion-specialist` | subagent | Read-only animation/motion/reduced-motion review | `opencode-motion-specialist` |
| `@accessibility-reviewer` | subagent | Read-only a11y review: keyboard, focus, labels, contrast, motion | `opencode-accessibility-reviewer` |
| `@ui-system-architect` | subagent | Read-only tokens/component anatomy/design-system review | `opencode-ui-system-architect` |
| `@visual-asset-generator` | subagent | Image-heavy asset manifest/generation jobs | `opencode-visual-asset-generator` |
| `@document-specialist` | subagent | PDF/spreadsheet/Office/document processing | `opencode-document-specialist` |
| `@council` | subagent | High-confidence consensus/advisory | `opencode-council` |
| `@quality-gate` | subagent | Final read-only conformance/risk gate | `opencode-quality-gate` |
| `@skill-improver` | subagent | Bounded post-task prompt/agent/skill refinement | `opencode-skill-improver` |

## Skill improvement dan quality status

`@skill-improver` dipakai untuk checkpoint kecil setelah pekerjaan non-trivial, repeated failures, policy gaps, atau explicit request. Ia tidak wajib untuk tugas trivial, tidak boleh membaca secret, tidak boleh melakukan no blind external updates, dan harus menghindari prompt bloat.

`@quality-gate` mengeluarkan status final deterministik:

- `PASS`
- `PASS_WITH_RISKS`
- `NEEDS_FIX`
- `BLOCKED`

Status `NEEDS_FIX` atau `BLOCKED` berarti commit/final claim harus ditahan sampai blocker selesai.

## Workflow gates

| Work type | Default route | Required validation |
|---|---|---|
| Unknown codebase discovery | `@explorer` | summarized file/symbol map |
| Library/API behavior | `@librarian` | official/current docs where possible |
| Implementation/tests | `@fixer` | Red → Green → Refactor evidence |
| Architecture/risk review | `@oracle` | trade-off/risk summary |
| UI/reference work | `@designer` + UI specialists | screenshots/evidence when runnable |
| Image-heavy UI assets | `@designer` manifest → `@visual-asset-generator` | asset metadata + integration notes |
| Prompt/config/security-sensitive changes | orchestrator + `@quality-gate` | prompt gates + final quality status |
| Final non-trivial task signoff | `@quality-gate` | `PASS` or `PASS_WITH_RISKS` without blocker |

## Validation

Run prompt gates after changing `AGENTS.md`, `agents/`, `skills/`, `commands/`, `opencode.json`, README invariants, or gate scripts:

```bash
npm run test:prompt-gates
```

Expected:

```text
Prompt gate regression passed.
```

Prompt gates currently check, among other things:

- standalone project identity,
- local agent availability and boundaries,
- retired/disabled built-ins,
- quality-gate routing,
- auto-commit safety,
- anti-AI-slop UI policies,
- visual asset generation gates,
- portability/path rules,
- commit-message format.

## Auto-commit policy

Auto-commit default ON untuk local commits only; never push automatically.

- Hanya setelah task plan-bound non-trivial selesai, validation lulus, dan `@quality-gate` memberi `PASS` atau `PASS_WITH_RISKS` tanpa blocker.
- Review `git status`/`git diff`, lalu stage hanya file relevan.
- Commit message otomatis memakai subject singkat plus body bullet-point.
- Jangan stage `.env`, secrets, tokens, credentials, unrelated untracked files, atau generated/vendor files kecuali plan/user menyetujui.
- Jangan gunakan `--no-verify`, `--no-gpg-sign`, `amend`, force push, atau destructive git commands.
- Kalau scope atau staging meragukan, berhenti dan tanya.

## Environment variables

Isi `.env` dari `.env.example`:

```bash
CLIPROXYAPI_BASE_URL="https://your-openai-compatible-endpoint/v1"
CLIPROXYAPI_API_KEY="your_cliproxyapi_api_key"
BRAVE_API_KEY="your_brave_search_api_key"
CONTEXT7_API_KEY="your_context7_api_key"
GITHUB_PERSONAL_ACCESS_TOKEN="your_github_pat"
GITHUB_TOOLSETS="context,repos,issues,pull_requests,actions,code_security"
STITCH_API_KEY="your_stitch_api_key"
IMAGE_ASSET_MODEL="gpt-image-2"
```

Token guidance:

- Gunakan fine-grained GitHub token jika memungkinkan.
- Beri GitHub write permission hanya jika agent memang perlu membuat/mengubah issue/PR.
- Rotasi token secara berkala.
- Jangan paste token ke chat atau commit ke repo.

## MCP configuration

MCP global di `opencode.json`:

| MCP | Fungsi | Env penting |
|---|---|---|
| `time` | waktu/timezone utility | - |
| `brave-search` | web search | `BRAVE_API_KEY` |
| `context7` | docs/library context | `CONTEXT7_API_KEY` |
| `grep_app` | code search examples | - |
| `playwright` | browser automation/validation | - |
| `shadcn` | shadcn/ui registry context | - |
| `stitch` | Google Stitch design-system/screen workflows | `STITCH_API_KEY` |
| `semgrep` | static/security analysis | - |
| `github` | repo/issues/PR/actions/security context | `GITHUB_PERSONAL_ACCESS_TOKEN`, `GITHUB_TOOLSETS` |
| `image-asset-generator` | local image asset generation wrapper | `CLIPROXYAPI_BASE_URL`, `CLIPROXYAPI_API_KEY`, `IMAGE_ASSET_MODEL` |

Cek status MCP:

```bash
set -a
source ~/.config/opencode/.env
set +a
opencode mcp list
```

Expected setelah token valid:

```text
✓ time
✓ brave-search
✓ context7
✓ grep_app
✓ playwright
✓ shadcn
✓ stitch
✓ semgrep
✓ github
```

## TDD workflow

Untuk coding task yang mengubah behavior production code, gunakan Red → Green → Refactor.

- **Red**: tulis failing test/regression evidence dulu.
- **Green**: implementasi perubahan terkecil agar test pass.
- **Refactor**: bersihkan struktur/readability setelah green.
- **Verification**: jalankan test/check relevan dan laporkan hasilnya.

TDD mandatory untuk production logic, bug fix, API behavior, service/use-case behavior, UI interaction behavior, validation logic, dan security-sensitive logic.

TDD tidak wajib untuk docs-only, prompt-only, config-only, `.gitignore`, command documentation, atau pure formatting; namun validation/prompt gate tetap wajib jika relevan.

Gunakan command:

```text
/tdd <task description>
```

## UI, reference, dan visual asset pipeline

Untuk website/frontend/mobile/dashboard/form/reference work:

1. Route ke `@designer` kecuali change tiny dan non-visual.
2. Hindari generic UI: no bland centered cards, random emoji icons, blank image frames, numeric-only service icons, atau placeholder final.
3. Untuk reference/replication, capture reference/current/final evidence dengan wait → stabilize → scroll → settle → screenshot.
4. Untuk substantial UI/reference work, butuh motion storyboard, icon strategy, asset manifest, image generation decision, dan final designer pass/fail review.
5. Untuk image-heavy UI, generate legal style-equivalent assets jika original/provided/licensed asset tidak tersedia.

### Image asset generation

Subagent image didefinisikan di:

```text
agents/visual-asset-generator.md
```

MCP lokal terdaftar sebagai:

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

Gunakan `{env:HOME}` untuk config-level MCP path. Untuk asset jobs, `project_root` harus menunjuk target app/project root dan `target_path` harus relatif terhadap root tersebut.

## OpenChamber setup

Jika OpenCode dibuka lewat OpenChamber dari Dock/app launcher, environment shell bisa tidak otomatis terbaca. Gunakan wrapper:

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

Set OpenChamber agar memakai wrapper:

```bash
launchctl setenv OPENCHAMBER_OPENCODE_PATH "$HOME/.config/opencode/bin/opencode-with-env"
```

Jika menjalankan dari terminal:

```bash
export OPENCHAMBER_OPENCODE_PATH="$HOME/.config/opencode/bin/opencode-with-env"
openchamber
```

## Portability policy

- Jangan hardcode concrete path seperti `/home/<user>` atau `/Users/<user>` di active prompt/config/script.
- Gunakan `$HOME` atau `{env:HOME}` untuk config-level examples.
- Bedakan **OpenCode config root** dari **target app/project root**.
- Untuk generated assets, simpan dengan `target_path` relatif terhadap `project_root`.

## Verifikasi agent

Setelah restart OpenCode, cek agent utama:

```text
ping all agents
```

Expected minimal:

```text
@explorer ✓
@librarian ✓
@oracle ✓
@designer ✓
@fixer ✓
```

Jika agent baru belum terbaca, restart OpenCode lagi dan pastikan file `agents/*.md` valid.

## Troubleshooting

### GitHub MCP gagal connect

Pastikan token tersedia dan `.env` sudah diload:

```bash
test -n "$GITHUB_PERSONAL_ACCESS_TOKEN" && printf present || printf missing
```

Jika remote GitHub MCP tidak bisa dipakai oleh runtime, cek fallback local/Docker sesuai kebutuhan:

```bash
docker --version
```

### Context7 / Brave gagal

```bash
test -n "$CONTEXT7_API_KEY" && printf context7-present || printf context7-missing
test -n "$BRAVE_API_KEY" && printf brave-present || printf brave-missing
```

### Semgrep pertama kali lambat

`uvx semgrep mcp -t stdio` bisa butuh waktu saat pertama kali download package. Jalankan ulang `opencode mcp list` setelah selesai.

### OpenCode tidak otomatis membaca `.env`

Gunakan wrapper OpenChamber di atas, atau load manual sebelum menjalankan `opencode`.

## Security notes

- Jangan commit `.env`.
- Jangan paste token ke chat.
- Batasi GitHub token ke repository/permission yang dibutuhkan.
- Revoke/regenerate token jika secret pernah ter-commit.
- Jangan memberi write permission bila hanya butuh read-only context.

## Maintenance checklist

Sebelum menganggap perubahan non-trivial selesai:

```bash
git status --short
npm run test:prompt-gates
```

Lalu pastikan:

- plan/evidence ada untuk task non-trivial,
- validation sudah dijalankan,
- `@quality-gate` memberi `PASS` atau `PASS_WITH_RISKS` tanpa blocker,
- commit lokal hanya men-stage file relevan,
- tidak ada `.env`, secrets, `node_modules`, atau generated/vendor unrelated files yang ikut staged,
- tidak push otomatis.
