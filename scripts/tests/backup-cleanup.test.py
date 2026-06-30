"""Tests for scripts/backup-cleanup.py.

Run:
    python3 scripts/tests/backup-cleanup.test.py
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "backup-cleanup.py"
SCRATCH_ROOT = Path("/var/home/ujang")


def _run(*args: str) -> tuple[int, str, str]:
    proc = subprocess.run(["python3", str(SCRIPT), *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def _tmprepo(prefix: str) -> Path:
    root = Path(tempfile.mkdtemp(prefix=prefix, dir=str(SCRATCH_ROOT)))
    (root / "backups").mkdir(parents=True, exist_ok=True)
    (root / "opencode-capybara" / "backups").mkdir(parents=True, exist_ok=True)
    return root


def _mkbackup(path: Path, age_days: int, size_kb: int = 1) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    blob = path / "blob.bin"
    blob.write_bytes(b"x" * 1024 * size_kb)
    ts = time.time() - age_days * 86400
    os.utime(path, (ts, ts))
    os.utime(blob, (ts, ts))
    return path


class BackupCleanupTests(unittest.TestCase):
    def test_scan_lists_old_entries(self) -> None:
        root = _tmprepo("backup-scan-")
        try:
            _mkbackup(root / "backups" / "old-one", age_days=5)
            _mkbackup(root / "opencode-capybara" / "backups" / "mirror-old", age_days=4)
            code, out, err = _run("--repo-root", str(root), "--scan", "--trash-age-days", "3")
            self.assertEqual(code, 0, msg=err or out)
            data = json.loads(out)
            self.assertEqual(data["trashable_now"], 2)
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_trash_moves_old_entries(self) -> None:
        root = _tmprepo("backup-trash-")
        try:
            old_repo = _mkbackup(root / "backups" / "old-one", age_days=5)
            old_mirror = _mkbackup(root / "opencode-capybara" / "backups" / "mirror-old", age_days=6)
            code, out, err = _run("--repo-root", str(root), "--trash", "--trash-age-days", "3")
            self.assertEqual(code, 0, msg=err or out)
            data = json.loads(out)
            self.assertEqual(data["trashed"], 2)
            self.assertFalse(old_repo.exists())
            self.assertFalse(old_mirror.exists())
            trash_dir = root / "backups" / ".trash"
            self.assertTrue(trash_dir.exists())
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_purge_removes_old_trash_dirs(self) -> None:
        root = _tmprepo("backup-purge-")
        try:
            trash_day = root / "backups" / ".trash" / "2026-01-01"
            _mkbackup(trash_day / "repo" / "old-one", age_days=30)
            code, out, err = _run("--repo-root", str(root), "--purge", "--purge-age-days", "14")
            self.assertEqual(code, 0, msg=err or out)
            data = json.loads(out)
            self.assertEqual(data["purged"], 1)
            self.assertFalse(trash_day.exists())
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_apply_runs_trash_then_purge(self) -> None:
        root = _tmprepo("backup-apply-")
        try:
            _mkbackup(root / "backups" / "old-one", age_days=5)
            trash_day = root / "backups" / ".trash" / "2026-01-01"
            _mkbackup(trash_day / "repo" / "very-old", age_days=30)
            code, out, err = _run("--repo-root", str(root), "--apply", "--trash-age-days", "3", "--purge-age-days", "14")
            self.assertEqual(code, 0, msg=err or out)
            data = json.loads(out)
            self.assertGreaterEqual(data["trashed"], 1)
            self.assertGreaterEqual(data["purged"], 1)
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def test_keep_prefix_is_respected(self) -> None:
        root = _tmprepo("backup-keep-")
        try:
            keep = _mkbackup(root / "backups" / "keep-important", age_days=10)
            code, out, err = _run("--repo-root", str(root), "--trash", "--trash-age-days", "3", "--keep-prefix", "keep-")
            self.assertEqual(code, 0, msg=err or out)
            self.assertTrue(keep.exists())
            data = json.loads(out)
            self.assertEqual(data["skipped"], 1)
        finally:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
