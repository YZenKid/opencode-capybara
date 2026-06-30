"""Tests for scripts/session-trace-audit.py.

Run:
    python3 scripts/tests/session-trace-audit.test.py
"""
from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "session-trace-audit.py"
TMP_ROOT = Path("/var/home/ujang")


def _run(*args: str, stdin: str | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["python3", str(SCRIPT), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _tmpdir(prefix: str) -> Path:
    return Path(tempfile.mkdtemp(prefix=prefix, dir=str(TMP_ROOT)))


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


GOOD_ORIENTED = textwrap.dedent("""\
    Skill I'm using: opencode-fixer
    MCPs I'm using: context7
    What I'm checking first: package.json

    confirmed_repo: package.json shows tailwind 4.0.0
    fixed the regression test and shipped a diff.
    """)


MISSING_ORIENTATION_MULTI_ISSUE = textwrap.dedent("""\
    Issue 1: foo failed.
    Issue 2: bar failed.
    Need to debug issue 1 then issue 2.
    No framework reference here.
    """)


class SessionTraceAuditTests(unittest.TestCase):
    def test_strict_mode_fails_on_warn(self) -> None:
        code, out, err = _run("-", stdin=MISSING_ORIENTATION_MULTI_ISSUE)
        self.assertEqual(code, 1, msg=f"non-strict should still fail on WARN; out={out} err={err}")
        code_strict, _, _ = _run(
            "--strict", "-", stdin=MISSING_ORIENTATION_MULTI_ISSUE
        )
        self.assertEqual(code_strict, 1)

    def test_clean_pass_does_not_fail(self) -> None:
        code, out, err = _run("-", stdin=GOOD_ORIENTED)
        self.assertEqual(code, 0, msg=f"expected PASS got {code}: {err or out}")

    def test_memory_reuse_signal(self) -> None:
        root = _tmpdir("trace-mem-")
        memory = json.dumps([
            {
                "id": "memory-tailwind-stack",
                "lesson": "OpenCode projects use tailwind 4 with shadcn new-york registry; tailwindcss identity must be preserved.",
                "tags": ["tailwind", "shadcn", "tokens"],
                "context": "landings",
            }
        ])
        _write(root / ".opencode" / "memory" / "knowledge.json", memory)

        bad = textwrap.dedent("""\
            Skill I'm using: opencode-frontend
            MCPs I'm using: context7
            confirmed_repo: tailwindcss 4.0.0 in package.json
            landing hero went out, ship plan.
        """)
        code_b, out_b, err_b = _run(
            "--project-root", str(root), "--json", "-", stdin=bad
        )
        self.assertEqual(code_b, 1, msg=f"expected WARN; got {code_b}: {err_b or out_b}")
        data = json.loads(out_b)
        codes = {f["code"] for f in data["findings"]}
        self.assertIn("memory_reuse_missed", codes)

        good = textwrap.dedent("""\
            Skill I'm using: opencode-frontend
            MCPs I'm using: context7
            confirmed_repo: tailwindcss 4.0.0 in package.json
            reuses memory-id: memory-tailwind-stack
            landing hero went out, ship plan.
        """)
        code_g, out_g, err_g = _run(
            "--project-root", str(root), "--json", "-", stdin=good
        )
        self.assertEqual(code_g, 0, msg=f"expected PASS; got {code_g}: {err_g or out_g}")


if __name__ == "__main__":
    unittest.main()
