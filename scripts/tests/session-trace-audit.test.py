"""Tests for scripts/session-trace-audit.py.

Run: python3 scripts/tests/session-trace-audit.test.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "session-trace-audit.py"


def _run(*args: str, stdin: str | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["python3", str(SCRIPT), *args],
        capture_output=True, text=True, input=stdin
    )
    return proc.returncode, proc.stdout, proc.stderr


def _tmpfile(content: str) -> Path:
    p = Path(tempfile.mkdtemp(prefix="trace-test-", dir="/var/home/ujang")) / "transcript.md"
    p.parent.mkdir(exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


# --- Fixtures that mimic the fppnDa05 session shape ---

FPPNDA05_BROKEN = """
# Session fppnDa05

User: I'm getting 409/400 errors on PUT /api/v1/courier/logistic/shippings/{id}/status.

## Issue 1: 409 "transisi status tidak valid"
Root cause: tryAutoPromote() in logistic_repository.go line 415-422 auto-promotes
PickingUp -> Delivering when all legs are PickedUp.

## Issue 2: 400 "leg sudah pernah dipickup"
After patch removed auto-promote, leg Sumber Rezeki was still PickedUp from first call.

## Issue 3: Schema Drift (DB Lokal)
shipping_status_notifications missing, shipping_order_photos missing columns.

## Issue 4: NOT NULL Constraint Violation (Production 500)
photo_url NOT NULL constraint fails on insert.

## Patches
- Commit 6481326: removed tryAutoPromote()
- Commit 93ae558: 2-call flow patch
- Commit 2b4d7b4: manual SQL migration

`atlas migrate apply --env local` ran in 21.77ms. Tests added: RT-04b, RT-04c, RT-04d.
"""


FPPNDA05_FIXED = """
# Session fppnDa05

Skill I'm using: opencode-backend
MCPs I'm using: sequential-thinking, context7
What I'm checking first: state machine in logistic_repository.go + atlas migration history
Not using grep_app: local grep across logistic_repository.go answered it quickly.
Not using playwright: backend-only flow, no browser surface.
Used local grep on logistic_repository.go and migration files.

## Issue 1: 409 "transisi status tidak valid"
Used sequential-thinking to frame 4 issues.
Used context7 to confirm atlas migration syntax.
Root cause: tryAutoPromote() in logistic_repository.go line 415-422.
Skill activation: backend skill pushed us to use repository pattern + regression test guards.

## Issue 2: 400 "leg sudah pernah dipickup"
Backend skill reminded us: separate the pickup-phase from the photo-phase.

## Issue 3: Schema Drift
context7 confirmed atlas syntax for ADD COLUMN IF NOT EXISTS.

## Issue 4: NOT NULL Constraint
Added ALTER COLUMN photo_url DROP NOT NULL.

Skill activation audit: backend skill changed the choice of regression test
naming (RT-04b/c/d vs ad-hoc labels).
MCP usage: sequential-thinking framed the 4 issues; context7 confirmed atlas syntax.
"""


class TestSessionTraceAudit(unittest.TestCase):
    def test_broken_session_flags_defects(self):
        p = _tmpfile(FPPNDA05_BROKEN)
        try:
            rc, out, _ = _run(str(p))
            self.assertEqual(rc, 1)  # WARN
            data = json.loads(_run(str(p), "--json")[1])
            codes = [f["code"] for f in data["findings"]]
            self.assertIn("missing_orientation", codes)
            self.assertIn("missing_sequential_thinking", codes)
            self.assertIn("missing_context7", codes)
        finally:
            import shutil; shutil.rmtree(p.parent)

    def test_fixed_session_passes(self):
        p = _tmpfile(FPPNDA05_FIXED)
        try:
            rc, out, _ = _run(str(p))
            self.assertEqual(rc, 0)
            self.assertIn("PASS", out)
            data = json.loads(_run(str(p), "--json")[1])
            self.assertEqual(data["status"], "PASS")
        finally:
            import shutil; shutil.rmtree(p.parent)

    def test_stdin_pipe(self):
        rc, out, _ = _run("-", stdin="Minor question: how to format JSON?")
        # No obvious task signals -> no findings -> PASS
        self.assertEqual(rc, 0)
        self.assertIn("PASS", out)

    def test_loaded_skill_but_not_activated(self):
        text = """
        Skill I'm using: opencode-backend
        Primary skill: opencode-backend

        ## Diagnosis
        The bug is in the handler.
        """
        p = _tmpfile(text)
        try:
            data = json.loads(_run(str(p), "--json")[1])
            codes = [f["code"] for f in data["findings"]]
            self.assertIn("skill_loaded_but_not_activated", codes)
        finally:
            import shutil; shutil.rmtree(p.parent)

    def test_skip_reason_suppresses_warning(self):
        text = """
        MCPs I'm using: sequential-thinking
        Skip sequential-thinking tool unavailable in this env.
        Fallback: framed scope manually.

        Multi-issue: 1, 2, 3 error count 5.
        """
        p = _tmpfile(text)
        try:
            data = json.loads(_run(str(p), "--json")[1])
            codes = [f["code"] for f in data["findings"]]
            self.assertNotIn("missing_sequential_thinking", codes)
        finally:
            import shutil; shutil.rmtree(p.parent)

    def test_signals_detected(self):
        text = """
        Schema drift: missing table.
        Atlas migration needed.
        Issue 1: something.
        Issue 2: another.
        """
        p = _tmpfile(text)
        try:
            data = json.loads(_run(str(p), "--json")[1])
            self.assertTrue(data["signals"]["multi_issue"])
            self.assertTrue(data["signals"]["version_sensitive"])
        finally:
            import shutil; shutil.rmtree(p.parent)


if __name__ == "__main__":
    unittest.main(verbosity=2)
