#!/usr/bin/env python3
"""Detect project stack and recommend skills/MCP/best-practices per stack.

Reads the curated `scripts/data/stack_resources.json` registry and inspects
a target project root for known stack signals (manifests, lockfiles,
CLI presence, directory conventions). For each matched stack, prints
the corresponding skill URLs, MCP server recommendations, idiomatic
best practices, and anti-patterns. Output is suitable for paste into
`.opencode/evidence/<task-id>/stack-resources-suggestion.md`.

This is a soft recommender, not an installer. No files are created in
the target project; only the local evidence file is written when
`--write-evidence <path>` is provided.

Usage:
  python3 ~/.config/opencode/scripts/stack-resource-suggester.py [project_root]
  python3 ~/.config/opencode/scripts/stack-resource-suggester.py /path/to/laravel-app
  python3 ~/.config/opencode/scripts/stack-resource-suggester.py . --json
  python3 ~/.config/opencode/scripts/stack-resource-suggester.py . --write-evidence .opencode/evidence/init/stack-suggestion.md
  python3 ~/.config/opencode/scripts/stack-resource-suggester.py --list-stacks
  python3 ~/.config/opencode/scripts/stack-resource-suggester.py --show laravel
  python3 ~/.config/opencode/scripts/stack-resource-suggester.py --help

Exit codes:
  0 = scan completed
  1 = at least one stack matched (informational; useful in CI to flag)
  2 = invalid arguments or unreadable target
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

REGISTRY_PATH = Path(__file__).resolve().parent / "data" / "stack_resources.json"


@dataclass
class StackMatch:
    stack_id: str
    name: str
    category: str
    signals_found: list[str] = field(default_factory=list)
    signals_missing: list[str] = field(default_factory=list)
    confidence: str = "low"  # low | medium | high
    skills: list[dict] = field(default_factory=list)
    mcp_servers: list[dict] = field(default_factory=list)
    best_practices: dict = field(default_factory=dict)
    anti_patterns: list[str] = field(default_factory=list)


@dataclass
class SuggestionReport:
    project_root: str
    matches: list[StackMatch] = field(default_factory=list)
    primary_stack: str = ""
    secondary_stacks: list[str] = field(default_factory=list)

    @property
    def has_match(self) -> bool:
        return bool(self.matches)


def _load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Registry not found: {REGISTRY_PATH}")
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def _check_signal(root: Path, signal: str) -> bool:
    """Check a single detection signal against the project root.

    Signal grammar (signal strings come from the registry):
      - Plain path/file/dir name -> exists in root (file or directory)
      - "X with Y" / "X has Y" / "X containing Y" -> file X exists AND its
        normalized content contains normalized substring Y
      - "X or Y" (inside a clause) -> either side passes
      - Glob pattern with '*' or '?' -> glob match

    Normalization for content matching: collapse all whitespace runs to a
    single space. This lets signals like "composer.json with require
    laravel/framework" match real files whose JSON pretty-prints the
    require section across multiple lines.
    """
    s = signal.strip()
    if not s:
        return False

    # Glob pattern
    if "*" in s or "?" in s:
        return any(root.glob(s))

    # Split off "X or Y" alternatives first
    # The "or" applies within the same clause: "routes/web.php or routes/api.php"
    or_parts = _split_or(s)
    if len(or_parts) > 1:
        return any(_check_signal(root, part) for part in or_parts)

    # "X with Y" / "X has Y" / "X containing Y" -> file + content
    m = re.match(
        r"^(.+?)\s+(?:with|has|containing|that\s+contains)\s+(.+)$", s, re.IGNORECASE
    )
    if m:
        file_part = m.group(1).strip().rstrip(".")
        content_part = m.group(2).strip().rstrip(".")
        file_path = root / file_part
        if not file_path.is_file():
            return False
        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return False
        norm_text = re.sub(r"\s+", " ", text).lower()
        norm_target = re.sub(r"\s+", " ", content_part).lower()
        return norm_target in norm_text

    # Plain path (file or dir)
    path = root / s
    return path.is_file() or path.is_dir()


def _split_or(s: str) -> list[str]:
    """Split a signal string on top-level ' or ' (not inside parentheses).

    Returns a single-item list if there is no top-level 'or'.
    """
    # Simple split: only split if " or " appears at top level (no nested parens).
    # For signals with parens we keep them intact (none in our registry yet).
    depth = 0
    for i in range(len(s) - 3):
        c = s[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif depth == 0 and s[i:i + 4].lower() == " or ":
            return [s[:i].strip(), s[i + 4:].strip()]
    return [s]


def detect_stacks(root: Path, registry: dict) -> list[StackMatch]:
    matches: list[StackMatch] = []
    for stack_id, stack in registry.get("stacks", {}).items():
        signals = stack.get("detection_signals", [])
        # Single-word path signals like "app", "lib", "internal" are
        # ambiguous across many stacks and produce false positives when
        # alone. Treat them as weak signals; require either a content
        # match or multiple weak signals to count as a real detection.
        weak_path_signals = {
            "app", "lib", "cmd", "internal", "pkg", "android", "ios",
            "routes", "migrations", "artisan", "psql", "schema.sql",
            "components.json", "main.go", "src/main.rs", "src/lib.rs",
            "eas.json", "bin/rails", "manage.py", "main.py",
            "tailwind.config.js", "tailwind.config.ts",
            "next.config.js", "next.config.ts", "next.config.mjs",
            "nuxt.config.ts", "vite.config.ts", "svelte.config.js",
            "app.config.js", "app.config.ts", "app.json",
            "supabase", "supabase/config.toml", "config/routes.rb",
            "app/controllers", "Cargo.toml", "go.mod",
        }
        weak_hits: list[str] = []
        strong_hits: list[str] = []
        for s in signals:
            if _check_signal(root, s):
                if s in weak_path_signals:
                    weak_hits.append(s)
                else:
                    strong_hits.append(s)
        # Confidence model:
        #   strong hit alone -> high (or medium if only one)
        #   2+ weak hits without strong -> low
        #   1 weak hit alone -> ignore
        n_strong = len(strong_hits)
        n_weak = len(weak_hits)
        if n_strong >= 2:
            confidence = "high"
        elif n_strong == 1:
            confidence = "medium"
        elif n_weak >= 2:
            confidence = "low"
        else:
            # Single weak hit alone, or zero hits — drop from matched list
            confidence = "ignore"
        found = strong_hits + weak_hits
        missing = [s for s in signals if not _check_signal(root, s)]
        match = StackMatch(
            stack_id=stack_id,
            name=stack.get("name", stack_id),
            category=stack.get("category", "unknown"),
            signals_found=found,
            signals_missing=missing,
            confidence=confidence,
            skills=stack.get("skills", []),
            mcp_servers=stack.get("mcp_servers", []),
            best_practices=stack.get("best_practices", {}),
            anti_patterns=stack.get("anti_patterns", []),
        )
        matches.append(match)
    # Sort by confidence desc, then by strong+weak hits count
    conf_rank = {"high": 3, "medium": 2, "low": 1, "ignore": 0}
    matches.sort(
        key=lambda m: (conf_rank.get(m.confidence, 0), len(m.signals_found)),
        reverse=True,
    )
    return matches


def filter_matched(matches: list[StackMatch]) -> list[StackMatch]:
    """Only return matches with non-ignored confidence."""
    return [m for m in matches if m.confidence != "ignore"]


def render_text(report: SuggestionReport) -> str:
    out = [f"stack-resource-suggester: {report.project_root}", ""]
    if not report.has_match:
        out.append("No stacks detected. Either the project is empty, or the registry")
        out.append("does not yet cover this stack. Pass --list-stacks to see what is supported.")
        return "\n".join(out)

    out.append(f"Detected {len(report.matches)} stack(s):")
    out.append("")
    for i, m in enumerate(report.matches, 1):
        marker = "★" if i == 1 else " "
        out.append(f"{marker} {i}. {m.name}  ({m.stack_id})  confidence: {m.confidence}")
        out.append(f"   Category: {m.category}")
        out.append(f"   Signals found ({len(m.signals_found)}):")
        for s in m.signals_found:
            out.append(f"     ✓ {s}")
        if m.signals_missing and m.confidence != "high":
            out.append(f"   Signals missing ({len(m.signals_missing)}):")
            for s in m.signals_missing[:5]:
                out.append(f"     · {s}")
        if m.skills:
            out.append(f"   Skills (skills.sh / official docs):")
            for sk in m.skills:
                out.append(f"     - {sk.get('url', '?')}")
                if sk.get("use_when"):
                    out.append(f"       use when: {sk['use_when']}")
        if m.mcp_servers:
            out.append(f"   MCP servers:")
            for srv in m.mcp_servers:
                out.append(f"     - {srv.get('name', '?')}: {srv.get('reason', '')}")
        if m.best_practices:
            out.append(f"   Idiomatic best practices:")
            for k, v in m.best_practices.items():
                out.append(f"     - {k}: {v}")
        if m.anti_patterns:
            out.append(f"   Anti-patterns to avoid:")
            for ap in m.anti_patterns:
                out.append(f"     ✗ {ap}")
        out.append("")
    return "\n".join(out)


def render_markdown(report: SuggestionReport) -> str:
    out = [f"# Stack Resource Suggestion", ""]
    out.append(f"Project: `{report.project_root}`")
    out.append("")
    if not report.has_match:
        out.append("No stacks detected. Run again after the project has its initial commit.")
        return "\n".join(out)
    out.append(f"Detected {len(report.matches)} stack(s):")
    out.append("")
    for i, m in enumerate(report.matches, 1):
        out.append(f"## {i}. {m.name}  (confidence: {m.confidence})")
        out.append("")
        out.append(f"- **Category**: {m.category}")
        out.append(f"- **Signals found**: {len(m.signals_found)}")
        for s in m.signals_found:
            out.append(f"  - ✓ `{s}`")
        if m.signals_missing and m.confidence != "high":
            out.append(f"- **Signals missing** (optional confirmation): {len(m.signals_missing)}")
            for s in m.signals_missing[:5]:
                out.append(f"  - · `{s}`")
        if m.skills:
            out.append("")
            out.append("### Skills (skills.sh / official docs)")
            out.append("")
            for sk in m.skills:
                out.append(f"- [{sk.get('url', '?')}]({sk.get('url', '#')})")
                if sk.get("source"):
                    out.append(f"  - source: `{sk['source']}`")
                if sk.get("use_when"):
                    out.append(f"  - use when: {sk['use_when']}")
                if sk.get("do_not_use_for"):
                    out.append(f"  - do not use for: {sk['do_not_use_for']}")
        if m.mcp_servers:
            out.append("")
            out.append("### MCP servers")
            out.append("")
            for srv in m.mcp_servers:
                out.append(f"- **{srv.get('name', '?')}** — {srv.get('reason', '')}")
        if m.best_practices:
            out.append("")
            out.append("### Idiomatic best practices")
            out.append("")
            out.append("| Practice | Guidance |")
            out.append("|---|---|")
            for k, v in m.best_practices.items():
                out.append(f"| **{k}** | {v} |")
        if m.anti_patterns:
            out.append("")
            out.append("### Anti-patterns to avoid")
            out.append("")
            for ap in m.anti_patterns:
                out.append(f"- ✗ {ap}")
        out.append("")
    out.append("---")
    out.append("")
    out.append("> Generated by `python3 ~/.config/opencode/scripts/stack-resource-suggester.py`.")
    out.append("> This is a soft recommendation, not an auto-install. Review each skill/MCP/best-practice,")
    out.append("> confirm with the user, then install only what fits the project.")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("project_root", nargs="?", default=".",
                   help="Project root to inspect (default: current directory).")
    p.add_argument("--json", action="store_true", help="Emit JSON output.")
    p.add_argument("--write-evidence", metavar="PATH",
                   help="Write markdown suggestion to PATH (e.g. .opencode/evidence/init/stack.md).")
    p.add_argument("--list-stacks", action="store_true",
                   help="List all known stack IDs and exit.")
    p.add_argument("--show", metavar="STACK_ID",
                   help="Show full details for a single stack and exit.")
    args = p.parse_args(argv)

    try:
        registry = _load_registry()
    except FileNotFoundError as e:
        print(f"stack-resource-suggester: {e}", file=sys.stderr)
        return 2

    if args.list_stacks:
        print("Known stacks:")
        for sid, s in registry.get("stacks", {}).items():
            n_skills = len(s.get("skills", []))
            n_mcp = len(s.get("mcp_servers", []))
            print(f"  {sid:24}  {s.get('name', ''):40}  skills={n_skills}  mcp={n_mcp}")
        return 0

    if args.show:
        stack = registry.get("stacks", {}).get(args.show)
        if not stack:
            print(f"Unknown stack: {args.show}", file=sys.stderr)
            print("Use --list-stacks to see available IDs.", file=sys.stderr)
            return 2
        print(json.dumps(stack, indent=2))
        return 0

    root = Path(args.project_root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"stack-resource-suggester: project root not found: {root}",
              file=sys.stderr)
        return 2

    all_matches = detect_stacks(root, registry)
    report = SuggestionReport(project_root=str(root), matches=filter_matched(all_matches))
    if report.matches:
        report.primary_stack = report.matches[0].stack_id
        report.secondary_stacks = [m.stack_id for m in report.matches[1:]]

    if args.json:
        print(json.dumps({
            "project_root": report.project_root,
            "primary_stack": report.primary_stack,
            "secondary_stacks": report.secondary_stacks,
            "matches": [asdict(m) for m in report.matches],
        }, indent=2))
    else:
        print(render_text(report))

    if args.write_evidence:
        ev_path = Path(args.write_evidence)
        if not ev_path.is_absolute():
            ev_path = Path.cwd() / ev_path
        ev_path.parent.mkdir(parents=True, exist_ok=True)
        ev_path.write_text(render_markdown(report), encoding="utf-8")
        print(f"\nWrote evidence: {ev_path}")

    return 1 if report.has_match else 0


if __name__ == "__main__":
    sys.exit(main())
