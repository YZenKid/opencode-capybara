#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_EXAMPLE="$ROOT_DIR/.env.example"
ENV_FILE="$ROOT_DIR/.env"
RTK_VERSION="${RTK_VERSION:-v0.39.0}"

PASS_COUNT=0
WARN_COUNT=0
AUTO_YES=0

platform_name() {
  uname -s
}

usage() {
  cat <<EOF
Usage: bash scripts/install.sh [--yes]

Options:
  --yes    Skip confirmation before third-party tool setup.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --yes)
      AUTO_YES=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      fail "Flag tidak dikenal: $1"
      ;;
  esac
done

section() {
  printf '\n== %s ==\n' "$1"
}

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  printf '[pass] %s\n' "$1"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  printf '[warn] %s\n' "$1"
}

fail() {
  printf '[fail] %s\n' "$1" >&2
  exit 1
}

note() {
  printf '  %s\n' "$1"
}

confirm_external_setup() {
  section "Konfirmasi third-party setup"
  note "Installer ini akan menjalankan setup tool eksternal berikut secara eksplisit:"
  note "- RTK ${RTK_VERSION} via Homebrew atau script resmi RTK yang dipin ke tag release"
  note "- Caveman via npx skills add JuliusBrussee/caveman -a opencode"

  if [[ "$AUTO_YES" -eq 1 ]]; then
    pass "Konfirmasi dilewati karena --yes"
    return
  fi

  if [[ ! -t 0 ]]; then
    fail "Session non-interaktif terdeteksi. Jalankan ulang dengan --yes jika kamu memang ingin melanjutkan third-party setup otomatis."
  fi

  printf 'Lanjutkan third-party setup? [y/N] '
  read -r answer
  case "$answer" in
    y|Y|yes|YES)
      pass "Third-party setup dikonfirmasi"
      ;;
    *)
      fail "Instalasi dibatalkan oleh pengguna."
      ;;
  esac
}

run_step() {
  local label="$1"
  shift
  printf '[run] %s\n' "$label"
  "$@"
  pass "$label selesai"
}

install_rtk() {
  section "RTK"
  note "RTK dipasang secara eksplisit oleh installer ini."
  note "Jangan jalankan rtk init dengan -g --opencode."
  note "Versi yang dipin: ${RTK_VERSION}"

  if command -v rtk >/dev/null 2>&1; then
    pass "rtk sudah terpasang"
    return
  fi

  if [[ "$(platform_name)" == "Darwin" ]] && command -v brew >/dev/null 2>&1; then
    run_step "brew install rtk" brew install rtk
    return
  fi

  if command -v curl >/dev/null 2>&1 && command -v sh >/dev/null 2>&1; then
    printf '[run] curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/%s/install.sh | RTK_VERSION=%s sh\n' "$RTK_VERSION" "$RTK_VERSION"
    sh -lc "curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/${RTK_VERSION}/install.sh | RTK_VERSION=${RTK_VERSION} sh"
    pass "rtk selesai dipasang lewat script resmi"
    return
  fi

  fail "Installer otomatis RTK tidak tersedia di platform ini. Pasang RTK manual lalu jalankan ulang installer."
}

install_caveman() {
  section "Caveman"
  note "Caveman ditambahkan secara eksplisit oleh installer ini."
  note "Repo ini memakai RTK dan Caveman bersama untuk workflow compression/context packing saat dibutuhkan."
  run_step "npx -y skills add JuliusBrussee/caveman -a opencode" npx -y skills add JuliusBrussee/caveman -a opencode
}

require_command() {
  local command_name="$1"
  local help_text="$2"
  if command -v "$command_name" >/dev/null 2>&1; then
    pass "$command_name ditemukan"
  else
    fail "$command_name tidak ditemukan. $help_text"
  fi
}

section "opencode-capybara installer"
note "Script ini membantu setup dasar untuk pemula."
note "Script ini tidak akan menimpa .env yang sudah ada."

section "Dependency dasar"
require_command git "Install git lalu jalankan ulang script ini."
require_command node "Install Node.js lalu jalankan ulang script ini."
require_command npm "Install npm atau distribusi Node.js yang menyertakannya lalu jalankan ulang script ini."

if command -v opencode >/dev/null 2>&1; then
  pass "opencode ditemukan"
else
  warn "opencode belum ditemukan di PATH"
  note "Lanjut setup tetap bisa dilakukan, tapi kamu tetap perlu memasang OpenCode/OpenChamber sebelum repo ini dipakai penuh."
fi

section "Install dan setup repo"
run_step "npm install" npm install
confirm_external_setup
install_rtk
install_caveman
run_step "npm run doctor" npm run doctor

section "Environment file"
if [[ -f "$ENV_FILE" ]]; then
  warn ".env sudah ada, tidak diubah"
else
  if [[ ! -f "$ENV_EXAMPLE" ]]; then
    fail ".env.example tidak ditemukan di $ROOT_DIR"
  fi

  cp "$ENV_EXAMPLE" "$ENV_FILE"
  pass ".env dibuat dari .env.example"
fi

section "Langkah berikutnya"
note "1. Buka file .env dan isi semua value yang masih placeholder."
note "2. Export env ke shell kamu. Contoh untuk bash/zsh:"
printf '\n'
printf '   set -a\n'
printf '   source "%s/.env"\n' "$ROOT_DIR"
printf '   set +a\n'
printf '\n'
note "3. Jalankan: opencode"
note "4. Kalau ingin verifikasi lebih ketat setelah setup dasar, jalankan: npm run test:prompt-gates"

section "Ringkasan"
pass "Setup dasar selesai"
note "Pass: $PASS_COUNT"
note "Warning: $WARN_COUNT"

if [[ $WARN_COUNT -gt 0 ]]; then
  note "Lanjutkan setelah warning di atas ditinjau."
fi
