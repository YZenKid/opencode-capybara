#!/usr/bin/env python3
"""Delegation log writer and validator for OpenCode worker contracts.

Each non-trivial task gets an append-only NDJSON log at
`.opencode/state/<task-id>/delegation.jsonl` with one record per
planner/orchestrator -> worker delegation and one per worker return.

Why this exists:
- Drift between planner, orchestrator, and worker is hard to audit
  after the fact without an explicit delegation trail.
- Without a log, "who handed off what scope to whom" reduces to LLM
  memory and the user's transcript.

Usage:
    python3 scripts/delegation-log.py --project-root . --task <id> \\
        --record --caller orchestrator --callee frontend \\
        --scope "Implement landing hero + 3 sections + CTA" \\
        --claim-level scoped \\
        --plan .opencode/plans/<id>.md \\
        --handoff .opencode/handoffs/<id>.yaml

    python3 scripts/delegation-log.py --project-root . --task <id> \\
        --record --caller frontend --callee orchestrator \\
        --kind return --claim-level partial \\
        --summary "Hero + 2 sections landed; CTA blocked on copy."

    python3 scripts/delegation-log.py --project-root . --task <id> \\
        --validate

    python3 scripts/delegation-log.py --project-root . --task <id> \\
        --summary

Exit codes:
    0 = record written / validation clean / summary printed
    1 = validation found malformed records
    2 = record rejected (missing required fields or bad values)
    3 = log file unreadable / IO error
    4 = invocation error
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_LANES = {
    "orchestrator",
    "artifact-planner",
    "fixer",
    "frontend",
    "backend",
    "mobile",
    "devops",
    "designer",
    "design-system-engineer",
    "fullstack",
    "explorer",
    "librarian",
    "oracle",
    "quality-gate",
    "system-analyst",
    "project-manager",
    "architect",
    "plan-reviewer",
    "visual-context-extractor",
    "visual-asset-generator",
    "skill-improver",
    "council",
}
ALLOWED_CLAIM_LEVELS = {"draft", "scoped", "partial", "done"}
ALLOWED_KINDS = {"delegate", "return", "ack", "block", "escalate"}

REQUIRED_RECORD_FIELDS = (
    "ts",
    "task_id",
    "kind",
    "caller",
    "callee",
    "scope",
    "claim_level",
)


def log_path(project_root: Path, task_id: str) -> Path:
    return (project_root / ".opencode" / "state" / task_id / "delegation.jsonl").resolve()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_record(
    task_id: str,
    kind: str,
    caller: str,
    callee: str,
    scope: str,
    claim_level: str,
    **extras: Any,
) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "ts": now_iso(),
        "task_id": task_id,
        "kind": kind,
        "caller": caller.lstrip("@"),
        "callee": callee.lstrip("@"),
        "scope": scope,
        "claim_level": claim_level,
    }
    for key, value in extras.items():
        if value is not None:
            rec[key] = value
    return rec


def validate_record(rec: dict[str, Any], source: str) -> list[str]:
    errors: list[str] = []
    for f in REQUIRED_RECORD_FIELDS:
        if f not in rec or rec[f] in ("", None, []):
            errors.append(f"[{source}] missing required field: {f}")
    caller = str(rec.get("caller", ""))
    if caller and caller not in ALLOWED_LANES:
        errors.append(f"[{source}] caller='{caller}' not in lane allowlist")
    callee = str(rec.get("callee", ""))
    if callee and callee not in ALLOWED_LANES:
        errors.append(f"[{source}] callee='{callee}' not in lane allowlist")
    claim = str(rec.get("claim_level", ""))
    if claim and claim not in ALLOWED_CLAIM_LEVELS:
        errors.append(f"[{source}] claim_level='{claim}' invalid")
    kind = str(rec.get("kind", ""))
    if kind and kind not in ALLOWED_KINDS:
        errors.append(f"[{source}] kind='{kind}' invalid; expected one of {sorted(ALLOWED_KINDS)}")
    return errors


def append_record(path: Path, rec: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def validate_log(path: Path) -> list[str]:
    if not path.is_file():
        return []
    errors: list[str] = []
    with path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rec = json.loads(stripped)
            except json.JSONDecodeError as e:
                errors.append(f"[{path.name}:{lineno}] invalid JSON: {e.msg}")
                continue
            if not isinstance(rec, dict):
                errors.append(f"[{path.name}:{lineno}] record is not a JSON object")
                continue
            errors.extend(
                f"[{path.name}:{lineno}] {e}"
                for e in validate_record(rec, f"{path.name}:{lineno}")
            )
    return errors


def summarize(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"records": 0, "by_lane": {}, "by_kind": {}, "by_claim": {}}
    counts_lane: dict[str, int] = {}
    counts_kind: dict[str, int] = {}
    counts_claim: dict[str, int] = {}
    total = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        total += 1
        counts_lane[rec.get("callee", "?")] = counts_lane.get(rec.get("callee", "?"), 0) + 1
        counts_kind[rec.get("kind", "?")] = counts_kind.get(rec.get("kind", "?"), 0) + 1
        counts_claim[rec.get("claim_level", "?")] = counts_claim.get(rec.get("claim_level", "?"), 0) + 1
    return {
        "records": total,
        "by_lane": counts_lane,
        "by_kind": counts_kind,
        "by_claim": counts_claim,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Delegation log writer / validator")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--task", required=True, help="task id; path is .opencode/state/<task>/delegation.jsonl")

    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", action="store_true", help="Append a delegation record")
    mode.add_argument("--validate", action="store_true", help="Validate the log file")
    mode.add_argument("--summary", action="store_true", help="Print summary")

    ap.add_argument("--caller", help="Caller lane")
    ap.add_argument("--callee", help="Callee lane")
    ap.add_argument("--scope", help="One-liner scope of the delegation")
    ap.add_argument("--claim-level", dest="claim_level", choices=sorted(ALLOWED_CLAIM_LEVELS))
    ap.add_argument("--kind", choices=sorted(ALLOWED_KINDS), help="Record kind")
    ap.add_argument("--plan", help="Optional plan path")
    ap.add_argument("--handoff", help="Optional handoff payload path")
    ap.add_argument("--summary-text", dest="summary_text", help="Free-form summary (for return records)")
    ap.add_argument("--blocked-reason", dest="blocked_reason", help="Reason when kind=block")
    ap.add_argument("--evidence", action="append", default=[], help="Evidence path (repeatable)")
    ap.add_argument("--json", action="store_true", help="Emit JSON output")
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    path = log_path(project_root, args.task)

    if args.validate:
        errors = validate_log(path)
        if args.json:
            print(json.dumps({"path": str(path), "ok": not errors, "errors": errors}, indent=2))
        else:
            if errors:
                print(f"FAIL ({len(errors)} issues in {path}):")
                for err in errors:
                    print(f"  - {err}")
            else:
                if path.is_file():
                    print(f"OK ({path})")
                else:
                    print(f"OK (no log file yet at {path})")
        return 0 if not errors else 1

    if args.summary:
        s = summarize(path)
        if args.json:
            s["path"] = str(path)
            print(json.dumps(s, indent=2))
        else:
            print(json.dumps(s, indent=2))
        return 0

    if args.record:
        for f in ("caller", "callee", "scope", "claim_level"):
            if not getattr(args, f):
                print(f"error: --record requires --{f.replace('_', '-')}", file=sys.stderr)
                return 4
        kind = args.kind or "delegate"
        extras: dict[str, Any] = {
            "plan": args.plan,
            "handoff": args.handoff,
            "summary": args.summary_text,
            "blocked_reason": args.blocked_reason,
            "evidence": args.evidence or None,
        }
        rec = build_record(
            task_id=args.task,
            kind=kind,
            caller=args.caller,
            callee=args.callee,
            scope=args.scope,
            claim_level=args.claim_level,
            **extras,
        )
        errors = validate_record(rec, "record")
        if errors:
            for err in errors:
                print(err, file=sys.stderr)
            return 2
        try:
            append_record(path, rec)
        except OSError as e:
            print(f"error: failed to append record: {e}", file=sys.stderr)
            return 3
        if args.json:
            print(json.dumps({"path": str(path), "record": rec}, indent=2))
        else:
            print(f"recorded -> {path}")
        return 0

    return 4


if __name__ == "__main__":
    sys.exit(main())
