"""Tests for scripts/delegation-log.py.

Run:
    python3 scripts/tests/delegation-log.test.py
"""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "delegation-log.py"
TMP_ROOT = Path("/var/home/ujang")


def _run(*args: str) -> tuple[int, str, str]:
    proc = subprocess.run(["python3", str(SCRIPT), *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def _tmpdir(prefix: str) -> Path:
    return Path(tempfile.mkdtemp(prefix=prefix, dir=str(TMP_ROOT)))


class DelegationLogTests(unittest.TestCase):
    def test_record_validate_summary_roundtrip(self) -> None:
        root = _tmpdir("deleg-log-")
        code, out, err = _run(
            "--project-root", str(root),
            "--task", "landing-1",
            "--record",
            "--caller", "orchestrator",
            "--callee", "frontend",
            "--scope", "Implement landing hero",
            "--claim-level", "scoped",
            "--kind", "delegate",
            "--handoff", ".opencode/handoffs/landing-1.yaml",
            "--evidence", ".opencode/evidence/landing-1/handoff.md",
        )
        self.assertEqual(code, 0, msg=err or out)

        code, out, err = _run("--project-root", str(root), "--task", "landing-1", "--validate")
        self.assertEqual(code, 0, msg=err or out)
        self.assertIn("OK", out)

        code, out, err = _run("--project-root", str(root), "--task", "landing-1", "--summary", "--json")
        self.assertEqual(code, 0, msg=err or out)
        data = json.loads(out)
        self.assertEqual(data["records"], 1)
        self.assertEqual(data["by_lane"].get("frontend"), 1)

    def test_invalid_lane_rejected(self) -> None:
        root = _tmpdir("deleg-log-bad-")
        code, out, err = _run(
            "--project-root", str(root),
            "--task", "x",
            "--record",
            "--caller", "orchestrator",
            "--callee", "wizard",
            "--scope", "Do x",
            "--claim-level", "scoped",
        )
        self.assertEqual(code, 2)
        self.assertIn("not in lane allowlist", err)

    def test_validate_detects_bad_json_line(self) -> None:
        root = _tmpdir("deleg-log-json-")
        path = root / ".opencode" / "state" / "x" / "delegation.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('{"ok":1}\nnot-json\n', encoding="utf-8")
        code, out, err = _run("--project-root", str(root), "--task", "x", "--validate")
        self.assertEqual(code, 1)
        self.assertIn("invalid JSON", out)


if __name__ == "__main__":
    unittest.main()
