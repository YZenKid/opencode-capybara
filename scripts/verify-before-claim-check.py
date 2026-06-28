#!/usr/bin/env python3
"""Verify-Before-Claim sanity check.

Reads a response transcript (chat log, evidence summary, or final summary)
and flags prose claims that look like factual assertions about code/runtime
state but lack a matching tool call that could have produced that fact.

This is a soft helper, not a hard gate. It catches the most common
"agent said X without verifying X" pattern; it does not catch every
form of overclaim. Use it to audit responses, not to auto-reject.

Usage:
  # Audit a markdown evidence file or chat log
  python3 ~/.config/opencode/scripts/verify-before-claim-check.py .opencode/evidence/<task>/summary.md
  # Pipe a single response (stdin)
  echo "the file contains 5 functions" | python3 verify-before-claim-check.py -
  # JSON output for CI
  python3 verify-before-claim-check.py <path> --json
  # Strict mode (exit non-zero on any flag)
  python3 verify-before-claim-check.py <path> --strict

Claim pattern categories (each maps to a required verification tool):
  file_content  → read_file / cat / grep / search_files
  function_def  → grep -n / search_files
  service_port  → ss -tlnp / curl / netstat
  package_ver   → pip show / npm ls / cat package.json
  doc_claim     → web_extract / librarian / web_search
  db_schema     → psql / sql client
  container_run → docker ps / podman ps
  env_var       → printenv / grep .env
  runtime       → terminal command output

Exit codes:
  0 = no flagged claims (or only `assumption` / `unverified` labels that the
      response itself acknowledges)
  1 = flagged confident claims without recorded verification
  2 = error (file not found, parse failure, etc.)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# Claim patterns. Each pattern: (label, regex, list of "verifying tool" tokens)
# A claim is considered "verified" if any of the listed tool tokens appears
# nearby in the transcript (within N lines) OR if the claim itself contains
# an explicit `confirmed_*` / `assumption` / `unverified` label.
CLAIM_PATTERNS: list[tuple[str, re.Pattern[str], set[str]]] = [
    (
        "file_content",
        re.compile(
            r"\b(the\s+file\s+(?:[\w./-]+\s+)?contains|"
            r"config\s+[\w.-]+\s+(?:is|are)\s+set\s+to|"
            r"(?:is|are)\s+(?:defined|declared|configured)\s+in\s+[\w./-]+\.[a-z]+)",
            re.IGNORECASE,
        ),
        {"read_file", "cat", "grep", "search_files", "rg", "head", "tail"},
    ),
    (
        "function_def",
        re.compile(
            r"\b(?:function|method|class|def)\s+[\w.]+\s+(?:is\s+(?:defined|lives|exists|resides)\s+in|"
            r"returns|exposes|has\s+the\s+signature)",
            re.IGNORECASE,
        ),
        {"grep", "rg", "search_files"},
    ),
    (
        "service_port",
        re.compile(
            r"\b(?:postgres|postgresql|mysql|redis|mongo|mongodb|nginx|caddy|"
            r"apache|traefik|minio|rabbitmq|wa|waha|cloudflared|cloudflare)\s+"
            r"(?:is\s+running|listens|runs)\s+(?:on\s+)?port\s+\d+",
            re.IGNORECASE,
        ),
        {"ss -tlnp", "netstat", "curl", "lsof"},
    ),
    (
        "service_generic",
        re.compile(
            r"\b(?:your\s+)?(?:postgres|postgresql|mysql|redis|mongo|minio|wa|waha|"
            r"cloudflared|cloudflare|nginx|caddy|apache|traefik)\s+(?:is\s+running|"
            r"is\s+up|is\s+down|is\s+installed|is\s+configured)",
            re.IGNORECASE,
        ),
        {"systemctl", "ps aux", "ss -tlnp", "docker ps", "podman ps"},
    ),
    (
        "package_ver",
        re.compile(
            r"\b(?:(?:version|ver\.?)\s+(?:of\s+)?[\w.-]+\s+is|"
            r"package\s+(?:version\s+)?[\w.-]+\s+(?:is\s+)?(?:installed|at\s+version)|"
            r"using\s+[\w.-]+\s+v?\d+\.\d+|"
            r"(?:installed|installed\s+at)\s+(?:at\s+)?v?\d+\.\d+|"
            r"package\s+version\s+is\s+v?\d+\.\d+)",
            re.IGNORECASE,
        ),
        {"pip show", "npm ls", "cat package.json", "cat requirements.txt",
         "cat pyproject.toml", "cat Cargo.toml", "cat go.mod"},
    ),
    (
        "doc_claim",
        re.compile(
            r"\b(?:according\s+to\s+(?:the\s+)?(?:docs?|documentation|api\s+ref)|"
            r"(?:the\s+)?docs?\s+say|the\s+api\s+(?:docs?\s+)?(?:say|state))",
            re.IGNORECASE,
        ),
        {"web_extract", "web_search", "@librarian", "context7"},
    ),
    (
        "previous_session",
        re.compile(
            r"\b(?:(?:in|earlier|before|previously)\s+(?:the\s+)?(?:previous|last|earlier)\s+(?:session|turn|conversation|message|slice|run)|"
            r"we\s+(?:already\s+)?(?:did|set\s+up|configured|installed|created|made|wrote|deployed)\s+(?:it\s+)?(?:before|earlier|last\s+time|previously)|"
            r"from\s+(?:a|an)\s+(?:previous|earlier|prior)\s+(?:session|turn|slice)|"
            r"remember\s+(?:when|that)\s+we|"
            r"as\s+(?:we|you)\s+(?:discussed|mentioned|agreed)\s+(?:earlier|before|previously))",
            re.IGNORECASE,
        ),
        {"session_search"},
    ),
    (
        "container_run",
        re.compile(
            r"\bcontainer\s+[\w./-]+\s+is\s+(?:running|up|stopped|down|restarting)",
            re.IGNORECASE,
        ),
        {"docker ps", "podman ps", "docker inspect", "podman inspect"},
    ),
    (
        "env_var",
        re.compile(
            r"\b(?:env(?:ironment)?\s+var(?:iable)?|var)\s+[A-Z_][A-Z0-9_]+\s+is\s+set",
            re.IGNORECASE,
        ),
        {"printenv", "env |", "grep .env", "cat .env"},
    ),
    (
        "repo_state",
        re.compile(
            r"\b(?:the\s+(?:repo|repository|project)\s+(?:already\s+)?(?:uses|has|contains|includes))\b",
            re.IGNORECASE,
        ),
        {"cat", "ls", "find", "grep", "rg", "search_files", "read_file", "git ls-files"},
    ),
]

# Explicit verification labels. If the claim is followed by one of these
# (within ~80 chars), the claim is self-labeled and not flagged.
VERIFICATION_LABELS = re.compile(
    r"\b(confirmed_repo|confirmed_runtime|confirmed_docs|user_confirmed|"
    r"assumption|unverified|assumed|repo-local\s+only|first-principles|"
    r"I\s+haven'?t\s+(?:verified|checked)|I'?m\s+inferring|to\s+confirm)\b",
    re.IGNORECASE,
)

# Tool-call sentinel: lines that look like they came from a tool execution.
# We look for the typical agent shell/tool prefix patterns.
TOOL_CALL_SENTINEL = re.compile(
    r"^\s*(?:"
    r"\$|"
    r"cat\s+[\w./-]+|"
    r"grep\s+|"
    r"rg\s+|"
    r"read_file|"
    r"search_files|"
    r"ss\s+|"
    r"netstat|"
    r"curl\s+|"
    r"pip\s+show|"
    r"npm\s+ls|"
    r"systemctl\s+|"
    r"docker\s+|"
    r"podman\s+|"
    r"printenv|"
    r"web_extract|"
    r"web_search|"
    r"session_search|"
    r"librarian|"
    r"@librarian|"
    r"@explorer|"
    r">\s+"
    r")",
    re.IGNORECASE,
)


@dataclass
class Flag:
    category: str
    line_no: int
    text: str
    reason: str
    suggested_verification: str


@dataclass
class Report:
    file: str
    flagged: list[Flag] = field(default_factory=list)
    total_claims_scanned: int = 0
    total_self_labeled: int = 0

    @property
    def clean(self) -> bool:
        return not self.flagged


def _nearby_has_tool_call(lines: list[str], idx: int, window: int = 12) -> bool:
    """Check whether any line within ±`window` of `idx` looks like a tool call.

    The window covers natural conversation flow: orchestrator may write
    intro prose, then the tool call, then the claim about the result.
    A 12-line window accommodates 6+ paragraphs of intermediate prose
    while still requiring the verification to be in the same response.
    """
    lo = max(0, idx - window)
    hi = min(len(lines), idx + window + 1)
    for j in range(lo, hi):
        if TOOL_CALL_SENTINEL.match(lines[j]):
            return True
    return False


def _self_labeled(line: str) -> bool:
    return bool(VERIFICATION_LABELS.search(line))


def scan_text(text: str, source: str) -> Report:
    lines = text.splitlines()
    report = Report(file=source)
    for idx, line in enumerate(lines):
        for category, pattern, verifying_tools in CLAIM_PATTERNS:
            for m in pattern.finditer(line):
                report.total_claims_scanned += 1
                if _self_labeled(line):
                    report.total_self_labeled += 1
                    continue
                if _nearby_has_tool_call(lines, idx):
                    continue
                report.flagged.append(Flag(
                    category=category,
                    line_no=idx + 1,
                    text=line.strip()[:240],
                    reason="Confident claim about code/runtime state without a "
                           "nearby tool call AND without an explicit "
                           "`confirmed_*` / `assumption` / `unverified` label.",
                    suggested_verification=" or ".join(sorted(verifying_tools)),
                ))
    return report


def render_text(report: Report) -> str:
    out = [f"verify-before-claim-check: {report.file}"]
    out.append(f"  claims scanned:        {report.total_claims_scanned}")
    out.append(f"  self-labeled:          {report.total_self_labeled}")
    out.append(f"  flagged (no verify):   {len(report.flagged)}")
    if report.flagged:
        out.append("")
        out.append("FLAGGED CLAIMS:")
        for f in report.flagged:
            out.append(f"  [{f.category}] line {f.line_no}")
            out.append(f"    {f.text}")
            out.append(f"    -> verify with: {f.suggested_verification}")
        out.append("")
        out.append("These claims look like factual assertions about the user's "
                    "code, runtime, or environment but lack a nearby tool call "
                    "and lack an explicit `assumption` / `unverified` label. "
                    "Re-verify, re-label, or rephrase to honest uncertainty.")
    else:
        out.append("  ok.")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("path", help="Path to a markdown/text file, or '-' for stdin.")
    p.add_argument("--json", action="store_true", help="Emit JSON report.")
    p.add_argument("--strict", action="store_true",
                   help="Exit non-zero on any flagged claim (default: exit 0 "
                        "with a report; use in CI to enforce).")
    args = p.parse_args(argv)

    try:
        if args.path == "-":
            text = sys.stdin.read()
            source = "<stdin>"
        else:
            text = Path(args.path).read_text(encoding="utf-8")
            source = args.path
    except OSError as e:
        print(f"verify-before-claim-check: cannot read {args.path}: {e}",
              file=sys.stderr)
        return 2

    report = scan_text(text, source)
    if args.json:
        print(json.dumps({
            "file": report.file,
            "clean": report.clean,
            "total_claims_scanned": report.total_claims_scanned,
            "total_self_labeled": report.total_self_labeled,
            "flagged": [asdict(f) for f in report.flagged],
        }, indent=2))
    else:
        print(render_text(report))

    if args.strict and not report.clean:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
