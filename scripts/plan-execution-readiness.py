#!/usr/bin/env python3
"""Validate plan readiness using canonical OpenCode governance scripts.

Tracker resolution checks nonempty OPENCODE_CONFIG_DIR, then
$HOME/.config/opencode, then this script's sibling task-progress.py.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TASK_ID = re.compile(r"^\s*\d+\.\s+\*\*([A-Z][A-Z0-9]*)\*\*")
UPDATE = re.compile(r"python3\s+(?:~/.config/opencode/)?scripts/task-progress\.py\s+([^\s]+)\s+--update\s+([^\s]+)")


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def resolve_tracker_script():
    config_root = os.environ.get("OPENCODE_CONFIG_DIR")
    candidates = []
    if config_root:
        candidates.append(Path(config_root).expanduser() / "scripts/task-progress.py")
    candidates.append(Path(os.path.expanduser("~/.config/opencode/scripts/task-progress.py")))
    candidates.append(Path(__file__).resolve().parent / "task-progress.py")
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return candidates[-1]


def validate(plan_path, project_root):
    text = Path(plan_path).read_text()
    status = re.search(r"^plan_status:\s*(\S+)", text, re.M)
    status = status.group(1) if status else ""
    ids = [m.group(1) for m in map(TASK_ID.match, text.splitlines()) if m]
    if not ids:
        return ["worklist has no numbered task IDs"]
    if len(ids) != len(set(ids)):
        return ["worklist contains duplicate task ID"]
    if status not in {"PASS", "PASS_FOR_SLICE"}:
        return [f"plan status is {status or 'missing'}, not PASS/PASS_FOR_SLICE"]
    errors = []
    tracker_commands = ""
    for line in text.splitlines():
        if any(field in line for field in ("init_command:", "summary_command:", "checklist_command:")):
            tracker_commands += line + "\n"
        elif "|" in line and "task-progress.py" in line and "--update" in line:
            tracker_commands += line + "\n"
    for obsolete in ("--project-root", "--task"):
        if obsolete in tracker_commands:
            errors.append(f"obsolete tracker flag {obsolete}")
    for command in ("init_command:", "summary_command:", "checklist_command:"):
        if command not in tracker_commands:
            errors.append(f"missing {command}")
    updates = UPDATE.findall(tracker_commands)
    mapped = [task for _, task in updates]
    if set(mapped) != set(ids) or len(mapped) != len(ids):
        errors.append(f"task map IDs {mapped} differ from worklist IDs {ids}")
    for task_id in ids:
        if not re.search(rf"\|\s*`?{re.escape(task_id)}`?\s*\|", text):
            errors.append(f"task {task_id} missing owner/evidence/update row")
    disposition = re.search(r"preflight_disposition:\s*`?([^`\s;]+)", text)
    if not disposition:
        errors.append("missing explicit preflight_disposition")
    elif disposition.group(1) == "preset-self":
        if not re.search(r"(?:evidence|purpose|root).{0,180}(?:preset|harness|governance)", text, re.I | re.S):
            errors.append("preset-self requires explicit purpose and file/command evidence")
    elif disposition.group(1) == "target-app":
        required = ["PROJECT_STACK.md", "PROJECT_COMMANDS.md", "FRAMEWORK_PLAYBOOK.md", "PROJECT_DETECTED_TOOLS.md"]
        if not all(Path(project_root, ".opencode/docs", item).exists() for item in required):
            errors.append("target-app preflight missing required PROJECT_* docs")
    else:
        errors.append(f"invalid preflight_disposition {disposition.group(1)}")
    question_state = False
    for line in text.splitlines():
        if re.search(r"(?:unresolved|open|outstanding)\s+(?:material|hard-stop|question|unknown)|(?:material|hard-stop)\s+(?:unresolved|open|outstanding)\s+(?:question|unknown)", line, re.I):
            if not re.search(r"^(?:\d+\.|\s*[-#]|```|{)", line.strip()):
                question_state = True
                break
    if question_state:
        errors.append("unresolved material question blocks PASS")
    if errors:
        return errors
    tracker_script = resolve_tracker_script()
    if not tracker_script.is_file():
        return [f"tracker script not found: checked OPENCODE_CONFIG_DIR, ~/.config/opencode/scripts/, and sibling directory"]
    with tempfile.TemporaryDirectory() as temp:
        result = subprocess.run([sys.executable, str(tracker_script), "readiness-check", "--init", "--plan", str(Path(plan_path).resolve())], cwd=temp, capture_output=True, text=True)
        if result.returncode:
            return [f"tracker init failed: {result.stderr.strip() or result.stdout.strip()}"]
        tracker = Path(temp, ".opencode/state/readiness-check/progress.json")
        if not tracker.exists():
            return ["tracker init did not create isolated progress.json"]
        tracker_ids = [task.get("id") for task in json.loads(tracker.read_text()).get("tasks", [])]
        if tracker_ids != ids:
            return [f"tracker task IDs {tracker_ids} differ from worklist IDs {ids}"]
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan")
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    errors = validate(args.plan, args.project_root)
    if errors:
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: execution readiness validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
