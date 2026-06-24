#!/usr/bin/env python3
"""Generate design-system registry docs from project files.

Usage:
  python3 ~/.config/opencode/scripts/design-system-docs.py --project-root . [--design-file DESIGN.md] [--registry-file .opencode/design-system/registry.md] [--output docs/generated/design-system-registry.md]
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8') if path.exists() else ''


def collect_files(root: Path, exts: tuple[str, ...]) -> list[Path]:
    files = []
    for ext in exts:
        files.extend(root.rglob(f'*{ext}'))
    return [p for p in files if '.git/' not in str(p) and 'node_modules/' not in str(p) and '.opencode/' not in str(p)]


def extract_tokens(files: list[Path]) -> list[tuple[str, str, str]]:
    found = []
    patterns = [
        re.compile(r'([A-Za-z0-9_-]+)\s*[:=]\s*["\']?(#[0-9A-Fa-f]{3,8}|\d+(?:px|rem|em|%)|[A-Za-z-]+\([^\)]*\))["\']?'),
        re.compile(r'--([A-Za-z0-9_-]+)\s*:\s*([^;]+);'),
    ]
    for path in files:
        text = read_text(path)
        for pattern in patterns:
            for match in pattern.finditer(text):
                name = match.group(1)
                value = match.group(2).strip()
                if len(name) > 2 and len(value) < 80:
                    found.append((name, value, str(path)))
    dedup = []
    seen = set()
    for name, value, source in found:
        key = (name, value)
        if key not in seen:
            seen.add(key)
            dedup.append((name, value, source))
    return dedup[:100]


def extract_components(files: list[Path]) -> list[tuple[str, str]]:
    comps = []
    for path in files:
        if path.suffix not in {'.tsx', '.jsx', '.vue', '.svelte', '.dart'}:
            continue
        stem = path.stem
        if stem and stem[0].isupper():
            comps.append((stem, str(path)))
    dedup = []
    seen = set()
    for name, source in comps:
        if name not in seen:
            seen.add(name)
            dedup.append((name, source))
    return dedup[:200]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--design-file', default='DESIGN.md')
    ap.add_argument('--registry-file', default='.opencode/design-system/registry.md')
    ap.add_argument('--catalog-file', default='.opencode/design-system/catalog.json')
    ap.add_argument('--output', default='docs/generated/design-system-registry.md')
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    design_file = root / args.design_file
    registry_file = root / args.registry_file
    catalog_file = root / args.catalog_file
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)

    files = collect_files(root, ('.ts', '.tsx', '.js', '.jsx', '.css', '.scss', '.vue', '.svelte', '.dart'))
    tokens = extract_tokens(files)
    components = extract_components(files)

    lines = [
        '# Generated Design System Registry',
        '',
        '> GENERATED FILE. Refresh with `python3 ~/.config/opencode/scripts/design-system-docs.py --project-root .`',
        '',
        f'- Project root: `{root}`',
        f'- DESIGN.md present: `{design_file.exists()}`',
        f'- Registry present: `{registry_file.exists()}`',
        f'- Scanned files: `{len(files)}`',
        '',
        '## Source files',
        f'- Design source: `{design_file.relative_to(root) if design_file.exists() else args.design_file}`',
        f'- Registry source: `{registry_file.relative_to(root) if registry_file.exists() else args.registry_file}`',
        '',
        '## Token candidates',
        '| Name | Value |',
        '|---|---|',
    ]
    if tokens:
        lines.extend([f'| `{name}` | `{value}` |' for name, value, _source in tokens[:50]])
    else:
        lines.append('| _none found_ | |')

    lines += ['', '## Component candidates', '']
    if components:
        lines.extend([f'- `{name}`' for name, _source in components[:100]])
    else:
        lines.append('- _none found_')

    lines += [
        '', '## Next actions',
        '- Confirm true shared tokens and prune false positives.',
        '- Promote real shared primitives into `.opencode/design-system/registry.md`.',
        '- Route shared-system gaps to `@design-system-engineer`.',
    ]
    output.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    catalog = catalog_file
    catalog.parent.mkdir(parents=True, exist_ok=True)
    try:
        existing = json.loads(catalog.read_text(encoding='utf-8'))
    except Exception:
        existing = {'tokens': [], 'primitives': [], 'components': [], 'patterns': [], 'sources': {}}
    existing['tokens'] = [{'name': n, 'value': v, 'source_file': f} for n, v, f in tokens[:200]]
    existing['components'] = [{'name': n, 'source_file': f} for n, f in components[:200]]
    existing.setdefault('primitives', [])
    existing.setdefault('patterns', [])
    existing.setdefault('sources', {})['generated'] = str(output)
    catalog.write_text(json.dumps(existing, indent=2) + '\n', encoding='utf-8')
    print(output)
    print(catalog)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
