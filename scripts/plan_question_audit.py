#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def audit(path: str) -> tuple[bool, list[str]]:
    errors = []
    ordinary = {}
    answers = {}
    for line_number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        event = json.loads(line)
        task = event.get("task_id")
        kind = event.get("event")
        if kind == "question_batch" and not event.get("hard_stop", False):
            ordinary[task] = ordinary.get(task, 0) + 1
        if kind == "answer":
            answers.setdefault(task, []).append(event.get("plan_path"))
        if kind == "plan_write" and event.get("plan_path") != f".opencode/plans/{task}.md":
            errors.append(f"line {line_number}: non-canonical plan path")
    for task, count in ordinary.items():
        if count > 1:
            errors.append(f"{task}: ordinary question_batch count {count}")
    for task, paths in answers.items():
        expected = f".opencode/plans/{task}.md"
        if any(path != expected for path in paths):
            errors.append(f"{task}: answer path mismatch")
    return not errors, errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: plan_question_audit.py <transaction.jsonl>")
        return 2
    ok, errors = audit(sys.argv[1])
    print("STATUS: PASS" if ok else "STATUS: FAIL")
    for error in errors:
        print(f"- {error}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
