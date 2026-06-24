#!/usr/bin/env python3
"""Aggregate design debt candidates from project memory.

Usage:
  python3 ~/.config/opencode/scripts/design-debt-tracker.py --project-root . [--output .opencode/evidence/design-debt.md]
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

DESIGN_TAGS = {'design', 'ui', 'ux', 'a11y', 'motion', 'token', 'component', 'responsive'}
DESIGN_CATEGORIES = {'ux', 'pattern', 'pitfall', 'architecture', 'testing'}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--output', default='.opencode/evidence/design-debt.md')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    memory_file = root / '.opencode' / 'memory' / 'knowledge.json'
    entries = json.loads(memory_file.read_text(encoding='utf-8')) if memory_file.exists() else []
    debt = []
    for item in entries:
        tags = set(item.get('tags') or [])
        category = item.get('category', '')
        text = f"{item.get('lesson','')} {item.get('context','')}".lower()
        if tags & DESIGN_TAGS or category in DESIGN_CATEGORIES or any(k in text for k in ('design', 'ui', 'ux', 'a11y', 'motion', 'token', 'responsive', 'component')):
            debt.append(item)
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ['# Design Debt Tracker', '', f'- Total design debt candidates: `{len(debt)}`', '', '| ID | Category | Importance | Lesson |', '|---|---|---|---|']
    for item in debt[:100]:
        lesson = (item.get('lesson','') or '').replace('|', '\\|')[:120]
        lines.append(f"| `{item.get('id','')}` | `{item.get('category','')}` | `{item.get('importance','')}` | {lesson} |")
    if not debt:
        lines.append('| _none_ | | | |')
    lines += ['', '## Next actions', '- Promote recurring items into registry or DESIGN.md updates.', '- Fix high-importance debt during substantial UI passes.', '- Archive resolved debt by updating/removing project memory entries.']
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(out)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
