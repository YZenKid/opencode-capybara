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
CONTRACT_OPTIONAL = ['required_selectors', 'required_attributes', 'dark_mode', 'reduced_motion']


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
    contract_path = manifest.parent / 'preview-contract.json'
    contract = json.loads(contract_path.read_text(encoding='utf-8')) if contract_path.exists() else {}
    missing = []
    lines = ['# Preview Evidence Check', '', f'- Manifest: `{manifest}`', f'- Contract: `{contract_path}`', '']
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
    if contract:
        lines += ['', '## Contract-required checks']
        selectors = contract.get('required_selectors', []) or []
        viewport_evidence = contract.get('viewport_evidence') or []
        if selectors:
            ok = all(bool(data.get(f'selector_{s}')) for s in selectors)
            lines.append(f'- [{"x" if ok else " "}] required selectors present: {len(selectors)}')
            if not ok:
                missing.append('required_selectors')
        if 'dark_mode' in contract and contract['dark_mode']:
            ok = bool(data.get('dark_screenshot'))
            lines.append(f'- [{"x" if ok else " "}] dark mode evidence')
            if not ok:
                missing.append('dark_mode')
        if 'reduced_motion' in contract and contract['reduced_motion']:
            ok = bool(data.get('reduced_motion_screenshot'))
            lines.append(f'- [{"x" if ok else " "}] reduced-motion evidence')
            if not ok:
                missing.append('reduced_motion')
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
