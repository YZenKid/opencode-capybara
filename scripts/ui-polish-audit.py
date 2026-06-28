#!/usr/bin/env python3
"""Run a UI polish audit checklist against a project.

Usage:
  python3 ~/.config/opencode/scripts/ui-polish-audit.py --project-root . [--design-file DESIGN.md] [--report .opencode/evidence/polish-audit.md]
"""
from __future__ import annotations
import argparse, re, sys
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
        (re.compile(r'akan diperbarui segera|foto (stok )?ilustrasi|dokumentasi asli menyusul|foto menyusul', re.I), 'Placeholder / amateur trust-breaking copy'),
        (re.compile(r'\b(pasti bisa|solusi terbaik|masa depan|berbasis sosial budaya lokal)\b', re.I), 'Generic AI-brochure copy'),
        (re.compile(r'Kontak resmi.*diperbarui', re.I), 'Contradictory contact readiness copy'),
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
    ap.add_argument('--strict-catalog', action='store_true', help='Fail if DESIGN.md lacks catalog_citation block (substantial UI)')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    design_file = root / args.design_file
    files = find_ui_files(root)
    findings = audit_files(files)

    # v2: catalog citation check (optional strict mode)
    catalog_citation_present = False
    catalog_citation_note = ""
    if design_file.exists():
        design_text = design_file.read_text(encoding='utf-8', errors='ignore')
        catalog_citation_present = ("Source & Provenance" in design_text) or ("## Catalog Citation" in design_text) or ("open-design.ai" in design_text)
        if catalog_citation_present:
            catalog_citation_note = "DESIGN.md cites the Open Design catalog."
        else:
            catalog_citation_note = "DESIGN.md does NOT cite the Open Design catalog. For substantial UI, run `python3 ~/.config/opencode/scripts/init-design-system.py --project-root . --system <slug>` to regenerate from the catalog."
    else:
        catalog_citation_note = "No DESIGN.md found."

    report = root / args.report
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        '# UI Polish Audit',
        '',
        f'- Scanned files: `{len(files)}`',
        f'- DESIGN.md present: `{design_file.exists()}`',
        f'- Catalog citation present: `{catalog_citation_present}`',
        f'- Potential AI-slop findings: `{len(findings)}`',
        '',
        '## Catalog Citation Check (v2)',
        f'- {catalog_citation_note}',
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
        '- [ ] CTAs have consistent styling, contrast, and benefit-specific copy',
        '- [ ] Motion is present where it adds aliveness (hover/scroll/texture) and reduced-motion support is present',
        '- [ ] Placeholder or trust-breaking copy is not shipped (`akan diperbarui segera`, `foto stok ilustrasi`, `dokumentasi asli menyusul`)',
        '- [ ] Homepage has professionalism/trust anchors (real contact readiness, legal/org metadata, address or operating context)',
        '- [ ] Imagery shows real process/people/materials/environment when domain requires it',
        '- [ ] Social proof / credibility preview exists for org/community sites',
        '- [ ] Mobile/tablet viewport behavior checked',
        '- [ ] Final visual review performed by `@designer`',
    ]
    report.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(report)
    # Exit code precedence: strict-catalog failure (2) > slop findings (1) > pass (0)
    if args.strict_catalog and not catalog_citation_present:
        print('FAIL: --strict-catalog set and DESIGN.md lacks catalog citation; see report', file=sys.stderr)
        return 2
    if findings:
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
