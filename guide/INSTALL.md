# Install

## Project ini sebenarnya apa?

`opencode-capybara` adalah konfigurasi OpenCode/OpenChamber yang mengatur agent, workflow, validasi, dan dokumentasi agar penggunaan OpenCode lebih rapi dan aman.

Ini **bukan aplikasi end-user biasa** yang langsung dibuka di browser.

## Yang perlu kamu siapkan

- `git`
- `node` dan `npm`
- akses ke **OpenCode** atau **OpenChamber**
- akses ke **CLIProxyAPI** atau endpoint OpenAI-compatible yang dipakai sebagai provider model utama repo ini
- beberapa API key yang dipakai repo ini, minimal sesuai `.env.example`

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

Catatan:

- installer ini **butuh network**
- installer ini menjalankan setup **third-party tools** secara eksplisit
- installer akan meminta **konfirmasi** sebelum third-party setup
- mode non-interaktif tersedia lewat `bash scripts/install.sh --yes`

Catatan versi RTK:

- jalur script resmi memakai fallback **pinned release** `RTK_VERSION=v0.39.0` secara default
- jalur Homebrew tetap mengikuti **versi formula saat ini**

## Setup manual / lanjutan

```bash
git clone <REPO_URL> ~/.config/opencode
cd ~/.config/opencode
npm install
npm run setup:tools
npm run doctor
npm run test:prompt-gates
```

Kalau `opencode.json`, routing model, atau file agent berubah, jalankan:

```bash
npm run post:update
```

## Langkah pertama setelah install

Kalau `.env` belum ada:

```bash
cp .env.example .env
```

Lalu isi `.env` dan export ke shell.

Contoh untuk bash/zsh:

```bash
set -a
source ~/.config/opencode/.env
set +a
opencode
```

Jangan commit `.env`.

## Setelah berhasil jalan

Urutan baca lanjutan yang disarankan:

1. `guide/ENVIRONMENT.md`
2. `guide/SCRIPTS.md`
3. `guide/MODEL_ROUTING.md`
4. `guide/TROUBLESHOOTING.md`

Kalau kamu butuh aturan repo atau policy internal harness, baru lanjut ke:

- `AGENTS.md`
- `.opencode/docs/index.md`
