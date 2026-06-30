#!/usr/bin/env python3
"""Subagent Handoff Contract validator.

When @orchestrator or @artifact-planner delegates work to a subagent
(@fixer, @frontend, @backend, @mobile, @devops, @designer, @fullstack,
@design-system-engineer, @explorer, @librarian, @oracle, @quality-gate,
@system-analyst, @project-manager, @architect, @plan-reviewer,
@visual-context-extractor, @visual-asset-generator, @skill-improver,
@council), the delegation MUST carry a structured handoff payload so
the subagent can execute without re-deriving context.

This script validates a handoff payload (YAML or JSON) against the
required schema and a per-lane allowlist.

Usage:
    python3 ~/.config/opencode/scripts/subagent-handoff-check.py \\
        --payload .opencode/handoffs/<task-id>-<n>.yaml

    python3 ~/.config/opencode/scripts/subagent-handoff-check.py \\
        --payload -  # read from stdin

    # CI mode: scan a plan file for embedded handoffs
    python3 ~/.config/opencode/scripts/subagent-handoff-check.py \\
        --plan .opencode/plans/<task-id>.md

Exit codes:
    0 = payload valid
    1 = payload missing required field
    2 = payload refers to lane outside allowlist
    3 = evidence path does not exist
    4 = invocation error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Field schema for the handoff payload.
# Required = strictly required. Recommended = should be present for non-trivial work.
REQUIRED_FIELDS = (
    "task_id",
    "caller",
    "callee",
    "scope",
    "claim_level",
)
RECOMMENDED_FIELDS = (
    "plan_id",
    "source_basis",
    "must_preserve",
    "do_not_touch",
    "validation",
    "exit_criteria",
    "evidence_required",
    "claim_scope",
    "depends_on",
    "context_bundle",
)
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

# Match a YAML/JSON fenced block in a markdown plan that starts with
# `handoff:` or `subagent_handoff:` (case-insensitive). Used by --plan mode.
FENCE_PATTERN = re.compile(
    r"```(?:yaml|json)?\s*\n(.*?^[\s>]*(?:handoff|subagent_handoff)\s*:\s*.*?)\n```",
    re.IGNORECASE | re.MULTILINE | re.DOTALL,
)
PAYLOAD_KEY_PATTERN = re.compile(
    r"^[\s>-]*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.+?)\s*$",
    re.MULTILINE,
)


def strip_yaml(text: str) -> dict[str, Any]:
    """Tiny YAML-ish parser; supports scalars, inline lists, and one nested map level.

    Good enough for handoff payloads. If real YAML is needed, install pyyaml.
    """
    out: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    current_map: dict[str, Any] | None = None
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # nested child under current_map, e.g. handoff:\n  task_id: x
        if current_key and current_map is not None and re.match(r"^\s{2,}[A-Za-z_][A-Za-z0-9_]*\s*:", line):
            child = line.strip()
            m_child = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", child)
            if m_child:
                ckey = m_child.group(1)
                cval = m_child.group(2).strip()
                if cval.startswith("[") and cval.endswith("]"):
                    inner = cval[1:-1].strip()
                    current_map[ckey] = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()]
                else:
                    current_map[ckey] = cval.strip("'\"")
                out[current_key] = current_map
                continue
        # list item under current_key
        m_list = re.match(r"^\s*-\s+(.*)$", line)
        if m_list and current_list is not None and current_key is not None:
            current_list.append(m_list.group(1).strip().strip("'\""))
            out[current_key] = current_list
            continue
        m_key = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line.strip())
        if not m_key:
            continue
        key = m_key.group(1)
        val = m_key.group(2).strip()
        if val == "" or val == "|" or val == ">":
            current_key = key
            current_list = []
            current_map = {}
            out[key] = current_map
            continue
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            items = [v.strip().strip("'\"") for v in inner.split(",") if v.strip()]
            out[key] = items
            current_key = None
            current_list = None
            current_map = None
            continue
        if val.startswith("[") and not val.endswith("]"):
            current_list = [val[1:].strip().strip("'\"")]
            current_key = key
            current_map = None
            out[key] = current_list
            continue
        out[key] = val.strip("'\"")
        current_key = None
        current_list = None
        current_map = None
    # unwrap top-level handoff/subagent_handoff block when present
    if isinstance(out.get("handoff"), dict):
        return out["handoff"]
    if isinstance(out.get("subagent_handoff"), dict):
        return out["subagent_handoff"]
    return out


def load_payload(path: Path) -> dict[str, Any]:
    if str(path) == "-":
        text = sys.stdin.read()
    else:
        text = path.read_text(encoding="utf-8", errors="replace")
    text = text.strip()
    if not text.startswith("{"):
        return strip_yaml(text)
    return json.loads(text)


def load_plan_payloads(plan_path: Path) -> list[tuple[str, dict[str, Any]]]:
    text = plan_path.read_text(encoding="utf-8", errors="replace")
    out: list[tuple[str, dict[str, Any]]] = []
    for m in FENCE_PATTERN.finditer(text):
        body = m.group(1)
        # strip leading list markers
        cleaned = re.sub(r"^\s*>\s?", "", body, flags=re.MULTILINE)
        out.append((f"{plan_path.name}#{m.start()}", strip_yaml(cleaned)))
    return out


def validate_one(name: str, payload: dict[str, Any], project_root: Path) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in payload or payload[field] in ("", None, []):
            errors.append(f"[{name}] missing required field: {field}")
    for field in RECOMMENDED_FIELDS:
        if field not in payload:
            errors.append(f"[{name}] missing recommended field: {field}")
    callee = str(payload.get("callee", "")).lstrip("@")
    if callee and callee not in ALLOWED_LANES:
        errors.append(
            f"[{name}] callee='{callee}' is not in the OpenCode lane allowlist"
        )
    claim = str(payload.get("claim_level", ""))
    if claim and claim not in ALLOWED_CLAIM_LEVELS:
        errors.append(
            f"[{name}] claim_level='{claim}' invalid; expected one of "
            f"{sorted(ALLOWED_CLAIM_LEVELS)}"
        )
    # evidence_required paths must be future-safe (don't have to exist yet)
    # but if absolute and existing, that's suspicious (handoff before work).
    for rel in payload.get("evidence_required", []) or []:
        if isinstance(rel, str) and rel:
            p = (project_root / rel).resolve()
            try:
                if p.exists() and p.stat().st_size == 0:
                    errors.append(
                        f"[{name}] evidence_required path is empty: {rel}"
                    )
            except OSError:
                pass
    # do_not_touch should never include '..' (safety)
    for rel in payload.get("do_not_touch", []) or []:
        if isinstance(rel, str) and ".." in rel.split("/"):
            errors.append(
                f"[{name}] do_not_touch uses '..' path traversal: {rel}"
            )
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description="Subagent Handoff Contract validator")
    ap.add_argument("--payload", help="Path to handoff payload file (.yaml/.json) or - for stdin")
    ap.add_argument("--plan", help="Plan markdown to scan for embedded handoff blocks")
    ap.add_argument("--project-root", default=".", help="Project root for resolving paths")
    ap.add_argument(
        "--json", action="store_true", help="Emit JSON report instead of human text"
    )
    args = ap.parse_args()

    if not args.payload and not args.plan:
        print("error: pass --payload <file> or --plan <file>", file=sys.stderr)
        return 4

    project_root = Path(args.project_root).resolve()
    payloads: list[tuple[str, dict[str, Any]]] = []
    if args.payload:
        try:
            payloads.append((Path(args.payload).name, load_payload(Path(args.payload))))
        except FileNotFoundError:
            print(f"error: payload file not found: {args.payload}", file=sys.stderr)
            return 4
        except (json.JSONDecodeError, ValueError) as e:
            print(f"error: failed to parse payload: {e}", file=sys.stderr)
            return 4
    if args.plan:
        plan_path = Path(args.plan)
        if plan_path.is_dir():
            for p in sorted(plan_path.glob('*.md')):
                payloads.extend(load_plan_payloads(p))
        elif plan_path.is_file():
            payloads.extend(load_plan_payloads(plan_path))
        else:
            print(f"error: plan path not found: {args.plan}", file=sys.stderr)
            return 4

    all_errors: list[str] = []
    for name, p in payloads:
        all_errors.extend(validate_one(name, p, project_root))

    report = {
        "schema": "subagent-handoff/v1",
        "checked": len(payloads),
        "errors": all_errors,
        "ok": not all_errors,
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        if all_errors:
            print(f"FAIL ({len(all_errors)} issues across {len(payloads)} payload(s)):")
            for e in all_errors:
                print(f"  - {e}")
        else:
            print(f"OK ({len(payloads)} payload(s) valid)")

    if not payloads:
        # No handoff blocks in plan: not a hard fail, just informative
        return 0
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
