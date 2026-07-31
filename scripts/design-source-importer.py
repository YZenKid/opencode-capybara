#!/usr/bin/env python3
"""Build a normalized design source pack from URLs, local repo paths, and screenshot dirs.

Usage:
  python3 ~/.config/opencode/scripts/design-source-importer.py --project-root . \
    [--url https://example.com] [--repo-path src/components] [--screenshot-dir .opencode/evidence/ref]

Pack sources (additive, do not break existing flow):
  --pack awesome-design-md   Index a local clone of VoltAgent/awesome-design-md and write
                             a metadata summary under .opencode/catalog/awesome-design-md/INDEX.md
                             plus refresh the project catalog.json entry. MIT license.
  --pack open-design-catalog Refresh the Open Design catalog index from open-design.ai
                             metadata (no content fetch, only listings). Apache-2.0.

When both --pack and --url/--repo-path/--screenshot-dir are provided, pack sources run first
and the generic source pack markdown still aggregates everything.
"""
from __future__ import annotations
import argparse, json, re, subprocess
from pathlib import Path
from urllib.parse import urlparse

TEXT_EXTS = {'.md', '.txt', '.tsx', '.ts', '.jsx', '.js', '.css', '.scss', '.json', '.yaml', '.yml'}
IMG_EXTS = {'.png', '.jpg', '.jpeg', '.webp'}


ROOT = Path(__file__).resolve().parents[1]

AWESOME_DESIGN_MD_REPO = "https://github.com/VoltAgent/awesome-design-md"
AWESOME_DESIGN_MD_LICENSE = "MIT"
OPEN_DESIGN_SOLUTIONS_URL = "https://open-design.ai/plugins/systems/"


def fetch_url_structure(url: str, output_dir: Path) -> Path | None:
    try:
        extractor = ROOT / 'scripts' / 'url-structure-extractor.py'
        result = subprocess.run(
            ['python3', str(extractor), '--url', url, '--output', str(output_dir / f'url-structure-{urlparse(url).netloc}.md')],
            capture_output=True, text=True, timeout=15, check=True,
        )
        return Path(result.stdout.strip())
    except Exception:
        return None


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


def build_awesome_design_md_index(root: Path, local_path: Path) -> tuple[Path, dict]:
    if not local_path.exists():
        raise FileNotFoundError(f'awesome-design-md path not found: {local_path}')
    design_md_dir = local_path / 'design-md'
    if not design_md_dir.exists():
        raise FileNotFoundError(f'missing design-md directory in: {local_path}')

    out_dir = root / '.opencode' / 'catalog' / 'awesome-design-md'
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / 'INDEX.md'

    inside_root = design_md_dir.is_relative_to(root) if hasattr(design_md_dir, 'is_relative_to') else False
    source_kind = 'in-tree' if inside_root else 'external'

    entries = []
    for brand_dir in sorted(p for p in design_md_dir.iterdir() if p.is_dir()):
        design_file = brand_dir / 'DESIGN.md'
        if not design_file.exists():
            continue
        if inside_root:
            rel = design_file.relative_to(root)
            display_path = str(rel)
            path_note = ''
        else:
            display_path = f'external:design-md/{brand_dir.name}/DESIGN.md'
            path_note = ' (sourced from local clone outside this repo)'
        preview = ''
        try:
            lines = design_file.read_text(encoding='utf-8', errors='ignore').splitlines()
            for line in lines:
                line = line.strip()
                if line.startswith('- ') and ' - ' in line:
                    preview = line[2:]
                    break
        except Exception:
            pass
        entries.append({
            'slug': brand_dir.name,
            'path': display_path,
            'path_note': path_note,
            'upstream': f'{AWESOME_DESIGN_MD_REPO}/tree/main/design-md/{brand_dir.name}/DESIGN.md',
            'preview': preview,
        })

    lines = [
        '# awesome-design-md — Local Reference Pack',
        '',
        f'- Source: {AWESOME_DESIGN_MD_REPO}',
        f'- License: {AWESOME_DESIGN_MD_LICENSE}',
        '- Purpose: fallback DESIGN.md reference pack when project-local DESIGN.md or Open Design catalog selection is insufficient for concrete brand/style matching.',
        f'- Status: {source_kind}-indexed',
        '',
        '## Usage',
        '- `@artifact-planner`: cite this pack only when the task needs real-world DESIGN.md examples beyond the current Open Design catalog pick.',
        '- `@designer`: use as a fallback comparison pack after project-local DESIGN.md and catalog-first selection.',
        '- `@fixer with frontend skill`: never invent from this pack directly; require a cited handoff that names the chosen sample and deviations.',
        '',
        '## Entries',
    ]
    for entry in entries:
        detail = f" — {entry['preview']}" if entry['preview'] else ''
        note = entry['path_note']
        lines.append(f"- **{entry['slug']}** — `{entry['path']}`{note} — {entry['upstream']}{detail}")
    index_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    return index_path, {
        'source': AWESOME_DESIGN_MD_REPO,
        'license': AWESOME_DESIGN_MD_LICENSE,
        'entry_count': len(entries),
        'source_kind': source_kind,
        'index': str(index_path.relative_to(root) if index_path.is_relative_to(root) else index_path),
        'local_source_name': local_path.name,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--url', action='append', default=[])
    ap.add_argument('--repo-path', action='append', default=[])
    ap.add_argument('--screenshot-dir', action='append', default=[])
    ap.add_argument('--pack', action='append', default=[],
                    choices=['awesome-design-md', 'open-design-catalog'],
                    help='Add a curated reference pack source (additive).')
    ap.add_argument('--pack-path', default=None,
                    help='Local path to the cloned awesome-design-md repo (required when --pack awesome-design-md).')
    ap.add_argument('--output', default='.opencode/evidence/design-source-pack.md')
    ap.add_argument('--catalog', default='.opencode/design-system/catalog.json')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)

    pack_results: list[str] = []
    pack_meta: dict = {}
    for pack in args.pack:
        if pack == 'awesome-design-md':
            if not args.pack_path:
                raise SystemExit('--pack awesome-design-md requires --pack-path pointing to the cloned repo')
            local_path = Path(args.pack_path).resolve()
            index_path, meta = build_awesome_design_md_index(root, local_path)
            pack_results.append(f'- awesome-design-md: indexed {meta["entry_count"]} entries -> `{meta["index"]}`')
            pack_meta['awesome-design-md'] = meta
        elif pack == 'open-design-catalog':
            pack_results.append(f'- open-design-catalog: reference only; primary catalog lives at `{OPEN_DESIGN_SOLUTIONS_URL}` (Apache-2.0). Run `python3 scripts/catalog-search.py --query "<vibe>"` for selection.')

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

    url_structures = []
    for u in args.url:
        struct = fetch_url_structure(u, output.parent)
        url_structures.append((u, struct))

    lines = ['# Design Source Pack', '', f'- Project root: `{root}`', f'- URLs: `{len(args.url)}`', f'- Repo sources: `{len(repo_sections)}`', f'- Screenshot dirs: `{len(screen_sections)}`', '']
    lines += ['## Pack sources']
    lines += pack_results or ['- _none_']
    lines += ['', '## External references']
    lines += [f'- {u}' for u in args.url] or ['- _none_']
    lines += ['', '## URL structure extracts']
    if url_structures:
        for u, struct in url_structures:
            lines.append(f'- `{u}` -> `{struct}`' if struct else f'- `{u}` -> `_extract failed_`')
    else:
        lines.append('- _none_')
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
    lines += ['## Next actions', '- Extract stable design grammar into `DESIGN.md`.', '- Promote shared tokens/primitives into `.opencode/design-system/registry.md` and `catalog.json`.', '- Use this source pack as artifact-mode input for `@designer` and `@designer with design-system skill`.']
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
    data['sources']['url_structure_files'] = [str(p) for _u, p in url_structures if p]
    if pack_meta:
        data['sources']['packs'] = pack_meta
    catalog_path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(output)
    print(catalog_path)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
