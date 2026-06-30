"""Tests for scripts/subagent-handoff-check.py.

Run:
    python3 scripts/tests/subagent-handoff-check.test.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "subagent-handoff-check.py"
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


VALID_PAYLOAD = textwrap.dedent(
    """\
    task_id: landing-2026-06-30
    plan_id: landing-2026-06-30
    caller: orchestrator
    callee: frontend
    scope: Implement landing hero + 3 feature sections + CTA
    claim_level: scoped
    claim_scope: hero+features+CTA only, no testimonials/pricing
    source_basis: [templates/dashboard/src/index.css, .opencode/AGENTS.md#N17]
    must_preserve: [Token identity with templates/dashboard/src/index.css, Shadcn new-york registry (N9)]
    do_not_touch: [templates/landingpage/, .env, package.json deps outside UI]
    validation: [npm run check:template-source, npm run check:agents]
    exit_criteria: [Template extraction trace present, No fake testimonials]
    evidence_required: [.opencode/evidence/landing-2026-06-30/template-extraction-trace.md, .opencode/evidence/landing-2026-06-30/visual-rubric.md]
    depends_on: [catalog-decision]
    context_bundle: [DESIGN.md, .opencode/AGENTS.md, templates/dashboard/src/index.css]
    """
)

BAD_CLAIM_LEVEL = textwrap.dedent(
    """\
    task_id: x
    plan_id: x
    caller: orchestrator
    callee: frontend
    scope: Implement x
    claim_level: finished-finished
    claim_scope: x only
    source_basis: [README.md]
    must_preserve: [Keep API stable]
    do_not_touch: [../secrets]
    validation: [npm test]
    exit_criteria: [Tests pass]
    evidence_required: [.opencode/evidence/x/out.md]
    depends_on: [none]
    context_bundle: [README.md]
    """
)

MISSING_REQUIRED = textwrap.dedent(
    """\
    task_id: x
    caller: orchestrator
    scope: Implement x
    claim_level: scoped
    """
)

UNKNOWN_LANE = textwrap.dedent(
    """\
    task_id: x
    plan_id: x
    caller: orchestrator
    callee: wizard
    scope: Implement x
    claim_level: scoped
    claim_scope: x only
    source_basis: [README.md]
    must_preserve: [Keep API stable]
    do_not_touch: [src/legacy]
    validation: [npm test]
    exit_criteria: [Tests pass]
    evidence_required: [.opencode/evidence/x/out.md]
    depends_on: [none]
    context_bundle: [README.md]
    """
)

PLAN_WITH_VALID_HANDOFF = textwrap.dedent(
    """\
    # Plan: landing-2026-06-30

    ## Goal
    Ship bounded landing slice.

    ## Execution-ready Worklist / Handoff Contract

    ```yaml
    handoff:
      task_id: landing-2026-06-30
      plan_id: landing-2026-06-30
      caller: orchestrator
      callee: frontend
      scope: Implement landing hero + 3 feature sections + CTA
      claim_level: scoped
      claim_scope: hero+features+CTA only, no testimonials/pricing
      source_basis: [templates/dashboard/src/index.css, .opencode/AGENTS.md#N17]
      must_preserve: [Token identity with templates/dashboard/src/index.css, Shadcn new-york registry (N9)]
      do_not_touch: [templates/landingpage/, .env, package.json deps outside UI]
      validation: [npm run check:template-source, npm run check:agents]
      exit_criteria: [Template extraction trace present, No fake testimonials]
      evidence_required: [.opencode/evidence/landing-2026-06-30/template-extraction-trace.md, .opencode/evidence/landing-2026-06-30/visual-rubric.md]
      depends_on: [catalog-decision]
      context_bundle: [DESIGN.md, .opencode/AGENTS.md, templates/dashboard/src/index.css]
    ```
    """
)

PLAN_WITH_BAD_HANDOFF = textwrap.dedent(
    """\
    # Plan: bad

    ## Execution-ready Worklist / Handoff Contract

    ```yaml
    handoff:
      task_id: bad
      caller: orchestrator
      callee: sorcerer
      scope: Do x
      claim_level: complete-complete
    ```
    """
)

PLAN_WITHOUT_HANDOFF = textwrap.dedent(
    """\
    # Plan: no-handoff

    ## Goal
    Nothing here yet.
    """
)


class SubagentHandoffCheckTests(unittest.TestCase):
    def test_requires_payload_or_plan(self) -> None:
        code, out, err = _run()
        self.assertEqual(code, 4)
        self.assertIn("pass --payload <file> or --plan <file>", err)

    def test_valid_payload_from_stdin(self) -> None:
        code, out, err = _run("--payload", "-", "--project-root", str(REPO_ROOT), stdin=VALID_PAYLOAD)
        self.assertEqual(code, 0, msg=err or out)
        self.assertIn("OK (1 payload(s) valid)", out)

    def test_missing_required_fields_fails(self) -> None:
        code, out, err = _run("--payload", "-", "--project-root", str(REPO_ROOT), stdin=MISSING_REQUIRED)
        self.assertEqual(code, 1)
        # schema validator runs first; either schema-form or legacy-form is acceptable
        self.assertTrue(
            "callee" in out and ("required" in out or "missing" in out),
            msg=out,
        )
        self.assertIn("missing recommended field: source_basis", out)

    def test_unknown_lane_and_bad_claim_level_fail(self) -> None:
        code, out, err = _run("--payload", "-", "--project-root", str(REPO_ROOT), stdin=UNKNOWN_LANE)
        self.assertEqual(code, 1)
        self.assertIn("not in the OpenCode lane allowlist", out)

        code, out, err = _run("--payload", "-", "--project-root", str(REPO_ROOT), stdin=BAD_CLAIM_LEVEL)
        self.assertEqual(code, 1)
        self.assertIn("claim_level='finished-finished' invalid", out)
        self.assertIn("path traversal", out)

    def test_valid_plan_file_passes(self) -> None:
        tmp = _tmpdir("handoff-plan-ok-")
        plan = _write(tmp / "plan-ok.md", PLAN_WITH_VALID_HANDOFF)
        code, out, err = _run("--plan", str(plan), "--project-root", str(REPO_ROOT))
        self.assertEqual(code, 0, msg=err or out)
        self.assertIn("OK (1 payload(s) valid)", out)

    def test_invalid_plan_file_fails(self) -> None:
        tmp = _tmpdir("handoff-plan-bad-")
        plan = _write(tmp / "plan-bad.md", PLAN_WITH_BAD_HANDOFF)
        code, out, err = _run("--plan", str(plan), "--project-root", str(REPO_ROOT))
        self.assertEqual(code, 1)
        self.assertIn("missing recommended field", out)
        self.assertIn("not in the OpenCode lane allowlist", out)
        self.assertIn("claim_level='complete-complete' invalid", out)

    def test_directory_scan_handles_multiple_plans(self) -> None:
        tmp = _tmpdir("handoff-plan-dir-")
        _write(tmp / "ok.md", PLAN_WITH_VALID_HANDOFF)
        _write(tmp / "none.md", PLAN_WITHOUT_HANDOFF)
        code, out, err = _run("--plan", str(tmp), "--project-root", str(REPO_ROOT))
        self.assertEqual(code, 0, msg=err or out)
        self.assertIn("OK (1 payload(s) valid)", out)

    def test_json_output(self) -> None:
        code, out, err = _run("--payload", "-", "--project-root", str(REPO_ROOT), "--json", stdin=VALID_PAYLOAD)
        self.assertEqual(code, 0, msg=err or out)
        data = json.loads(out)
        self.assertTrue(data["ok"])
        self.assertEqual(data["checked"], 1)
        self.assertEqual(data["errors"], [])


if __name__ == "__main__":
    unittest.main()
