"""Tests for scripts/mcp-memory-store.py.

Run:
    python3 scripts/tests/mcp-memory-store.test.py
"""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "mcp-memory-store.py"
TMP_ROOT = Path("/var/home/ujang")


def _run(*args: str) -> tuple[int, str, str]:
    proc = subprocess.run(["python3", str(SCRIPT), *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def _tmpdir(prefix: str) -> Path:
    return Path(tempfile.mkdtemp(prefix=prefix, dir=str(TMP_ROOT)))


class McpMemoryStoreTests(unittest.TestCase):
    def test_finalize_creates_local_record(self) -> None:
        root = _tmpdir("mcp-mem-create-")
        code, out, err = _run(
            "--project-root", str(root),
            "--finalize",
            "--task", "landing-2026-06-30",
            "--summary", "Shipped landing hero using dashboard tokens.",
            "--decision", "Use dashboard tokens as source of truth.",
            "--file", "resources/js/pages/welcome.tsx",
            "--claim-level", "done",
            "--json",
        )
        self.assertEqual(code, 0, msg=err or out)
        data = json.loads(out)
        self.assertTrue(data["ok"])
        self.assertIn(data["backend"], {"mcp+local", "local-fallback"})
        self.assertEqual(data["record"]["entity_name"], "task::landing-2026-06-30")
        self.assertTrue((root / ".opencode" / "mcp-memory").exists())

    def test_finalize_same_task_replaces_prior_revision(self) -> None:
        root = _tmpdir("mcp-mem-replace-")
        for summary in ["v1 summary", "v2 summary"]:
            code, out, err = _run(
                "--project-root", str(root),
                "--finalize",
                "--task", "same-task",
                "--summary", summary,
                "--decision", "keep latest only",
                "--claim-level", "done",
                "--json",
            )
            self.assertEqual(code, 0, msg=err or out)
        code, out, err = _run("--project-root", str(root), "--graph", "--json")
        self.assertEqual(code, 0, msg=err or out)
        data = json.loads(out)
        active = [r for r in data["records"] if r["status"] == "active"]
        archived = [r for r in data["records"] if r["status"] == "archived"]
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["revision"], 2)
        # archive is stored in archive.json, record list may or may not retain archived snapshot
        self.assertEqual(active[0]["summary"], "v2 summary")
        archive = json.loads(next((root / ".opencode" / "mcp-memory").glob("*/archive.json")).read_text())
        self.assertGreaterEqual(len(archive), 1)
        self.assertEqual(archive[-1]["archived_reason"], "replaced_by_newer_task_memory")

    def test_search_hits_record(self) -> None:
        root = _tmpdir("mcp-mem-search-")
        _run(
            "--project-root", str(root),
            "--finalize",
            "--task", "tokens-task",
            "--summary", "Tailwind tokens aligned with dashboard source.",
            "--decision", "Keep token identity.",
            "--claim-level", "done",
        )
        code, out, err = _run("--project-root", str(root), "--search", "tailwind", "--json")
        self.assertEqual(code, 0, msg=err or out)
        data = json.loads(out)
        self.assertGreaterEqual(len(data["hits"]), 1)

    def test_cap_archives_oldest(self) -> None:
        root = _tmpdir("mcp-mem-cap-")
        for i in range(3):
            code, out, err = _run(
                "--project-root", str(root),
                "--finalize",
                "--task", f"task-{i}",
                "--summary", f"summary {i}",
                "--decision", "bounded memory",
                "--claim-level", "done",
                "--max-active", "2",
                "--json",
            )
            self.assertEqual(code, 0, msg=err or out)
        bundle = next((root / ".opencode" / "mcp-memory").glob("*"))
        idx = json.loads((bundle / "index.json").read_text())
        archive = json.loads((bundle / "archive.json").read_text())
        active = [r for r in idx["records"] if r["status"] == "active"]
        self.assertLessEqual(len(active), 2)
        self.assertGreaterEqual(len(archive), 1)
        self.assertEqual(archive[-1]["archived_reason"], "cap_exceeded")

    def test_requires_finalize_args(self) -> None:
        root = _tmpdir("mcp-mem-args-")
        code, out, err = _run("--project-root", str(root), "--finalize")
        self.assertEqual(code, 4)


if __name__ == "__main__":
    unittest.main()
