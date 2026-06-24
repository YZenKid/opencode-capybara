#!/usr/bin/env python3
"""Check preview evidence bundle completeness for substantial UI claims.

Usage:
  python3 ~/.config/opencode/scripts/preview-evidence-check.py --project-root . --task-id my-task
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

REQUIRED = ['preview_url', 'desktop_screenshot', 'mobile_screenshot']
OPTIONAL = ['dark_screenshot', 'reduced_motion_screenshot']


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--task-id', required=True)
    ap.add_argument('--manifest', default='')
    ap.add_argument('--output', default='')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    manifest = Path(args.manifest) if args.manifest else root / '.opencode' / 'evidence' / args.task_id / 'preview.json'
    output = Path(args.output) if args.output else root / '.opencode' / 'evidence' / args.task_id / 'preview-check.md'
    output.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {}
    missing = []
    lines = ['# Preview Evidence Check', '', f'- Manifest: `{manifest}`', '']
    lines += ['## Required']
    for key in REQUIRED:
        value = data.get(key, '')
        ok = bool(value)
        lines.append(f'- [{"x" if ok else " "}] `{key}`: `{value}`')
        if not ok:
            missing.append(key)
    lines += ['', '## Optional']
    for key in OPTIONAL:
        value = data.get(key, '')
        lines.append(f'- [{"x" if value else " "}] `{key}`: `{value}`')
    lines += ['', '## Verdict']
    if missing:
        lines.append(f'- Missing required preview evidence: `{", ".join(missing)}`')
        code = 1
    else:
        lines.append('- Preview evidence complete for baseline desktop/mobile claim.')
        code = 0
    output.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(output)
    return code

if __name__ == '__main__':
    raise SystemExit(main())
