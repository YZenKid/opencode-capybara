#!/usr/bin/env python3
import hashlib
from pathlib import Path


def retry_plan_in_place(plan_path: str, failures: list[str], attempts: int = 3) -> dict:
    path = Path(plan_path).resolve()
    fingerprint = hashlib.sha256((str(path) + "\n" + "\n".join(failures)).encode()).hexdigest()
    seen = set()
    for attempt in range(1, attempts + 1):
        state = (fingerprint, path.read_bytes())
        if state in seen:
            return {"status": "NO_PROGRESS", "attempts": attempt, "plan_path": str(path), "fingerprint": fingerprint}
        seen.add(state)
    return {"status": "NEEDS_DEPTH", "attempts": attempts, "plan_path": str(path), "fingerprint": fingerprint}
