#!/usr/bin/env python3
"""Audit an OpenCode session transcript for skill/MCP activation defects.

Goal: detect the specific failure mode the user reported:
- answers/mechanics are unclear or meandering,
- a skill exists but was never really activated,
- useful MCPs were available but silently not used.

This is an advisory heuristic checker, not a runtime blocker. It can scan:
- a pasted transcript / exported chat log,
- an evidence summary,
- a plan file,
- or any markdown/plaintext that records the session flow.

Usage:
  python3 scripts/session-trace-audit.py path/to/transcript.md
  python3 scripts/session-trace-audit.py path/to/transcript.md --json
  python3 scripts/session-trace-audit.py path/to/transcript.md --strict
  cat transcript.md | python3 scripts/session-trace-audit.py -

Output classes:
- PASS: no obvious activation defects found
- WARN: likely clarity / activation / MCP-usage issues
- FAIL (only with --strict): any WARN counts as a non-zero exit for CI

Checks:
1. Non-trivial session should have a skill/MCP orientation block
   (`Skill I'm using`, `MCPs I'm using`, `What I'm checking first`) or
   equivalent (`Primary skill`, `Applicable MCPs`).
2. Declared skill should later influence execution (same transcript
   contains a concrete instruction from that domain or an explicit
   activation audit sentence).
3. Obvious MCPs should be used for obvious task classes unless a skip
   reason is recorded.
4. Multi-issue / cascading-debug sessions should use sequential-thinking.
5. Version-sensitive framework/API/library work should use context7 or
   an explicit skip reason.
6. Cross-session memory reuse: a session that records a verification
   claim (`confirmed_repo` / `confirmed_runtime` / `confirmed_docs`)
   with a topic keyword should reference the corresponding entry in
   `.opencode/memory/knowledge.json` if one exists, instead of
   re-deriving the same fact. Reported as `WARN memory_reuse_missed`
   when an obvious memory entry was not referenced.

ponytail: heuristic matching only; false positives/negatives are possible.
Upgrade path: parse structured OpenCode transcript format when available.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path


@dataclass
class Finding:
    level: str  # WARN
    code: str
    message: str
    evidence: list[str] = field(default_factory=list)


@dataclass
class Report:
    source: str
    findings: list[Finding] = field(default_factory=list)
    signals: dict = field(default_factory=dict)

    @property
    def status(self) -> str:
        return "PASS" if not self.findings else "WARN"


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8", errors="replace")


def find_lines(pattern: str, text: str) -> list[str]:
    rx = re.compile(pattern, re.IGNORECASE | re.MULTILINE)
    return [m.group(0).strip() for m in rx.finditer(text)]


def has(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text, re.IGNORECASE | re.MULTILINE))


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, re.IGNORECASE | re.MULTILINE))


def task_signals(text: str) -> dict:
    """Infer a few coarse task classes from transcript prose."""
    return {
        "multi_issue": (
            count(r"\bissue\s+[0-9]+\b", text) >= 2
            or count(r"\berror\b", text) >= 3
            or count(r"\bcommit\b", text) >= 2
            or has(r"cascade|cascading|root cause|chronology|reconstructed", text)
        ),
        "version_sensitive": has(
            r"atlas|migration|sdk|framework|version|api contract|schema drift|docs", text
        ),
        "broad_code_search": has(
            r"\bgrep_app\b|grep across|where is\b|call-site|which file\b|find ownership",
            text,
        ),
        "repo_remote_context": has(
            r"pull request|PR\b|github|branch|commit [0-9a-f]{6,}|remote", text
        ),
        "security_or_pattern_scan": has(
            r"security|secret|token|unsafe|anti-pattern|smell|semgrep|credential|password|auth|permission|rbac|xss|csrf|sql injection",
            text,
        ),
        "browser_ui_runtime": has(
            r"\bbrowser\b|\bui\b|\bdom\b|\bplaywright\b|\bpage\b|\bclick\b|\brender\b|\blayout\b|\bscreen\b",
            text,
        ),
    }


def declared_skills(text: str) -> list[str]:
    out = []
    for m in re.finditer(
        r"(?:Skill I'm using|Primary skill)\s*:\s*([\w-]+)",
        text,
        re.IGNORECASE,
    ):
        out.append(m.group(1))
    return out


def declared_mcps(text: str) -> list[str]:
    out = []
    for m in re.finditer(
        r"(?:MCPs I'm using|Applicable MCPs|Will use now)\s*:\s*([^\n]+)",
        text,
        re.IGNORECASE,
    ):
        raw = m.group(1)
        for part in re.split(r"[,/]|\band\b", raw):
            token = part.strip(" `.-")
            if token:
                out.append(token)
    return out


def used_mcps(text: str) -> set[str]:
    patterns = {
        "sequential-thinking": r"sequential[-_ ]thinking|sequential_thinking",
        "context7": r"\bcontext7\b",
        "grep_app": r"\bgrep_app\b|grep\.app|grep_app search",
        "github": r"\bgithub\b|pull request|PR\b|issue #[0-9]+",
        "semgrep": r"\bsemgrep\b",
        "playwright": r"\bplaywright\b",
        "shadcn": r"\bshadcn\b",
        "9router.web_search": r"9router|web_search",
    }
    used = set()
    for name, pat in patterns.items():
        if has(pat, text):
            used.add(name)
    return used


def skill_activation_evidence(skill: str, text: str) -> list[str]:
    """Very rough evidence that a skill influenced execution."""
    domain_patterns = {
        "opencode-backend": [r"go service|repository|migration|schema|transaction|http handler|sql"],
        "opencode-frontend": [r"component|page|tailwind|layout|responsive|accessibility"],
        "opencode-devops": [r"docker|systemd|deploy|ci/cd|env|monitor|rollback"],
        "opencode-quality-gate": [r"pass|fail|risk|regression|signoff|evidence"],
        "opencode-orchestrator": [r"route|delegate|specialist|lane|plan-first"],
        "opencode-librarian": [r"official docs|context7|web_extract|current docs"],
        "opencode-fixer": [r"patch|regression test|diff|fix applied|commit"],
    }
    pats = domain_patterns.get(skill, [])
    hits = []
    for pat in pats:
        if has(pat, text):
            hits.append(pat)
    if has(r"changed about the execution|skill activation audit", text):
        hits.append("activation_audit")
    return hits


def explicit_skip_reason(mcp: str, text: str) -> bool:
    return has(
        rf"(?:skip|not using|didn't use|tool unavailable|fallback).*{re.escape(mcp)}",
        text,
    )


VERIFICATION_PREFIX = re.compile(
    r"(?:confirmed_repo|confirmed_runtime|confirmed_docs|user_confirmed|assumption|unverified)\s*[:\-]\s*([^\n]+)",
    re.IGNORECASE,
)
MEMORY_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_./\-]{2,}")
KEYWORD_STOPWORDS = {
    "the", "this", "that", "with", "from", "into", "and", "for", "but", "not",
    "have", "has", "had", "was", "were", "are", "but", "yet", "use", "using",
    "uses", "used", "via", "after", "before", "should", "would", "could",
    "into", "onto", "over", "under", "then", "than", "because", "while",
    "case", "file", "line", "lines", "code", "work", "task", "session",
    "page", "test", "tests", "agent", "agents", "skill", "skills",
    "context", "memory", "claim", "claims", "claim_level",
    "tutorial", "example", "note", "notes", "doc", "docs",
}


def keyword_set(text: str) -> set[str]:
    return {tok.lower() for tok in MEMORY_TOKEN_RE.findall(text) if len(tok) >= 4} - KEYWORD_STOPWORDS


def load_memory_entries(project_root: Path) -> list[dict]:
    memory_path = project_root / ".opencode" / "memory" / "knowledge.json"
    if not memory_path.is_file():
        return []
    try:
        data = json.loads(memory_path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def memory_reuse_misses(text: str, project_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    entries = load_memory_entries(project_root)
    if not entries:
        return findings
    text_keywords = keyword_set(text)
    if not text_keywords:
        return findings
    for entry in entries:
        lesson = str(entry.get("lesson") or entry.get("text") or "")
        tags = entry.get("tags") or []
        ctx = str(entry.get("context") or "")
        corpus = " ".join([lesson, ctx, " ".join(tags) if isinstance(tags, list) else str(tags)])
        mem_keywords = keyword_set(corpus)
        overlap = text_keywords & mem_keywords
        if len(overlap) < 1:
            continue
        # Reuse signal present?
        cid = str(entry.get("id") or entry.get("memory_id") or lesson[:40])
        if re.search(rf"\bmemory[-_ ]?id\s*[:=]\s*{re.escape(cid)}", text, re.IGNORECASE):
            continue
        if re.search(rf"\b{re.escape(cid)}\b", text):
            continue
        if has(r"memory[-_ ]?reuse|memory[-_ ]?recall|reuse[d]? from memory|from memory", text):
            continue
        findings.append(Finding(
            level="WARN",
            code="memory_reuse_missed",
            message=(
                f"Memory entry '{cid}' looks relevant (overlap={sorted(overlap)[:5]}) "
                "but the session re-derived instead of referencing it."
            ),
            evidence=[cid, *sorted(overlap)[:5]],
        ))
    return findings


def audit(text: str, source: str) -> Report:
    report = Report(source=source)
    signals = task_signals(text)
    report.signals = signals

    orientation_present = any(
        has(pat, text)
        for pat in [
            r"Skill I'm using\s*:",
            r"MCPs I'm using\s*:",
            r"What I'm checking first\s*:",
            r"Primary skill\s*:",
            r"Applicable MCPs\s*:",
        ]
    )

    if any(signals.values()) and not orientation_present:
        report.findings.append(Finding(
            level="WARN",
            code="missing_orientation",
            message="Non-trivial session has no visible skill/MCP orientation block.",
            evidence=[
                "expected one of: Skill I'm using / Primary skill / MCPs I'm using / Applicable MCPs",
            ],
        ))

    skills = declared_skills(text)
    mcps_declared = declared_mcps(text)
    mcps_used = used_mcps(text)

    for skill in skills:
        ev = skill_activation_evidence(skill, text)
        if not ev:
            report.findings.append(Finding(
                level="WARN",
                code="skill_loaded_but_not_activated",
                message=f"Skill declared but no concrete activation evidence found: {skill}",
                evidence=[skill],
            ))

    if signals["multi_issue"] and "sequential-thinking" not in mcps_used and not explicit_skip_reason("sequential", text):
        report.findings.append(Finding(
            level="WARN",
            code="missing_sequential_thinking",
            message="Multi-issue / cascading-debug session did not show sequential-thinking usage or skip reason.",
            evidence=["multi_issue=true"],
        ))

    if signals["version_sensitive"] and "context7" not in mcps_used and not explicit_skip_reason("context7", text):
        report.findings.append(Finding(
            level="WARN",
            code="missing_context7",
            message="Version-sensitive framework/API/library work did not show context7 usage or skip reason.",
            evidence=["version_sensitive=true"],
        ))

    if signals["broad_code_search"] and "grep_app" not in mcps_used and not explicit_skip_reason("grep_app", text):
        report.findings.append(Finding(
            level="WARN",
            code="missing_grep_app",
            message="Broad code-search / ownership hunt had no grep_app usage or skip reason.",
            evidence=["broad_code_search=true"],
        ))

    if signals["repo_remote_context"] and "github" not in mcps_used and not explicit_skip_reason("github", text):
        report.findings.append(Finding(
            level="WARN",
            code="missing_github_mcp",
            message="Repo / PR / remote-state question had no github MCP usage or skip reason.",
            evidence=["repo_remote_context=true"],
        ))

    if signals["security_or_pattern_scan"] and "semgrep" not in mcps_used and not explicit_skip_reason("semgrep", text):
        report.findings.append(Finding(
            level="WARN",
            code="missing_semgrep",
            message="Security / anti-pattern scan task had no semgrep usage or skip reason.",
            evidence=["security_or_pattern_scan=true"],
        ))

    if signals["browser_ui_runtime"] and "playwright" not in mcps_used and not explicit_skip_reason("playwright", text):
        report.findings.append(Finding(
            level="WARN",
            code="missing_playwright",
            message="Browser/UI/runtime task had no playwright usage or skip reason.",
            evidence=["browser_ui_runtime=true"],
        ))

    for mcp in mcps_declared:
        norm = mcp.lower()
        if norm in {"sequential-thinking", "context7", "grep_app", "github", "semgrep", "playwright", "shadcn", "9router.web_search"}:
            if norm not in mcps_used and not explicit_skip_reason(norm, text):
                report.findings.append(Finding(
                    level="WARN",
                    code="declared_mcp_not_used",
                    message=f"Declared MCP but no later usage/skip evidence found: {mcp}",
                    evidence=[mcp],
                ))

    report.signals.update({
        "orientation_present": orientation_present,
        "declared_skills": skills,
        "declared_mcps": mcps_declared,
        "used_mcps": sorted(mcps_used),
    })
    return report


def render_text(report: Report) -> str:
    lines = [f"session-trace-audit: {report.source}", f"status: {report.status}", ""]
    lines.append("signals:")
    for k, v in report.signals.items():
        lines.append(f"  {k}: {v}")
    lines.append("")
    if not report.findings:
        lines.append("PASS: no obvious skill/MCP activation defects found.")
        return "\n".join(lines)
    lines.append(f"{len(report.findings)} finding(s):")
    for i, f in enumerate(report.findings, 1):
        lines.append(f"{i}. [{f.code}] {f.message}")
        for ev in f.evidence:
            lines.append(f"   - {ev}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", help="Transcript/evidence path, or '-' for stdin")
    p.add_argument("--json", action="store_true", help="Emit JSON report")
    p.add_argument("--strict", action="store_true", help="Exit non-zero on any WARN finding (CI mode)")
    p.add_argument("--project-root", default=".", help="Project root for memory cross-check")
    args = p.parse_args(argv)

    text = read_text(args.source)
    project_root = Path(args.project_root).resolve()
    report = audit(text, args.source)
    report.findings.extend(memory_reuse_misses(text, project_root))
    if args.json:
        print(json.dumps({
            "source": report.source,
            "status": report.status,
            "signals": report.signals,
            "findings": [asdict(f) for f in report.findings],
        }, indent=2))
    else:
        print(render_text(report))
    return 0 if report.status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
