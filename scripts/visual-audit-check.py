#!/usr/bin/env python3
"""Visual audit fallback that checks live/URL UI without requiring working browser stack.

Uses urllib + HTML parsing to detect placeholder content, generic blobs, missing CTAs, etc.
Optionally enhances with Playwright screenshots if available.

v2 additions (catalog-aware):
- --contract mode: validates a visual-quality-contract.md (v2) for catalog_citation block,
  must_use_tokens, must_avoid_token, deviation_audit, etc.
- --token-parity mode: scans project CSS/Tailwind/JS for token values declared in the contract
  and reports which are used/missing.
- Exits non-zero on mechanical failures so it can be wired into CI / quality-gate.

Usage:
  python3 ~/.config/opencode/scripts/visual-audit-check.py --url https://example.com --output .opencode/evidence/visual-audit.md
  python3 ~/.config/opencode/scripts/visual-audit-check.py --project-root . --contract .opencode/evidence/<task-id>/visual-quality-contract.md
  python3 ~/.config/opencode/scripts/visual-audit-check.py --project-root . --contract <path> --token-parity
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def run_url_extractor(url: str, out_dir: Path) -> Path | None:
    out = out_dir / 'url-audit-structure.md'
    try:
        subprocess.run(
            ['python3', '~/.config/opencode/scripts/url-structure-extractor.py', '--url', url, '--output', str(out)],
            capture_output=True, text=True, timeout=20, check=True,
        )
        return out
    except Exception:
        return None


def audit_url(url: str, root: Path) -> list[dict]:
    """Run lightweight audit and return findings."""
    findings = []
    try:
        req = __import__('urllib.request').request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with __import__('urllib.request').request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore').lower()
    except Exception as e:
        findings.append({'severity': 'error', 'issue': 'fetch_failed', 'detail': str(e)})
        return findings

    if 'lorem ipsum' in html or 'placeholder' in html:
        findings.append({'severity': 'high', 'issue': 'placeholder_copy', 'detail': 'placeholder text found'})
    if '<nav' not in html:
        findings.append({'severity': 'medium', 'issue': 'missing_nav', 'detail': 'no <nav> element'})
    if '<footer' not in html:
        findings.append({'severity': 'info', 'issue': 'missing_footer', 'detail': 'no <footer> element'})
    if '<main' not in html and '<header' not in html:
        findings.append({'severity': 'medium', 'issue': 'no_main_or_header', 'detail': 'no <main> or <header> landmark'})
    if html.count('<button') + html.count('type="submit"') == 0:
        findings.append({'severity': 'medium', 'issue': 'no_cta_button', 'detail': 'no visible button/CTA'})
    if 'class="bg-gradient' in html or 'class="bg-[url(' in html:
        findings.append({'severity': 'info', 'issue': 'generic_gradient_detected', 'detail': 'gradient background present, verify it is intentional'})
    return findings


def audit_contract_v2(contract_path: Path) -> list[dict]:
    """Validate a v2 visual-quality-contract.md for catalog_citation, must_use_tokens, etc.

    Returns findings as list of dicts with keys: severity (high|medium|low), issue, detail.
    Severity 'high' is a mechanical failure (NEEDS_FIX).
    """
    findings: list[dict] = []
    if not contract_path.exists():
        findings.append({"severity": "high", "issue": "contract_missing", "detail": f"{contract_path} not found"})
        return findings
    text = contract_path.read_text(encoding="utf-8")

    # Detect schema version
    is_v2 = "Schema version**: v2" in text or "schema: v2" in text
    is_v1 = "Schema version**: v1" in text or "schema: v1" in text or "Visual Quality Contract" in text and "v2" not in text

    # Check catalog_citation block (v2 only)
    if is_v2:
        if "## 2. Catalog Citation" not in text and "## 2. Catalog Citation (v2" not in text:
            findings.append({"severity": "high", "issue": "v2_catalog_citation_missing", "detail": "v2 contract must have a '## 2. Catalog Citation' section"})
        else:
            # Validate the YAML block (or pseudo-YAML) has required keys
            for required_key in ("design_system:", "template_pattern:", "pair_rationale:", "deviation_audit:", "must_use_tokens:", "must_avoid_token:"):
                if required_key not in text:
                    findings.append({"severity": "high", "issue": "v2_citation_key_missing", "detail": f"required key '{required_key}' not found in catalog_citation block"})
            # Validate the design system URL points to open-design.ai
            ds_url_match = re.search(r"design_system:[\s\S]*?source:\s*\"?([^\"\n]+)\"?", text)
            if ds_url_match and "open-design.ai" not in ds_url_match.group(1):
                findings.append({"severity": "high", "issue": "v2_catalog_url_not_official", "detail": f"design_system.source must reference open-design.ai, got: {ds_url_match.group(1)}"})
            tp_url_match = re.search(r"template_pattern:[\s\S]*?source:\s*\"?([^\"\n]+)\"?", text)
            if tp_url_match and "open-design.ai" not in tp_url_match.group(1):
                findings.append({"severity": "high", "issue": "v2_template_url_not_official", "detail": f"template_pattern.source must reference open-design.ai, got: {tp_url_match.group(1)}"})
            # pair_rationale must be >= 2 sentences
            rationale_match = re.search(r"pair_rationale:\s*\|\s*\n((?:\s{4,}.+\n)+)", text)
            if rationale_match:
                sentences = [s for s in re.split(r"[.!?]+", rationale_match.group(1)) if s.strip()]
                if len(sentences) < 2:
                    findings.append({"severity": "medium", "issue": "v2_rationale_too_short", "detail": "pair_rationale should be >= 2 sentences"})
            # deviation_audit: must be a list (with '- ' entries) or explicit "no deviations" note
            audit_match = re.search(r"deviation_audit:\s*\n((?:\s{4,}.+\n)+)", text)
            if not audit_match or "[]" not in (audit_match.group(1) if audit_match else ""):
                if not audit_match or "  -" not in audit_match.group(1):
                    # Check for explicit no-deviations note
                    if "no deviations" not in text.lower():
                        findings.append({"severity": "medium", "issue": "v2_deviation_audit_empty", "detail": "deviation_audit should list entries or include an explicit 'no deviations' note"})
    elif is_v1:
        # v1 contracts are still valid for non-substantial UI; flag a soft note
        findings.append({"severity": "low", "issue": "v1_contract_for_non_substantial", "detail": "v1 contract in use; for substantial UI, upgrade to v2 with catalog_citation block"})
        # Heuristic: if the contract filename suggests substantial UI work, upgrade the finding to high
        if "substance" in contract_path.name.lower() or "substantial" in contract_path.name.lower() or "greenfield" in contract_path.name.lower():
            findings[-1] = {"severity": "high", "issue": "v1_contract_substantial_ui", "detail": "filename suggests substantial UI; v2 with catalog_citation block is required"}

    # Check structured fields (v1 + v2)
    if "### Must Show" not in text:
        findings.append({"severity": "high", "issue": "must_show_missing", "detail": "section '### Must Show' not found"})
    if "### Must NOT Show" not in text:
        findings.append({"severity": "high", "issue": "must_not_show_missing", "detail": "section '### Must NOT Show' not found"})
    if "### Reject If" not in text:
        findings.append({"severity": "high", "issue": "reject_if_missing", "detail": "section '### Reject If' not found"})

    return findings


def token_parity(contract_path: Path, project_root: Path) -> dict:
    """Scan project for declared must_use_tokens / must_avoid_token. Returns parity report.

    Whitelist: tokens listed in `deviation_audit` as already-changed are excluded
    from the "missing" count (they are intentionally not present in their original form).
    """
    if not contract_path.exists():
        return {"error": "contract_missing"}
    text = contract_path.read_text(encoding="utf-8")
    # Extract must_use_tokens
    must_use = re.findall(r"must_use_tokens:\s*\n((?:\s+-\s+.+\n)+)", text)
    must_use_list: list[str] = []
    if must_use:
        for line in must_use[0].splitlines():
            m = re.match(r"\s+-\s+(.+)", line)
            if m:
                must_use_list.append(m.group(1).strip().strip('"').strip("'"))
    must_avoid = re.findall(r"must_avoid_token:\s*\n((?:\s+-\s+.+\n)+)", text)
    must_avoid_list: list[str] = []
    if must_avoid:
        for line in must_avoid[0].splitlines():
            m = re.match(r"\s+-\s+(.+)", line)
            if m:
                must_avoid_list.append(m.group(1).strip().strip('"').strip("'"))

    # Extract deviation_audit "what" entries to whitelist from must_use
    audit_block = re.search(r"deviation_audit:\s*\n((?:\s{4,}.+\n)+)", text)
    deviation_whats: list[str] = []
    if audit_block:
        for line in audit_block.group(1).splitlines():
            m = re.match(r"\s+-\s+what:\s*(.+)", line)
            if m:
                deviation_whats.append(m.group(1).strip())

    # Tokens that are explicitly deviated are removed from the must_use expected list
    whitelisted: set[str] = set()
    for d in deviation_whats:
        # parse "token_name -> #newvalue" or "accent #5e6ad2 -> #ff5722"
        for token in must_use_list:
            if token.lower() in d.lower():
                whitelisted.add(token)
    effective_must_use = [t for t in must_use_list if t not in whitelisted]

    # Scan project for these tokens in CSS, Tailwind config, JSON tokens, and any .ts/.tsx/.js/.jsx
    text_extensions = {".css", ".scss", ".ts", ".tsx", ".js", ".jsx", ".json", ".vue", ".svelte"}
    used: set[str] = set()
    avoided_found: list[tuple[str, str]] = []
    for ext in text_extensions:
        for path in project_root.rglob(f"*{ext}"):
            # Skip node_modules, .next, dist, build, .opencode, generated
            skip = any(part in path.parts for part in ("node_modules", ".next", "dist", "build", ".opencode", "generated"))
            if skip:
                continue
            try:
                file_text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for token in effective_must_use:
                if token.startswith("#") and token.lower() in file_text.lower():
                    used.add(token)
                elif not token.startswith("#") and re.search(rf"\b{re.escape(token)}\b", file_text):
                    used.add(token)
            for token in must_avoid_list:
                if token.startswith("#") and token.lower() in file_text.lower():
                    avoided_found.append((token, str(path.relative_to(project_root))))

    # Parity is computed against effective (non-deviated) list
    if effective_must_use:
        must_use_pct = (len(used) / len(effective_must_use) * 100)
    else:
        must_use_pct = 100.0  # all declared must_use tokens were whitelisted by deviations

    return {
        "must_use_total": len(must_use_list),
        "must_use_effective": len(effective_must_use),
        "must_use_whitelisted_by_deviation": sorted(whitelisted),
        "must_use_found": sorted(used),
        "must_use_missing": sorted(set(effective_must_use) - used),
        "must_use_parity_pct": round(must_use_pct, 1),
        "must_avoid_violations": avoided_found,
    }


CONTENT_AUTHENTICITY_REQUIRED_ROWS = [
    "testimonial_real",
    "pricing_real",
    "faq_grounded",
    "stats_meaningful",
    "hero_shows_real_domain",
    "copy_no_brochure_slogans",
    "cta_routes_resolve",
    "contact_real",
]

CONTENT_HARD_FAIL_PATTERNS = [
    (re.compile(r'\bMaya\s+R\.\b'), "fabricated_testimonial_Maya_R"),
    (re.compile(r'\bAndre\s+F\.\b'), "fabricated_testimonial_Andre_F"),
    (re.compile(r'\bNisa\s+A\.\b'), "fabricated_testimonial_Nisa_A"),
    (re.compile(r'(?i)\bpasti\s+bisa\b'), "brochure_slogan_pasti_bisa"),
    (re.compile(r'(?i)\bsolusi\s+terbaik\b'), "brochure_slogan_solusi_terbaik"),
    (re.compile(r'(?i)\bfoto\s+menyusul\b'), "foto_menyusul_placeholder"),
    (re.compile(r'(?i)\bkontak\s+akan\s+diperbarui\b'), "kontak_akan_diperbarui_placeholder"),
    (re.compile(r'(?i)your trusted partner'), "brochure_slogan_your_trusted_partner"),
    (re.compile(r'href\s*=\s*"#"\s*data-cta'), "cta_link_to_hash"),
    (re.compile(r'\bcoming soon\b', re.IGNORECASE), "coming_soon_label"),
]


def _detect_section(text: str, heading: str) -> str:
    """Extract content under a markdown heading (## or ###) until the next same-or-higher heading."""
    pat = re.compile(rf'(?im)^#{{2,3}}\s+{re.escape(heading)}\b.*?(?=^#{{2,3}}\s+|\Z)', re.DOTALL)
    m = pat.search(text)
    return m.group(0) if m else ''


def content_authenticity(contract_path: Path, root: Path) -> dict:
    """Inspect a visual-quality-contract.md for content authenticity blocks + hard-fail patterns.

    Required blocks (substantive UI):
    - `## Content Provenance` (or `content_provenance`) — table per section with provenance column.
    - `## Content Authenticity Checklist` (or `content_authenticity_checklist`) — 8 pass/fail rows.

    Optional but recommended when `templates/<dir>/` exists:
    - `.opencode/evidence/<task-id>/template-extraction-trace.md`
    """
    result: dict = {
        "has_content_provenance": False,
        "has_content_authenticity_checklist": False,
        "checklist_failing": [],
        "hard_fail_patterns": [],
        "templates_dir_missing_trace": False,
    }
    if not contract_path.exists():
        result["hard_fail_patterns"].append("contract_file_not_found")
        return result
    text = contract_path.read_text(encoding="utf-8", errors="ignore")

    prov_block = _detect_section(text, "Content Provenance") or _detect_section(text, "content_provenance")
    if prov_block and re.search(r'\|\s*Provenance\s*\|', prov_block, re.IGNORECASE):
        result["has_content_provenance"] = True

    check_block = _detect_section(text, "Content Authenticity Checklist") or _detect_section(text, "content_authenticity_checklist")
    if check_block:
        result["has_content_authenticity_checklist"] = True
        rows = re.findall(r'\|\s*([a-z_]+)\s*\|\s*(pass|fail|yes|no|partial|n/?a)\s*\|', check_block, re.IGNORECASE)
        present = {k.lower(): v.lower() for k, v in rows}
        for required in CONTENT_AUTHENTICITY_REQUIRED_ROWS:
            if required not in present:
                result["checklist_failing"].append(f"{required}:missing")
            elif present[required] in ("fail", "no"):
                result["checklist_failing"].append(f"{required}:{present[required]}")

    for rx, name in CONTENT_HARD_FAIL_PATTERNS:
        if rx.search(text):
            result["hard_fail_patterns"].append(name)

    # Template extraction trace check (only when project has templates/<dir>/)
    try:
        templates_root = root / "templates"
        if templates_root.exists() and any(templates_root.iterdir()):
            # find task id from contract path: .opencode/evidence/<task-id>/visual-quality-contract.md
            parts = contract_path.parts
            trace_path = None
            for i, p in enumerate(parts):
                if p == "evidence" and i + 1 < len(parts):
                    task_id = parts[i + 1]
                    candidate = root / ".opencode" / "evidence" / task_id / "template-extraction-trace.md"
                    if candidate.exists():
                        trace_path = candidate
                        break
            if not trace_path:
                # also check root/.opencode/evidence/<task-id>/ where task id is parent dir of contract_path
                for parent in contract_path.parents:
                    if parent.name == "evidence" and parent.parent.name == ".opencode":
                        candidate = parent / "template-extraction-trace.md"
                        if candidate.exists() and candidate.stat().st_size > 0:
                            trace_path = candidate
                            break
            if not trace_path:
                result["templates_dir_missing_trace"] = True
    except Exception:
        # Be conservative: don't fail the gate on filesystem ambiguity
        pass

    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--url', help='URL to audit (legacy mode)')
    ap.add_argument('--contract', help='Path to visual-quality-contract.md (v2 mode)')
    ap.add_argument('--token-parity', action='store_true', help='In contract mode, also check token parity')
    ap.add_argument('--content-authenticity', action='store_true', help='In contract mode, check content_provenance + content_authenticity_checklist blocks')
    ap.add_argument('--output', default='.opencode/evidence/visual-audit.md')
    args = ap.parse_args()
    root = Path(args.project_root).resolve()

    # v2 contract mode
    if args.contract:
        contract_path = (root / args.contract) if not Path(args.contract).is_absolute() else Path(args.contract)
        findings = audit_contract_v2(contract_path)
        parity = None
        if args.token_parity:
            parity = token_parity(contract_path, root)
            # Mechanical enforcement (v2): parity < 80% on effective must_use -> high severity
            if parity.get("must_use_parity_pct", 100) < 80:
                findings.append({
                    "severity": "high",
                    "issue": "v2_token_parity_low",
                    "detail": f"token parity {parity['must_use_parity_pct']}% is below 80% threshold; missing: {parity.get('must_use_missing', [])}",
                })
            # must_avoid violations -> high severity
            if parity.get("must_avoid_violations"):
                findings.append({
                    "severity": "high",
                    "issue": "v2_must_avoid_violation",
                    "detail": f"must_avoid_token violations: {parity['must_avoid_violations']}",
                })

        if args.content_authenticity:
            ca = content_authenticity(contract_path, root)
            if not ca.get("has_content_provenance"):
                findings.append({
                    "severity": "high",
                    "issue": "content_provenance_missing",
                    "detail": "visual-quality-contract.md must include a ## Content Provenance (or content_provenance) block per section",
                })
            if not ca.get("has_content_authenticity_checklist"):
                findings.append({
                    "severity": "high",
                    "issue": "content_authenticity_checklist_missing",
                    "detail": "visual-quality-contract.md must include a ## Content Authenticity Checklist (or content_authenticity_checklist) block with 8 rows",
                })
            elif ca.get("checklist_failing"):
                findings.append({
                    "severity": "high",
                    "issue": "content_authenticity_checklist_failed",
                    "detail": f"failing rows: {ca['checklist_failing']}",
                })
            if ca.get("hard_fail_patterns"):
                findings.append({
                    "severity": "high",
                    "issue": "content_hard_fail_pattern",
                    "detail": f"hard-fail patterns detected in contract: {ca['hard_fail_patterns']}",
                })
            if ca.get("templates_dir_missing_trace"):
                findings.append({
                    "severity": "high",
                    "issue": "template_extraction_trace_missing",
                    "detail": "project contains a templates/<dir>/ directory but template-extraction-trace.md is missing or empty in .opencode/evidence/<task-id>/",
                })

        out = root / args.output
        out.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"# Visual Audit Check (v2 — contract): {contract_path.name}", ""]
        if parity:
            lines += [
                "## Token Parity",
                f"- must_use tokens declared: {parity.get('must_use_total', 0)}",
                f"- must_use tokens effective (after deviation whitelist): {parity.get('must_use_effective', parity.get('must_use_total', 0))}",
                f"- must_use tokens whitelisted by deviation: {parity.get('must_use_whitelisted_by_deviation', [])}",
                f"- must_use tokens found: {parity.get('must_use_effective', 0) - len(parity.get('must_use_missing', []))}",
                f"- parity: {parity.get('must_use_parity_pct', 0)}% (threshold 80%)",
                f"- missing: {parity.get('must_use_missing', [])}",
                f"- must_avoid violations: {len(parity.get('must_avoid_violations', []))}",
                "",
            ]
        lines += ["## Findings", "| Severity | Issue | Detail |", "|---|---|---|"]
        for f in findings:
            lines.append(f"| `{f['severity']}` | `{f['issue']}` | {f['detail']} |")
        if not findings:
            lines.append("| `pass` | `none` | all mechanical checks passed |")
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(out)
        # Exit non-zero on any high-severity (mechanical failure)
        high_count = sum(1 for f in findings if f["severity"] == "high")
        if high_count > 0:
            print(f"FAIL: {high_count} mechanical failure(s); see {out}", file=sys.stderr)
            return 1
        return 0

    # Legacy URL mode
    if not args.url:
        ap.error("either --url (legacy) or --contract (v2) is required")

    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)

    findings = audit_url(args.url, root)
    structure_file = run_url_extractor(args.url, out.parent)

    lines = [f'# Visual Audit Check: {args.url}', '', f'- Structure extract: `{structure_file}`', f'- Findings: `{len(findings)}`', '']
    if findings:
        lines += ['## Findings', '| Severity | Issue | Detail |', '|---|---|---|']
        for f in findings:
            lines.append(f"| `{f['severity']}` | `{f['issue']}` | {f['detail']} |")
    else:
        lines.append('No obvious mechanical issues detected.')
    lines += ['', '## Note', '- This is a fallback audit. For full visual/parity verification, run `python3 ~/.config/opencode/scripts/dom-preview-verifier.py` when Playwright is available.']
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
