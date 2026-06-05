# Runtime Operations

Panduan singkat untuk operator runtime repo-local. Fitur ini **tidak khusus repo ini saja**. Selama target adalah git repo biasa dan kamu menjalankan CLI dengan `--project-root /path/to/repo`, runtime state akan dibuat di `TARGET/.opencode/state/`.

## Kapan dipakai
- butuh durable run/task/mailbox di repo lain
- ingin inspect board/log execution tanpa masuk TUI
- ingin bounded supervisor tick untuk repo non-opencode lain

## Syarat minimal
- target adalah git repo lokal
- repo boleh belum punya `.opencode/`; runtime scripts akan membuat state saat dibutuhkan
- jalankan dari repo ini **atau** panggil `node scripts/runtime/cli.mjs` langsung, tapi set `--project-root` ke repo target

## Command umum

```bash
node ~/.config/opencode/scripts/runtime/cli.mjs board --project-root /path/to/other-repo --run-id run-1
node ~/.config/opencode/scripts/runtime/cli.mjs board --project-root /path/to/other-repo --run-id run-1 --watch --ticks 5 --interval-ms 250
node ~/.config/opencode/scripts/runtime/cli.mjs tail --project-root /path/to/other-repo --run-id run-1 --execution-id exec-1 --lines 20
node ~/.config/opencode/scripts/runtime/cli.mjs tail --project-root /path/to/other-repo --run-id run-1 --execution-id exec-1 --follow --timeout-ms 5000 --poll-ms 250
node ~/.config/opencode/scripts/runtime/cli.mjs poll --project-root /path/to/other-repo --run-id run-1
node ~/.config/opencode/scripts/runtime/cli.mjs consume --project-root /path/to/other-repo --run-id run-1 --worker-name backend-1
node ~/.config/opencode/scripts/runtime/cli.mjs retry --project-root /path/to/other-repo --run-id run-1 --task-id task-1 --execution-id exec-1 --max-attempts 3
node ~/.config/opencode/scripts/runtime/cli.mjs heartbeat --project-root /path/to/other-repo --run-id run-1 --worker-name backend-1 --owner worker-1 --lease-ms 30000
node ~/.config/opencode/scripts/runtime/cli.mjs lease-status --project-root /path/to/other-repo --run-id run-1 --worker-name backend-1
node ~/.config/opencode/scripts/runtime/cli.mjs lease-cleanup --project-root /path/to/other-repo --run-id run-1 --worker-name backend-1 --force
node ~/.config/opencode/scripts/runtime/cli.mjs lease-sweep --project-root /path/to/other-repo --run-id run-1 --force
node ~/.config/opencode/scripts/runtime/cli.mjs diagnostics --project-root /path/to/other-repo --run-id run-1
node ~/.config/opencode/scripts/runtime/cli.mjs diagnostics-snapshot --project-root /path/to/other-repo --run-id run-1 --snapshot-id snap-1
node ~/.config/opencode/scripts/runtime/cli.mjs dashboard-export --project-root /path/to/other-repo --run-id run-1 --snapshot-id dash-1
node ~/.config/opencode/scripts/runtime/cli.mjs tail-session-start --project-root /path/to/other-repo --run-id run-1 --execution-id exec-1 --session-id tail-1
node ~/.config/opencode/scripts/runtime/cli.mjs tail-session-status --project-root /path/to/other-repo --run-id run-1 --session-id tail-1
node ~/.config/opencode/scripts/runtime/cli.mjs tail-session-stop --project-root /path/to/other-repo --run-id run-1 --session-id tail-1
node ~/.config/opencode/scripts/runtime/cli.mjs tail-session-gc --project-root /path/to/other-repo --run-id run-1 --max-age-ms 3600000 --include-stopped
node ~/.config/opencode/scripts/runtime/cli.mjs supervise --project-root /path/to/other-repo --run-id run-1 --max-retries 3 --retry-base-ms 1000 --retry-multiplier 2 --retry-jitter-ratio 0.15 --renew-heartbeats
```

## Apa yang disimpan
- `TARGET/.opencode/state/runs/<run-id>/run.json`
- `TARGET/.opencode/state/runs/<run-id>/board.txt`
- `TARGET/.opencode/state/runs/<run-id>/board.json`
- `TARGET/.opencode/state/runs/<run-id>/workers/*.json`
- `TARGET/.opencode/state/runs/<run-id>/logs/<execution-id>/stdout.log`
- `TARGET/.opencode/state/runs/<run-id>/logs/<execution-id>/stderr.log`
- `TARGET/.opencode/state/mailbox/<run-id>/<worker>/*.json`
- `TARGET/.opencode/state/locks/*.lease.json`

## Safety notes
- retry memakai backoff bounded dari metadata execution, bisa ditambah jitter deterministik untuk menyebar retry tanpa mengorbankan replayability
- mailbox consumer bisa pakai lease lock per worker supaya dua consumer tidak makan mailbox sama; heartbeat bisa memperpanjang lease aktif
- live follow memakai timeout-bounded polling loop; persistent tail session manager menyimpan status sesi di state repo supaya polling berikutnya tidak kehilangan konteks
- supervisor bisa auto-renew heartbeat lease saat loop/tick berjalan
- lease sweeper bisa membersihkan semua worker stale sekaligus
- diagnostics report menggabungkan board + lease status dalam satu output
- diagnostics snapshots bisa diarsipkan per run untuk audit/replay ringan
- dashboard export menulis artifact text + HTML ke state run
- tail session garbage collector bisa membersihkan sesi usang / stopped
- board watch mode tetap bounded, bukan daemon permanen
- runtime state ada di `.opencode/state/`, jadi source repo lain tetap terpisah dari file runtime
