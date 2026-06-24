#!/usr/bin/env python3
"""Generate starter token files from DESIGN.md.

Usage:
  python3 ~/.config/opencode/scripts/design-token-generator.py --project-root . [--design-file DESIGN.md] [--out-dir .opencode/generated-design]
"""
from __future__ import annotations
import argparse, re, json
from pathlib import Path

HEX = re.compile(r'#[0-9A-Fa-f]{3,8}')
SIZE = re.compile(r'\b\d+(?:px|rem|em)\b')

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--design-file', default='DESIGN.md')
    ap.add_argument('--out-dir', default='.opencode/generated-design')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    text = (root / args.design_file).read_text(encoding='utf-8')
    colors = sorted(set(HEX.findall(text)))
    sizes = sorted(set(SIZE.findall(text)))
    out_dir = root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    data = {
        'colors': {f'color_{i+1}': v for i, v in enumerate(colors[:40])},
        'sizes': {f'size_{i+1}': v for i, v in enumerate(sizes[:40])},
    }
    (out_dir / 'tokens.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    css_lines = [':root {']
    for k, v in data['colors'].items(): css_lines.append(f'  --{k}: {v};')
    for k, v in data['sizes'].items(): css_lines.append(f'  --{k}: {v};')
    css_lines.append('}')
    (out_dir / 'tokens.css').write_text('\n'.join(css_lines) + '\n', encoding='utf-8')
    print(out_dir)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
