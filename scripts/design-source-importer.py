#!/usr/bin/env python3
"""Build a normalized design source pack from URLs, local repo paths, and screenshot dirs.

Usage:
  python3 ~/.config/opencode/scripts/design-source-importer.py --project-root . \
    [--url https://example.com] [--repo-path src/components] [--screenshot-dir .opencode/evidence/ref]
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

TEXT_EXTS = {'.md', '.txt', '.tsx', '.ts', '.jsx', '.js', '.css', '.scss', '.json', '.yaml', '.yml'}
IMG_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}


def summarize_repo_path(path: Path, root: Path) -> list[str]:
    if not path.exists():
        return [f'- Missing repo path: `{path}`']
    files = sorted([p for p in path.rglob('*') if p.is_file()])[:50] if path.is_dir() else [path]
    out = []
    for file in files:
        rel = file.relative_to(root) if file.is_relative_to(root) else file
        line = f'- `{rel}`'
        if file.suffix in TEXT_EXTS:
            try:
                text = file.read_text(encoding='utf-8', errors='ignore')[:220].replace('\n', ' ')
                if text:
                    line += f' — `{text}`'
            except Exception:
                pass
        out.append(line)
    return out or [f'- Empty repo path: `{path}`']


def summarize_screens(dirpath: Path, root: Path) -> tuple[list[str], list[str]]:
    if not dirpath.exists():
        return [f'- Missing screenshot dir: `{dirpath}`'], []
    files = sorted([p for p in dirpath.rglob('*') if p.is_file() and p.suffix.lower() in IMG_EXTS])
    bullets = []
    names = []
    for file in files[:100]:
        rel = file.relative_to(root) if file.is_relative_to(root) else file
        bullets.append(f'- `{rel}`')
        names.append(file.name)
    return bullets or [f'- No screenshots in `{dirpath}`'], names


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--url', action='append', default=[])
    ap.add_argument('--repo-path', action='append', default=[])
    ap.add_argument('--screenshot-dir', action='append', default=[])
    ap.add_argument('--output', default='.opencode/evidence/design-source-pack.md')
    ap.add_argument('--catalog', default='.opencode/design-system/catalog.json')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)

    repo_sections = []
    for raw in args.repo_path:
        path = (root / raw).resolve() if not raw.startswith('/') else Path(raw)
        repo_sections.append((raw, summarize_repo_path(path, root)))

    screen_sections = []
    screenshot_names = []
    for raw in args.screenshot_dir:
        path = (root / raw).resolve() if not raw.startswith('/') else Path(raw)
        bullets, names = summarize_screens(path, root)
        screen_sections.append((raw, bullets))
        screenshot_names.extend(names)

    lines = ['# Design Source Pack', '', f'- Project root: `{root}`', f'- URLs: `{len(args.url)}`', f'- Repo sources: `{len(repo_sections)}`', f'- Screenshot dirs: `{len(screen_sections)}`', '']
    lines += ['## External references']
    lines += [f'- {u}' for u in args.url] or ['- _none_']
    lines += ['', '## Repo evidence']
    if repo_sections:
        for raw, bullets in repo_sections:
            lines += [f'### `{raw}`'] + bullets + ['']
    else:
        lines += ['- _none_','']
    lines += ['## Screenshot inventory']
    if screen_sections:
        for raw, bullets in screen_sections:
            lines += [f'### `{raw}`'] + bullets + ['']
    else:
        lines += ['- _none_','']
    lines += ['## Next actions', '- Extract stable design grammar into `DESIGN.md`.', '- Promote shared tokens/primitives into `.opencode/design-system/registry.md` and `catalog.json`.', '- Use this source pack as artifact-mode input for `@designer` and `@design-system-engineer`.']
    output.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    catalog_path = root / args.catalog
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog = {'sources': {'urls': args.url, 'repo_paths': args.repo_path, 'screenshot_dirs': args.screenshot_dir, 'screenshot_files': screenshot_names}}
    if catalog_path.exists():
        try:
            data = json.loads(catalog_path.read_text(encoding='utf-8'))
        except Exception:
            data = {}
    else:
        data = {}
    data.setdefault('sources', {}).update(catalog['sources'])
    catalog_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(output)
    print(catalog_path)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
