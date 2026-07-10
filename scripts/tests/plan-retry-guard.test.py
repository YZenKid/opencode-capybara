#!/usr/bin/env python3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from plan_retry_guard import retry_plan_in_place

failures = 0

# 1. Same content + same failures = NO_PROGRESS
with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
    f.write("# test\n## Goal\ntest\n")
    p = f.name

r = retry_plan_in_place(p, ["missing_goal"], attempts=3)
if r["status"] != "NO_PROGRESS":
    print(f"✗ expected NO_PROGRESS got {r['status']}")
    failures += 1
else:
    print(f"✓ no-progress: {r['status']} after {r['attempts']} attempts")

Path(p).unlink()

# 2. Different content = NEEDS_DEPTH (no repeat)
with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
    f.write("# v1\n")
    p = f.name

r = retry_plan_in_place(p, ["missing_goal"], attempts=1)
if r["status"] != "NEEDS_DEPTH":
    print(f"✗ expected NEEDS_DEPTH got {r['status']}")
    failures += 1
else:
    print(f"✓ different content: {r['status']} after {r['attempts']} attempts")

Path(p).unlink()

# 3. Canonical plan path preserved
with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
    f.write("# test\n")
    p = f.name

r = retry_plan_in_place(p, ["x"], attempts=1)
if not r["plan_path"].endswith(".md"):
    print(f"✗ plan_path not preserved: {r['plan_path']}")
    failures += 1
else:
    print(f"✓ canonical path: {r['plan_path']}")

Path(p).unlink()

if failures:
    print(f"\nRetry guard test failed with {failures} issue(s).")
    sys.exit(1)
print("\nAll retry guard tests passed.")
