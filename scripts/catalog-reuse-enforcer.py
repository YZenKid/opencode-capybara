#!/usr/bin/env python3
"""Enforce design-system catalog reuse for UI changes.

Scans changed UI files and checks if their component/class tokens already exist in catalog.json.
Flags new ad-hoc components/patterns that should be promoted to shared system.

Usage:
  python3 ~/.config/opencode/scripts/catalog-reuse-enforcer.py --project-root . --catalog .opencode/design-system/catalog.json --files src/pages/Home.tsx,src/components/NewCard.tsx
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path


REACT_COMPONENT_RE = re.compile(r'(?:export\s+)?(?:const|function|class)\s+([A-Z][A-Za-z0-9_]*)')
TAILWIND_CLASS_RE = re.compile(r'\b(bg|text|border|ring|shadow|rounded|p|m|gap|space|font|tracking|leading|w|h|min|max)-[A-Za-z0-9_-]+\b')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--catalog', default='.opencode/design-system/catalog.json')
    ap.add_argument('--files', required=True)
    ap.add_argument('--output', default='.opencode/evidence/catalog-reuse-report.md')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    catalog_path = root / args.catalog
    report = root / args.output
    report.parent.mkdir(parents=True, exist_ok=True)

    catalog = {'tokens': [], 'primitives': [], 'components': [], 'patterns': []}
    if catalog_path.exists():
        try:
            catalog.update(json.loads(catalog_path.read_text(encoding='utf-8')))
        except Exception:
            pass

    known_components = {c.get('name', c) if isinstance(c, dict) else c for c in catalog.get('components', [])}
    known_primitives = {p.get('name', p) if isinstance(p, dict) else p for p in catalog.get('primitives', [])}

    findings = []
    for file in args.files.split(','):
        path = root / file.strip()
        if not path.exists():
            findings.append({'file': file, 'issue': 'file_not_found', 'severity': 'error'})
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        for match in REACT_COMPONENT_RE.finditer(text):
            name = match.group(1)
            if name not in known_components:
                findings.append({'file': file, 'issue': 'new_component_not_in_catalog', 'name': name, 'severity': 'warning'})
        classes = set(TAILWIND_CLASS_RE.findall(text))
        # ad-hoc token detection: many arbitrary utility combos without primitive wrapper
        if len(classes) > 10:
            findings.append({'file': file, 'issue': 'heavy_ad_hoc_utilities', 'count': len(classes), 'severity': 'info'})

    lines = ['# Catalog Reuse Enforcement Report', '', f'- Catalog: `{catalog_path}`', f'- Files checked: `{len(args.files.split(","))}`', f'- Findings: `{len(findings)}`', '']
    if findings:
        lines += ['## Findings', '| File | Issue | Severity |', '|---|---|---|']
        for f in findings:
            lines.append(f"| `{f.get('file')}` | `{f.get('issue')}` ({f.get('name', f.get('count', ''))}) | `{f.get('severity')}` |")
    else:
        lines.append('No reuse violations.')

    lines += ['', '## Next actions', '- Promote new shared components to catalog via `@design-system-engineer`.', '- Refactor heavy ad-hoc utility usage into shared primitives.', '- Document bypass rationale for intentional one-off components.']
    report.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(report)
    return 1 if any(f.get('severity') == 'error' for f in findings) else 0


if __name__ == '__main__':
    raise SystemExit(main())
