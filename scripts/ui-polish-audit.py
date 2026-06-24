#!/usr/bin/env python3
"""Run a UI polish audit checklist against a project.

Usage:
  python3 ~/.config/opencode/scripts/ui-polish-audit.py --project-root . [--design-file DESIGN.md] [--report .opencode/evidence/polish-audit.md]
"""
from __future__ import annotations
import argparse, re
from pathlib import Path


def find_ui_files(root: Path) -> list[Path]:
    files = []
    for ext in ('*.tsx', '*.jsx', '*.vue', '*.svelte', '*.html', '*.css', '*.scss'):
        files.extend(root.rglob(ext))
    return [p for p in files if 'node_modules/' not in str(p) and '.git/' not in str(p) and '.opencode/' not in str(p)]


def audit_files(files: list[Path]) -> list[dict]:
    findings = []
    anti_slop_patterns = [
        (re.compile(r'bg-gradient.*from-(purple|indigo|blue|violet)'), 'Generic gradient background'),
        (re.compile(r'w-[0-9/]+\s+.*h-[0-9/]+\s+.*rounded\b'), 'Generic rounded placeholder'),
        (re.compile(r'(99%|24/7|10x|100k|1M)\b'), 'Fake metric claim'),
        (re.compile(r'placeholder\.com|via\.placeholder|picsum|lorem\s+ipsum', re.I), 'Placeholder content'),
        (re.compile(r'<div[^>]*>\s*TODO\s*</div>', re.I), 'Debug TODO in UI'),
    ]
    for path in files[:500]:
        text = path.read_text(encoding='utf-8', errors='ignore')
        for pattern, reason in anti_slop_patterns:
            if pattern.search(text):
                findings.append({'file': str(path), 'reason': reason})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--design-file', default='DESIGN.md')
    ap.add_argument('--report', default='.opencode/evidence/polish-audit.md')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    design_file = root / args.design_file
    files = find_ui_files(root)
    findings = audit_files(files)

    report = root / args.report
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        '# UI Polish Audit',
        '',
        f'- Scanned files: `{len(files)}`',
        f'- DESIGN.md present: `{design_file.exists()}`',
        f'- Potential AI-slop findings: `{len(findings)}`',
        '',
        '## Findings',
    ]
    if findings:
        lines.append('| File | Reason |')
        lines.append('|---|---|')
        lines.extend([f"| `{f['file']}` | {f['reason']} |" for f in findings])
    else:
        lines.append('- No obvious AI-slop patterns detected.')

    lines += [
        '',
        '## Checklist',
        '- [ ] Consistent spacing and alignment across sections',
        '- [ ] Typography hierarchy matches DESIGN.md',
        '- [ ] Focus and hover states are visible',
        '- [ ] CTAs have consistent styling and contrast',
        '- [ ] Reduced motion support is present',
        '- [ ] Placeholder content is not shipped',
        '- [ ] Mobile/tablet viewport behavior checked',
        '- [ ] Final visual review performed by `@designer`',
    ]
    report.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(report)
    return 1 if findings else 0

if __name__ == '__main__':
    raise SystemExit(main())
