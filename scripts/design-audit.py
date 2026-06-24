#!/usr/bin/env python3
"""Run a design technical audit: accessibility, responsiveness, theming, and anti-patterns.

Usage:
  python3 ~/.config/opencode/scripts/design-audit.py --project-root . [--report .opencode/evidence/design-audit.md]
"""
from __future__ import annotations
import argparse, re
from pathlib import Path


def find_ui_files(root: Path) -> list[Path]:
    files = []
    for ext in ('*.tsx', '*.jsx', '*.vue', '*.svelte', '*.html', '*.css', '*.scss'):
        files.extend(root.rglob(ext))
    return [p for p in files if 'node_modules/' not in str(p) and '.git/' not in str(p) and '.opencode/' not in str(p)]


def audit(files: list[Path]) -> list[dict]:
    findings = []
    patterns = [
        (re.compile(r'dark:|@media\s+\(prefers-color-scheme:\s*dark\)'), 'Dark mode support absent', True),
        (re.compile(r'prefers-reduced-motion'), 'Reduced-motion support absent', True),
        (re.compile(r'aria-label|aria-labelledby|alt\s*=|htmlFor'), 'Accessibility attributes missing', True),
        (re.compile(r'onClick\s*=\s*\{'), 'Interactive element without button/link role', False),
    ]
    for path in files[:500]:
        text = path.read_text(encoding='utf-8', errors='ignore')
        for pattern, reason, missing in patterns:
            if not pattern.search(text):
                if missing:
                    findings.append({'file': str(path), 'reason': reason, 'severity': 'MEDIUM'})
    # Check for hardcoded colors
    for path in files[:500]:
        text = path.read_text(encoding='utf-8', errors='ignore')
        if re.search(r'#[0-9A-Fa-f]{3,8}', text) and 'tokens' not in text.lower():
            findings.append({'file': str(path), 'reason': 'Hardcoded color tokens detected', 'severity': 'LOW'})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--report', default='.opencode/evidence/design-audit.md')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    files = find_ui_files(root)
    findings = audit(files)
    report = root / args.report
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = ['# Design Technical Audit', '', f'- Scanned files: `{len(files)}`', f'- Findings: `{len(findings)}`', '', '## Findings']
    if findings:
        lines.append('| File | Reason | Severity |')
        lines.append('|---|---|---|')
        lines.extend([f"| `{f['file']}` | {f['reason']} | {f['severity']} |" for f in findings])
    else:
        lines.append('- No obvious design issues detected.')
    lines += [
        '', '## Manual checks required',
        '- [ ] Color contrast verified with real tokens',
        '- [ ] Keyboard navigation fully tested',
        '- [ ] Screen reader labels meaningful',
        '- [ ] Touch targets >= 44x44px',
        '- [ ] Dark/light mode toggles work',
        '- [ ] Reduced-motion media query honored',
    ]
    report.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(report)
    return 1 if findings else 0

if __name__ == '__main__':
    raise SystemExit(main())
