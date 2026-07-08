#!/usr/bin/env python3
"""Validate DESIGN.md 9-section contract.

Usage:
  python3 ~/.config/opencode/scripts/design-md-grader.py --project-root .
  python3 ~/.config/opencode/scripts/design-md-grader.py --file /path/to/DESIGN.md

Exit codes:
  0 -> PASS
  2 -> NEEDS_FIX (missing/empty/duplicated sections)
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_SECTIONS = [
    "Visual Theme & Atmosphere",
    "Color Palette & Roles",
    "Typography Rules",
    "Component Stylings",
    "Layout Principles",
    "Depth & Elevation",
    "Do's and Don'ts",
    "Responsive Behavior",
    "Agent Prompt Guide",
]

HEADER_RE = re.compile(r"^##\s+(?:\d+\.\s+)?(.+?)\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"^```", re.MULTILINE)


def normalize(name: str) -> str:
    return name.strip().lower()


def strip_code_fences(text: str) -> str:
    out = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        out.append(line)
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate DESIGN.md against the 9-section contract.")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--file", default=None)
    args = ap.parse_args()

    design_file = Path(args.file).resolve() if args.file else Path(args.project_root).resolve() / "DESIGN.md"
    if not design_file.exists():
        print(f"BLOCKED: DESIGN.md not found at {design_file}")
        return 2

    text = design_file.read_text(encoding="utf-8", errors="ignore")
    prose_text = strip_code_fences(text)
    headers = HEADER_RE.findall(prose_text)
    normalized_headers = [normalize(h) for h in headers]

    missing = []
    duplicates = []
    empty = []

    for section in REQUIRED_SECTIONS:
        key = normalize(section)
        count = normalized_headers.count(key)
        if count == 0:
            missing.append(section)
            continue
        if count > 1:
            duplicates.append(section)

        pattern = re.compile(rf"^##\s+(?:\d+\.\s+)?{re.escape(section)}\s*$", re.MULTILINE)
        match = pattern.search(prose_text)
        if not match:
            # fallback for case variation, already counted above
            continue
        start = match.end()
        next_match = re.search(r"^##\s+", prose_text[start:], re.MULTILINE)
        body = prose_text[start:start + next_match.start()] if next_match else prose_text[start:]
        if len(body.strip()) < 20:
            empty.append(section)

    if missing or duplicates or empty:
        print("NEEDS_FIX")
        if missing:
            print("- Missing sections:")
            for section in missing:
                print(f"  - {section}")
        if duplicates:
            print("- Duplicate sections:")
            for section in duplicates:
                print(f"  - {section}")
        if empty:
            print("- Too-short / effectively empty sections:")
            for section in empty:
                print(f"  - {section}")
        return 2

    print("PASS")
    print(f"- File: {design_file}")
    print(f"- Sections: {len(REQUIRED_SECTIONS)} / {len(REQUIRED_SECTIONS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
