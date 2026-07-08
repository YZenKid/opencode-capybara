#!/usr/bin/env python3
"""Normalize an Open Design catalog DESIGN.md into the 9-section project-local contract.

Source schema (catalog): numbered sections 1..N, often including:
  1. Visual Theme & Atmosphere
  2. Color Palette & Roles
  3. Typography Scale
  4. Spacing & Layout
  5. Motion Language
  6. Voice & Copy
  7. Imagery Strategy
  8. Component Variants
  9. Anti-Patterns (Reject If)
  10. Source & Provenance
  11. Project Overrides (fork only)

Target schema (project-local): unnumbered, exactly 9 sections, in this order:
  Visual Theme & Atmosphere
  Color Palette & Roles
  Typography Rules
  Component Stylings
  Layout Principles
  Depth & Elevation
  Do's and Don'ts
  Responsive Behavior
  Agent Prompt Guide

Usage:
  python3 ~/.config/opencode/scripts/catalog-to-design-md.py \\
      --source .opencode/catalog/systems/linear/DESIGN.md \\
      --out /tmp/proj/DESIGN.md
  python3 ~/.config/opencode/scripts/catalog-to-design-md.py \\
      --source .opencode/catalog/systems/editorial/DESIGN.md

Exit codes:
  0 -> wrote a 9-section DESIGN.md (validated by design-md-grader.py)
  2 -> could not read or normalize; details printed to stderr
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

GRADER_SCRIPT = Path(__file__).resolve().parent / "design-md-grader.py"

HEADER_RE = re.compile(r"^##\s+(?:\d+\.\s+)?(.+?)\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"^```", re.MULTILINE)


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


def split_sections(text: str) -> list[tuple[str, str]]:
    """Return ordered list of (section_title, section_body) from a markdown document."""
    prose = strip_code_fences(text)
    sections: list[tuple[str, str]] = []
    current_title: str | None = None
    buf: list[str] = []

    for line in prose.splitlines():
        m = HEADER_RE.match(line)
        if m:
            if current_title is not None:
                sections.append((current_title, "\n".join(buf).strip("\n")))
            current_title = m.group(1).strip()
            buf = []
            continue
        if current_title is None:
            continue
        buf.append(line)
    if current_title is not None:
        sections.append((current_title, "\n".join(buf).strip("\n")))
    return sections


def normalize_title(title: str) -> str:
    t = title.strip().lower()
    t = re.sub(r"[^a-z0-9 &'-]", "", t)
    t = t.replace("&", "and")
    t = re.sub(r"\s+", " ", t).strip()
    return t


SOURCE_TO_TARGET = {
    "visual theme and atmosphere": "Visual Theme & Atmosphere",
    "color palette and roles": "Color Palette & Roles",
    "typography scale": "Typography Rules",
    "component variants": "Component Stylings",
    "imagery strategy": "Component Stylings",
    "spacing and layout": "Layout Principles",
    "do's and don'ts": "Do's and Don'ts",
    "do's and don'ts (reject if)": "Do's and Don'ts",
    "anti-patterns (reject if)": "Do's and Don'ts",
    "voice and copy": "Do's and Don'ts",
    "motion language": "Agent Prompt Guide",
    "source and provenance": "Agent Prompt Guide",
    "project overrides (fork only)": "Agent Prompt Guide",
}

TARGET_ORDER = [
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


def extract_title_block(text: str) -> tuple[str, str]:
    """Return (h1_title, provenance_block) from the front matter (lines before first H2)."""
    prose = strip_code_fences(text)
    h1_match = re.search(r"^#\s+(.+?)\s*$", prose, re.MULTILINE)
    title = h1_match.group(1).strip() if h1_match else "Design System"
    # Drop the "Design System:" prefix from the h1 if present
    title = re.sub(r"^Design System:\s*", "", title).strip()

    blockquote_lines: list[str] = []
    in_blockquote_zone = True
    for line in prose.splitlines():
        if line.startswith("## "):
            break
        if not in_blockquote_zone:
            continue
        if line.startswith("---") or line.startswith("# "):
            continue
        if line.startswith(">") or line.strip() == "":
            blockquote_lines.append(line.lstrip("> ").rstrip())
            continue
        in_blockquote_zone = False
    provenance = "\n".join(s for s in blockquote_lines if s).strip()
    return title, provenance


def normalize(source_path: Path, project_name: str | None = None) -> str:
    text = source_path.read_text(encoding="utf-8", errors="ignore")
    sections = split_sections(text)
    title, provenance = extract_title_block(text)
    if project_name:
        title = project_name

    buckets: dict[str, list[str]] = {target: [] for target in TARGET_ORDER}

    for sec_title, sec_body in sections:
        key = normalize_title(sec_title)
        target = SOURCE_TO_TARGET.get(key)
        if not target:
            # Unknown section: append to Agent Prompt Guide as a "Notes from source"
            if sec_body.strip():
                buckets["Agent Prompt Guide"].append(f"### Source section: {sec_title}\n\n{sec_body.strip()}")
            continue
        if sec_body.strip():
            existing = buckets[target]
            if existing:
                existing.append("\n---\n")
            existing.append(f"### From catalog: {sec_title}\n\n{sec_body.strip()}")
            buckets[target] = existing

    # Special handling: motion language -> also seed Agent Prompt Guide with reduced-motion rule
    # (Already merged via SOURCE_TO_TARGET; keep that mapping.)
    # Special handling: Depth & Elevation is often empty for catalogs that fold shadow into Spacing.
    if not buckets["Depth & Elevation"]:
        buckets["Depth & Elevation"] = [
            "No explicit depth rules in the source. Default: flat by default; one shadow level "
            "for floating dialogs/modals only; focus ring is 2px primary with 2px offset. "
            "Confirm and customize per project surface."
        ]

    if not buckets["Responsive Behavior"]:
        buckets["Responsive Behavior"] = [
            "No explicit responsive rules in the source. Default: mobile-first, 12-col grid on "
            "desktop, 8-col on tablet, 4-col on mobile; navigation collapses to bottom sheet or "
            "drawer below 768px; touch targets >= 44x44; respect `prefers-reduced-motion: reduce`."
        ]

    out_lines = [f"# {title} Design System", ""]
    if provenance:
        out_lines += ["> Source & Provenance:", ""]
        for line in provenance.splitlines():
            if line.strip():
                out_lines += [f"> {line.strip()}"]
        out_lines += [""]
    else:
        out_lines += ["> Source & Provenance: catalog source unknown; verify before use.", ""]
    out_lines += [
        "> Mapping: sections were normalized from the catalog's numbered schema into the 9-section project-local contract.",
        "",
    ]

    for target in TARGET_ORDER:
        out_lines.append(f"## {target}")
        out_lines.append("")
        body = "\n".join(buckets[target]).strip()
        if body:
            out_lines.append(body)
        else:
            out_lines.append("Project-specific guidance required. Replace this placeholder before relying on this section.")
        out_lines.append("")

    return "\n".join(out_lines).rstrip() + "\n"


def run_grader(target_file: Path) -> int:
    if not GRADER_SCRIPT.exists():
        return 0
    import subprocess
    result = subprocess.run(
        ["python3", str(GRADER_SCRIPT), "--file", str(target_file)],
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize a catalog DESIGN.md into the 9-section project-local contract.")
    ap.add_argument("--source", required=True, help="Path to the catalog DESIGN.md to normalize")
    ap.add_argument("--out", default=None, help="Output file (default: stdout)")
    ap.add_argument("--project-name", default=None, help="Override the project name in the h1")
    ap.add_argument("--validate", action="store_true", help="Run design-md-grader after writing (requires --out)")
    args = ap.parse_args()

    src = Path(args.source).resolve()
    if not src.exists():
        print(f"ERROR: source not found: {src}", file=sys.stderr)
        return 2

    output = normalize(src, args.project_name)
    if args.out:
        out = Path(args.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output, encoding="utf-8")
        print(f"WROTE: {out}")
        if args.validate:
            return run_grader(out)
        return 0
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
