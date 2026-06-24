#!/usr/bin/env python3
"""Classify revamp scope and emit required evidence contract.

Usage:
  python3 ~/.config/opencode/scripts/design-revamp-contract.py --project-root . --task-id my-task --class full-revamp
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

REQUIREMENTS = {
    'polish': ['design-review.md', 'preview.json'],
    'surface-refresh': ['design-handoff.md', 'design-review.md', 'preview.json', 'parity-report.md'],
    'flow-redesign': ['design-handoff.md', 'design-review.md', 'preview.json', 'parity-report.md', 'design-debt.md'],
    'full-revamp': ['design-handoff.md', 'design-review.md', 'preview.json', 'parity-report.md', 'design-debt.md'],
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--task-id', required=True)
    ap.add_argument('--class', dest='revamp_class', required=True, choices=REQUIREMENTS.keys())
    ap.add_argument('--output', default='')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    out = Path(args.output) if args.output else root / '.opencode' / 'evidence' / args.task_id / 'revamp-contract.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    data = {
        'revamp_class': args.revamp_class,
        'required_artifacts': REQUIREMENTS[args.revamp_class],
        'required_preview_checks': ['preview_url', 'desktop_screenshot', 'mobile_screenshot'],
        'required_gates': ['ui-polish-audit', 'design-audit', 'preview-evidence-check'],
    }
    out.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
