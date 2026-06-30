#!/usr/bin/env python3
"""Pre-quality-gate plan compliance checker.

This script is the mechanical checkpoint between execution and @quality-gate:
it validates that the plan still matches what execution claims happened.

Checks:
- Plan exists and contains execution handoff/worklist markers
- Embedded handoff payloads, if present, validate via subagent-handoff-check.py
- Progress tracker exists (when non-trivial work claims execution happened)
- Delegation log validates cleanly when present
- Evidence paths referenced by embedded handoffs exist or are explicitly absent

This is intentionally conservative. It does not try to understand every plan
style; it only guards against the most common silent failures.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_CHECKER = REPO_ROOT / "scripts" / "subagent-handoff-check.py"
DELEGATION_LOG = REPO_ROOT / "scripts" / "delegation-log.py"

TASK_ID_RE = re.compile(r"(?m)^#\s+Plan:\s+([A-Za-z0-9_.\-]+)\s*$")
HAS_WORKLIST_MARKER = re.compile(r"Execution-ready Worklist / Handoff Contract|Executor Handoff Prompt")
STATE_ROOT = Path(".opencode/state")


def run(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def infer_task_id(plan: Path) -> str:
    text = plan.read_text(encoding="utf-8", errors="replace")
    m = TASK_ID_RE.search(text)
    if m:
        return m.group(1)
    return plan.stem


def progress_path(project_root: Path, task_id: str) -> Path:
    return project_root / ".opencode" / "state" / task_id / "progress.json"


def delegation_log_path(project_root: Path, task_id: str) -> Path:
    return project_root / ".opencode" / "state" / task_id / "delegation.jsonl"


def main() -> int:
    ap = argparse.ArgumentParser(description="Plan compliance checker")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--plan", required=True)
    ap.add_argument("--task-id", help="override task id; default from plan stem/title")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    plan = (project_root / args.plan).resolve() if not Path(args.plan).is_absolute() else Path(args.plan)
    if not plan.is_file():
        print(f"error: plan file not found: {args.plan}", file=sys.stderr)
        return 4

    text = plan.read_text(encoding="utf-8", errors="replace")
    task_id = args.task_id or infer_task_id(plan)
    issues: list[str] = []
    notes: list[str] = []

    if not HAS_WORKLIST_MARKER.search(text):
        issues.append("plan missing execution handoff/worklist marker")

    # Validate embedded handoffs if present
    handoff_cmd = [
        sys.executable,
        str(HANDOFF_CHECKER),
        "--plan",
        str(plan),
        "--project-root",
        str(project_root),
        "--json",
    ]
    code, out, err = run(handoff_cmd, project_root)
    try:
        handoff_report = json.loads(out) if out.strip() else {"checked": 0, "errors": []}
    except json.JSONDecodeError:
        handoff_report = {"checked": 0, "errors": [err or out or "handoff report unreadable"]}
    if code != 0:
        for e in handoff_report.get("errors", []):
            issues.append(f"handoff: {e}")
    elif handoff_report.get("checked", 0) == 0:
        notes.append("no embedded handoff payloads found in plan")

    # Progress tracker should exist for non-trivial execution-bound plans
    prog = progress_path(project_root, task_id)
    if prog.is_file():
        try:
            pdata = json.loads(prog.read_text(encoding="utf-8"))
            if not isinstance(pdata.get("tasks", []), list):
                issues.append("progress tracker malformed: tasks must be a list")
        except json.JSONDecodeError:
            issues.append("progress tracker malformed JSON")
    else:
        notes.append(f"progress tracker not found: {prog}")

    # Delegation log, if present, must validate cleanly
    dlog = delegation_log_path(project_root, task_id)
    if dlog.is_file():
        dcmd = [
            sys.executable,
            str(DELEGATION_LOG),
            "--project-root",
            str(project_root),
            "--task",
            task_id,
            "--validate",
            "--json",
        ]
        dcode, dout, derr = run(dcmd, project_root)
        try:
            drep = json.loads(dout) if dout.strip() else {"errors": []}
        except json.JSONDecodeError:
            drep = {"errors": [derr or dout or "delegation log report unreadable"]}
        if dcode != 0:
            for e in drep.get("errors", []):
                issues.append(f"delegation-log: {e}")
    else:
        notes.append(f"delegation log not found: {dlog}")

    report: dict[str, Any] = {
        "plan": str(plan),
        "task_id": task_id,
        "ok": not issues,
        "issues": issues,
        "notes": notes,
        "handoff_checked": handoff_report.get("checked", 0),
        "progress_path": str(prog),
        "delegation_log": str(dlog),
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        if issues:
            print(f"FAIL ({len(issues)} issue(s)):")
            for i in issues:
                print(f"  - {i}")
        else:
            print("OK")
            for n in notes:
                print(f"  note: {n}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
