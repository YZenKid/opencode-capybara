#!/usr/bin/env python3
"""External legal/source inventory helper.

Purpose:
- inventory external sources before code/asset reuse,
- classify license/permission posture,
- flag high-risk reuse patterns early,
- discover likely license/terms pages and aggregate their evidence.

Usage:
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://example.com --kind website --json
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://github.com/user/repo --kind repo --summary-only
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://cdn.example.com/logo.svg --kind asset --intent direct-reuse --json
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://example.com --out /tmp/legal.json
  python3 ~/.config/opencode/scripts/legal-source-check.py \\
      --source https://example.com --project-root /tmp/proj --task-id demo \\
      # writes to /tmp/proj/.opencode/evidence/demo/legal-source-check.json

Exit codes:
  0 = report emitted, no blocking risk detected
  1 = emitted, but needs clarification / high-risk / restricted / unknown for requested intent
  2 = invocation error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import Any

LICENSE_PATTERNS = [
    (re.compile(r"\bMIT\b", re.I), "MIT"),
    (re.compile(r"\bApache(?:\s+License)?\s*2(?:\.0)?\b", re.I), "Apache-2.0"),
    (re.compile(r"\bBSD(?:[- ](?:2|3)[- ]Clause)?\b", re.I), "BSD"),
    (re.compile(r"\bISC\b", re.I), "ISC"),
    (re.compile(r"\bMPL\s*2(?:\.0)?\b", re.I), "MPL-2.0"),
    (re.compile(r"\bCC0(?:[- ]1\.0)?\b", re.I), "CC0-1.0"),
    (re.compile(r"\bUnlicense\b", re.I), "Unlicense"),
    (re.compile(r"\bLGPL\b", re.I), "LGPL"),
    (re.compile(r"\bGPL\b", re.I), "GPL"),
    (re.compile(r"\bAGPL\b", re.I), "AGPL"),
    (re.compile(r"\bSSPL\b", re.I), "SSPL"),
]

RESTRICTED_PATTERNS = [
    re.compile(r"all rights reserved", re.I),
    re.compile(r"do not (?:copy|reuse|redistribute)", re.I),
    re.compile(r"no scraping", re.I),
    re.compile(r"automated access prohibited", re.I),
    re.compile(r"watermark", re.I),
    re.compile(r"copyright\s+(?:all rights reserved|notice: do not copy|notice: reuse prohibited)", re.I),
]

PERMISSION_PATTERNS = [
    re.compile(r"licensed under", re.I),
    re.compile(r"permission granted", re.I),
    re.compile(r"open source", re.I),
    re.compile(r"creative commons", re.I),
]

HIGH_RISK_INTENTS = {"clone", "1:1", "copy-from", "direct-reuse"}


def fetch_text(url: str, limit: int = 50000) -> tuple[str, dict[str, str], str | None]:
    req = Request(url, headers={"User-Agent": "OpenCode legal-source-check/1.0"})
    with urlopen(req, timeout=15) as resp:
        raw = resp.read(limit)
        headers = {k.lower(): v for k, v in resp.headers.items()}
        charset = "utf-8"
        ctype = headers.get("content-type", "")
        m = re.search(r"charset=([^;\s]+)", ctype, re.I)
        if m:
            charset = m.group(1)
        text = raw.decode(charset, errors="replace")
        return text, headers, resp.geturl()


def classify_license(text: str) -> str:
    for pattern, label in LICENSE_PATTERNS:
        if pattern.search(text):
            return label
    return "unknown"


def source_classification(kind: str, headers: dict[str, str], text: str, license_label: str) -> str:
    robots = headers.get("x-robots-tag", "")
    if any(p.search(text) for p in RESTRICTED_PATTERNS) or "noindex" in robots.lower() or "nofollow" in robots.lower():
        return "restricted"
    if license_label != "unknown" or any(p.search(text) for p in PERMISSION_PATTERNS):
        return "licensed"
    if kind in {"website", "asset"}:
        return "public-but-unlicensed"
    return "unknown"


def license_risk(license_label: str) -> str:
    if license_label in {"MIT", "Apache-2.0", "BSD", "ISC", "MPL-2.0", "CC0-1.0", "Unlicense"}:
        return "permissive"
    if license_label in {"LGPL", "GPL", "AGPL", "SSPL"}:
        return "copyleft-or-caution"
    return "unknown"


def kind_from_url(url: str) -> str:
    path = urlparse(url).path.lower()
    if "github.com" in urlparse(url).netloc.lower():
        return "repo"
    if any(path.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".mp4", ".pdf")):
        return "asset"
    return "website"


def detect_high_risk(url: str, kind: str, intent: str, text: str) -> list[str]:
    out: list[str] = []
    host = urlparse(url).netloc.lower()
    if intent in HIGH_RISK_INTENTS and kind == "website":
        out.append("requested verbatim reuse from website source")
    if re.search(r"logo|trademark|brand assets?", text, re.I):
        out.append("source mentions logos/trademarks/brand assets")
    if re.search(r"watermark", text, re.I):
        out.append("source mentions watermark")
    if any(x in host for x in ("gettyimages", "shutterstock", "istockphoto", "adobe.com")):
        out.append("stock/media provider source detected")
    return out


def candidate_license_urls(source: str) -> list[str]:
    """Build likely license/terms page URLs to probe, based on source kind."""
    parsed = urlparse(source)
    netloc = parsed.netloc.lower()
    scheme = parsed.scheme or "https"
    base = f"{scheme}://{parsed.netloc}"
    path = parsed.path
    candidates: list[str] = []

    if "github.com" in netloc:
        # owner/repo
        parts = [p for p in path.split("/") if p][:2]
        if len(parts) == 2:
            owner, repo = parts
            for branch in ("HEAD", "main", "master"):
                for tail in ("/LICENSE", "/LICENSE.md", "/License.md", "/license.txt", "/COPYING"):
                    candidates.append(f"{scheme}://raw.githubusercontent.com/{owner}/{repo}/{branch}{tail}")
            for tail in ("/blob/HEAD/LICENSE", "/blob/HEAD/LICENSE.md", "/blob/HEAD/license.txt", "/blob/main/LICENSE", "/blob/master/LICENSE"):
                candidates.append(f"{base}/{owner}/{repo}{tail}")
            candidates.append(f"{base}/{owner}/{repo}")
        return candidates

    # generic website: probe common paths (try both bare and .html/.txt forms)
    for tail in ("/license", "/licence", "/legal", "/terms", "/terms-of-service", "/terms-and-conditions", "/copyright", "/about/license"):
        candidates.append(urljoin(base, tail))
        for ext in (".html", ".htm", ".txt", ".md"):
            candidates.append(urljoin(base, tail + ext))
    candidates.append(base)
    return candidates


def probe_license_pages(source: str, primary_text: str, limit: int = 20000) -> list[dict[str, Any]]:
    """Fetch each candidate license/terms URL and extract license + restriction hints."""
    out: list[dict[str, Any]] = []
    primary_host = urlparse(source).netloc.lower()
    for url in candidate_license_urls(source):
        try:
            text, headers, final = fetch_text(url, limit=limit)
        except (URLError, HTTPError, TimeoutError, ValueError):
            continue
        if urlparse(final).netloc.lower() != primary_host:
            # keep on the same host only
            continue
        ctype = headers.get("content-type", "").lower()
        if "html" not in ctype and "text" not in ctype:
            continue
        license_label = classify_license(text)
        restricted_hits = [p.pattern for p in RESTRICTED_PATTERNS if p.search(text)]
        permission_hits = [p.pattern for p in PERMISSION_PATTERNS if p.search(text)]
        if license_label == "unknown" and not restricted_hits and not permission_hits:
            continue
        out.append({
            "url": final,
            "license": license_label,
            "license_risk": license_risk(license_label),
            "restricted_hits": restricted_hits,
            "permission_hits": permission_hits,
            "byte_sample": len(text),
        })
    return out


def aggregate_license_evidence(discovery: list[dict[str, Any]]) -> str:
    """Combine license label from primary page + discovered pages; prefer the most specific non-unknown."""
    for entry in discovery:
        if entry["license"] not in {"", "unknown"}:
            return entry["license"]
    return "unknown"


def build_report(source: str, kind: str, intent: str) -> dict[str, Any]:
    text = ""
    headers: dict[str, str] = {}
    final_url = source
    fetch_error = None
    try:
        text, headers, final_url = fetch_text(source)
        final_url = str(final_url or source)
    except (URLError, HTTPError, TimeoutError, ValueError) as exc:
        fetch_error = str(exc)

    normalized_final_url: str = str(final_url or source)
    primary_license = classify_license(text) if text else "unknown"
    primary_classification = source_classification(kind, headers, text, primary_license) if text else "unknown"

    discovery = probe_license_pages(source, text) if text else []
    aggregated_license = aggregate_license_evidence([{"license": primary_license}] + discovery)
    classification = primary_classification
    license_label = primary_license
    if aggregated_license != "unknown":
        license_label = aggregated_license
        if primary_classification in {"public-but-unlicensed", "unknown"} and license_risk(license_label) == "permissive":
            classification = "licensed"

    risk = license_risk(license_label)
    high_risk_flags = detect_high_risk(normalized_final_url, kind, intent, text)
    for entry in discovery:
        if entry["restricted_hits"]:
            high_risk_flags.append(f"license page exposes restrictions: {entry['url']}")

    recommendations: list[str] = []
    needs_clarification = False
    if classification in {"public-but-unlicensed", "restricted", "unknown"} and intent in HIGH_RISK_INTENTS:
        needs_clarification = True
        recommendations.append("Do not reuse verbatim by default; ask for permission/license confirmation or switch to style-equivalent/structure-only output.")
    if classification == "restricted":
        needs_clarification = True
        recommendations.append("Do not bypass robots/terms/paywall/auth restrictions.")
    if risk == "copyleft-or-caution":
        needs_clarification = True
        recommendations.append("Escalate license risk before reuse.")
    if high_risk_flags:
        needs_clarification = True
        recommendations.append("High-risk asset/brand signal detected; prefer substitute, omit, or ask for explicit ownership/permission.")
    if not discovery and primary_license == "unknown" and kind in {"website", "repo"}:
        recommendations.append("Could not locate a license/terms page; record reason in evidence and treat as unknown unless user provides permission.")
    if not recommendations:
        recommendations.append("No immediate blocker detected from fetched metadata; still record source and permission status in evidence before direct reuse.")

    return {
        "schema": "legal-source-check/v1",
        "source": source,
        "final_url": normalized_final_url,
        "kind": kind,
        "intent": intent,
        "fetch_error": fetch_error,
        "headers": {
            "content-type": headers.get("content-type", ""),
            "x-robots-tag": headers.get("x-robots-tag", ""),
        },
        "license": license_label,
        "primary_license": primary_license,
        "license_risk": risk,
        "source_classification": classification,
        "high_risk_flags": high_risk_flags,
        "license_pages_probed": discovery,
        "needs_user_clarification": needs_clarification,
        "recommendations": recommendations,
    }


def resolve_evidence_path(args: argparse.Namespace) -> Path | None:
    if args.out:
        return Path(args.out).resolve()
    if args.project_root and args.task_id:
        safe_task = re.sub(r"[^A-Za-z0-9_.-]", "_", args.task_id)
        return (Path(args.project_root).resolve() / ".opencode" / "evidence" / safe_task / "legal-source-check.json")
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Inventory external source + license/risk posture before reuse")
    ap.add_argument("--source", required=True, help="External URL to inspect")
    ap.add_argument("--kind", choices=["website", "repo", "asset", "auto"], default="auto")
    ap.add_argument("--intent", choices=["reference-only", "style-equivalent", "direct-reuse", "copy-from", "clone", "1:1"], default="reference-only")
    ap.add_argument("--json", action="store_true", help="Emit JSON to stdout")
    ap.add_argument("--summary-only", action="store_true", help="Emit short human summary to stdout")
    ap.add_argument("--out", help="Write report JSON to this file (parent dirs are created)")
    ap.add_argument("--project-root", help="Project root for default evidence path (paired with --task-id)")
    ap.add_argument("--task-id", help="Task id for default evidence path; required with --project-root")
    args = ap.parse_args()

    parsed = urlparse(args.source)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        print(f"error: source must be a valid http/https URL: {args.source}", file=sys.stderr)
        return 2
    if (args.project_root and not args.task_id) or (args.task_id and not args.project_root):
        print("error: --project-root and --task-id must be used together", file=sys.stderr)
        return 2

    kind = kind_from_url(args.source) if args.kind == "auto" else args.kind
    report = build_report(args.source, kind, args.intent)

    out_path = resolve_evidence_path(args)
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.summary_only:
        print(f"source: {report['source']}")
        print(f"final_url: {report['final_url']}")
        print(f"kind: {report['kind']}")
        print(f"intent: {report['intent']}")
        print(f"license: {report['license']} ({report['license_risk']})")
        print(f"classification: {report['source_classification']}")
        print(f"needs_user_clarification: {report['needs_user_clarification']}")
        if report.get("license_pages_probed"):
            print("license_pages_probed:")
            for entry in report["license_pages_probed"]:
                print(f"  - {entry['url']} license={entry['license']} restricted_hits={len(entry['restricted_hits'])}")
        if report['high_risk_flags']:
            print("high_risk_flags:")
            for item in report['high_risk_flags']:
                print(f"  - {item}")
        if report['recommendations']:
            print("recommendations:")
            for item in report['recommendations']:
                print(f"  - {item}")
        if out_path:
            print(f"wrote: {out_path}")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        if out_path:
            print(f"wrote: {out_path}", file=sys.stderr)

    if report["needs_user_clarification"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
