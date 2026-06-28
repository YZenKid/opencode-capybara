#!/usr/bin/env python3
"""Search the local Open Design catalog (.opencode/catalog/) by name, category, vibe, or tags.

v1 features:
- Searches systems by name fuzzy match, category substring, or vibe keywords.
- Searches templates by name fuzzy match, category, or tags.
- Optional --surface filter for systems (web | mobile | both).
- Optional --pair to suggest a system + template combination for a query.
- Outputs ranked list with score + URL.

Usage:
  # all systems matching a vibe
  python3 catalog-search.py --query "editorial"
  # only systems for web
  python3 catalog-search.py --query "saas" --surface web
  # search templates
  python3 catalog-search.py --kind templates --query "dashboard"
  # suggest a system + template pair for a use case
  python3 catalog-search.py --pair --query "marketing site for AI startup"
  # JSON output for programmatic use
  python3 catalog-search.py --query "premium" --json
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[1]
CATALOG_ROOT = HARNESS_ROOT / ".opencode" / "catalog"
SYSTEMS_DIR = CATALOG_ROOT / "systems"
TEMPLATES_DIR = CATALOG_ROOT / "templates"
INDEX_FILE = CATALOG_ROOT / "INDEX.md"

# A small keyword -> category hint map for the --pair suggestion mode
USE_CASE_HINTS = {
    "marketing": ("stripe", "vercel", ["example-aerocore", "example-acreage-farming", "example-saas-layout"]),
    "saas": ("linear", "stripe", ["example-saas-layout", "example-live-dashboard"]),
    "dashboard": ("linear", "supabase", ["example-live-dashboard"]),
    "editorial": ("editorial", "medium", ["example-hps-academic-paper", "image-editorial-hero"]),
    "deck": ("editorial", "swiss", ["example-hps-academic-paper", "example-brand-pitch", "example-product-launch"]),
    "academic": ("editorial", "swiss", ["example-hps-academic-paper"]),
    "investor": ("stripe", "vercel", ["example-brand-pitch", "example-investor-update"]),
    "pitch": ("stripe", "vercel", ["example-brand-pitch"]),
    "ai": ("openai", "claude-anthropic", ["example-ai-designer-portfolio"]),
    "developer": ("github", "vercel", ["example-tech-talk"]),
    "dashboard live": ("linear", "supabase", ["example-live-dashboard"]),
    "pricing": ("linear", "stripe", ["example-live-pricing"]),
    "portfolio": ("vercel", "neon", ["example-3d-creator-portfolio", "example-ai-designer-portfolio"]),
    "3d": ("vercel", "neon", ["example-3d-creator-portfolio"]),
    "agriculture": ("vercel", "calm", ["example-acreage-farming"]),
    "premium": ("stripe", "vercel", ["example-aerocore"]),
    "cinematic": ("vercel", "stripe", ["example-aerocore"]),
}


def list_systems() -> list[dict]:
    if not SYSTEMS_DIR.exists():
        return []
    out = []
    for p in sorted(SYSTEMS_DIR.iterdir()):
        if not p.is_dir():
            continue
        design_md = p / "DESIGN.md"
        if not design_md.exists():
            continue
        text = design_md.read_text(encoding="utf-8")
        meta = {"slug": p.name, "path": str(design_md), "source": f"https://open-design.ai/plugins/systems/example-{p.name}"}
        # Extract category from frontmatter
        m = re.search(r">\s*Category:\s*([^\n]+)", text)
        meta["category"] = m.group(1).strip() if m else "(uncategorized)"
        # Extract vibe from frontmatter
        m = re.search(r">\s*Vibe:\s*([^\n]+)", text)
        meta["vibe"] = m.group(1).strip() if m else ""
        # Extract surface from frontmatter
        m = re.search(r">\s*Surface:\s*([^\n]+)", text)
        meta["surface"] = m.group(1).strip() if m else "both"
        out.append(meta)
    return out


def list_templates() -> list[dict]:
    if not TEMPLATES_DIR.exists():
        return []
    out = []
    for p in sorted(TEMPLATES_DIR.glob("*.md")):
        if p.stem == "INDEX":
            continue
        text = p.read_text(encoding="utf-8")
        meta = {"slug": p.stem, "path": str(p), "source": f"https://open-design.ai/plugins/templates/{p.stem}"}
        m = re.search(r">\s*Category:\s*([^\n]+)", text)
        meta["category"] = m.group(1).strip() if m else "(uncategorized)"
        m = re.search(r"^#\s*Template:\s*([^\n]+)", text, re.MULTILINE)
        meta["name"] = m.group(1).strip() if m else p.stem
        m = re.search(r"\*\*Tags\*\*:\s*([^\n]+)", text)
        meta["tags"] = [t.strip() for t in m.group(1).split(",")] if m else []
        out.append(meta)
    return out


def score(text: str, query: str) -> int:
    """Simple substring + word-match score. Higher = better."""
    if not query:
        return 1
    q = query.lower()
    t = text.lower()
    if q in t:
        return 10
    words = q.split()
    hits = sum(1 for w in words if w in t)
    return hits


def search_systems(query: str, surface: str | None, limit: int) -> list[tuple[int, dict]]:
    candidates = list_systems()
    if surface and surface != "both":
        candidates = [c for c in candidates if c.get("surface") == surface or c.get("surface") == "both"]
    scored = []
    for c in candidates:
        s = score(c["slug"], query) * 3 + score(c.get("vibe", ""), query) * 2 + score(c.get("category", ""), query)
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda x: -x[0])
    return scored[:limit]


def search_templates(query: str, limit: int) -> list[tuple[int, dict]]:
    candidates = list_templates()
    scored = []
    for c in candidates:
        s = score(c["slug"], query) * 3 + score(c.get("name", ""), query) * 2 + score(c.get("category", ""), query)
        for tag in c.get("tags", []):
            s += score(tag, query)
        if s > 0:
            scored.append((s, c))
    scored.sort(key=lambda x: -x[0])
    return scored[:limit]


def pair_suggestion(query: str) -> dict | None:
    q = query.lower()
    for hint, (sys_a, sys_b, tmpls) in USE_CASE_HINTS.items():
        if hint in q or all(w in q for w in hint.split()):
            return {
                "use_case": hint,
                "systems": [sys_a, sys_b],
                "templates": tmpls,
                "rationale": f"Query matches known use-case pattern '{hint}'.",
            }
    # Fallback: search systems + templates and pair top hits
    sys_hits = search_systems(query, None, 2)
    tpl_hits = search_templates(query, 3)
    if not sys_hits and not tpl_hits:
        return None
    return {
        "use_case": "(no exact use-case match; closest picks)",
        "systems": [s[1]["slug"] for s in sys_hits[:2]],
        "templates": [t[1]["slug"] for t in tpl_hits[:3]],
        "rationale": "Top scoring systems and templates from catalog-search.",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Search the local Open Design catalog.")
    ap.add_argument("--query", "-q", help="Search query (vibe keyword, category, name, or use case)")
    ap.add_argument("--kind", choices=["systems", "templates", "all"], default="all")
    ap.add_argument("--surface", choices=["web", "mobile", "both"], help="Filter systems by surface")
    ap.add_argument("--limit", "-n", type=int, default=10)
    ap.add_argument("--pair", action="store_true", help="Suggest a system + template pair for the query")
    ap.add_argument("--json", action="store_true", help="Output JSON")
    args = ap.parse_args()

    if not args.query:
        print("ERROR: --query is required (or use --list-systems/--list-templates via init-design-system.py)", file=sys.stderr)
        return 2

    if args.pair:
        result = pair_suggestion(args.query)
        if not result:
            print(f"No pair suggestion for query: {args.query!r}")
            return 1
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"# Pair suggestion for: {args.query!r}\n")
            print(f"Use case: {result['use_case']}")
            print(f"Rationale: {result['rationale']}\n")
            print("Systems:")
            for s in result["systems"]:
                print(f"  - {s}  https://open-design.ai/plugins/systems/example-{s}")
            print("Templates:")
            for t in result["templates"]:
                print(f"  - {t}  https://open-design.ai/plugins/templates/{t}")
        return 0

    results: dict = {}
    if args.kind in ("systems", "all"):
        results["systems"] = [
            {"score": s, **meta} for s, meta in search_systems(args.query, args.surface, args.limit)
        ]
    if args.kind in ("templates", "all"):
        results["templates"] = [
            {"score": s, **meta} for s, meta in search_templates(args.query, args.limit)
        ]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if "systems" in results:
            print(f"\n# Systems matching {args.query!r}{f' (surface={args.surface})' if args.surface else ''}\n")
            if not results["systems"]:
                print("  (no matches)")
            for r in results["systems"]:
                print(f"  - {r['slug']:25} score={r['score']:3}  category={r['category']}")
                print(f"      vibe: {r['vibe']}")
                print(f"      {r['source']}")
        if "templates" in results:
            print(f"\n# Templates matching {args.query!r}\n")
            if not results["templates"]:
                print("  (no matches)")
            for r in results["templates"]:
                tags = ", ".join(r.get("tags", []))
                print(f"  - {r['slug']:35} score={r['score']:3}  category={r['category']}  tags=[{tags}]")
                print(f"      {r['source']}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
