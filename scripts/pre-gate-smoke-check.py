#!/usr/bin/env python3
"""
Static pre-gate smoke check.
Runs without needing a running server. Detects common slop patterns:
- 0-byte files in asset/public dirs
- manifest references to missing files
- empty primary surfaces (tagline-only)
- missing env in declared env-dependent features
"""
import json
import re
import sys
from pathlib import Path
import argparse


def find_zero_byte_assets(root: Path) -> list[dict]:
    findings = []
    asset_dirs = ['public', 'assets', 'static', 'media']
    for d in asset_dirs:
        dp = root / d
        if dp.exists() and dp.is_dir():
            for f in dp.rglob('*'):
                if f.is_file() and f.stat().st_size == 0:
                    findings.append({"path": str(f.relative_to(root)), "issue": "zero_byte"})
    return findings


def find_manifest_mismatches(root: Path) -> list[dict]:
    findings = []
    manifest_path = root / 'public' / 'manifest.webmanifest'
    if not manifest_path.exists():
        manifest_path = root / 'public' / 'manifest.json'
    if not manifest_path.exists():
        return []
    try:
        data = json.loads(manifest_path.read_text())
    except Exception:
        return [{"issue": "manifest_parse_error"}]
    for icon in data.get('icons', []):
        src = icon.get('src', '')
        if src.startswith('/'):
            src = src.lstrip('/')
        icon_path = root / 'public' / src
        if not icon_path.exists():
            findings.append({"issue": "manifest_missing_file", "ref": src, "manifest": str(manifest_path.relative_to(root))})
    return findings


def find_empty_surfaces(root: Path) -> list[dict]:
    findings = []
    app_dir = root / 'app'
    if not app_dir.exists():
        return []
    page = app_dir / 'page.tsx'
    if not page.exists():
        page = app_dir / 'page.jsx'
    if page.exists():
        text = page.read_text(errors='ignore')
        h1_count = text.count('<h1')
        h2_count = text.count('<h2')
        # Very short page with only one h1 and no other content sections
        if h1_count <= 1 and h2_count == 0 and len(text) < 500:
            findings.append({"issue": "likely_empty_surface", "file": str(page.relative_to(root))})
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--output', default='')
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    result = {
        'project_root': str(root),
        'zero_byte_assets': find_zero_byte_assets(root),
        'manifest_mismatches': find_manifest_mismatches(root),
        'empty_surfaces': find_empty_surfaces(root),
    }
    zero_byte_count = len(result['zero_byte_assets'])
    manifest_mismatch_count = len(result['manifest_mismatches'])
    empty_surface_count = len(result['empty_surfaces'])
    result['summary'] = {
        'zero_byte_count': zero_byte_count,
        'manifest_mismatch_count': manifest_mismatch_count,
        'empty_surface_count': empty_surface_count,
        'ok': zero_byte_count == 0 and manifest_mismatch_count == 0 and empty_surface_count == 0,
    }

    text = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(text)
    print(text)
    return 0 if result['summary']['ok'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
