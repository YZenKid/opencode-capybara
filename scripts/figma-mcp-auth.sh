#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/opencode.json"
MODE="auth"
VERIFY=0

usage() {
  cat <<'EOF'
Usage: bash scripts/figma-mcp-auth.sh [auth|reauth|bootstrap] [--verify]

Modes:
  auth      Jalankan: opencode mcp auth figma (default)
  reauth    Jalankan: opencode mcp logout figma lalu opencode mcp auth figma
  bootstrap Jalankan helper bootstrap OAuth ke auth store OpenCode

Options:
  --verify      Setelah flow utama, jalankan verifikasi MCP list + debug figma
  --help, -h    Tampilkan bantuan
EOF
}

note() {
  printf '  %s\n' "$1"
}

pass() {
  printf '[pass] %s\n' "$1"
}

warn() {
  printf '[warn] %s\n' "$1"
}

fail() {
  printf '[fail] %s\n' "$1" >&2
  exit 1
}

section() { printf '\n== %s ==\n' "$1"; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    auth|reauth|bootstrap)
      MODE="$1"
      shift
      ;;
    --verify)
      VERIFY=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      fail "Argumen tidak dikenal: $1"
      ;;
  esac
done

[[ -f "$CONFIG_FILE" ]] || fail "Config tidak ditemukan: $CONFIG_FILE"

FIGMA_STATE="$(node - "$CONFIG_FILE" <<'EOF'
const fs = require('node:fs')
const path = process.argv[2]
const data = JSON.parse(fs.readFileSync(path, 'utf8'))
const mcp = data.mcp ?? {}
const figma = mcp.figma
if (!figma) {
  console.log('missing')
  process.exit(0)
}
console.log(JSON.stringify({
  type: figma.type ?? null,
  url: figma.url ?? null,
  oauth: figma.oauth ?? null,
  enabled: figma.enabled ?? null,
}))
EOF
)"

if [[ "$FIGMA_STATE" == "missing" ]]; then
  fail "Entry MCP 'figma' tidak ditemukan di opencode.json"
fi

FIGMA_TYPE="$(node -e 'const o=JSON.parse(process.argv[1]); process.stdout.write(String(o.type ?? ""))' "$FIGMA_STATE")"
FIGMA_URL="$(node -e 'const o=JSON.parse(process.argv[1]); process.stdout.write(String(o.url ?? ""))' "$FIGMA_STATE")"
FIGMA_OAUTH_KIND="$(node -e 'const o=JSON.parse(process.argv[1]); const v=o.oauth; if (v === false) process.stdout.write("false"); else if (v === true) process.stdout.write("true"); else if (v && typeof v === "object") process.stdout.write("object"); else if (v == null) process.stdout.write("missing"); else process.stdout.write(typeof v)' "$FIGMA_STATE")"
FIGMA_ENABLED="$(node -e 'const o=JSON.parse(process.argv[1]); process.stdout.write(String(o.enabled ?? ""))' "$FIGMA_STATE")"

note "config figma: type=${FIGMA_TYPE:-<kosong>} url=${FIGMA_URL:-<kosong>} oauth=${FIGMA_OAUTH_KIND:-<kosong>} enabled=${FIGMA_ENABLED:-<kosong>}"

[[ "$FIGMA_TYPE" == "remote" ]] || fail "Config figma bukan remote. Expected: type=remote"
[[ "$FIGMA_URL" == "https://mcp.figma.com/mcp" ]] || fail "URL figma tidak sesuai. Expected: https://mcp.figma.com/mcp"
[[ "$FIGMA_OAUTH_KIND" == "object" ]] || fail "Config figma harus memakai oauth object, misalnya: \"oauth\": {}"
[[ "$FIGMA_ENABLED" == "true" ]] || fail "Config figma belum enabled=true"

pass "Config Figma MCP sudah sesuai posture repo"

run_cmd() {
  local label="$1"
  shift
  section "$label"
  printf '+ %s\n' "$*"
  "$@"
}

if [[ "$MODE" == "auth" ]]; then
  run_cmd "Auth" opencode mcp auth figma
elif [[ "$MODE" == "reauth" ]]; then
  run_cmd "Logout" opencode mcp logout figma
  run_cmd "Re-auth" opencode mcp auth figma
else
  run_cmd "Bootstrap" node "$ROOT_DIR/scripts/figma-mcp-auth-bootstrap.mjs" https://mcp.figma.com/mcp
fi

if [[ "$VERIFY" -eq 1 ]]; then
  run_cmd "Verify list" opencode mcp list
  run_cmd "Verify debug" opencode mcp debug figma
fi

pass "Flow ${MODE} selesai"
