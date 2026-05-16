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

- `CLIPROXYAPI_BASE_URL`
- `CLIPROXYAPI_API_KEY`
- semua `OPENCODE_MODEL_*`

## RTK atau Caveman belum tersedia

Jalankan:

```bash
npm run setup:tools
```

Untuk cek read-only:

```bash
npm run setup:tools:check
```

## Image asset generator gagal konek ke provider

Pastikan nilai ini benar:

- `CLIPROXYAPI_BASE_URL`
- `CLIPROXYAPI_API_KEY`
- `IMAGE_ASSET_MODEL`

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
