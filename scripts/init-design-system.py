#!/usr/bin/env python3
"""Seed DESIGN.md and design-system registry into a project.

Usage:
  python3 ~/.config/opencode/scripts/init-design-system.py --project-root .
"""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN_TEMPLATE = ROOT / 'skills' / 'opencode-designer' / 'references' / 'DESIGN-MD-TEMPLATE.md'
REGISTRY_TEMPLATE = ROOT / 'skills' / 'opencode-design-system-engineer' / 'references' / 'DESIGN-SYSTEM-REGISTRY-TEMPLATE.md'


def copy_if_missing(src: Path, dest: Path) -> bool:
    if dest.exists():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args()
    project_root = Path(args.project_root).resolve()
    design_dest = project_root / 'DESIGN.md'
    registry_dest = project_root / '.opencode' / 'design-system' / 'registry.md'

    created = []
    if args.force or not design_dest.exists():
        design_dest.parent.mkdir(parents=True, exist_ok=True)
        design_dest.write_text(DESIGN_TEMPLATE.read_text(encoding='utf-8'), encoding='utf-8')
        created.append(str(design_dest))
    if args.force or not registry_dest.exists():
        registry_dest.parent.mkdir(parents=True, exist_ok=True)
        registry_dest.write_text(REGISTRY_TEMPLATE.read_text(encoding='utf-8'), encoding='utf-8')
        created.append(str(registry_dest))
    for item in created:
        print(item)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
