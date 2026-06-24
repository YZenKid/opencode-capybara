#!/usr/bin/env python3
"""DOM-level preview verification for substantial UI claims.

Verifies actual rendered content, not just file existence.
Checks: required selectors, interactive elements, viewport rendering, accessibility attributes.

Usage:
  python3 dom-preview-verifier.py --project-root . --task-id <id> --manifest .opencode/evidence/<task-id>/preview-contract.json
"""
import sys
import json
import subprocess
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


def verify_preview(project_root: Path, task_id: str, manifest_path: Path) -> dict:
    """Verify preview against contract requirements."""
    result = {
        'task_id': task_id,
        'verifications': [],
        'passed': 0,
        'failed': 0,
    }

    # Load manifest
    if not manifest_path.exists():
        result['error'] = f'Manifest not found: {manifest_path}'
        return result

    with open(manifest_path) as f:
        contract = json.load(f)

    preview_url = contract.get('preview_url')
    if not preview_url:
        result['error'] = 'No preview_url in contract'
        return result

    required_selectors = contract.get('required_selectors', [])
    required_attributes = contract.get('required_attributes', [])
    viewport = contract.get('viewport', {'width': 1920, 'height': 1080})

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport=viewport)

        try:
            page.goto(preview_url, timeout=30000, wait_until='networkidle')
        except Exception as e:
            result['error'] = f'Failed to load preview: {e}'
            browser.close()
            return result

        # Check required selectors
        for selector in required_selectors:
            try:
                page.wait_for_selector(selector, timeout=5000)
                result['verifications'].append({
                    'type': 'selector',
                    'selector': selector,
                    'status': 'pass',
                })
                result['passed'] += 1
            except:
                result['verifications'].append({
                    'type': 'selector',
                    'selector': selector,
                    'status': 'fail',
                    'reason': 'selector not found',
                })
                result['failed'] += 1

        # Check required attributes
        for attr in required_attributes:
            selector = attr.get('selector')
            attribute = attr.get('attribute')
            try:
                element = page.query_selector(selector)
                if element:
                    value = element.get_attribute(attribute)
                    if value is not None:
                        result['verifications'].append({
                            'type': 'attribute',
                            'selector': selector,
                            'attribute': attribute,
                            'value': value,
                            'status': 'pass',
                        })
                        result['passed'] += 1
                    else:
                        result['verifications'].append({
                            'type': 'attribute',
                            'selector': selector,
                            'attribute': attribute,
                            'status': 'fail',
                            'reason': f'{attribute} not set',
                        })
                        result['failed'] += 1
                else:
                    result['verifications'].append({
                        'type': 'attribute',
                        'selector': selector,
                        'attribute': attribute,
                        'status': 'fail',
                        'reason': 'element not found',
                    })
                    result['failed'] += 1
            except Exception as e:
                result['verifications'].append({
                    'type': 'attribute',
                    'selector': selector,
                    'attribute': attribute,
                    'status': 'fail',
                    'reason': str(e),
                })
                result['failed'] += 1

        # Check dark mode implementation
        if contract.get('dark_mode'):
            try:
                # Check for dark class or data attribute
                dark_indicator = page.evaluate('''() => {
                    return document.documentElement.classList.contains('dark') ||
                           document.documentElement.getAttribute('data-theme') === 'dark' ||
                           document.body.classList.contains('dark') ||
                           window.matchMedia('(prefers-color-scheme: dark)').matches;
                }''')
                if dark_indicator:
                    result['verifications'].append({
                        'type': 'dark_mode',
                        'status': 'pass',
                    })
                    result['passed'] += 1
                else:
                    result['verifications'].append({
                        'type': 'dark_mode',
                        'status': 'fail',
                        'reason': 'no dark mode indicator found',
                    })
                    result['failed'] += 1
            except Exception as e:
                result['verifications'].append({
                    'type': 'dark_mode',
                    'status': 'fail',
                    'reason': str(e),
                })
                result['failed'] += 1

        # Check reduced motion support
        if contract.get('reduced_motion'):
            try:
                # Check for prefers-reduced-motion media query usage
                has_reduced_motion = page.evaluate('''() => {
                    const styles = Array.from(document.styleSheets);
                    for (const sheet of styles) {
                        try {
                            const rules = Array.from(sheet.cssRules || []);
                            for (const rule of rules) {
                                if (rule.conditionText && rule.conditionText.includes('prefers-reduced-motion')) {
                                    return true;
                                }
                            }
                        } catch(e) {}
                    }
                    return false;
                }''')
                if has_reduced_motion:
                    result['verifications'].append({
                        'type': 'reduced_motion',
                        'status': 'pass',
                    })
                    result['passed'] += 1
                else:
                    result['verifications'].append({
                        'type': 'reduced_motion',
                        'status': 'fail',
                        'reason': 'no prefers-reduced-motion media query found',
                    })
                    result['failed'] += 1
            except Exception as e:
                result['verifications'].append({
                    'type': 'reduced_motion',
                    'status': 'fail',
                    'reason': str(e),
                })
                result['failed'] += 1

        # Take screenshot for visual verification
        screenshot_path = project_root / '.opencode/evidence' / task_id / 'dom-verification.png'
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshot_path), full_page=True)
        result['screenshot'] = str(screenshot_path)

        browser.close()

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-root', type=Path, default=Path('.'))
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()

    result = verify_preview(args.project_root, args.task_id, args.manifest)

    # Save verification report
    report_path = args.project_root / '.opencode/evidence' / args.task_id / 'dom-verification-report.json'
    with open(report_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))

    if result.get('error'):
        sys.exit(1)
    elif result['failed'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
