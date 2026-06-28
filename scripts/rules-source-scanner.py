#!/usr/bin/env python3
"""Detect and summarize agent-rules files in a target project.

Scans a project root for known rules file locations used by various
agentic tools and reports what is present, what is missing, and what
overlaps. This is the first step of `init-harness` source harmonization.

Known locations (current as of 2026-06):

| Tool         | Path(s)                                       | Format         |
|--------------|-----------------------------------------------|----------------|
| OpenCode     | `AGENTS.md`, `.opencode/docs/`                | Markdown       |
| Claude Code  | `CLAUDE.md`, `.claude/`, `.claude/agents/`    | Markdown       |
| Codex        | `AGENTS.md`, `.codex/`, `.codex/AGENTS.md`    | Markdown/YAML  |
| Aider        | `CONVENTIONS.md`, `.aider.conf.yml`           | Markdown/YAML  |
| Cursor       | `.cursorrules`, `.cursor/rules/`              | Plain/YAML     |
| Windsurf     | `.windsurfrules`, `.windsurf/rules/`          | Plain          |
| Continue     | `.continue/`, `.continue/config.json`         | JSON           |
| Cline        | `.clinerules`, `.cline/`                      | Plain          |
| Cody         | `.cody/`, `.cody/agents.md`                   | Markdown       |
| Roo Code     | `.roo/`                                       | JSON           |
| GitHub       | `.github/agents.md`, `.github/copilot-instructions.md` | Markdown |
| GitLab       | `.gitlab/duo/`, `.gitlab/agents.md`           | Markdown       |
| Generic      | `AGENT.md`, `AGENTS.local.md`, `.agents/`     | Markdown       |

Usage:
  python3 ~/.config/opencode/scripts/rules-source-scanner.py [project_root]
  # defaults to current directory
  python3 ~/.config/opencode/scripts/rules-source-scanner.py /path/to/project --json
  python3 ~/.config/opencode/scripts/rules-source-scanner.py --summary-only
  python3 ~/.config/opencode/scripts/rules-source-scanner.py --help

Exit codes:
  0 = scan completed (whether or not rules files are present)
  2 = invalid arguments or unreadable target
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable


@dataclass
class SourceHit:
    tool: str
    path: str
    exists: bool
    size_bytes: int = 0
    line_count: int = 0
    preview: str = ""
    notes: str = ""


@dataclass
class ScanReport:
    project_root: str
    hits: list[SourceHit] = field(default_factory=list)
    opencode_native_present: bool = False
    opencode_native_paths: list[str] = field(default_factory=list)
    external_rules_present: list[str] = field(default_factory=list)
    recommended_action: str = ""

    @property
    def has_external_rules(self) -> bool:
        return bool(self.external_rules_present)

    @property
    def needs_init_harness(self) -> bool:
        return not self.opencode_native_present


# Source registry: (tool, glob/filename, kind, notes)
SOURCES: list[tuple[str, str, str, str]] = [
    ("opencode", "AGENTS.md", "file", "OpenCode native; map to orchestrator routing"),
    ("opencode", ".opencode", "dir", "OpenCode canonical docs system of record"),
    ("opencode", "DESIGN.md", "file", "OpenCode design source of truth"),
    ("claude-code", "CLAUDE.md", "file", "Claude Code memory file"),
    ("claude-code", ".claude", "dir", "Claude Code local config / agents"),
    ("claude-code", ".claude/agents", "dir", "Claude Code custom subagents"),
    ("codex", "AGENTS.md", "file", "Codex/Codex CLI native (overlaps with OpenCode)"),
    ("codex", ".codex", "dir", "Codex CLI config dir"),
    ("codex", ".codex/AGENTS.md", "file", "Codex CLI explicit AGENTS.md"),
    ("cursor", ".cursorrules", "file", "Cursor legacy rules file"),
    ("cursor", ".cursor/rules", "dir", "Cursor modern rules directory"),
    ("windsurf", ".windsurfrules", "file", "Windsurf legacy rules file"),
    ("windsurf", ".windsurf/rules", "dir", "Windsurf modern rules directory"),
    ("continue", ".continue", "dir", "Continue config dir"),
    ("continue", ".continue/config.json", "file", "Continue config file"),
    ("cline", ".clinerules", "file", "Cline legacy rules file"),
    ("cline", ".cline", "dir", "Cline state dir"),
    ("cody", ".cody", "dir", "Cody config dir"),
    ("cody", ".cody/agents.md", "file", "Cody agents file"),
    ("roo", ".roo", "dir", "Roo Code config dir"),
    ("aider", "CONVENTIONS.md", "file", "Aider conventions file"),
    ("aider", ".aider.conf.yml", "file", "Aider config file"),
    ("github", ".github/agents.md", "file", "GitHub Copilot coding agent instructions"),
    ("github", ".github/copilot-instructions.md", "file", "GitHub Copilot legacy instructions"),
    ("gitlab", ".gitlab/agents.md", "file", "GitLab Duo agent instructions"),
    ("generic", "AGENT.md", "file", "Generic singular AGENT.md"),
    ("generic", "AGENTS.local.md", "file", "Local override AGENTS.md"),
    ("generic", ".agents", "dir", "Generic agents directory"),
]


def _is_file(p: Path) -> bool:
    try:
        return p.is_file()
    except OSError:
        return False


def _is_dir(p: Path) -> bool:
    try:
        return p.is_dir()
    except OSError:
        return False


def _preview(path: Path, max_lines: int = 5) -> str:
    if not _is_file(path):
        return ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    lines = text.splitlines()[:max_lines]
    return "\n".join(lines)


def _line_count(path: Path) -> int:
    if not _is_file(path):
        return 0
    try:
        return sum(1 for _ in path.open("rb"))
    except OSError:
        return 0


def _size(path: Path) -> int:
    try:
        return path.stat().st_size
    except OSError:
        return 0


def scan(root: Path) -> ScanReport:
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Project root not found: {root}")
    report = ScanReport(project_root=str(root.resolve()))

    for tool, rel, kind, notes in SOURCES:
        path = root / rel
        if kind == "file":
            exists = _is_file(path)
        else:
            exists = _is_dir(path)
        hit = SourceHit(
            tool=tool,
            path=rel,
            exists=exists,
            size_bytes=_size(path) if exists and kind == "file" else 0,
            line_count=_line_count(path) if exists and kind == "file" else 0,
            preview=_preview(path) if exists and kind == "file" else "",
            notes=notes,
        )
        report.hits.append(hit)
        if not exists:
            continue
        if tool == "opencode":
            report.opencode_native_present = True
            report.opencode_native_paths.append(rel)
        else:
            report.external_rules_present.append(rel)

    report.recommended_action = _recommend(report)
    return report


def _recommend(report: ScanReport) -> str:
    if not report.opencode_native_present and not report.has_external_rules:
        return ("No agent-rules files present. Run `/init-harness` to scaffold "
                "AGENTS.md + .opencode/docs + DESIGN.md from scratch.")
    if not report.opencode_native_present and report.has_external_rules:
        return (f"External rules present ({len(report.external_rules_present)} "
                f"file(s)) but no OpenCode native AGENTS.md. Run `/init-harness` "
                f"to import + harmonize external rules into AGENTS.md + "
                f".opencode/docs/SOURCE_RULES.md (audit trail).")
    if report.opencode_native_present and not report.has_external_rules:
        return ("OpenCode native rules present. No external rules to import. "
                "Optional: forward AGENTS.md rules to other tool formats if you "
                "also use Codex/Claude Code/Cursor in this project.")
    # both present
    return (f"Both OpenCode native ({len(report.opencode_native_paths)} path(s)) "
            f"and external rules ({len(report.external_rules_present)} file(s)) "
            f"present. Run `/init-harness` with `--harmonize` to detect conflicts, "
            f"merge where compatible, and keep both in sync via "
            f".opencode/docs/SOURCE_RULES.md (canonical).")


def render_text(report: ScanReport, summary_only: bool = False) -> str:
    out = [f"rules-source-scanner: {report.project_root}"]
    opencode_hits = [h for h in report.hits if h.tool == "opencode" and h.exists]
    external_hits = [h for h in report.hits if h.tool != "opencode" and h.exists]

    out.append(f"  OpenCode native present:  {len(opencode_hits)} ({', '.join(h.path for h in opencode_hits) or 'none'})")
    out.append(f"  External rules present:   {len(external_hits)}")
    for h in external_hits:
        out.append(f"    [{h.tool}] {h.path}  ({h.line_count} lines, {h.size_bytes} bytes)")

    if not summary_only:
        out.append("")
        out.append("All known sources (presence only):")
        for h in report.hits:
            mark = "✓" if h.exists else "·"
            out.append(f"  {mark} [{h.tool:13}] {h.path}")
        if external_hits:
            out.append("")
            out.append("Previews of detected external rules (first 5 lines each):")
            for h in external_hits[:8]:
                if h.preview:
                    out.append(f"  --- {h.path} ---")
                    for line in h.preview.splitlines():
                        out.append(f"    {line}")

    out.append("")
    out.append(f"Recommended action: {report.recommended_action}")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("project_root", nargs="?", default=".",
                   help="Project root to scan (default: current directory).")
    p.add_argument("--json", action="store_true", help="Emit JSON output.")
    p.add_argument("--summary-only", action="store_true",
                   help="Show only counts + recommendation, no per-source list.")
    args = p.parse_args(argv)

    try:
        report = scan(Path(args.project_root).resolve())
    except FileNotFoundError as e:
        print(f"rules-source-scanner: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({
            "project_root": report.project_root,
            "opencode_native_present": report.opencode_native_present,
            "opencode_native_paths": report.opencode_native_paths,
            "external_rules_present": report.external_rules_present,
            "recommended_action": report.recommended_action,
            "hits": [asdict(h) for h in report.hits],
        }, indent=2))
    else:
        print(render_text(report, summary_only=args.summary_only))
    return 0


if __name__ == "__main__":
    sys.exit(main())
