#!/usr/bin/env python3
"""Cross-session memory reuse validator.

When a task is taking a verification action, the agent should reuse a
relevant entry from `.opencode/memory/knowledge.json` instead of
re-deriving the same fact from scratch. This script scans evidence,
plan, and handoff files for verification claims and cross-checks them
against the project memory store.

Why this exists:
- Cross-session memory is the second-most-frequent source of context
  drift (after prose-only delegation). The agent re-reads a file in
  session B that was already verified in session A, but the second
  verification is not the same fact: it can drift, and it can
  disagree with the first.
- Project memory (`scripts/project-memory.py`) is the official memory
  store. Subagents should grep/load it before claiming a fact.

This script does not enforce a hard fail by default. It is a
heuristic signal: for each verification claim that overlaps a memory
entry, the script emits a "reuse" hint. Missing reuse becomes a
finding only when a strict mode is requested.

Usage:
    python3 scripts/memory-reuse-check.py \\
        --project-root . \\
        --files .opencode/evidence/<task>/summary.md \\
                 .opencode/plans/<task>.md

    python3 scripts/memory-reuse-check.py \\
        --project-root . --json \\
        --files evidence.md plan.md

    # CI mode: emit a non-zero exit when any VERIFIED claim missed reuse
    python3 scripts/memory-reuse-check.py \\
        --project-root . --strict \\
        --files summary.md

Exit codes:
    0 = no missed reuses (or only advisory in non-strict mode)
    1 = strict mode and at least one missed reuse
    2 = file read error or malformed memory store
    4 = invocation error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

VERIFICATION_CLAIM = re.compile(
    r"\b(confirmed_repo|confirmed_runtime|confirmed_docs|user_confirmed)\b\s*[:\-]\s*([^\n]+)",
    re.IGNORECASE,
)
ASSUMPTION_CLAIM = re.compile(
    r"\b(assumption|unverified)\b\s*[:\-]\s*([^\n]+)",
    re.IGNORECASE,
)
MEMORY_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_./\-]{2,}")
KEYWORD_STOPWORDS = {
    "the", "this", "that", "with", "from", "into", "and", "for", "but", "not",
    "have", "has", "had", "was", "were", "are", "yet", "use", "using", "uses",
    "used", "via", "after", "before", "should", "would", "could", "onto",
    "over", "under", "then", "than", "because", "while", "case", "file",
    "line", "lines", "code", "work", "task", "session", "page", "test",
    "tests", "agent", "agents", "skill", "skills", "context", "memory",
    "claim", "claims", "claim_level", "tutorial", "example", "note", "notes",
    "doc", "docs", "read", "write", "json", "yaml", "stdout", "stderr",
    "true", "false", "string", "list", "dict", "none", "value", "values",
    "lane", "lanes", "block", "blocks", "verb", "noun",
}


def keyword_set(text: str) -> set[str]:
    return {tok.lower() for tok in MEMORY_TOKEN_RE.findall(text) if len(tok) >= 4} - KEYWORD_STOPWORDS


def load_memory_entries(project_root: Path) -> list[dict[str, Any]]:
    memory_path = project_root / ".opencode" / "memory" / "knowledge.json"
    if not memory_path.is_file():
        return []
    try:
        data = json.loads(memory_path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def find_reuse_signals(text: str) -> set[str]:
    """Return memory ids / categories the session actually referenced."""
    signals: set[str] = set()
    for m in re.finditer(
        r"\bmemory[-_ ]?(?:id|category)\s*[:=]\s*([\w\-./]+)",
        text, re.IGNORECASE,
    ):
        signals.add(m.group(1))
    for m in re.finditer(
        r"\b(?:reuse[d]?|recall(?:ed)?|loaded)\s+from\s+(?:memory|knowledge\.json)\s*[:=]?\s*([\w\-./]+)?",
        text, re.IGNORECASE,
    ):
        if m.group(1):
            signals.add(m.group(1))
    for m in re.finditer(
        r"\bproject-memory\.py\s+--load\b[^\n]*?--context\s+\"([^\"]+)\"",
        text,
    ):
        signals.add(m.group(1))
    return signals


def extract_claims(text: str) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for m in VERIFICATION_CLAIM.finditer(text):
        out.append((m.group(1).lower(), m.group(2).strip(), "verified"))
    for m in ASSUMPTION_CLAIM.finditer(text):
        out.append((m.group(1).lower(), m.group(2).strip(), "assumption"))
    return out


def build_findings(
    text: str,
    source: str,
    memory_entries: list[dict[str, Any]],
    reuse_signals: set[str],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not memory_entries:
        return findings
    claims = extract_claims(text)
    if not claims:
        return findings
    for level, claim_text, _kind in claims:
        claim_keywords = keyword_set(claim_text)
        if not claim_keywords:
            continue
        best: dict[str, Any] | None = None
        best_overlap: set[str] = set()
        for entry in memory_entries:
            lesson = str(entry.get("lesson") or entry.get("text") or "")
            ctx = str(entry.get("context") or "")
            tags = entry.get("tags") or []
            corpus = " ".join([lesson, ctx, " ".join(tags) if isinstance(tags, list) else str(tags)])
            mem_keywords = keyword_set(corpus)
            overlap = claim_keywords & mem_keywords
            if len(overlap) < 1:
                continue
            if len(overlap) > len(best_overlap):
                best = entry
                best_overlap = overlap
        if not best:
            continue
        eid = str(best.get("id") or best.get("memory_id") or str(best.get("lesson") or "")[:40])
        if eid in reuse_signals:
            continue
        if any(sig in claim_text for sig in reuse_signals):
            continue
        findings.append({
            "level": "WARN",
            "code": "memory_reuse_missed",
            "source": source,
            "claim": f"{level}: {claim_text}",
            "memory_id": eid,
            "overlap": sorted(best_overlap)[:6],
            "lesson_excerpt": str(best.get("lesson") or "")[:160],
        })
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--files", nargs="+", required=True, help="Markdown/JSON files to scan")
    ap.add_argument("--strict", action="store_true", help="Exit non-zero on any finding")
    ap.add_argument("--json", action="store_true", help="Emit JSON report")
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    if not args.files:
        print("error: --files is required", file=sys.stderr)
        return 4

    memory_entries = load_memory_entries(project_root)
    if not memory_entries:
        print(
            "info: no memory store at .opencode/memory/knowledge.json; reuse check is a no-op",
            file=sys.stderr,
        )

    all_findings: list[dict[str, Any]] = []
    read_errors: list[str] = []
    for raw in args.files:
        path = (project_root / raw).resolve() if not Path(raw).is_absolute() else Path(raw)
        if not path.is_file():
            read_errors.append(f"file not found: {raw}")
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            read_errors.append(f"read error: {raw}: {e}")
            continue
        reuse = find_reuse_signals(text)
        all_findings.extend(build_findings(text, str(path), memory_entries, reuse))

    report = {
        "project_root": str(project_root),
        "memory_entries_loaded": len(memory_entries),
        "files_scanned": len(args.files) - len(read_errors),
        "findings": all_findings,
        "ok": not all_findings,
        "read_errors": read_errors,
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        if all_findings:
            print(f"FAIL ({len(all_findings)} missed reuse(s)):")
            for f in all_findings:
                print(f"  - [{f['code']}] {f['source']}")
                print(f"      claim:   {f['claim']}")
                print(f"      memory:  {f['memory_id']}")
                print(f"      overlap: {f['overlap']}")
                print(f"      lesson:  {f['lesson_excerpt']}")
        else:
            if read_errors:
                print(f"WARN: scan completed with read errors: {read_errors}")
            else:
                print("OK (no missed memory reuse)")
    if read_errors:
        return 2
    return 0 if not all_findings else (1 if args.strict else 0)


if __name__ == "__main__":
    sys.exit(main())
