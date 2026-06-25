#!/usr/bin/env python3
"""
Deterministic validator for experiential UI quality evidence.

Checks that cross-lane artifacts exist and are properly structured:
- visual-quality-contract.md (shared contract from planner → designer → frontend → QG)
- visual-rubric.md (QG taste/texture rubric)
- design_pushback.md (frontend pushback artifact)
- reference-essence.md (designer reference analysis)

Exit codes:
  0 = all required evidence present
  1 = missing or malformed evidence
  2 = runtime error

Usage:
  python3 ~/.config/opencode/scripts/verify-visual-quality-evidence.py --project-root . --task <task-id>
  python3 ~/.config/opencode/scripts/verify-visual-quality-evidence.py --project-root . --task <task-id> --verbose
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def read_file(path: Path) -> str:
    """Read file content, return empty string if missing."""
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return ""


def check_file_exists(path: Path, required: bool = True) -> dict:
    """Check if file exists and return status."""
    exists = path.exists() and path.is_file()
    return {
        "path": str(path),
        "exists": exists,
        "required": required,
        "status": "pass" if exists else ("fail" if required else "warn"),
    }


def check_structured_fields(content: str, fields: list[str]) -> dict:
    """Check if content has required structured fields."""
    found = {}
    for field in fields:
        # Match field as markdown header or bold label
        patterns = [
            rf"#{1,4}\s+{re.escape(field)}",  # # field
            rf"\*\*{re.escape(field)}\*\*",    # **field**
            rf"{re.escape(field)}:",           # field:
        ]
        found[field] = any(re.search(p, content, re.IGNORECASE) for p in patterns)
    
    missing = [f for f, present in found.items() if not present]
    return {
        "fields_checked": fields,
        "found": found,
        "missing": missing,
        "status": "pass" if not missing else "fail",
    }


def check_surface_reject_if(content: str) -> dict:
    """Check if content has per-surface reject_if conditions."""
    # Look for surface headers with reject_if
    surface_pattern = r"#{1,4}\s+(?:Surface|Hero|Product|Companion|Garden|Deck|Landing)[^:\n]*"
    reject_if_pattern = r"(?:\*\*)?reject_if(?:\*\*)?[:\s]"
    
    surfaces = re.findall(surface_pattern, content, re.IGNORECASE | re.MULTILINE)
    reject_if_blocks = re.findall(reject_if_pattern, content, re.IGNORECASE)
    
    return {
        "surfaces_found": len(surfaces),
        "reject_if_blocks": len(reject_if_blocks),
        "status": "pass" if len(reject_if_blocks) >= max(1, len(surfaces) // 2) else "fail",
    }


def check_rubric_checks(content: str) -> dict:
    """Check if visual rubric has required yes/no checks."""
    required_checks = [
        "feels real vs template",
        "human warmth",
        "domain texture",
        "decorative abstraction",
        "screenshot evidence",
        "must_show",
        "reject_if",
    ]
    
    found = {}
    for check in required_checks:
        # Look for check as header or yes/no question
        pattern = rf"(?:\*\*)?{re.escape(check)}(?:\*\*)?.*(?:yes|no|\?)"
        found[check] = bool(re.search(pattern, content, re.IGNORECASE))
    
    missing = [c for c, present in found.items() if not present]
    return {
        "checks_found": sum(found.values()),
        "checks_total": len(required_checks),
        "missing": missing,
        "status": "pass" if len(missing) <= 2 else "fail",  # Allow up to 2 missing
    }


def verify_evidence(project_root: Path, task_id: str, verbose: bool = False) -> dict:
    """Verify all required visual quality evidence artifacts."""
    evidence_dir = project_root / ".opencode" / "evidence" / task_id
    plan_path = project_root / ".opencode" / "plans" / f"{task_id}.md"
    
    results = {
        "task_id": task_id,
        "project_root": str(project_root),
        "evidence_dir": str(evidence_dir),
        "checks": {},
    }
    
    # 1. Check visual-quality-contract.md (shared contract)
    contract_path = evidence_dir / "visual-quality-contract.md"
    contract_check = check_file_exists(contract_path, required=False)
    if contract_check["exists"]:
        content = read_file(contract_path)
        fields_check = check_structured_fields(
            content,
            ["must_show", "must_not_show", "reject_if", "fake_warmth_patterns", "template_smells"]
        )
        surface_check = check_surface_reject_if(content)
        contract_check["fields"] = fields_check
        contract_check["surfaces"] = surface_check
        contract_check["status"] = (
            "pass"
            if fields_check["status"] == "pass" and surface_check["status"] == "pass"
            else "fail"
        )
    results["checks"]["visual_quality_contract"] = contract_check
    
    # 2. Check visual-rubric.md (QG rubric)
    rubric_path = evidence_dir / "visual-rubric.md"
    rubric_check = check_file_exists(rubric_path, required=False)
    if rubric_check["exists"]:
        content = read_file(rubric_path)
        rubric_fields = check_rubric_checks(content)
        rubric_check["rubric"] = rubric_fields
        rubric_check["status"] = rubric_fields["status"]
    results["checks"]["visual_rubric"] = rubric_check
    
    # 3. Check design_pushback.md (frontend pushback)
    pushback_path = evidence_dir / "design_pushback.md"
    pushback_check = check_file_exists(pushback_path, required=False)
    if pushback_check["exists"]:
        content = read_file(pushback_path)
        pushback_fields = check_structured_fields(
            content,
            ["pushback_reason", "failure_class", "specific_failures", "required_fixes", "evidence_required"]
        )
        pushback_check["fields"] = pushback_fields
        pushback_check["status"] = pushback_fields["status"]
    results["checks"]["design_pushback"] = pushback_check
    
    # 4. Check reference-essence.md (designer reference analysis)
    essence_path = evidence_dir / "reference-essence.md"
    essence_check = check_file_exists(essence_path, required=False)
    if essence_check["exists"]:
        content = read_file(essence_path)
        essence_fields = check_structured_fields(
            content,
            ["warmth", "humanity", "texture", "domain-specific", "lived reality"]
        )
        essence_check["fields"] = essence_fields
        essence_check["status"] = essence_fields["status"]
    results["checks"]["reference_essence"] = essence_check
    
    # 5. Check plan has per-surface reject_if
    plan_check = check_file_exists(plan_path, required=True)
    if plan_check["exists"]:
        content = read_file(plan_path)
        plan_surface_check = check_surface_reject_if(content)
        plan_check["surfaces"] = plan_surface_check
        # Plan must have at least 2 surfaces with reject_if for substantial UI
        plan_check["status"] = "pass" if plan_surface_check["surfaces_found"] >= 2 else "warn"
    results["checks"]["plan_surfaces"] = plan_check
    
    # Compute overall status
    all_checks = [c for c in results["checks"].values()]
    required_failures = [c for c in all_checks if c.get("required") and c["status"] == "fail"]
    optional_problems = [c for c in all_checks if not c.get("required") and c["status"] in ("fail", "warn")]
    required_warnings = [c for c in all_checks if c.get("required") and c["status"] == "warn"]
    
    if required_failures:
        results["status"] = "fail"
        results["reason"] = f"Required evidence failed: {[c['path'] for c in required_failures]}"
    elif required_warnings or optional_problems:
        results["status"] = "warn"
        problem_paths = [c['path'] for c in required_warnings + optional_problems]
        results["reason"] = f"Evidence incomplete or missing: {problem_paths}"
    else:
        results["status"] = "pass"
        results["reason"] = "All required evidence present"
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Verify experiential UI quality evidence artifacts"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        required=True,
        help="Project root directory",
    )
    parser.add_argument(
        "--task",
        required=True,
        help="Task ID (e.g., 20260625-0817-production-ready)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed check results",
    )
    
    args = parser.parse_args()
    
    if not args.project_root.exists():
        print(f"Error: project root not found: {args.project_root}", file=sys.stderr)
        sys.exit(2)
    
    try:
        results = verify_evidence(args.project_root, args.task, args.verbose)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    
    # Print results
    if args.verbose:
        print(json.dumps(results, indent=2))
    else:
        print(f"Task: {results['task_id']}")
        print(f"Status: {results['status'].upper()}")
        print(f"Reason: {results['reason']}")
        print()
        for check_name, check_data in results["checks"].items():
            status_icon = "✓" if check_data["status"] == "pass" else ("⚠" if check_data["status"] == "warn" else "✗")
            print(f"{status_icon} {check_name}: {check_data['status']}")
            if "missing" in check_data:
                missing = check_data["missing"]
                if missing:
                    print(f"  Missing fields: {', '.join(missing)}")
    
    # Exit code
    if results["status"] == "pass":
        sys.exit(0)
    elif results["status"] == "warn":
        sys.exit(1)
    else:  # fail
        sys.exit(1)


if __name__ == "__main__":
    main()
