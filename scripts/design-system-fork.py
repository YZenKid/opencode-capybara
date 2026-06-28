#!/usr/bin/env python3
"""Clone a catalog design system into a project-specific fork with documented deviations.

Usage:
  # fork a catalog system into a project, with token deviations
  python3 design-system-fork.py --base linear --out /path/to/project/DESIGN.md \
      --deviate "primary=#ff0066" --deviate "surface=#fafafa"

  # fork with a description and license
  python3 design-system-fork.py --base editorial --out ./DESIGN.md \
      --deviate "ink=#111111" --author "Mang Ujang" --purpose "ScyllaX docs site"

Deviation syntax: "name=value" where name is a token role (ink, accent, surface, ...)
and value is a hex color. Multiple --deviate flags supported.

The fork is written as a new DESIGN.md with:
- Sections 1-9 copied from the base
- Token values overwritten in section 2 per deviation
- Section 11 (Project Overrides) populated with deviation_audit entries
- A `## Catalog Citation` block added
"""
from __future__ import annotations
import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[1]
CATALOG_SYSTEMS = HARNESS_ROOT / ".opencode" / "catalog" / "systems"


def parse_deviation(spec: str) -> tuple[str, str]:
    """Parse 'name=value' deviation spec."""
    if "=" not in spec:
        raise ValueError(f"Invalid deviation spec (expected name=value): {spec!r}")
    name, value = spec.split("=", 1)
    return name.strip().lower(), value.strip()


def apply_deviation(content: str, name: str, value: str) -> tuple[str, bool]:
    """Replace a token line in the Color Palette section. Returns (new_content, applied)."""
    # Match a token line: - **Name** (`#oldhex`): description
    line_re = re.compile(r"^-\s+\*\*([A-Z][A-Za-z\s]*)\*\*\s+\(`(#[0-9A-Fa-f]+)`\):\s*(.+)$")
    applied = False
    new_lines = []
    for line in content.splitlines():
        if not applied:
            m = line_re.match(line)
            if m:
                role_label = m.group(1).strip()
                role_key = role_label.lower().replace(" ", "_")
                if role_key == name:
                    new_line = f"- **{role_label}** (`{value}`): {m.group(3)}"
                    new_lines.append(new_line)
                    applied = True
                    continue
        new_lines.append(line)
    return "\n".join(new_lines) + ("\n" if content.endswith("\n") else ""), applied


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="Catalog system slug to fork (e.g. linear)")
    ap.add_argument("--out", required=True, help="Output path for the forked DESIGN.md")
    ap.add_argument("--deviate", action="append", default=[], help="Deviation spec: name=value (e.g. ink=#ff0066). Repeatable.")
    ap.add_argument("--author", default="OpenCode harness", help="Author of this fork")
    ap.add_argument("--purpose", default="", help="Purpose of the fork (one line)")
    ap.add_argument("--dry-run", action="store_true", help="Show what would be written without writing")
    args = ap.parse_args()

    base_path = CATALOG_SYSTEMS / args.base / "DESIGN.md"
    if not base_path.exists():
        print(f"ERROR: catalog system '{args.base}' not found at {base_path}", file=sys.stderr)
        print(f"Available: {sorted(p.name for p in CATALOG_SYSTEMS.iterdir() if p.is_dir())}", file=sys.stderr)
        return 1

    content = base_path.read_text(encoding="utf-8")
    deviations: list[dict] = []

    for spec in args.deviate:
        name, value = parse_deviation(spec)
        content, applied = apply_deviation(content, name, value)
        deviations.append({
            "what": f"{name} token -> {value}",
            "applied": applied,
            "reason": "(not specified; please document)",
            "risk": "Document any contrast/accessibility/brand risk before merge.",
        })
        if not applied:
            print(f"WARN: deviation {name}={value} did not match any token role in {args.base}", file=sys.stderr)

    # Build deviation audit block
    audit_lines = [
        "",
        "## Catalog Citation (this fork)",
        "",
        f"- **Base system**: `{args.base}` — https://open-design.ai/plugins/systems/example-{args.base} (Apache-2.0)",
        f"- **Forked by**: {args.author}",
        f"- **Forked on**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
    ]
    if args.purpose:
        audit_lines.append(f"- **Purpose**: {args.purpose}")

    if deviations:
        audit_lines.extend([
            "",
            "### Deviation Audit",
            "",
            "| What | Reason | Risk |",
            "|---|---|---|",
        ])
        for d in deviations:
            audit_lines.append(f"| {d['what']} | {d['reason']} | {d['risk']} |")
        audit_lines.extend([
            "",
            "Reviewer: confirm each deviation has business justification and accessibility evidence before merge.",
        ])

    fork_block = "\n".join(audit_lines) + "\n"

    # Insert before the existing Project Overrides section, or append
    if "Project Overrides (fork only)" in content:
        content = content.replace(
            "Project Overrides (fork only)",
            "Project Overrides (fork only)\n" + fork_block,
            1,
        )
    else:
        content += "\n" + fork_block

    out_path = Path(args.out).resolve()

    if args.dry_run:
        print(f"--- DRY RUN: would write to {out_path} ---")
        print(f"Base: {args.base}")
        print(f"Deviations: {len(deviations)}")
        for d in deviations:
            print(f"  - {d['what']} (applied={d['applied']})")
        print()
        print("First 30 lines of forked output:")
        for line in content.splitlines()[:30]:
            print(f"  | {line}")
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"Wrote fork: {out_path}")
    print(f"Base: {args.base}")
    print(f"Deviations applied: {sum(1 for d in deviations if d['applied'])}/{len(deviations)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
