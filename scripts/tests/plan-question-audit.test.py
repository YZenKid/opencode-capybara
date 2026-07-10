#!/usr/bin/env python3
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from plan_question_audit import audit

valid = '{"task_id":"x","event":"question_batch"}\n{"task_id":"x","event":"answer","plan_path":".opencode/plans/x.md"}\n{"task_id":"x","event":"plan_write","plan_path":".opencode/plans/x.md"}\n'
invalid = valid + '{"task_id":"x","event":"question_batch"}\n'
for text, expected in ((valid, True), (invalid, False)):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        f.write(text)
        path = f.name
    ok, _ = audit(path)
    Path(path).unlink()
    if ok != expected:
        raise SystemExit("question audit mismatch")

# also test the fixture files
root = Path(__file__).resolve().parents[2]
ok, _ = audit(str(root / ".opencode" / "evidence" / "20260710-planner-one-pass" / "transaction.jsonl"))
if not ok:
    raise SystemExit("valid fixture should pass")
ok, _ = audit(str(root / "scripts" / "evals" / "fixtures" / "plans" / "bad-transaction.jsonl"))
if ok:
    raise SystemExit("bad fixture should fail")
print("All question audit tests passed.")
