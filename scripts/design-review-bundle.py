#!/usr/bin/env python3
"""Create standard design review bundle files for a task.

Usage:
  python3 ~/.config/opencode/scripts/design-review-bundle.py --project-root . --task-id my-task
"""
from __future__ import annotations
import argparse
from pathlib import Path

FILES = {
    'design-handoff.md': '# Design Handoff\n\n## Design Read\n\n## Source pack summary\n\n## Chosen direction\n\n## Visual specs\n\n## Component/system notes\n\n## States and responsive rules\n\n## Accessibility and motion\n\n## Implementation route\n',
    'design-review.md': '# Design Review\n\n## Checks\n- [ ] DESIGN.md reviewed\n- [ ] Source pack attached\n- [ ] Shared-system impact reviewed\n- [ ] Screenshot evidence attached\n- [ ] Preview evidence attached\n\n## Findings\n',
    'parity-report.md': '# Parity Report\n\n## Reference\n\n## Current\n\n## Gaps\n\n## Acceptable deviations\n',
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--task-id', required=True)
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    base = root / '.opencode' / 'evidence' / args.task_id
    base.mkdir(parents=True, exist_ok=True)
    created = []
    for name, content in FILES.items():
        path = base / name
        if not path.exists():
            path.write_text(content, encoding='utf-8')
            created.append(path)
    debt = base / 'design-debt.md'
    if not debt.exists():
        debt.write_text('# Design Debt\n\nRun `python3 ~/.config/opencode/scripts/design-debt-tracker.py --project-root . --output .opencode/evidence/%s/design-debt.md`\n' % args.task_id, encoding='utf-8')
        created.append(debt)
    preview = base / 'preview.json'
    if not preview.exists():
        preview.write_text('{\n  "preview_url": "",\n  "desktop_screenshot": "",\n  "mobile_screenshot": "",\n  "dark_screenshot": "",\n  "reduced_motion_screenshot": ""\n}\n', encoding='utf-8')
        created.append(preview)
    contract = base / 'preview-contract.json'
    if not contract.exists():
        contract.write_text('{\n  "preview_url": "",\n  "required_selectors": [],\n  "required_attributes": [],\n  "viewport_evidence": ["desktop", "mobile"],\n  "dark_mode": false,\n  "reduced_motion": false\n}\n', encoding='utf-8')
        created.append(contract)
    for item in created:
        print(item)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
