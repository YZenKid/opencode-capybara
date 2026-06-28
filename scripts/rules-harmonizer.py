#!/usr/bin/env python3
"""Import and harmonize external agent-rules files into the OpenCode native format.

When a project has rules files from other tools (Claude Code `CLAUDE.md`,
Cursor `.cursorrules`, Codex `.codex/`, etc.), this script:

1. Reads each detected external file (output of `rules-source-scanner.py`).
2. Categorizes its content into rule buckets: routing, build/test,
   style, security, workflow, etc.
3. Writes an audit-trail file at `.opencode/docs/SOURCE_RULES.md` listing
   every imported rule, its source file, and the harmonized mapping.
4. Optionally (with --apply) updates the root `AGENTS.md` to include
   cross-references and a "Source rules" appendix that names the
   original tools and file paths.
5. Optionally (with --forward-to) writes a mirror of the harmonized
   rules to specified external tool files (e.g. `CLAUDE.md`,
   `.codex/AGENTS.md`, `.cursor/rules/`) so they stay in sync.

This is a soft harmonizer. It NEVER deletes or overwrites the source
files; it only reads them and writes the canonical `.opencode/docs/`
record + optional AGENTS.md update + optional forward mirrors.

Usage:
  python3 ~/.config/opencode/scripts/rules-harmonizer.py [project_root]
  python3 ~/.config/opencode/scripts/rules-harmonizer.py . --apply
  python3 ~/.config/opencode/scripts/rules-harmonizer.py . --forward-to claude,codex,cursor
  python3 ~/.config/opencode/scripts/rules-harmonizer.py --dry-run .
  python3 ~/.config/opencode/scripts/rules-harmonizer.py --help

Exit codes:
  0 = harmonization completed
  2 = invalid arguments or unreadable target
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class ExternalRule:
    source_tool: str
    source_path: str
    line_no: int
    text: str
    category: str = "uncategorized"
    harmonized_target: str = ""


@dataclass
class HarmonizeReport:
    project_root: str
    rules: list[ExternalRule] = field(default_factory=list)
    output_path: str = ""
    apply_applied: bool = False
    forward_targets: list[str] = field(default_factory=list)

    @property
    def has_rules(self) -> bool:
        return bool(self.rules)


# Categorization rules: ordered by priority. First match wins.
# Priority order matters: more specific (security, data) must come BEFORE
# broader buckets (git_workflow, build_test) so that, e.g., "never commit
# .env" is recognized as a security rule, not a git-workflow rule.
CATEGORY_RULES: list[tuple[str, str]] = [
    ("routing", r"\b(?:route|delegate|orchestrat|orchestrator|@[\w-]+|"
                 r"dispatch|handoff|escalat)\b"),
    ("security_secrets", r"\b(?:secret|\.env|api\s*key|token|credential|"
                         r"password|passwordless|rbac|auth|permission|"
                         r"encryption|pii|gdpr|hipaa|soc2|"
                         r"never\s+commit|don'?t\s+commit|do\s+not\s+commit)\b"),
    ("data_db", r"\b(?:database|migration|schema|sql|postgres|mysql|"
                r"redis|orm|eloquent|prisma|drizzle|mongoose)\b"),
    ("build_test", r"\b(?:build|test|spec|lint|coverage|tdd|jest|pytest|"
                   r"phpunit|pest|cargo\s+test|go\s+test|vitest|"
                   r"playwright|cypress)\b"),
    ("deployment", r"\b(?:deploy|ci/cd|github\s+actions|vercel|netlify|"
                   r"docker|kubernetes|k8s|terraform|ansible|"
                   r"release|rollback)\b"),
    ("dependency", r"\b(?:depend|composer|npm|yarn|pnpm|bun|pip|poetry|"
                   r"go\s+mod|cargo|pubspec|gem|bundle)\b"),
    ("style_format", r"\b(?:format|prettier|eslint|pint|black|gofmt|"
                     r"rustfmt|tabs|spaces|indent|line\s+length|"
                     r"naming\s+convention|snake_case|camelCase|PascalCase)\b"),
    ("ui_design", r"\b(?:design|figma|tailwind|shadcn|component|"
                 r"responsive|accessibility|a11y|wcag|hero|landing)\b"),
    ("git_workflow", r"\b(?:commit|pull\s+request|merge|rebase|branch|"
                     r"tag|conventional\s+commit|changelog|monorepo|"
                     r"submodule|worktree)\b"),
    ("docs", r"\b(?:readme|changelog|jsdoc|docstring|comment|"
             r"documentation|docs/)\b"),
]


def _categorize(text: str) -> str:
    for cat, pattern in CATEGORY_RULES:
        if re.search(pattern, text, re.IGNORECASE):
            return cat
    return "uncategorized"


def _harmonized_target(category: str, source_tool: str) -> str:
    """Map a category to where it should be documented in OpenCode native."""
    mapping = {
        "routing": "AGENTS.md (Default Flow + Risk Triggers) + .opencode/docs/AGENT_ROUTING.md",
        "build_test": ".opencode/docs/PROJECT_COMMANDS.md + .opencode/docs/FRAMEWORK_PLAYBOOK.md",
        "style_format": ".opencode/docs/FRAMEWORK_PLAYBOOK.md (under style/conventions)",
        "security_secrets": ".opencode/docs/SECURITY.md",
        "git_workflow": "AGENTS.md (Non-negotiable Rules) + .opencode/docs/RELEASE.md",
        "dependency": ".opencode/docs/PROJECT_STACK.md + .opencode/docs/PROJECT_COMMANDS.md",
        "deployment": ".opencode/docs/RELEASE.md + .opencode/docs/PROJECT_COMMANDS.md",
        "docs": "AGENTS.md (Notes) + .opencode/docs/index.md",
        "data_db": ".opencode/docs/PROJECT_STACK.md + .opencode/docs/FRAMEWORK_PLAYBOOK.md",
        "ui_design": ".opencode/docs/DESIGN.md (project) + .opencode/docs/AGENT_ROUTING.md (UI/UX section)",
        "uncategorized": "AGENTS.md (Notes) + .opencode/docs/SOURCE_RULES.md (audit)",
    }
    return mapping.get(category, mapping["uncategorized"])


# Tool -> known external file path (mirrors rules-source-scanner.py)
EXTERNAL_PATHS: dict[str, list[str]] = {
    "claude-code": ["CLAUDE.md", ".claude/agents"],
    "codex": ["AGENTS.md", ".codex", ".codex/AGENTS.md"],
    "cursor": [".cursorrules", ".cursor/rules"],
    "windsurf": [".windsurfrules", ".windsurf/rules"],
    "continue": [".continue/config.json"],
    "cline": [".clinerules", ".cline"],
    "cody": [".cody/agents.md"],
    "aider": ["CONVENTIONS.md", ".aider.conf.yml"],
    "github": [".github/agents.md", ".github/copilot-instructions.md"],
    "gitlab": [".gitlab/agents.md"],
    "generic": ["AGENT.md", "AGENTS.local.md", ".agents"],
}


def _read_text_file(path: Path) -> str:
    if not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _list_dir_files(path: Path, extensions: tuple = (".md", ".txt", ".yml", ".yaml", ".json")) -> list[Path]:
    if not path.is_dir():
        return []
    out: list[Path] = []
    for ext in extensions:
        out.extend(path.glob(f"*{ext}"))
    return sorted(out)


def _extract_rules_from_text(tool: str, rel_path: str, text: str) -> list[ExternalRule]:
    """Extract individual rules from a markdown-ish text.

    Strategy: a rule is a line that is non-empty, non-heading-only,
    and not just punctuation. Headings and blank lines are kept as
    context but not classified as rules themselves.

    Skips lines inside the "Imported rules" section of a forward-mirror
    file so re-running the harmonizer on a previously-mirrored project
    does not multiply the rule count.
    """
    rules: list[ExternalRule] = []
    in_imported_section = False
    in_opencode_derived = False
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            # blank lines do NOT close the imported/derived section;
            # only the next top-level heading does
            continue
        # Detect OpenCode-derived mirror header (blockquote pattern)
        if line.startswith(">") and "OpenCode-derived" in line:
            in_opencode_derived = True
            continue
        if line.startswith(">"):
            continue  # inside blockquote intro
        if in_opencode_derived and not line.startswith("#"):
            # Inside the OpenCode-derived body; skip until next top-level heading
            continue
        if in_opencode_derived and line.startswith("#"):
            in_opencode_derived = False
        # Top-level headings (level 1 only) close the mirror body section
        # and the "imported rules" sub-section. Sub-headings (level 2+)
        # are content, not section terminators.
        if line.startswith("# "):
            # level-1 heading closes any active section
            in_imported_section = False
            in_opencode_derived = False
            continue
        if line.startswith("## "):
            # level-2 heading opens/closes the "imported rules" section
            in_imported_section = line.lower().startswith("## imported rules")
            continue
        if line.startswith("<!--") and line.endswith("-->"):
            continue
        if re.match(r"^[-*_]{3,}$", line):
            continue
        if line.startswith("#") or line.startswith("//"):
            continue
        if in_imported_section:
            continue
        rules.append(ExternalRule(
            source_tool=tool,
            source_path=rel_path,
            line_no=i,
            text=line,
        ))
    return rules


def collect_external_rules(root: Path) -> list[ExternalRule]:
    rules: list[ExternalRule] = []
    for tool, paths in EXTERNAL_PATHS.items():
        for rel in paths:
            p = root / rel
            if not p.exists():
                continue
            if p.is_file():
                text = _read_text_file(p)
                rules.extend(_extract_rules_from_text(tool, rel, text))
            elif p.is_dir():
                for f in _list_dir_files(p):
                    if f.is_file():
                        text = _read_text_file(f)
                        rel_in_dir = f"{rel}/{f.relative_to(p).as_posix()}"
                        rules.extend(_extract_rules_from_text(tool, rel_in_dir, text))
    # Categorize and assign target
    for r in rules:
        r.category = _categorize(r.text)
        r.harmonized_target = _harmonized_target(r.category, r.source_tool)
    return rules


def _group_by_category(rules: list[ExternalRule]) -> dict[str, list[ExternalRule]]:
    groups: dict[str, list[ExternalRule]] = {}
    for r in rules:
        groups.setdefault(r.category, []).append(r)
    return groups


def render_source_rules_markdown(report: HarmonizeReport) -> str:
    out: list[str] = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out.append("# Source Rules (Imported Audit Trail)")
    out.append("")
    out.append(f"Project: `{report.project_root}`")
    out.append(f"Generated: {now}")
    out.append("")
    out.append("This file is the canonical audit trail for rules imported from")
    out.append("external agent-tools (Claude Code, Cursor, Codex, etc.) into this")
    out.append("project's OpenCode-native format. It is generated by")
    out.append("`python3 ~/.config/opencode/scripts/rules-harmonizer.py`.")
    out.append("")
    out.append("Local OpenCode `AGENTS.md` and `.opencode/docs/` remain the source")
    out.append("of truth for routing. The source rules below are kept for")
    out.append("transparency and to ensure external tools (if used in the same")
    out.append("project) can be re-synced via `--forward-to`.")
    out.append("")
    if not report.has_rules:
        out.append("No external rules files were detected. Run")
        out.append("`python3 ~/.config/opencode/scripts/rules-source-scanner.py .`")
        out.append("to confirm.")
        return "\n".join(out)

    out.append(f"Total rules imported: {len(report.rules)}")
    out.append("")
    out.append("Tools that contributed rules:")
    tools_seen: dict[str, int] = {}
    for r in report.rules:
        tools_seen[r.source_tool] = tools_seen.get(r.source_tool, 0) + 1
    for tool, count in sorted(tools_seen.items()):
        out.append(f"- `{tool}`: {count} rule(s)")
    out.append("")

    # Group by category
    by_cat = _group_by_category(report.rules)
    out.append("## Rules by category")
    out.append("")
    for cat in sorted(by_cat):
        items = by_cat[cat]
        out.append(f"### {cat} ({len(items)})")
        out.append("")
        # Group by source file within category
        by_source: dict[str, list[ExternalRule]] = {}
        for r in items:
            by_source.setdefault(r.source_path, []).append(r)
        for src, src_rules in by_source.items():
            tool = src_rules[0].source_tool
            out.append(f"- **From `{src}` ({tool}):**")
            for r in src_rules:
                target = r.harmonized_target
                snippet = r.text
                if len(snippet) > 200:
                    snippet = snippet[:200] + "..."
                out.append(f"  - L{r.line_no}: {snippet}")
                out.append(f"    → harmonized to: `{target}`")
            out.append("")

    out.append("## How to use this audit")
    out.append("")
    out.append("- When updating `AGENTS.md` or `.opencode/docs/`, keep this")
    out.append("  file in sync so the import provenance is preserved.")
    out.append("- When removing an external tool's rules file, re-run")
    out.append("  `--apply` to drop the corresponding entries here.")
    out.append("- When re-syncing external tools (after OpenCode-side rule")
    out.append("  changes), re-run with `--forward-to claude,codex,cursor`")
    out.append("  to write harmonized mirrors back to the external files.")
    out.append("")
    return "\n".join(out)


def update_agents_md_appendix(root: Path, rules: list[ExternalRule]) -> None:
    """Append a 'Source Rules' section to AGENTS.md if not already present."""
    agents_path = root / "AGENTS.md"
    if not agents_path.exists():
        return
    text = agents_path.read_text(encoding="utf-8", errors="replace")
    marker = "## Source Rules"
    if marker in text:
        return  # already appended
    tools = sorted({r.source_tool for r in rules})
    appendix = [
        "",
        "## Source Rules",
        "",
        "This project's `AGENTS.md` is the primary source of truth. Additional",
        "rules imported from external agent-tools are recorded at",
        "`.opencode/docs/SOURCE_RULES.md` (audit trail) and may also exist in:",
        "",
    ]
    for tool in tools:
        appendix.append(f"- `{tool}` rules — see `.opencode/docs/SOURCE_RULES.md`")
    appendix.append("")
    appendix.append("When in doubt, OpenCode-native rules (this file + `.opencode/docs/`)")
    appendix.append("win. Run `/init-harness` to re-synchronize.")
    appendix.append("")
    agents_path.write_text(text + "\n".join(appendix), encoding="utf-8")


def write_forward_mirrors(root: Path, rules: list[ExternalRule],
                        targets: list[str]) -> list[str]:
    """Write a condensed mirror of the imported rules to each target file.

    Each mirror file gets a header explaining it is a derived copy of
    OpenCode's audit trail, plus the categorized rule list. Existing
    content is preserved (header appended) so as not to clobber
    project-specific notes.
    """
    written: list[str] = []
    by_cat = _group_by_category(rules)
    body_lines = [
        "# Source rules mirror (OpenCode-derived)",
        "",
        "> This file is a mirror generated by",
        "> `python3 ~/.config/opencode/scripts/rules-harmonizer.py --forward-to`.",
        "> Edit `.opencode/docs/SOURCE_RULES.md` and re-run the harmonizer",
        "> to refresh. OpenCode-native `AGENTS.md` + `.opencode/docs/`",
        "> remain the source of truth.",
        "",
        "## Imported rules",
        "",
    ]
    for cat in sorted(by_cat):
        body_lines.append(f"### {cat}")
        body_lines.append("")
        for r in by_cat[cat]:
            snippet = r.text
            if len(snippet) > 200:
                snippet = snippet[:200] + "..."
            body_lines.append(f"- (from `{r.source_path}` L{r.line_no}) {snippet}")
        body_lines.append("")
    body = "\n".join(body_lines)

    target_paths: dict[str, str] = {
        "claude": "CLAUDE.md",
        "codex": ".codex/AGENTS.md",
        "cursor": ".cursor/rules/OPENCODE_HARMONIZED.md",
        "windsurf": ".windsurf/rules/OPENCODE_HARMONIZED.md",
    }
    for tgt in targets:
        rel = target_paths.get(tgt.strip())
        if not rel:
            continue
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        existing = _read_text_file(p)
        if not existing:
            p.write_text(body, encoding="utf-8")
        else:
            # Append with a clear separator; do not clobber
            sep = "\n\n---\n\n"
            if "OPENCODE_HARMONIZED" in existing or "OpenCode-derived" in existing:
                # Already mirrored; skip append to avoid duplication
                written.append(str(p) + " (already mirrored; skipped)")
                continue
            p.write_text(existing + sep + body, encoding="utf-8")
        written.append(str(p))
    return written


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("project_root", nargs="?", default=".",
                   help="Project root to harmonize (default: current directory).")
    p.add_argument("--apply", action="store_true",
                   help="Append a 'Source Rules' section to root AGENTS.md.")
    p.add_argument("--forward-to", metavar="TOOLS",
                   help="Comma-separated list of external tools to mirror to. "
                        "Supported: claude, codex, cursor, windsurf.")
    p.add_argument("--dry-run", action="store_true",
                   help="Report what would be written without writing anything.")
    args = p.parse_args(argv)

    root = Path(args.project_root).resolve()
    if not root.exists() or not root.is_dir():
        print(f"rules-harmonizer: project root not found: {root}", file=sys.stderr)
        return 2

    rules = collect_external_rules(root)
    report = HarmonizeReport(
        project_root=str(root),
        rules=rules,
    )

    # Decide output path
    opencode_docs = root / ".opencode" / "docs"
    output_path = opencode_docs / "SOURCE_RULES.md"
    report.output_path = str(output_path)

    if args.dry_run:
        print(f"rules-harmonizer: DRY RUN for {root}")
        print(f"  external rules found: {len(rules)}")
        if rules:
            by_cat = _group_by_category(rules)
            print(f"  by category:")
            for cat, items in sorted(by_cat.items()):
                print(f"    {cat}: {len(items)}")
        print(f"  would write: {output_path}")
        if args.apply:
            print(f"  would append to: {root / 'AGENTS.md'}")
        if args.forward_to:
            print(f"  would forward to: {args.forward_to}")
        return 0

    # Write the audit-trail file
    opencode_docs.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_source_rules_markdown(report), encoding="utf-8")
    print(f"rules-harmonizer: wrote {output_path} ({len(rules)} rule(s))")

    # Optionally apply to AGENTS.md
    if args.apply and rules:
        update_agents_md_appendix(root, rules)
        report.apply_applied = True
        print(f"rules-harmonizer: appended Source Rules section to "
              f"{root / 'AGENTS.md'}")

    # Optionally forward to external tool files
    if args.forward_to and rules:
        targets = [t.strip() for t in args.forward_to.split(",") if t.strip()]
        written = write_forward_mirrors(root, rules, targets)
        report.forward_targets = written
        for w in written:
            print(f"rules-harmonizer: forwarded to {w}")

    if not rules:
        print(f"rules-harmonizer: no external rules found in {root}. "
              f"Wrote empty audit trail at {output_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
