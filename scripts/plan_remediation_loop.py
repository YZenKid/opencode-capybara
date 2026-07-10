#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

from plan_retry_guard import retry_plan_in_place


def validate(plan_path: Path, mode: str) -> tuple[int, str, list[str], str]:
    command = [sys.executable, str(Path(__file__).with_name("validate-plan-depth.py")), str(plan_path), "--mode", mode]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout + result.stderr
    failures = [line.split(":", 1)[0].lstrip("- ") for line in output.splitlines() if "=> FAIL" in line]
    if "RESULT: PASS_FOR_SLICE" in output:
        status = "PASS_FOR_SLICE"
    elif "RESULT: PASS" in output:
        status = "PASS"
    else:
        status = "NEEDS_DEPTH"
    return result.returncode, output, failures, status


def resolve_transaction(task_id: str, project_root: str) -> dict:
    path = Path(project_root) / ".opencode" / "evidence" / task_id / "transaction.jsonl"
    if not path.exists():
        return {"ordinary": [], "hard_stop": False, "audit_ok": True}
    from plan_question_audit import audit
    ok, errors = audit(str(path))
    ordinary = []
    hard_stop = False
    for line in path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("event") == "question_batch":
            if event.get("hard_stop", False):
                hard_stop = True
            else:
                ordinary.append(event)
    return {"ordinary": ordinary, "hard_stop": hard_stop, "audit_ok": ok, "audit_errors": errors}


def run_remediation(plan_path: str, mode: str = "auto", attempts: int = 3, repair=None, evidence_path: str | None = None, transaction: dict | None = None) -> dict:
    path = Path(plan_path).resolve()
    evidence = Path(evidence_path or path.parent.parent / "evidence" / path.stem / "plan-remediation.jsonl")
    evidence.parent.mkdir(parents=True, exist_ok=True)
    records = []
    seen = set()
    for attempt in range(1, attempts + 1):
        code, output, failures, status = validate(path, mode)
        records.append({"attempt": attempt, "status": status, "failures": failures, "plan_path": str(path)})
        if status in {"PASS", "PASS_FOR_SLICE"}:
            result = {"status": status, "attempts": attempt, "plan_path": str(path), "evidence": str(evidence)}
            break
        state = (tuple(failures), path.read_bytes())
        if state in seen:
            result = {"status": "NO_PROGRESS", "attempts": attempt, "plan_path": str(path), "evidence": str(evidence)}
            break
        seen.add(state)
        guard = retry_plan_in_place(str(path), failures, attempts=1)
        if repair is None or not repair(path, failures, attempt):
            result = {"status": "NEEDS_DEPTH", "attempts": attempt, "plan_path": str(path), "evidence": str(evidence)}
            break
    else:
        result = {"status": "NEEDS_DEPTH", "attempts": attempts, "plan_path": str(path), "evidence": str(evidence)}
    evidence.write_text("\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n", encoding="utf-8")
    if transaction is not None and not transaction.get("audit_ok", True):
        result["status"] = "NO_PROGRESS"
        result["audit_errors"] = transaction.get("audit_errors", [])
    result["question_batch"] = (transaction or {"ordinary": [], "hard_stop": False})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("task_id")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--mode", default="auto")
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--transaction-path", default=None)
    args = parser.parse_args()
    plan = Path(args.project_root) / ".opencode" / "plans" / f"{args.task_id}.md"
    transaction = resolve_transaction(args.task_id, args.project_root)
    if args.transaction_path:
        from plan_question_audit import audit
        ok, errors = audit(args.transaction_path)
        transaction = {"ordinary": [], "hard_stop": False, "audit_ok": ok, "audit_errors": errors}
    result = run_remediation(str(plan), args.mode, args.attempts, transaction=transaction)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] in {"PASS", "PASS_FOR_SLICE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
