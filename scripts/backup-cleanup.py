#!/usr/bin/env python3
"""Auto-cleanup of old backup directories under `.config/opencode`.

Policy:
- `trash_age_days` (default 3): a backup entry older than this is moved into
  `<repo>/backups/.trash/<YYYY-MM-DD>/` (preserves subdir structure).
- `purge_age_days` (default 14): a trashed entry older than this is hard-deleted.
- Skip-list: any entry whose name starts with the user's `--keep-prefix` (e.g.
  `keep-`) is never touched.
- Dry-run by default; use `--apply` to actually move/delete.
- Scope: `backups/` of the repo root and (optionally) the `opencode-capybara/`
  mirror; both default to enabled.

Usage:
  # see what would happen (no changes)
  python3 scripts/backup-cleanup.py --scan

  # trash backup entries older than 3 days
  python3 scripts/backup-cleanup.py --trash --trash-age-days 3

  # purge trashed entries older than 14 days
  python3 scripts/backup-cleanup.py --purge --purge-age-days 14

  # both, with the defaults above
  python3 scripts/backup-cleanup.py --apply

Exit codes:
  0 = clean / nothing to do
  1 = action performed (with or without errors) — see JSON report
  2 = invalid invocation
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

DATE_FMT = "%Y-%m-%d"
REPO_DEFAULT = "/var/home/ujang/.config/opencode"

# Directories we scan for backup entries. Each maps to a scope label.
DEFAULT_SCOPES = {
    "repo": "backups",
    "mirror": "opencode-capybara/backups",
}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_mtime_utc(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def age_days(path: Path, now: datetime) -> float:
    return (now - parse_mtime_utc(path)).total_seconds() / 86400.0


def size_human(num: int) -> str:
    n = float(num)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{int(n)}B" if unit == "B" else f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def dir_size(path: Path) -> int:
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(Path(root) / f)
            except OSError:
                pass
    return total


def list_entries(scope_root: Path) -> list[Path]:
    if not scope_root.is_dir():
        return []
    out = []
    for entry in scope_root.iterdir():
        if entry.is_dir() and not entry.name.startswith("."):
            out.append(entry)
    return out


def scan(repo_root: Path, now: datetime) -> list[dict[str, Any]]:
    """Return entries that can be trashed right now."""
    found: list[dict[str, Any]] = []
    for scope, rel in DEFAULT_SCOPES.items():
        scope_root = repo_root / rel
        for entry in list_entries(scope_root):
            if entry.name == ".trash":
                continue
            mtime = parse_mtime_utc(entry)
            size = dir_size(entry)
            found.append({
                "scope": scope,
                "path": str(entry),
                "name": entry.name,
                "size_bytes": size,
                "size_human": size_human(size),
                "mtime": mtime.isoformat(),
                "age_days": round(age_days(entry, now), 2),
            })
    found.sort(key=lambda x: x["age_days"], reverse=True)
    return found


def trash_root(repo_root: Path) -> Path:
    return repo_root / "backups" / ".trash"


def trash_today(repo_root: Path, now: datetime) -> Path:
    target = trash_root(repo_root) / now.strftime(DATE_FMT)
    target.mkdir(parents=True, exist_ok=True)
    return target


def move_to_trash(
    repo_root: Path,
    entry: dict[str, Any],
    now: datetime,
    keep_prefixes: tuple[str, ...] = (),
) -> dict[str, Any]:
    src = Path(entry["path"])
    if not src.exists():
        return {"ok": False, "path": str(src), "error": "missing"}
    if any(src.name.startswith(p) for p in keep_prefixes):
        return {"ok": True, "skipped": True, "reason": "keep-prefix", "path": str(src)}
    rel = Path(entry["scope"]) / src.name
    dest = trash_today(repo_root, now) / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        shutil.move(str(src), str(dest))
        return {"ok": True, "moved_to": str(dest), "src": str(src), "size_bytes": entry["size_bytes"]}
    except OSError as e:
        return {"ok": False, "src": str(src), "error": str(e)}


def list_trash(repo_root: Path) -> list[dict[str, Any]]:
    root = trash_root(repo_root)
    if not root.is_dir():
        return []
    days = []
    for day in sorted(root.iterdir()):
        if not day.is_dir():
            continue
        size = dir_size(day)
        days.append({"name": day.name, "path": str(day), "size_bytes": size, "size_human": size_human(size)})
    return days


def purge_trash(
    repo_root: Path,
    purge_age_days: int,
    now: datetime,
    keep_prefixes: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    root = trash_root(repo_root)
    if not root.is_dir():
        return []
    cutoff = now - timedelta(days=purge_age_days)
    actions: list[dict[str, Any]] = []
    for day in list(root.iterdir()):
        if not day.is_dir():
            continue
        # honor the day's name as date; only purge days strictly older than cutoff
        try:
            day_date = datetime.strptime(day.name, DATE_FMT).replace(tzinfo=timezone.utc)
        except ValueError:
            actions.append({"ok": False, "path": str(day), "error": "unparseable date dir"})
            continue
        if day_date >= cutoff:
            continue
        # safety: never purge a dir whose name starts with keep-prefix
        if any(day.name.startswith(p) for p in keep_prefixes):
            actions.append({"ok": True, "skipped": True, "reason": "keep-prefix", "path": str(day)})
            continue
        size = dir_size(day)
        try:
            shutil.rmtree(day)
            actions.append({"ok": True, "purged": str(day), "size_bytes": size})
        except OSError as e:
            actions.append({"ok": False, "path": str(day), "error": str(e)})
    return actions


def cmd_scan(args: argparse.Namespace) -> int:
    repo = Path(args.repo_root)
    now = now_utc()
    entries = scan(repo, now)
    trashable = [e for e in entries if e["age_days"] >= args.trash_age_days]
    payload = {
        "repo_root": str(repo),
        "now": now.isoformat(),
        "trash_age_days": args.trash_age_days,
        "purge_age_days": args.purge_age_days,
        "scanned": len(entries),
        "trashable_now": len(trashable),
        "trashable": trashable,
        "trash": list_trash(repo),
    }
    print(json.dumps(payload, indent=2))
    return 0


def cmd_trash(args: argparse.Namespace) -> int:
    repo = Path(args.repo_root)
    now = now_utc()
    keep = tuple(args.keep_prefix or ())
    entries = [e for e in scan(repo, now) if e["age_days"] >= args.trash_age_days]
    actions = [move_to_trash(repo, e, now, keep) for e in entries]
    failed = [a for a in actions if not a.get("ok")]
    payload = {
        "trashed": len([a for a in actions if a.get("ok") and not a.get("skipped")]),
        "skipped": len([a for a in actions if a.get("skipped")]),
        "failed": len(failed),
        "actions": actions,
        "trash_total_size_bytes": sum(a.get("size_bytes", 0) for a in actions if a.get("ok")),
    }
    print(json.dumps(payload, indent=2))
    return 1 if failed else 0


def cmd_purge(args: argparse.Namespace) -> int:
    repo = Path(args.repo_root)
    now = now_utc()
    keep = tuple(args.keep_prefix or ())
    actions = purge_trash(repo, args.purge_age_days, now, keep)
    failed = [a for a in actions if not a.get("ok")]
    payload = {
        "purged": len([a for a in actions if a.get("ok") and not a.get("skipped")]),
        "skipped": len([a for a in actions if a.get("skipped")]),
        "failed": len(failed),
        "actions": actions,
        "freed_bytes": sum(a.get("size_bytes", 0) for a in actions if a.get("ok")),
    }
    print(json.dumps(payload, indent=2))
    return 1 if failed else 0


def cmd_apply(args: argparse.Namespace) -> int:
    repo = Path(args.repo_root)
    now = now_utc()
    keep = tuple(args.keep_prefix or ())
    entries = [e for e in scan(repo, now) if e["age_days"] >= args.trash_age_days]
    trash_actions = [move_to_trash(repo, e, now, keep) for e in entries]
    purge_actions = purge_trash(repo, args.purge_age_days, now, keep)
    failed = [a for a in trash_actions + purge_actions if not a.get("ok")]
    payload = {
        "trashed": len([a for a in trash_actions if a.get("ok") and not a.get("skipped")]),
        "purged": len([a for a in purge_actions if a.get("ok") and not a.get("skipped")]),
        "failed": len(failed),
        "trash_actions": trash_actions,
        "purge_actions": purge_actions,
    }
    print(json.dumps(payload, indent=2))
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo-root", default=REPO_DEFAULT)
    ap.add_argument("--trash-age-days", type=int, default=3)
    ap.add_argument("--purge-age-days", type=int, default=14)
    ap.add_argument("--keep-prefix", action="append", default=[], help="Skip dirs whose name starts with this prefix. Repeatable.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--scan", action="store_true", help="List trashable and trashed entries; do not modify anything.")
    mode.add_argument("--trash", action="store_true", help="Move backup entries older than --trash-age-days into .trash/.")
    mode.add_argument("--purge", action="store_true", help="Hard-delete .trash/<day>/ dirs older than --purge-age-days.")
    mode.add_argument("--apply", action="store_true", help="Run --trash then --purge in one pass.")
    args = ap.parse_args()

    if not any([args.scan, args.trash, args.purge, args.apply]):
        args.scan = True

    if args.scan:
        return cmd_scan(args)
    if args.trash:
        return cmd_trash(args)
    if args.purge:
        return cmd_purge(args)
    return cmd_apply(args)


if __name__ == "__main__":
    sys.exit(main())
