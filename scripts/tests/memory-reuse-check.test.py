"""Tests for scripts/memory-reuse-check.py.

Run:
    python3 scripts/tests/memory-reuse-check.test.py
"""
from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "memory-reuse-check.py"
TMP_ROOT = Path("/var/home/ujang")


def _run(*args: str) -> tuple[int, str, str]:
    proc = subprocess.run(["python3", str(SCRIPT), *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def _tmpdir(prefix: str) -> Path:
    return Path(tempfile.mkdtemp(prefix=prefix, dir=str(TMP_ROOT)))


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


SAMPLE_MEMORY = json.dumps([
    {
        "id": "memory-stack-2024",
        "lesson": "OpenCode stack uses Tailwind 4 with shadcn new-york registry; token conversion must preserve visual identity.",
        "tags": ["tailwind", "shadcn", "tokens"],
        "context": "open-design migration; project Journal.",
    },
    {
        "id": "memory-templates-n19",
        "lesson": "Trafalgar Pug/Gulp/Bootstrap template is blocked from direct reuse by AGENTS.md constraint N19.",
        "tags": ["templates", "n19", "constraint"],
        "context": "Journal templates rules.",
    },
], indent=2)


SUMMARY_WITH_REUSE = textwrap.dedent("""\
    # Evidence summary for landing-2026-06-30

    Skill I'm using: opencode-frontend

    confirmed_repo: package.json#tailwindcss shows Tailwind 4.0.0
    confirmed_repo: templates/dashboard/package.json license MIT

    Memory reuse:
    - reuses memory-id: memory-stack-2024 (Tailwind token identity)
    - reuses memory-id: memory-templates-n19 (N19 constraint)
    """)


SUMMARY_WITHOUT_REUSE = textwrap.dedent("""\
    # Evidence summary for landing-2026-06-30

    Skill I'm using: opencode-frontend

    confirmed_repo: package.json#tailwindcss shows Tailwind 4.0.0
    confirmed_repo: templates/dashboard/package.json license MIT
    """)


class MemoryReuseCheckTests(unittest.TestCase):
    def test_reuse_signals_pass(self) -> None:
        root = _tmpdir("mem-reuse-ok-")
        _write(root / ".opencode" / "memory" / "knowledge.json", SAMPLE_MEMORY)
        ev = _write(root / ".opencode" / "evidence" / "landing-2026-06-30" / "summary.md", SUMMARY_WITH_REUSE)
        code, out, err = _run("--project-root", str(root), "--files", str(ev), "--json")
        self.assertEqual(code, 0, msg=err or out)
        data = json.loads(out)
        self.assertTrue(data["ok"])
        self.assertEqual(data["findings"], [])

    def test_missed_reuse_warns_non_strict(self) -> None:
        root = _tmpdir("mem-reuse-warn-")
        _write(root / ".opencode" / "memory" / "knowledge.json", SAMPLE_MEMORY)
        ev = _write(root / ".opencode" / "evidence" / "landing-2026-06-30" / "summary.md", SUMMARY_WITHOUT_REUSE)
        code, out, err = _run("--project-root", str(root), "--files", str(ev), "--json")
        # non-strict mode: advisory exit 0, but findings present
        self.assertEqual(code, 0, msg=err or out)
        data = json.loads(out)
        self.assertFalse(data["ok"])
        self.assertGreaterEqual(len(data["findings"]), 1)
        codes = {f["code"] for f in data["findings"]}
        self.assertIn("memory_reuse_missed", codes)

    def test_missed_reuse_fails_under_strict(self) -> None:
        root = _tmpdir("mem-reuse-strict-")
        _write(root / ".opencode" / "memory" / "knowledge.json", SAMPLE_MEMORY)
        ev = _write(root / ".opencode" / "evidence" / "landing-2026-06-30" / "summary.md", SUMMARY_WITHOUT_REUSE)
        code, out, err = _run("--project-root", str(root), "--files", str(ev), "--strict")
        self.assertEqual(code, 1)

    def test_missing_memory_store_is_informational(self) -> None:
        root = _tmpdir("mem-reuse-empty-")
        ev = _write(root / ".opencode" / "evidence" / "x" / "summary.md", SUMMARY_WITHOUT_REUSE)
        code, out, err = _run("--project-root", str(root), "--files", str(ev), "--json")
        self.assertEqual(code, 0, msg=err or out)
        data = json.loads(out)
        self.assertEqual(data["memory_entries_loaded"], 0)
        self.assertEqual(data["findings"], [])

    def test_missing_file_is_reported(self) -> None:
        root = _tmpdir("mem-reuse-nofile-")
        code, out, err = _run(
            "--project-root", str(root), "--files", str(root / "does-not-exist.md")
        )
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
