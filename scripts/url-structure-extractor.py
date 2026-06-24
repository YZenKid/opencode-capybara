#!/usr/bin/env python3
"""Fetch URL content and extract structural info for design source packs.

Usage:
  python3 ~/.config/opencode/scripts/url-structure-extractor.py --url https://example.com --output .opencode/evidence/url-structure.md
"""
from __future__ import annotations
import argparse, re
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser


class StructureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []
        self.links = []
        self.forms = []
        self.ctas = []
        self.current_tag = None
        self.current_text = []
        self.in_heading = False
        self.in_form = False
        self.in_link = False
        self.link_href = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.in_heading = True
            self.current_text = []
        elif tag == 'form':
            self.in_form = True
            self.forms.append(attrs_dict.get('action', ''))
        elif tag == 'a':
            self.in_link = True
            self.link_href = attrs_dict.get('href', '')
            self.current_text = []
        elif tag in ['button', 'input']:
            if attrs_dict.get('type') in ['submit', 'button'] or tag == 'button':
                self.ctas.append(attrs_dict.get('value', ''))

    def handle_data(self, data):
        if self.in_heading or self.in_link:
            self.current_text.append(data)

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and self.in_heading:
            self.in_heading = False
            text = ' '.join(self.current_text).strip()
            if text:
                self.headings.append((tag, text))
            self.current_text = []
        elif tag == 'a' and self.in_link:
            self.in_link = False
            text = ' '.join(self.current_text).strip()
            if text:
                self.links.append((text, self.link_href))
            self.current_text = []


def extract_structure(url: str) -> dict:
    result = {'headings': [], 'links': [], 'forms': [], 'ctas': [], 'error': None}
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        parser = StructureParser()
        parser.feed(html)
        result['headings'] = parser.headings[:50]
        result['links'] = parser.links[:100]
        result['forms'] = parser.forms[:20]
        result['ctas'] = parser.ctas[:20]
    except (URLError, HTTPError, Exception) as e:
        result['error'] = str(e)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--url', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    url = args.url
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    structure = extract_structure(url)

    lines = [f'# URL Structure: {url}', '']
    if structure['error']:
        lines += [f'**Error**: {structure["error"]}', '']
    else:
        lines += [f'- Headings: {len(structure["headings"])}', f'- Links: {len(structure["links"])}', f'- Forms: {len(structure["forms"])}', f'- CTAs: {len(structure["ctas"])}', '']

    if structure['headings']:
        lines += ['## Headings']
        for tag, text in structure['headings']:
            lines.append(f'- `{tag}`: {text}')
        lines.append('')

    if structure['ctas']:
        lines += ['## CTAs']
        for cta in structure['ctas']:
            lines.append(f'- {cta}')
        lines.append('')

    if structure['forms']:
        lines += ['## Forms']
        for form in structure['forms']:
            lines.append(f'- action: `{form}`')
        lines.append('')

    if structure['links']:
        lines += ['## Links (first 20)']
        for text, href in structure['links'][:20]:
            lines.append(f'- [{text}]({href})')
        lines.append('')

    output.write_text('\n'.join(lines), encoding='utf-8')
    print(output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
