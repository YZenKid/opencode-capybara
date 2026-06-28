#!/usr/bin/env python3
"""Quick helper: given a brief, recommend a system + template pair from the catalog.

Wrapper around `catalog-search.py --pair` that adds a one-shot printable summary
suitable for handing to a designer as a starting point. It does NOT make the
choice for the designer; it just lists the top 3 system+template pairs and
asks the designer to pick one (or justify an off-list pick).

Usage:
  python3 ~/.config/opencode/skills/ui-ux-pro-max/scripts/select-catalog.py --brief "marketing site for AI ops tool"
  python3 ~/.config/opencode/skills/ui-ux-pro-max/scripts/select-catalog.py --brief "AI ops dashboard for engineers" --surface web
  python3 ~/.config/opencode/skills/ui-ux-pro-max/scripts/select-catalog.py --brief "..." --json
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CATALOG_SEARCH = Path("/var/home/ujang/.config/opencode/scripts/catalog-search.py")


def run_catalog_search(brief: str, surface: str | None) -> dict:
    cmd = ["python3", str(CATALOG_SEARCH), "--pair", "--query", brief, "--json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: catalog-search.py failed: {e.stderr}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return {}


def run_system_search(brief: str, surface: str | None, kind: str, limit: int) -> list[dict]:
    cmd = ["python3", str(CATALOG_SEARCH), "--kind", kind, "--query", brief, "--limit", str(limit), "--json"]
    if surface and kind == "systems":
        cmd += ["--surface", surface]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, check=True)
        data = json.loads(result.stdout)
        return data.get(kind, [])
    except Exception as e:
        print(f"WARN: {kind} search failed: {e}", file=sys.stderr)
        return []


def main() -> int:
    ap = argparse.ArgumentParser(description="Recommend catalog system+template pairs for a brief.")
    ap.add_argument("--brief", required=True, help="One-line task brief or use-case description")
    ap.add_argument("--surface", choices=["web", "mobile", "both"], help="Optional surface filter")
    ap.add_argument("--limit", type=int, default=3, help="Number of pairs to recommend")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    pair = run_catalog_search(args.brief, args.surface)
    systems = run_system_search(args.brief, args.surface, "systems", args.limit)
    templates = run_system_search(args.brief, args.surface, "templates", args.limit * 2)

    if args.json:
        print(json.dumps({
            "brief": args.brief,
            "surface": args.surface,
            "primary_pair": pair,
            "candidate_systems": systems,
            "candidate_templates": templates,
        }, indent=2))
        return 0

    print(f"# Catalog recommendation for: {args.brief!r}\n")
    if pair:
        print(f"## Primary pair (from use-case match)")
        print(f"- Use case: {pair.get('use_case', '(no match)')}")
        print(f"- Rationale: {pair.get('rationale', '')}")
        print(f"- Systems: {', '.join(pair.get('systems', []))}")
        print(f"- Templates: {', '.join(pair.get('templates', []))}\n")
    else:
        print("## No use-case match; use ranked candidates below.\n")

    print(f"## Top {args.limit} candidate systems")
    for s in systems[:args.limit]:
        print(f"  - {s['slug']:25} score={s['score']:3}  category={s['category']}")
        print(f"      vibe: {s.get('vibe', '')}")
        print(f"      {s['source']}")
    print()

    print(f"## Top {args.limit * 2} candidate templates")
    for t in templates[:args.limit * 2]:
        tags = ", ".join(t.get("tags", []))
        print(f"  - {t['slug']:35} score={t['score']:3}  category={t['category']}  tags=[{tags}]")
        print(f"      {t['source']}")
    print()

    print("## Next steps for @designer")
    print("1. Pick 1 system + 1 template pair from above (or justify an off-list pick).")
    print("2. Document the pick in `.opencode/evidence/<task-id>/catalog-decision.md`.")
    print("3. Run `python3 ~/.config/opencode/scripts/init-design-system.py --project-root . --system <slug> --template <slug>` to seed DESIGN.md v2.")
    print("4. Fill the visual-quality-contract.md v2 with the catalog_citation block.")
    print("5. Hand off to @frontend / @mobile with the contract and tokens.json.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
