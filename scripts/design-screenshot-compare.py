#!/usr/bin/env python3
"""Compare before/after screenshot inventories and produce checklist-oriented evidence.

Usage:
  python3 ~/.config/opencode/scripts/design-screenshot-compare.py --before-dir .opencode/evidence/task/before --after-dir .opencode/evidence/task/after [--output .opencode/evidence/task/design-compare.md]
"""
from __future__ import annotations
import argparse, hashlib
from pathlib import Path

EXTS = {'.png', '.jpg', '.jpeg', '.webp'}

def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()[:12]

def inventory(dir_path: Path) -> dict[str, dict]:
    if not dir_path.exists():
        return {}
    items = {}
    for path in sorted(dir_path.rglob('*')):
        if path.is_file() and path.suffix.lower() in EXTS:
            rel = str(path.relative_to(dir_path))
            items[rel] = {'size': path.stat().st_size, 'hash': file_hash(path)}
    return items

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--before-dir', required=True)
    ap.add_argument('--after-dir', required=True)
    ap.add_argument('--output', default='')
    args = ap.parse_args()
    before = inventory(Path(args.before_dir))
    after = inventory(Path(args.after_dir))
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(k for k in set(before) & set(after) if before[k]['hash'] != after[k]['hash'])
    unchanged = sorted(k for k in set(before) & set(after) if before[k]['hash'] == after[k]['hash'])

    lines = [
        '# Design Screenshot Comparison', '',
        f'- Before count: `{len(before)}`', f'- After count: `{len(after)}`',
        f'- Added: `{len(added)}`', f'- Removed: `{len(removed)}`', f'- Changed: `{len(changed)}`', f'- Unchanged: `{len(unchanged)}`', '',
        '## Added', *([f'- `{x}`' for x in added] or ['- none']), '',
        '## Removed', *([f'- `{x}`' for x in removed] or ['- none']), '',
        '## Changed', *([f'- `{x}`' for x in changed] or ['- none']), '',
        '## Review checklist',
        '- Confirm changed screenshots correspond to intended surfaces only.',
        '- Confirm no key viewport/state screenshot disappeared unintentionally.',
        '- Pair this inventory with human visual review for layout/parity judgment.',
    ]
    text = '\n'.join(lines) + '\n'
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding='utf-8')
        print(out)
    else:
        print(text)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
