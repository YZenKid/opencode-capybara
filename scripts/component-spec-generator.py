#!/usr/bin/env python3
"""Generate component spec skeletons from component files.

Usage:
  python3 ~/.config/opencode/scripts/component-spec-generator.py --project-root . [--src-dir src] [--out-dir .opencode/generated-design]
"""
from __future__ import annotations
import argparse, re
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--src-dir', default='src')
    ap.add_argument('--out-dir', default='.opencode/generated-design')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    src = root / args.src_dir
    out_dir = root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    
    comps = []
    for ext in ('*.tsx', '*.jsx', '*.vue', '*.svelte'):
        for path in src.rglob(ext):
            if 'node_modules' in str(path):
                continue
            name = path.stem
            text = path.read_text(encoding='utf-8')
            # Extract props from TypeScript/TSX
            props = re.findall(r'(?:interface|type)\s+Props\s*=\s*\{([^}]+)\}', text)
            variants = re.findall(r"variants:\s*\{([^}]+)\}", text)
            spec = {
                'name': name,
                'file': str(path.relative_to(root)),
                'props_snippet': props[0][:200] if props else None,
                'variants_snippet': variants[0][:200] if variants else None,
                'states': ['default', 'hover', 'focus', 'active', 'disabled'],
                'notes': 'AUTO-GENERATED - review and complete',
            }
            comps.append(spec)
    
    lines = ['# Component Specifications', '']
    lines.append(f'> Auto-generated from `{src.name}/`. Review and complete each spec.')
    lines.append('')
    for c in comps[:50]:  # Limit to 50 components
        lines.append(f"## {c['name']}")
        lines.append(f"- File: `{c['file']}`")
        lines.append(f"- States: {', '.join(c['states'])}")
        if c['props_snippet']:
            lines.append(f"- Props: ```{c['props_snippet'][:100]}...```")
        if c['variants_snippet']:
            lines.append(f"- Variants: ```{c['variants_snippet'][:100]}...```")
        lines.append('')
    
    (out_dir / 'component-specs.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f"Generated {len(comps)} component specs → {out_dir}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
