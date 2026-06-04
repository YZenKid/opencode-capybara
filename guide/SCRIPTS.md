# Scripts

## Setup dan onboarding

| Script | Fungsi | Kapan dipakai |
|---|---|---|
| `bash scripts/install.sh` | Installer pemula: install dependency, setup tool eksternal, buat `.env` jika belum ada, lalu beri instruksi next step | Saat pertama kali setup repo ini |
| `npm run setup:tools` | Menyiapkan RTK dan Caveman secara eksplisit | Kalau tool pendukung belum terpasang atau ingin setup manual tanpa installer pemula |
| `npm run setup:tools:check` | Verifikasi read-only apakah tool setup sudah tersedia | Saat ingin cek kondisi tool tanpa mengubah sistem |
| `npm run doctor` | Menjalankan pemeriksaan repo, env posture, sync agent model, dan sync OpenChamber | Setelah setup atau saat troubleshooting |
| `npm run post:update` | Menjalankan sync agent model, sync OpenChamber, lalu `doctor` | Setelah update config, model routing, atau file agent |

## Sinkronisasi model dan config

| Script | Fungsi | Kapan dipakai |
|---|---|---|
| `npm run sync:agent-models` | Menyamakan `model:` di `agents/*.md` dengan `OPENCODE_MODEL_*` dari `.env`, termasuk split khusus `OPENCODE_MODEL_VISUAL_ASSET` dan `OPENCODE_MODEL_QUALITY_GATE` | Setelah mengubah model di `.env` |
| `npm run sync:agent-models:check` | Cek read-only apakah model agent sudah sinkron dengan `.env` | Untuk audit atau validasi CI/manual |
| `npm run sync:openchamber` | Menyinkronkan setting OpenChamber agar mengikuti config OpenCode sebagai source of truth; `defaultModel` diarahkan ke model orchestrator untuk new session, plus menulis metadata `opencodeAgentModelMap` untuk mirror routing agent | Saat `doctor` memberi warning OpenChamber out of sync |
| `npm run sync:openchamber:check` | Cek read-only sync OpenChamber | Saat hanya ingin audit tanpa menulis file |
| `npm run sync:openchamber:seed` | Sync OpenChamber sambil menambahkan repo root ke approved directories bila perlu | Saat environment OpenChamber baru atau approved directory belum ada |
| `npm run sync:openchamber:seed:check` | Cek read-only untuk flow sync + seed approved directories | Saat ingin audit kondisi OpenChamber lengkap |
| `npm run compare:openchamber-models` | Menampilkan tabel perbandingan setting model OpenCode vs OpenChamber, termasuk mirror `opencodeAgentModelMap` | Saat ingin audit cepat mismatch atau memastikan hasil sync |

## Runtime operator helpers

| Script | Fungsi | Kapan dipakai |
|---|---|---|
| `npm run runtime:board -- --run-id <id>` | Tampilkan board summary run | Saat butuh ringkasan task/mailbox/execution |
| `npm run runtime:watch -- --run-id <id> --ticks 5 --interval-ms 250` | Snapshot board berulang secara bounded | Saat ingin watch mode ringan tanpa daemon |
| `npm run runtime:poll -- --run-id <id>` | Poll semua execution aktif | Saat ingin update status process |
| `npm run runtime:tail -- --run-id <id> --execution-id <id> --lines 20` | Ambil tail stdout/stderr execution | Saat debugging worker tertentu |
| `npm run runtime:tail -- --run-id <id> --execution-id <id> --follow --timeout-ms 5000 --poll-ms 250` | Live follow log sampai timeout | Saat perlu `tail -f` bounded untuk worker tertentu |
| `npm run runtime:retry -- --run-id <id> --task-id <task> --execution-id <id>` | Paksa retry bounded untuk task gagal | Saat perlu retry manual |
| `npm run runtime:consume -- --run-id <id> --worker-name <worker>` | Consume mailbox worker sekali | Saat ingin drain mailbox manual |
| `npm run runtime:heartbeat -- --run-id <id> --worker-name <worker> --owner <owner>` | Perpanjang lease worker aktif | Saat consumer/worker perlu keepalive lease |
| `npm run runtime:lease-status -- --run-id <id> --worker-name <worker>` | Tampilkan owner/expiry lock worker | Saat debugging lease conflict |
| `npm run runtime:lease-cleanup -- --run-id <id> --worker-name <worker> --force` | Bersihkan lease stale / paksa cleanup | Saat lock yatim menghalangi consumer |
| `npm run runtime:lease-sweep -- --run-id <id> --force` | Sweep lease untuk semua worker pada run | Saat ingin bersihkan stale lock massal |
| `npm run runtime:diagnostics -- --run-id <id>` | Tampilkan board + lease report gabungan | Saat butuh ringkasan operator penuh |
| `npm run runtime:tail-session-start -- --run-id <id> --execution-id <id> --session-id tail-1` | Mulai sesi tail persisten | Saat ingin polling tail lintas command |
| `npm run runtime:tail-session-status -- --run-id <id> --session-id tail-1` | Poll status sesi tail persisten | Saat lanjut memantau sesi tail |
| `npm run runtime:tail-session-stop -- --run-id <id> --session-id tail-1` | Hentikan sesi tail persisten | Saat sesi tail tidak dibutuhkan lagi |
| `npm run runtime:supervise -- --run-id <id> --max-retries 3` | Jalankan supervisor tick/loop bounded | Saat ingin auto poll/consume/retry tanpa daemon |
| `npm run test:runtime-phase7` | Validasi tail/watch/leases/backoff dan generic temp-repo flow | Setelah ubah runtime operator layer |
| `npm run test:runtime-phase8` | Validasi tail follow, heartbeat, jitter, dan generic temp-repo flow | Setelah ubah follow/lease/backoff layer |
| `npm run test:runtime-phase9` | Validasi live follow, auto-heartbeat renewal, lease diagnostics/cleanup, dan generic temp-repo flow | Setelah ubah lease/live-follow layer |
| `npm run test:runtime-phase10` | Validasi tail session manager, lease sweeper, diagnostics report, dan generic temp-repo flow | Setelah ubah operator aggregation layer |

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
