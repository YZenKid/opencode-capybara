#!/usr/bin/env python3
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/plan-execution-readiness.py"

BASE = """---
plan_status: PASS_FOR_SLICE
---
## Worklist

1. **A1** | `@fixer` | Build validator
2. **A2** | `@quality-gate` | Align contracts

## Progress Tracking

- preflight_disposition: `preset-self`
- purpose: governance validator for planner/start-work contract
- evidence: ~/.config/opencode/scripts/task-progress.py is authoritative CLI; commands/init-harness.md is non-executable workflow
- init_command: `python3 ~/.config/opencode/scripts/task-progress.py demo --init --plan plan.md`
- summary_command: `python3 ~/.config/opencode/scripts/task-progress.py demo --summary`
- checklist_command: `python3 ~/.config/opencode/scripts/task-progress.py demo --checklist`
- update_rules: at every status transition and evidence write

| ID | Owner | Evidence | Update command |
| --- | --- | --- | --- |
| A1 | `@fixer` | `A1.md` | `python3 ~/.config/opencode/scripts/task-progress.py demo --update A1 --status completed --owner @fixer --evidence A1.md` |
| A2 | `@fixer` | `A2.md` | `python3 ~/.config/opencode/scripts/task-progress.py demo --update A2 --status completed --owner @fixer --evidence A2.md` |
"""


def run(content):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d) / "project-root"
        root.mkdir()
        plan = Path(d) / "plan.md"
        plan.write_text(content)
        return subprocess.run([sys.executable, str(VALIDATOR), str(plan), "--project-root", str(root)], capture_output=True, text=True)


def check(name, content, expected):
    result = run(content)
    assert result.returncode == expected, f"{name}: {result.returncode}\n{result.stdout}\n{result.stderr}"
    return result.stdout + result.stderr


spec = importlib.util.spec_from_file_location("plan_execution_readiness", VALIDATOR)
assert spec is not None and spec.loader is not None
validator_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator_mod)

def fake_tracker_run(*args, **kwargs):
    from pathlib import Path
    import subprocess
    tracker = Path(kwargs["cwd"]) / ".opencode/state/readiness-check/progress.json"
    tracker.parent.mkdir(parents=True, exist_ok=True)
    tracker.write_text('{"tasks": [{"id": "A1"}, {"id": "B2"}]}')
    return subprocess.CompletedProcess(args, 0, "", "")


def check_tracker_parity_mismatch():
    import unittest.mock
    with tempfile.TemporaryDirectory() as d:
        plan = Path(d) / "plan.md"
        plan.write_text(BASE)
        with unittest.mock.patch.object(validator_mod.subprocess, "run", side_effect=fake_tracker_run):
            errors = validator_mod.validate(str(plan), ROOT)
    assert any("differ from worklist IDs" in error for error in errors), f"Expected parity error; got {errors}"


def check_config_root_resolver_selects_actual_script():
    with tempfile.TemporaryDirectory() as d:
        script = Path(d) / "scripts/task-progress.py"
        script.parent.mkdir()
        script.write_text("tracker")
        with mock.patch.dict("os.environ", {"OPENCODE_CONFIG_DIR": d}, clear=False):
            selected = validator_mod.resolve_tracker_script()
    assert selected == script, f"Expected configured tracker script; got {selected}"


def check_config_root_resolver_falls_back_to_sibling():
    with tempfile.TemporaryDirectory() as d:
        fake_home = Path(d) / "home"
        fake_home.mkdir()
        sibling_dir = Path(d) / "sibling"
        sibling_dir.mkdir()
        sibling_script = sibling_dir / "task-progress.py"
        sibling_script.write_text("tracker")
        with mock.patch.dict("os.environ", {"OPENCODE_CONFIG_DIR": str(Path(d) / "nonexistent"), "HOME": str(fake_home)}, clear=False), mock.patch.object(validator_mod, "__file__", str(sibling_script)):
            selected = validator_mod.resolve_tracker_script()
        assert selected == sibling_script, f"Expected sibling fallback; got {selected}"


check("obsolete tracker syntax", BASE.replace("--init --plan", "--project-root . --task demo --init --plan"), 1)
check("prose obsolete flags", BASE.replace("## Worklist", "## Confirmed Facts\nTracker used `--project-root . --task demo` before positional syntax.\n\n## Worklist"), 0)
check("task map mismatch", BASE.replace("| A2 |", "| B2 |"), 1)
check("invalid preflight", BASE.replace("preset-self", "target-app"), 1)
assert check("valid preset-self", BASE, 0).startswith("PASS")
check("unresolved question", BASE + "material unknown remains unresolved question", 1)
check_tracker_parity_mismatch()
check_config_root_resolver_selects_actual_script()
check_config_root_resolver_falls_back_to_sibling()
print("9 readiness fixtures passed")
