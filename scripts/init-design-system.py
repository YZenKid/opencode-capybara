#!/usr/bin/env python3
"""Seed DESIGN.md v2 (from Open Design catalog) and design-system registry into a project.

v2 changes vs v1:
- Reads source from local .opencode/catalog/systems/<slug>/DESIGN.md when --system is provided.
- Emits DESIGN.md v2 with `## Source & Provenance` block citing the catalog.
- Adds `## Project Overrides` section (only in forks).
- Falls back to the canonical 9-section local template when no catalog entry exists for the requested system.
- Runs `design-md-grader.py` after writing so `/init-harness` and direct init use the same structural contract.

Usage:
  # legacy behavior (stub DESIGN.md, no catalog citation)
  python3 init-design-system.py --project-root .

  # v2: from a catalog system (recommended for greenfield / substantial UI)
  python3 init-design-system.py --project-root . --system linear
  python3 init-design-system.py --project-root . --system editorial --template example-hps-academic-paper

  # force overwrite
  python3 init-design-system.py --project-root . --system vercel --force

  # list available catalog systems
  python3 init-design-system.py --list-systems
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[1]
CATALOG_ROOT = HARNESS_ROOT / ".opencode" / "catalog"
SYSTEMS_DIR = CATALOG_ROOT / "systems"
TEMPLATES_DIR = CATALOG_ROOT / "templates"
INDEX_FILE = CATALOG_ROOT / "INDEX.md"

LEGACY_DESIGN_TEMPLATE = HARNESS_ROOT / "skills" / "opencode-designer" / "references" / "DESIGN-MD-TEMPLATE.md"
REGISTRY_TEMPLATE = HARNESS_ROOT / "skills" / "opencode-design-system-engineer" / "references" / "DESIGN-SYSTEM-REGISTRY-TEMPLATE.md"
GRADER_SCRIPT = HARNESS_ROOT / "scripts" / "design-md-grader.py"
NORMALIZER_SCRIPT = HARNESS_ROOT / "scripts" / "catalog-to-design-md.py"


def list_systems() -> list[str]:
    if not SYSTEMS_DIR.exists():
        return []
    return sorted(p.name for p in SYSTEMS_DIR.iterdir() if p.is_dir() and (p / "DESIGN.md").exists())


def list_templates() -> list[str]:
    if not TEMPLATES_DIR.exists():
        return []
    return sorted(p.stem for p in TEMPLATES_DIR.glob("*.md") if p.stem != "INDEX")


def copy_if_missing(src: Path, dest: Path) -> bool:
    if dest.exists():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return True


def run_grader(design_dest: Path) -> int:
    if not GRADER_SCRIPT.exists():
        print(f"NOTE: grader not found at {GRADER_SCRIPT}; skipping validation")
        return 0
    import subprocess
    result = subprocess.run(
        ["python3", str(GRADER_SCRIPT), "--file", str(design_dest)],
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode


def extract_template_markdown(project_root: Path) -> str:
    text = LEGACY_DESIGN_TEMPLATE.read_text(encoding="utf-8")
    parts = text.split("```markdown", 1)
    if len(parts) != 2:
        raise ValueError(f"Template missing fenced markdown block: {LEGACY_DESIGN_TEMPLATE}")
    body, _rest = parts[1].split("```", 1)
    project_name = project_root.name.replace("-", " ").replace("_", " ").strip() or "Project"
    return body.strip().replace("[Project Name]", project_name.title()) + "\n"


def write_from_catalog(system_slug: str, project_root: Path, template_slug: str | None, force: bool) -> str | None:
    """Write project DESIGN.md based on a catalog entry. Returns the path written, or None on failure."""
    src = SYSTEMS_DIR / system_slug / "DESIGN.md"
    if not src.exists():
        print(f"ERROR: catalog system '{system_slug}' not found at {src}", file=sys.stderr)
        print("Run: python3 ~/.config/opencode/scripts/init-design-system.py --list-systems", file=sys.stderr)
        return None

    design_dest = project_root / "DESIGN.md"
    if design_dest.exists() and not force:
        print(f"SKIP: {design_dest} already exists (use --force to overwrite)")
        return None

    import subprocess
    cmd = [
        "python3",
        str(NORMALIZER_SCRIPT),
        "--source",
        str(src),
        "--out",
        str(design_dest),
        "--project-name",
        project_root.name.replace("-", " ").replace("_", " ").strip().title() or system_slug.title(),
        "--validate",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    if result.returncode != 0:
        return None

    # Append template citation to Agent Prompt Guide for execution traceability.
    if template_slug:
        template_src = TEMPLATES_DIR / f"{template_slug}.md"
        if template_src.exists():
            content = design_dest.read_text(encoding="utf-8")
            citation_block = (
                f"\n### Catalog Citation\n\n"
                f"- **Design System**: `{system_slug}` — https://open-design.ai/plugins/systems/example-{system_slug} (Apache-2.0)\n"
                f"- **Template Pattern**: `{template_slug}` — https://open-design.ai/plugins/templates/{template_slug} (Apache-2.0)\n"
                f"- **Generated by**: `python3 ~/.config/opencode/scripts/init-design-system.py --system {system_slug} --template {template_slug}`\n"
                f"- **Status**: normalized into the 9-section project-local contract.\n"
            )
            if "## Agent Prompt Guide" in content:
                content = content.replace("## Agent Prompt Guide\n\n", "## Agent Prompt Guide\n\n" + citation_block)
                design_dest.write_text(content, encoding="utf-8")
        else:
            print(f"WARN: template '{template_slug}' not found at {template_src}; proceeding without template citation", file=sys.stderr)

    return str(design_dest)


def write_legacy(project_root: Path, force: bool) -> str | None:
    design_dest = project_root / "DESIGN.md"
    if design_dest.exists() and not force:
        print(f"SKIP: {design_dest} already exists (use --force to overwrite)")
        return None
    design_dest.parent.mkdir(parents=True, exist_ok=True)
    design_dest.write_text(extract_template_markdown(project_root), encoding="utf-8")
    return str(design_dest)


def write_registry(project_root: Path, force: bool) -> str | None:
    registry_dest = project_root / ".opencode" / "design-system" / "registry.md"
    if registry_dest.exists() and not force:
        print(f"SKIP: {registry_dest} already exists (use --force to overwrite)")
        return None
    registry_dest.parent.mkdir(parents=True, exist_ok=True)
    registry_dest.write_text(REGISTRY_TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    return str(registry_dest)


def main() -> int:
    ap = argparse.ArgumentParser(description="Initialize project DESIGN.md from Open Design catalog (v2) or legacy template (v1).")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--system", help="Catalog system slug (e.g. linear, editorial, vercel). If omitted, writes legacy stub.")
    ap.add_argument("--template", help="Catalog template slug to pair with the system (e.g. example-aerocore)")
    ap.add_argument("--force", action="store_true", help="Overwrite existing DESIGN.md")
    ap.add_argument("--list-systems", action="store_true", help="Print available catalog systems and exit")
    ap.add_argument("--list-templates", action="store_true", help="Print available catalog templates and exit")
    ap.add_argument("--skip-grader", action="store_true", help="Skip the post-write 9-section grader check")
    args = ap.parse_args()

    if args.list_systems:
        systems = list_systems()
        print(f"Available catalog systems ({len(systems)}):")
        for s in systems:
            print(f"  - {s}")
        return 0

    if args.list_templates:
        templates = list_templates()
        print(f"Available catalog templates ({len(templates)}):")
        for t in templates:
            print(f"  - {t}")
        return 0

    project_root = Path(args.project_root).resolve()
    created = []
    grader_failures = []

    if args.system:
        result = write_from_catalog(args.system, project_root, args.template, args.force)
        if result:
            created.append(result)
        else:
            return 2  # catalog system invalid; do not write a stray registry
    else:
        result = write_legacy(project_root, args.force)
        if result:
            created.append(result)

    result = write_registry(project_root, args.force)
    if result:
        created.append(result)

    for item in created:
        print(item)

    design_path = project_root / "DESIGN.md"
    if not args.skip_grader and design_path.exists():
        rc = run_grader(design_path)
        if rc != 0:
            grader_failures.append(str(design_path))

    if not created:
        return 1  # nothing to do (all skipped)
    if grader_failures:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
