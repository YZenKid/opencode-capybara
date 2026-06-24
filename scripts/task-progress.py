#!/usr/bin/env python3
"""
Task progress tracker for OpenCode plans.

Usage:
  task-progress.py <task-id> --init --plan <plan-path>
  task-progress.py <task-id> --update <task-number> --status <status> [--owner <agent>] [--evidence <path>]
  task-progress.py <task-id> --summary
  task-progress.py <task-id> --checklist

Examples:
  task-progress.py my-feature --init --plan .opencode/plans/my-feature.md
  task-progress.py my-feature --update A1 --status completed --owner @fixer --evidence tests/pass.log
  task-progress.py my-feature --summary
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

STATE_DIR = Path(".opencode/state")


def load_progress(task_id: str) -> dict | None:
    path = STATE_DIR / task_id / "progress.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def save_progress(task_id: str, data: dict):
    state_dir = STATE_DIR / task_id
    state_dir.mkdir(parents=True, exist_ok=True)
    path = state_dir / "progress.json"
    path.write_text(json.dumps(data, indent=2))


def init_progress(task_id: str, plan_path: str):
    """Initialize progress tracker from plan worklist."""
    plan = Path(plan_path)
    if not plan.exists():
        print(f"Error: plan {plan_path} not found", file=sys.stderr)
        sys.exit(1)

    # Extract worklist from plan (simple regex for now)
    import re
    content = plan.read_text()

    # Look for numbered items like "1. **A1** | ..." or "- [ ] A1: ..."
    tasks = []

    # Pattern 1: numbered worklist
    pattern1 = r'(\d+)\.\s+\*\*([A-Z]\d+)\*\*\s*\|\s*`@(\w+)`'
    for match in re.finditer(pattern1, content):
        num, task_id_num, owner = match.groups()
        tasks.append({
            "id": task_id_num,
            "title": f"Task {task_id_num}",
            "status": "pending",
            "owner": f"@{owner}",
            "depends_on": [],
            "started": None,
            "completed": None,
            "evidence": []
        })

    # Pattern 2: checkbox worklist
    pattern2 = r'- \[ \]\s+([A-Z]\d+):\s*(.+?)(?:\s*\|$|$)'
    for match in re.finditer(pattern2, content, re.MULTILINE):
        task_id_num, title = match.groups()
        tasks.append({
            "id": task_id_num,
            "title": title.strip(),
            "status": "pending",
            "owner": None,
            "depends_on": [],
            "started": None,
            "completed": None,
            "evidence": []
        })

    if not tasks:
        print("Warning: no worklist found in plan", file=sys.stderr)
        print("Plan should contain numbered worklist like:", file=sys.stderr)
        print("  1. **A1** | `@fixer` | Description", file=sys.stderr)

    progress = {
        "task_id": task_id,
        "plan_path": plan_path,
        "created": datetime.now().isoformat(),
        "tasks": tasks
    }

    save_progress(task_id, progress)
    print(f"Initialized progress tracker with {len(tasks)} tasks")
    print(f"File: {STATE_DIR / task_id / 'progress.json'}")


def update_task(task_id: str, task_num: str, status: str, owner: str = None, evidence: str = None):
    """Update task status."""
    progress = load_progress(task_id)
    if not progress:
        print(f"Error: progress tracker for {task_id} not found", file=sys.stderr)
        print(f"Run: task-progress.py {task_id} --init --plan <plan-path>", file=sys.stderr)
        sys.exit(1)

    task = next((t for t in progress["tasks"] if t["id"] == task_num), None)
    if not task:
        print(f"Error: task {task_num} not found", file=sys.stderr)
        sys.exit(1)

    task["status"] = status
    if owner:
        task["owner"] = owner
    if status == "in_progress" and not task["started"]:
        task["started"] = datetime.now().isoformat()
    if status in ["completed", "blocked", "cancelled"]:
        task["completed"] = datetime.now().isoformat()
    if evidence:
        task["evidence"].append(evidence)

    save_progress(task_id, progress)
    print(f"Updated {task_num} -> {status}")


def print_summary(task_id: str):
    """Print progress summary."""
    progress = load_progress(task_id)
    if not progress:
        print(f"Error: progress tracker for {task_id} not found", file=sys.stderr)
        sys.exit(1)

    tasks = progress["tasks"]
    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "completed")
    in_progress = sum(1 for t in tasks if t["status"] == "in_progress")
    blocked = sum(1 for t in tasks if t["status"] == "blocked")
    pending = sum(1 for t in tasks if t["status"] == "pending")

    print(f"## Task: {task_id}")
    print(f"Plan: {progress['plan_path']}")
    print(f"Created: {progress['created']}")
    print()
    print(f"### Progress: {completed}/{total} completed")
    print(f"- Completed: {completed}")
    print(f"- In progress: {in_progress}")
    print(f"- Blocked: {blocked}")
    print(f"- Pending: {pending}")
    print()

    if blocked > 0:
        print("### Blocked tasks:")
        for t in tasks:
            if t["status"] == "blocked":
                print(f"- {t['id']}: {t['title']} (owner: {t['owner']})")
        print()

    if in_progress > 0:
        print("### Currently working:")
        for t in tasks:
            if t["status"] == "in_progress":
                print(f"- {t['id']}: {t['title']} (owner: {t['owner']}, started: {t['started']})")
        print()

    if completed > 0:
        print("### Completed:")
        for t in tasks:
            if t["status"] == "completed":
                evidence_str = ", ".join(t["evidence"]) if t["evidence"] else "no evidence"
                print(f"- {t['id']}: {t['title']} (completed: {t['completed']}, {evidence_str})")


def print_checklist(task_id: str):
    """Print markdown checklist."""
    progress = load_progress(task_id)
    if not progress:
        print(f"Error: progress tracker for {task_id} not found", file=sys.stderr)
        sys.exit(1)

    print(f"# Progress Checklist: {task_id}\n")
    for t in progress["tasks"]:
        checkbox = {
            "completed": "x",
            "in_progress": " ",
            "blocked": " ",
            "pending": " ",
            "cancelled": "-"
        }.get(t["status"], " ")

        status_emoji = {
            "completed": "✅",
            "in_progress": "🔄",
            "blocked": "🚫",
            "pending": "⏳",
            "cancelled": "❌"
        }.get(t["status"], "?")

        owner_str = f" ({t['owner']})" if t['owner'] else ""
        print(f"- [{checkbox}] {status_emoji} {t['id']}: {t['title']}{owner_str}")


def main():
    parser = argparse.ArgumentParser(description="Task progress tracker")
    parser.add_argument("task_id", help="Task identifier")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--init", action="store_true", help="Initialize progress tracker")
    group.add_argument("--update", metavar="TASK_NUM", help="Update task status")
    group.add_argument("--summary", action="store_true", help="Print progress summary")
    group.add_argument("--checklist", action="store_true", help="Print markdown checklist")

    parser.add_argument("--plan", help="Plan file path (for --init)")
    parser.add_argument("--status", choices=["pending", "in_progress", "completed", "blocked", "cancelled"], help="New status (for --update)")
    parser.add_argument("--owner", help="Task owner (for --update)")
    parser.add_argument("--evidence", help="Evidence path (for --update)")

    args = parser.parse_args()

    if args.init:
        if not args.plan:
            print("Error: --plan required for --init", file=sys.stderr)
            sys.exit(1)
        init_progress(args.task_id, args.plan)

    elif args.update:
        if not args.status:
            print("Error: --status required for --update", file=sys.stderr)
            sys.exit(1)
        update_task(args.task_id, args.update, args.status, args.owner, args.evidence)

    elif args.summary:
        print_summary(args.task_id)

    elif args.checklist:
        print_checklist(args.task_id)


if __name__ == "__main__":
    main()
