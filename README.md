# opencode-capybara

<p align="center">
  <img src="assets/opencode-capybara-icon.png" alt="opencode-capybara capybara mascot icon" width="128" height="128" />
</p>

Standalone OpenCode multi-agent configuration yang tenang, terarah, dan safety-gated untuk coding, docs, UI, browser validation, security scan, GitHub context, dan visual asset workflow.

`opencode-capybara` adalah konfigurasi OpenCode untuk OpenCode/OpenChamber. Repo ini membantu mengatur agent, workflow, validasi, dan dokumentasi agar penggunaan OpenCode lebih rapi dan aman.

Secara internal repo ini memakai local Markdown agents, standalone `opencode-*` skills, prompt gates, MCP, dan dokumentasi terstruktur di `.opencode/docs/`.

Repository ini juga diposisikan sebagai **local harness engineering system**.

## Mulai dari sini

Kalau kamu baru pertama kali melihat repo ini, anggap proyek ini sebagai:

- **bukan aplikasi end-user biasa**, melainkan
- **konfigurasi dan workflow untuk OpenCode/OpenChamber**.

Repo ini paling cocok untuk:

- user yang memakai OpenCode/OpenChamber secara rutin,
- orang yang ingin workflow agent-based yang lebih ketat,
- maintainer yang butuh docs, quality gate, dan evidence yang rapi.

Repo ini **kurang cocok** kalau ekspektasimu adalah:

- aplikasi visual yang langsung dibuka di browser,
- boilerplate frontend/backend sederhana,
- setup tanpa API key atau tools tambahan.

## Quick start untuk pemula

```bash
git clone <REPO_URL> ~/.config/opencode
cd ~/.config/opencode
bash scripts/install.sh
```

Installer ini akan menjalankan:

- `npm install`
- setup RTK secara eksplisit di dalam installer
- setup Caveman secara eksplisit di dalam installer
- `npm run doctor`

Installer ini **butuh network** dan menjalankan setup **third-party tools** secara eksplisit. Kalau kamu butuh mode non-interaktif, gunakan `bash scripts/install.sh --yes`.

## Dokumentasi pengguna

Panduan user-facing dipindahkan ke folder [`guide/`](./guide/README.md):

- [`guide/INSTALL.md`](./guide/INSTALL.md)
- [`guide/ENVIRONMENT.md`](./guide/ENVIRONMENT.md)
- [`guide/SCRIPTS.md`](./guide/SCRIPTS.md)
- [`guide/MODEL_ROUTING.md`](./guide/MODEL_ROUTING.md)
- [`guide/TROUBLESHOOTING.md`](./guide/TROUBLESHOOTING.md)

## Dokumentasi internal harness

- `AGENTS.md` adalah peta singkat aturan repo
- `.opencode/docs/index.md` adalah titik masuk utama policy dan architecture

`AGENTS.md` sekarang adalah table of contents + non-negotiable rules.
Detail policy hidup di `.opencode/docs/`.
Plans adalah first-class artifacts di `.opencode/plans/`.

## Struktur project singkat

Kalau kamu pemula, cukup kenali 4 area ini dulu:

- `README.md` → panduan mulai
- `guide/` → panduan penggunaan repo
- `AGENTS.md` → aturan singkat
- `.opencode/docs/` → dokumentasi detail internal

## Kenapa capybara?

Capybara dipilih karena tenang, sosial, adaptif, dan bisa berdampingan dengan banyak spesies—metafora untuk orchestration layer yang menyatukan banyak agent, skill, MCP, dan safety gate tanpa menambah noise.

- **Calm orchestration** — `@orchestrator` meredam chaos multi-agent/multi-tool.
- **Coexistence** — agents, docs, browser, security, GitHub, documents, dan image tooling hidup berdampingan.
- **Social coordination** — multi-agent collaboration bekerja lebih baik dengan role yang jelas.
- **Low drama, high utility** — safety gates dan validation lebih penting daripada aksi agresif.
- **Adaptability** — satu setup bisa berpindah konteks antara code, docs, UI, security, dan document work.

Capybara bukan simbol “cepat sendiri”; ia simbol “tenang bersama-sama sampai hasilnya benar”.

## Ringkasan model routing

### Apa itu CLIProxyAPI di repo ini?

Di repo ini, **CLIProxyAPI** adalah provider model utama yang dipakai OpenCode untuk menjalankan agent-agent lokal.

- `CLIPROXYAPI_BASE_URL` → base URL endpoint OpenAI-compatible
- `CLIPROXYAPI_API_KEY` → API key untuk autentikasi ke provider tersebut

Kalau dua nilai ini salah atau kosong, agent bisa gagal memanggil model meskipun konfigurasi lain terlihat benar.

Copy `.env.example` to `.env` and set every `OPENCODE_MODEL_*` value before launching OpenCode. Missing env vars resolve to an empty string, which can break OpenCode model routing.

Model routing sekarang diterapkan lewat dua jalur:

- `opencode.json` memakai `OPENCODE_MODEL_DEFAULT` untuk model default runtime
- `scripts/sync-agent-models.mjs` menyamakan `model:` literal di `agents/*.md` dengan nilai `OPENCODE_MODEL_*` dari `.env`

Kalau kamu mengubah `OPENCODE_MODEL_*`, jalankan:

```bash
npm run sync:agent-models
```

### Model routing table

| Env var | Default / recommended model | Used by / capability | Cost guidance |
|---|---|---|---|
| `OPENCODE_MODEL_DEFAULT` | `cliproxyapi/gpt-5.3-codex` | Top-level default model and general fallback | Use Codex lane as balanced default for coding-heavy work while keeping specialist high-risk lanes stronger. |
| `OPENCODE_MODEL_ORCHESTRATOR` | `cliproxyapi/gpt-5.4` | `@orchestrator` primary routing/integration | Keep high quality for delegation, coordination, and final synthesis. |
| `OPENCODE_MODEL_PLANNER` | `cliproxyapi/gpt-5.3-codex` | `@artifact-planner`, `modes/plan.md`, `agents-disabled/plan.md` | Planning is codebase-heavy and can use Codex to reduce cost while keeping structure strong. |
| `OPENCODE_MODEL_DESIGN` | `cliproxyapi/gpt-5.4` | `@designer`, `@visual-parity-auditor`, `@ui-system-architect` | UI and visual reasoning are higher-value, so keep quality high. |
| `OPENCODE_MODEL_REVIEW` | `cliproxyapi/gpt-5.4` | `@oracle`, `@quality-gate`, `@council` | Review lanes should stay strict and high quality; optimize for correctness over cost. |
| `OPENCODE_MODEL_ADVISORY` | `cliproxyapi/gpt-5.4` | `@product-architect`, `@saas-architect`, `@ai-systems-architect`, `@security-privacy-reviewer`, `@release-engineer`, `@mobile-architect` | Advisory work is often high-stakes; keep the stronger model unless cost pressure is extreme. |
| `OPENCODE_MODEL_EXECUTION` | `cliproxyapi/gpt-5.3-codex` | `@fixer` | Use Codex for bounded implementation/testing because this lane is code-edit heavy. |
| `OPENCODE_MODEL_DISCOVERY` | `cliproxyapi/gpt-5.4-mini` | `@explorer`, `@librarian`, `@motion-specialist`, `@accessibility-reviewer` | Discovery and read-only analysis can usually use the lower-cost model. |
| `OPENCODE_MODEL_DOCUMENTS` | `cliproxyapi/gpt-5.4-mini` | `@document-specialist` | Document processing is usually utility work; keep it cost-efficient. |
| `OPENCODE_MODEL_IMPROVEMENT` | `cliproxyapi/gpt-5.4-mini` | `@skill-improver` | Small prompt/skill refinements should stay on the cheaper lane. |

## Ringkasan domain specialist dan workflow

Domain specialists bersifat conditional.
Tiny UI polish tetap ke `@designer`, dan isolated bugfix tetap ke `@fixer`.

- `@skill-improver` dipakai untuk non-trivial follow-up, repeated failures, policy gaps, atau explicit request.
- no blind external updates.
- `@quality-gate` memberi status seperti `PASS_WITH_RISKS`, `NEEDS_FIX`, dan `BLOCKED`.
- Redundant `build` and `general` local agents have been removed.

## Script penting

- `npm run setup:tools`
- `npm run doctor`
- `npm run post:update`
- `npm run sync:agent-models`
- `npm run test:prompt-gates`

Lihat penjelasan lengkap di [`guide/SCRIPTS.md`](./guide/SCRIPTS.md).

## RTK dan Caveman singkat

- jika setup otomatis tidak tersedia, script akan memberi **manual fallback** command yang jelas
- repo ini menerapkan **no unsafe lifecycle install hooks policy**
- **OpenCode command rewriting** tetap **opt-in**
- untuk **token compression / context packing**, gunakan **RTK dan Caveman secara bersamaan**

## Ringkasan validasi

Validasi yang paling umum:

```bash
npm run test:prompt-gates
npm run check:harness
```

Harness checks tambahan:

```bash
npm run check:docs
npm run check:agents
npm run check:skills
npm run check:evidence
```

## Ringkasan validasi dan auto-commit

Auto-commit default ON untuk local commits only; never push automatically.

- Jalan hanya setelah task **plan-bound non-trivial selesai**, **validation lulus**, dan `@quality-gate` memberi `PASS` atau `PASS_WITH_RISKS` tanpa blocker.
- Review `git status`/`git diff`, lalu **stage hanya file relevan**.
- Commit message otomatis memakai **subject singkat plus body bullet-point**.
- Jangan stage `.env`, secrets, tokens, credentials, unrelated untracked files, atau generated/vendor files kecuali plan/user menyetujui.
- Jangan gunakan `--no-verify`, `--no-gpg-sign`, `amend`, force push, atau destructive git commands.
- Kalau scope atau staging meragukan, berhenti dan tanya.

## Ringkasan internal workflow

- Redundant `build` and `general` local agents have been removed.
- `@skill-improver` dipakai untuk non-trivial follow-up, repeated failures, policy gaps, atau explicit request.
- `@quality-gate` memberi status seperti `PASS_WITH_RISKS`, `NEEDS_FIX`, dan `BLOCKED`.

Detail lengkap tetap ada di `.opencode/docs/` dan file agent/skill terkait.
