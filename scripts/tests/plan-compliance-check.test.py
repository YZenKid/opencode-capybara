"""Tests for scripts/plan-compliance-check.py.

Run:
    python3 scripts/tests/plan-compliance-check.test.py
"""
from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "plan-compliance-check.py"
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


PLAN_WITH_VALID_HANDOFF = textwrap.dedent("""\
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
  evidence_required: [.opencode/evidence/landing-2026-06-30/template-extraction-trace.md]
  depends_on: [catalog-decision]
  context_bundle: [DESIGN.md, .opencode/AGENTS.md, templates/dashboard/src/index.css]
```
""")

PLAN_BAD = textwrap.dedent("""\
# Plan: bad

## Goal
No worklist or handoff here.
""")


class PlanComplianceTests(unittest.TestCase):
    def test_valid_plan_returns_ok_with_notes(self) -> None:
        root = _tmpdir("plan-compliance-ok-")
        plan = _write(root / ".opencode" / "plans" / "landing-2026-06-30.md", PLAN_WITH_VALID_HANDOFF)
        code, out, err = _run("--project-root", str(root), "--plan", str(plan), "--json")
        self.assertEqual(code, 0, msg=err or out)
        data = json.loads(out)
        self.assertTrue(data["ok"])
        self.assertEqual(data["handoff_checked"], 1)

    def test_bad_plan_fails(self) -> None:
        root = _tmpdir("plan-compliance-bad-")
        plan = _write(root / ".opencode" / "plans" / "bad.md", PLAN_BAD)
        code, out, err = _run("--project-root", str(root), "--plan", str(plan))
        self.assertEqual(code, 1)
        self.assertIn("missing execution handoff/worklist marker", out)


if __name__ == "__main__":
    unittest.main()
