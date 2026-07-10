#!/usr/bin/env python3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from plan_remediation_loop import resolve_transaction, run_remediation


def plan(text):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False)
    f.write(text)
    f.close()
    return Path(f.name)

failures = 0
with tempfile.TemporaryDirectory() as root:
    project = Path(root)
    plan_path = project / ".opencode" / "plans" / "task.md"
    plan_path.parent.mkdir(parents=True)
    plan_path.write_text((Path(__file__).resolve().parents[2] / ".opencode/plans/20260710-planner-one-pass.md").read_text(), encoding="utf-8")
    tx = project / ".opencode" / "evidence" / "task" / "transaction.jsonl"
    tx.parent.mkdir(parents=True)
    tx.write_text('{"task_id":"task","event":"question_batch","hard_stop":false}\n', encoding="utf-8")
    transaction = resolve_transaction("task", root)
    result = run_remediation(str(plan_path), transaction=transaction)
    if result["question_batch"]["ordinary"] != [{"task_id": "task", "event": "question_batch", "hard_stop": False}]:
        print("✗ transaction ordinary batch not returned")
        failures += 1
    tx.write_text('{"task_id":"task","event":"question_batch","hard_stop":false}\n{"task_id":"task","event":"question_batch","hard_stop":false}\n', encoding="utf-8")
    duplicate = run_remediation(str(plan_path), transaction=resolve_transaction("task", root))
    if duplicate["status"] != "NO_PROGRESS":
        print(f"✗ duplicate transaction status: {duplicate['status']}")
        failures += 1
    else:
        print("✓ transaction batch and duplicate audit")
p = plan("# Plan\n## Goal\nsmall\n")
def noop(_, __, ___):
    return True
r = run_remediation(str(p), attempts=2, repair=noop)
if r["status"] != "NO_PROGRESS":
    print(f"✗ unchanged plan: {r['status']}")
    failures += 1
else:
    print("✓ unchanged plan: NO_PROGRESS")
p.unlink()

p = plan("# Plan\n## Goal\nsmall\n")
r = run_remediation(str(p), attempts=1)
if r["status"] != "NEEDS_DEPTH":
    print(f"✗ bounded failure: {r['status']}")
    failures += 1
else:
    print("✓ bounded failure: NEEDS_DEPTH")
p.unlink()

p = plan("# Plan\n## Goal\nsmall\n")
def recover(path, _, __):
    path.write_text("# Plan\n## Mode\n`plan_profile: maintenance`\n## Goal\nThis small maintenance plan fixes regression safely with bounded validation and preserves existing behavior. All changes are minimal and safe.\n## Requirements\n1. done\n2. done\n3. done\n4. done\n5. done\n6. done\n7. done\n8. done\n## Acceptance Criteria\n1. done\n2. done\n3. done\n4. done\n5. done\n6. done\n## Implementation Steps\n1. done\n2. done\n3. done\n4. done\n## Validation Commands\n1. done\n2. done\n3. done\n## Existing Patterns/Reuse\nrepo\n## Source Anatomy\nrepo\n## Reference Map\n- repo\n## Decisions/Assumptions\nassumption\n## Execution Source of Truth\nrepo\n## Execution-ready Worklist / Handoff Contract\nready\n## Evidence Requirements\nevidence\n## Done Criteria\ndone\n", encoding="utf-8")
    return True
r = run_remediation(str(p), attempts=2, repair=recover)
if r["status"] != "PASS":
    print(f"✗ recovery: {r['status']}")
    failures += 1
else:
    print("✓ recovery: PASS")
p.unlink()

if failures:
    raise SystemExit(1)
print("All remediation loop tests passed.")
