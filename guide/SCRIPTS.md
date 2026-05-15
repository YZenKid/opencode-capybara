# Scripts

## Setup dan onboarding

| Script | Fungsi | Kapan dipakai |
|---|---|---|
| `bash scripts/install.sh` | Installer pemula: install dependency, setup tool eksternal, buat `.env` jika belum ada, lalu beri instruksi next step | Saat pertama kali setup repo ini |
| `npm run setup:tools` | Menyiapkan RTK dan Caveman secara eksplisit | Kalau tool pendukung belum terpasang atau ingin setup manual tanpa installer pemula |
| `npm run setup:tools:check` | Verifikasi read-only apakah tool setup sudah tersedia | Saat ingin cek kondisi tool tanpa mengubah sistem |
| `npm run doctor` | Menjalankan pemeriksaan repo, env posture, sync agent model, dan sync OpenChamber | Setelah setup atau saat troubleshooting |
| `npm run post:update` | Menjalankan sync agent model, sync OpenChamber, lalu `doctor` | Setelah update config, model routing, atau file agent |
| `bash scripts/figma-mcp-auth.sh auth` | Direct wrapper: validasi config lalu eksekusi `opencode mcp auth figma` | Saat ingin connect Figma MCP pertama kali |
| `bash scripts/figma-mcp-auth.sh reauth` | Direct wrapper: validasi config lalu eksekusi `opencode mcp logout figma` dan `opencode mcp auth figma` | Saat auth perlu direset/diulang |
| `bash scripts/figma-mcp-auth.sh bootstrap` | Direct wrapper: validasi config lalu eksekusi helper bootstrap OAuth (`node scripts/figma-mcp-auth-bootstrap.mjs https://mcp.figma.com/mcp`) | Saat native auth gagal (approved-client restriction/403) |
| `bash scripts/figma-mcp-auth.sh <mode> --verify` | Menjalankan verifikasi pasca-flow: `opencode mcp list` + `opencode mcp debug figma` | Setelah auth/reauth/bootstrap untuk cek status aktual |

### Catatan Figma MCP

- Config repo ini untuk Figma MCP memakai `oauth: {}` (object), bukan API-key auth.
- Bootstrap helper menulis token ke `~/.local/share/opencode/mcp-auth.json`.
- File token tersebut sensitif: jangan commit dan jangan disebar.
- Untuk machine/device baru, ulangi flow auth di device itu (disarankan), bukan copy token antar mesin.

## Sinkronisasi model dan config

| Script | Fungsi | Kapan dipakai |
|---|---|---|
| `npm run sync:agent-models` | Menyamakan `model:` di `agents/*.md` dengan `OPENCODE_MODEL_*` dari `.env` | Setelah mengubah model di `.env` |
| `npm run sync:agent-models:check` | Cek read-only apakah model agent sudah sinkron dengan `.env` | Untuk audit atau validasi CI/manual |
| `npm run sync:openchamber` | Menyinkronkan setting OpenChamber agar mengikuti config OpenCode sebagai source of truth; `defaultModel` diarahkan ke model orchestrator untuk new session, plus menulis metadata `opencodeAgentModelMap` untuk mirror routing agent | Saat `doctor` memberi warning OpenChamber out of sync |
| `npm run sync:openchamber:check` | Cek read-only sync OpenChamber | Saat hanya ingin audit tanpa menulis file |
| `npm run sync:openchamber:seed` | Sync OpenChamber sambil menambahkan repo root ke approved directories bila perlu | Saat environment OpenChamber baru atau approved directory belum ada |
| `npm run sync:openchamber:seed:check` | Cek read-only untuk flow sync + seed approved directories | Saat ingin audit kondisi OpenChamber lengkap |
| `npm run compare:openchamber-models` | Menampilkan tabel perbandingan setting model OpenCode vs OpenChamber, termasuk mirror `opencodeAgentModelMap` | Saat ingin audit cepat mismatch atau memastikan hasil sync |

## Validasi dan quality checks

| Script | Fungsi | Kapan dipakai |
|---|---|---|
| `npm run test:prompt-gates` | Menjalankan regression checks untuk prompt/config/docs contract | Setelah mengubah agent, skill, config, README, atau policy |
| `npm run check:docs` | Validasi integritas dokumentasi utama | Setelah mengubah docs atau indeks dokumentasi |
| `npm run check:agents` | Validasi boundary dan kontrak agent | Setelah mengubah file di `agents/` |
| `npm run check:skills` | Validasi kontrak skill | Setelah mengubah file di `skills/` |
| `npm run check:evidence` | Validasi contract evidence/artifact repo | Saat mengubah workflow evidence atau artifact |
| `npm run check:harness` | Menjalankan prompt gates + mechanical checks utama | Saat ingin validasi standar sebelum menyimpulkan perubahan aman |
| `npm run check:harness:strict` | Menjalankan `check:harness` lalu eval tambahan | Saat ingin validasi lebih ketat |
| `npm run eval:harness` | Menjalankan harness eval ringan dan menulis report replayable | Saat mengecek perilaku harness secara lebih sistematis |

## Contoh alur pakai umum

Setup pertama kali:

```bash
bash scripts/install.sh
```

Setelah ganti model di `.env`:

```bash
npm run sync:agent-models
npm run doctor
```

Setelah ubah config/agent/docs:

```bash
npm run post:update
npm run test:prompt-gates
```

Sebelum final check yang lebih lengkap:

```bash
npm run check:harness
```
