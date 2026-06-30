# OpenCode local backup cleanup (optional)

The script `scripts/backup-cleanup.py` is shipped in this repo but **not** wired
into any scheduler by default. It is intended to be run manually:

```bash
npm run cleanup:backups:scan     # dry-run: list trashable entries + trash
npm run cleanup:backups:trash    # move entries older than 3 days into backups/.trash/<date>/
npm run cleanup:backups:purge    # hard-delete .trash/<day>/ dirs older than 14 days
npm run cleanup:backups:apply    # both, with the defaults above
```

If you want it to run unattended, drop the unit + timer below under
`~/.config/systemd/user/` and enable it. They are **not enabled** automatically
by this repo.

`~/.config/systemd/user/opencode-backup-cleanup.service`:

```ini
[Unit]
Description=OpenCode backup cleanup (trash + purge)

[Service]
Type=oneshot
WorkingDirectory=/var/home/ujang/.config/opencode
ExecStart=/usr/bin/npm run --silent cleanup:backups:apply
Nice=10
```

`~/.config/systemd/user/opencode-backup-cleanup.timer`:

```ini
[Unit]
Description=Run OpenCode backup cleanup daily at 03:00

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true
AccuracySec=5min

[Install]
WantedBy=timers.target
```

Enable + start:

```bash
systemctl --user daemon-reload
systemctl --user enable --now opencode-backup-cleanup.timer
systemctl --user list-timers | grep opencode-backup-cleanup
```

Disable if you no longer want it:

```bash
systemctl --user disable --now opencode-backup-cleanup.timer
```

The script itself is fail-safe: it never deletes outside `backups/` and never
touches entries whose name starts with a `--keep-prefix` (e.g. `keep-`).
