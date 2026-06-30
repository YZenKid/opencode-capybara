#!/usr/bin/env python3
"""Template/Source Discovery helper.

When a user says "pakai templates" or the project has a `templates/`
directory, this script inventories it, parses entry files, and scans
`.opencode/AGENTS.md` for non-negotiables that reference templates.

It does NOT make decisions; it emits a discovery report that the
agent must read and the user must confirm (or override) before any
implementation begins.

Usage:
    python3 ~/.config/opencode/scripts/template-source-discovery.py \\
        --project-root . [--json] [--summary-only]

Exit codes:
    0 = discovery report emitted (no conflicts OR no templates found)
    1 = conflict detected (user intent "pakai templates" vs. an N# that
        blocks a specific template folder); still emits the report so
        the agent can show the user what was found.
    2 = invocation error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

TEMPLATES_DIRS = ("templates", "template", "design-templates", "design_templates")
AGENTS_FILES = (".opencode/AGENTS.md", "AGENTS.md")
INTENT_PATTERNS = [
    r"\bpakai\s+templates?\b",
    r"\bikutin\s+template\b",
    r"\bmirip\s+(?:web\s+)?(?:ini|itu|gini|gini)\b",
    r"\bclone\s+(?:1\s*:\s*1|literal)\b",
    r"\bport(?:ing)?\b",
    r"\bcopy\s+(?:dari|from)\b",
    r"\breplicate\b",
    r"\b1\s*:\s*1\b",
    r"\b(?:style|seperti)\s+(?:web\s+)?(?:ini|itu)\b",
]
CONSTRAINT_PATTERN = re.compile(
    r"\bN(\d+)\s*[:\-]\s*([^\n]+)", re.IGNORECASE
)


def detect_user_intent(prompt: str) -> list[str]:
    out = []
    for pat in INTENT_PATTERNS:
        for m in re.finditer(pat, prompt, re.IGNORECASE):
            out.append(m.group(0))
    return out


def find_templates_root(project_root: Path) -> list[Path]:
    """Return the immediate template subdirectories, not the wrapper `templates/`
    parent. So a project that has `templates/dashboard/` + `templates/landingpage/`
    yields two entries, not one."""
    out: list[Path] = []
    parents: list[Path] = []
    for name in TEMPLATES_DIRS:
        cand = project_root / name
        if cand.is_dir():
            parents.append(cand)
    for parent in parents:
        for child in sorted(parent.iterdir()):
            if child.is_dir() and not child.name.startswith("."):
                out.append(child)
    return out


def inventory_template_dir(d: Path) -> dict[str, Any]:
    """Parse one template directory. Reads index.html/CSS/JS/Pug/SCSS and
    package.json when present."""
    entry_files: list[str] = []
    for cand in (
        "index.html", "index.htm", "public/index.html",
        "src/index.css", "src/index.tsx", "src/main.tsx", "src/main.js",
        "src/index.js", "src/pug/index.pug", "src/scss/main.scss",
        "src/scss/style.scss", "gulpfile.js", "vite.config.ts", "vite.config.js",
    ):
        if (d / cand).is_file():
            entry_files.append(cand)
    pkg: dict[str, Any] = {}
    pkg_path = d / "package.json"
    if pkg_path.is_file():
        try:
            pkg = json.loads(pkg_path.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            pkg = {"_error": "package.json not parseable as JSON"}
    license_text = str(pkg.get("license") or "").strip()
    if not license_text:
        for name in ("LICENSE", "LICENSE.md", "License.md", "Readme.md", "README.md"):
            p = d / name
            if p.is_file():
                try:
                    head = p.read_text(encoding="utf-8", errors="replace")[:2000]
                except Exception:
                    continue
                m = re.search(r"(MIT|Apache-2\.0|ISC|GPL-?[23]\.0|AGPL-?3\.0|BSD-[23]-Clause|Unlicense|CC0-1\.0|MPL-2\.0)", head)
                if m:
                    license_text = m.group(1)
                    break
    stack_hints: list[str] = []
    deps = {}
    for key in ("dependencies", "devDependencies"):
        deps.update(pkg.get(key, {}) or {})
    stack_signals = {
        "react": any(k in deps for k in ("react", "react-dom")),
        "vue": any(k in deps for k in ("vue",)),
        "vite": any(k in deps for k in ("vite", "@vitejs/plugin-react", "@vitejs/plugin-vue")),
        "tailwind": any(k in deps for k in ("tailwindcss",)),
        "bootstrap": any(k in deps for k in ("bootstrap",)),
        "pug": any(k in deps for k in ("pug",)),
        "gulp": any(k in deps for k in ("gulp",)),
        "react-router": "react-router-dom" in deps,
        "inertia": "@inertiajs/react" in deps or "@inertiajs/vue3" in deps,
        "recharts": "recharts" in deps,
        "framer-motion": "framer-motion" in deps,
    }
    for k, v in stack_signals.items():
        if v:
            stack_hints.append(k)
    return {
        "name": d.name,
        "path": str(d.relative_to(d.parent.parent)) if d.parent else d.name,
        "entry_files": entry_files,
        "package_name": pkg.get("name", ""),
        "stack_hints": stack_hints,
        "license": license_text or "unknown",
    }


def find_agents_files(project_root: Path) -> list[Path]:
    out = []
    for rel in AGENTS_FILES:
        p = project_root / rel
        if p.is_file():
            out.append(p)
    return out


def scan_constraints(agents_files: list[Path]) -> list[dict[str, Any]]:
    constraints: list[dict[str, Any]] = []
    for f in agents_files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for m in CONSTRAINT_PATTERN.finditer(text):
            num, body = m.group(1), m.group(2).strip()
            constraints.append(
                {
                    "id": f"N{num}",
                    "body": body,
                    "source": str(f.relative_to(f.parent.parent.parent)) if f.parent else str(f),
                }
            )
    return constraints


def detect_conflicts(
    user_intent: list[str],
    templates: list[dict[str, Any]],
    constraints: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not user_intent or not templates:
        return []
    block_words = (
        "tidak", "jangan", "blocked", "not used",
        "tidak dipakai", "not allowed", "larangan", "banned",
    )
    out: list[dict[str, Any]] = []
    for tmpl in templates:
        tmpl_lc = tmpl["name"].lower()
        for c in constraints:
            body_lc = c["body"].lower()
            blocked = any(w in body_lc for w in block_words)
            if not blocked:
                continue
            # match by template directory name, path token, or package name alias
            tmpl_path_token = f"templates/{tmpl_lc}"
            pkg_lc = str(tmpl.get("package_name") or "").lower()
            if tmpl_lc in body_lc or tmpl_path_token in body_lc or (pkg_lc and pkg_lc in body_lc):
                out.append(
                    {
                        "type": "constraint-blocks-template",
                        "constraint_id": c["id"],
                        "constraint_body": c["body"],
                        "template": tmpl["name"],
                        "rationale": "User said 'pakai templates' but a project N# constraint blocks this template folder; ask the user to clarify before continuing.",
                    }
                )
    return out


def emit_report(project_root: Path) -> dict[str, Any]:
    templates_dirs = find_templates_root(project_root)
    templates_inv = [inventory_template_dir(d) for d in templates_dirs]
    agents_files = find_agents_files(project_root)
    constraints = scan_constraints(agents_files)
    return {
        "schema": "template-source-discovery/v1",
        "project_root": str(project_root),
        "agents_files": [str(p) for p in agents_files],
        "templates_found": len(templates_inv) > 0,
        "templates": templates_inv,
        "constraints_referenced": constraints,
        "needs_user_clarification": False,  # filled in by main when invoked with intent
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Template/Source Discovery helper")
    ap.add_argument("--project-root", default=".", help="Project root to scan")
    ap.add_argument(
        "--user-intent",
        default="",
        help="Optional raw user prompt to detect template intent keywords",
    )
    ap.add_argument("--json", action="store_true", help="Emit JSON only")
    ap.add_argument("--summary-only", action="store_true", help="Human summary only")
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    if not project_root.is_dir():
        print(f"error: project root not found: {project_root}", file=sys.stderr)
        return 2

    report = emit_report(project_root)
    user_intent = detect_user_intent(args.user_intent)
    conflicts: list[dict[str, Any]] = []
    if user_intent:
        report["user_intent"] = user_intent
        conflicts = detect_conflicts(user_intent, report["templates"], report["constraints_referenced"])
        report["conflicts"] = conflicts
        report["needs_user_clarification"] = bool(conflicts)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif args.summary_only:
        print(f"project_root: {report['project_root']}")
        print(f"templates_found: {report['templates_found']}")
        for t in report["templates"]:
            print(
                f"  - {t['name']:24s} license={t['license']:10s} "
                f"stack={','.join(t['stack_hints']) or '-'}"
            )
        if conflicts:
            print("conflicts:")
            for c in conflicts:
                print(f"  ! {c['type']}: {c['constraint_id']} blocks {c['template']}")
        if not report["templates_found"]:
            print("(no templates/ directory at project root)")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))

    if conflicts:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
