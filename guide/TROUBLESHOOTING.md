# Troubleshooting

## `doctor` bilang OpenChamber out of sync

Jalankan:

```bash
npm run sync:openchamber
```

Kalau butuh sekaligus seed approved directories:

```bash
npm run sync:openchamber:seed
```

## Model agent belum sinkron dari `.env`

Jalankan:

```bash
npm run sync:agent-models
```

Lalu cek lagi dengan:

```bash
npm run doctor
```

## `.env` belum ada atau belum lengkap

```bash
cp .env.example .env
```

Isi semua value penting, terutama:

- `NINEROUTER_URL`
- `NINEROUTER_KEY`
- semua `OPENCODE_MODEL_*`, termasuk `OPENCODE_MODEL_VISUAL_ASSET` dan `OPENCODE_MODEL_QUALITY_GATE`

## RTK atau Caveman belum tersedia

Jalankan:

```bash
npm run setup:tools
```

Untuk cek read-only:

```bash
npm run setup:tools:check
```

## 9Router atau image asset gagal konek

Pastikan nilai ini benar:

- `NINEROUTER_URL`
- `NINEROUTER_KEY`
- `NINEROUTER_IMAGE_MODEL`

Gejala umum:

- `Missing NINEROUTER_URL` → env belum ter-load
- `401` → `NINEROUTER_KEY` salah/kedaluwarsa
- `400 Invalid model format` → model tidak ada di 9Router
- `503 All accounts unavailable` → account upstream 9Router sedang habis/offline

## OpenChamber tidak mewarisi env shell

Buat wrapper sederhana yang me-load `.env` sebelum menjalankan `opencode`:

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
launchctl setenv OPENCHAMBER_OPENCODE_PATH "$HOME/.config/opencode/bin/opencode-with-env"
```
