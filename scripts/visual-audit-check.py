#!/usr/bin/env python3
"""Visual audit fallback that checks live/URL UI without requiring working browser stack.

Uses urllib + HTML parsing to detect placeholder content, generic blobs, missing CTAs, etc.
Optionally enhances with Playwright screenshots if available.

Usage:
  python3 ~/.config/opencode/scripts/visual-audit-check.py --url https://example.com --output .opencode/evidence/visual-audit.md
"""
from __future__ import annotations
import argparse
import subprocess
from pathlib import Path


def run_url_extractor(url: str, out_dir: Path) -> Path | None:
    out = out_dir / 'url-audit-structure.md'
    try:
        subprocess.run(
            ['python3', '~/.config/opencode/scripts/url-structure-extractor.py', '--url', url, '--output', str(out)],
            capture_output=True, text=True, timeout=20, check=True,
        )
        return out
    except Exception:
        return None


def audit_url(url: str, root: Path) -> list[dict]:
    """Run lightweight audit and return findings."""
    findings = []
    try:
        req = __import__('urllib.request').request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with __import__('urllib.request').request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore').lower()
    except Exception as e:
        findings.append({'severity': 'error', 'issue': 'fetch_failed', 'detail': str(e)})
        return findings

    if 'lorem ipsum' in html or 'placeholder' in html:
        findings.append({'severity': 'high', 'issue': 'placeholder_copy', 'detail': 'placeholder text found'})
    if '<nav' not in html:
        findings.append({'severity': 'medium', 'issue': 'missing_nav', 'detail': 'no <nav> element'})
    if '<footer' not in html:
        findings.append({'severity': 'info', 'issue': 'missing_footer', 'detail': 'no <footer> element'})
    if '<main' not in html and '<header' not in html:
        findings.append({'severity': 'medium', 'issue': 'no_main_or_header', 'detail': 'no <main> or <header> landmark'})
    if html.count('<button') + html.count('type="submit"') == 0:
        findings.append({'severity': 'medium', 'issue': 'no_cta_button', 'detail': 'no visible button/CTA'})
    if 'class="bg-gradient' in html or 'class="bg-[url(' in html:
        findings.append({'severity': 'info', 'issue': 'generic_gradient_detected', 'detail': 'gradient background present, verify it is intentional'})
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--url', required=True)
    ap.add_argument('--output', default='.opencode/evidence/visual-audit.md')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)

    findings = audit_url(args.url, root)
    structure_file = run_url_extractor(args.url, out.parent)

    lines = [f'# Visual Audit Check: {args.url}', '', f'- Structure extract: `{structure_file}`', f'- Findings: `{len(findings)}`', '']
    if findings:
        lines += ['## Findings', '| Severity | Issue | Detail |', '|---|---|---|']
        for f in findings:
            lines.append(f"| `{f['severity']}` | `{f['issue']}` | {f['detail']} |")
    else:
        lines.append('No obvious mechanical issues detected.')
    lines += ['', '## Note', '- This is a fallback audit. For full visual/parity verification, run `python3 ~/.config/opencode/scripts/dom-preview-verifier.py` when Playwright is available.']
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
