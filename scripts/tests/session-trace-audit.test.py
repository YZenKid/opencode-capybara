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
TMP_ROOT = Path(tempfile.gettempdir())


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

    def test_scope_guard_fixture_matrix(self) -> None:
        cases = [
            ("planner_read_only", "planner_on_read_only"),
            ("mutation_after_audit", "mutation_after_read_only"),
            ("security_audit_stays_read_only", None),
            ("explicit_fix_promotion", None),
            ("tiny_budget_excess", "tiny_budget_exceeded"),
            ("deep_checkpoint_allowed", None),
            ("unknown_schema", "unknown_trace_schema"),
            ("repeated_orientation", "repeated_orientation"),
        ]
        fixture_root = REPO_ROOT / "scripts" / "tests" / "fixtures" / "session-trace"
        for name, expected_code in cases:
            with self.subTest(name=name):
                code, out, err = _run(
                    "--json", str(fixture_root / f"{name}.md")
                )
                data = json.loads(out)
                codes = {finding["code"] for finding in data["findings"]}
                if expected_code:
                    self.assertIn(expected_code, codes)
                    self.assertEqual(code, 1)
                else:
                    self.assertEqual(code, 0, msg=f"{name}: {err or out}")

    def test_graphify_enforcement_fixture_matrix(self) -> None:
        fixture_root = REPO_ROOT / "scripts" / "tests" / "fixtures" / "session-trace"
        cases = [
            ("graphify_query_first", 0, None),
            ("graphify_query_missing", 1, "graphify_query_missing"),
            ("graphify_fallback", 0, None),
            ("graphify_tiny_skip", 0, None),
        ]
        for name, expected_code, finding_code in cases:
            with self.subTest(name=name):
                code, out, err = _run("--json", str(fixture_root / f"{name}.md"))
                data = json.loads(out)
                codes = {finding["code"] for finding in data["findings"]}
                self.assertEqual(code, expected_code, msg=f"{name}: {err or out}")
                if finding_code:
                    self.assertIn(finding_code, codes)

    def test_strict_mode_only_fails_concrete_scope_violations(self) -> None:
        fixture_root = REPO_ROOT / "scripts" / "tests" / "fixtures" / "session-trace"
        unknown = _run("--strict", str(fixture_root / "unknown_schema.md"))
        self.assertEqual(unknown[0], 0)
        unknown_json = json.loads(_run("--json", str(fixture_root / "unknown_schema.md"))[1])
        self.assertEqual(unknown_json["status"], "WARN")
        self.assertIn("unknown_trace_schema", {finding["code"] for finding in unknown_json["findings"]})
        deep = _run("--strict", str(fixture_root / "deep_checkpoint_allowed.md"))
        self.assertEqual(deep[0], 0, msg=deep[2] or deep[1])



if __name__ == "__main__":
    unittest.main()
