#!/usr/bin/env python3
import re
import sys
from pathlib import Path

MIN_TOTAL_LINES = 5000
MIN_GOAL_WORDS = 200
MIN_REQUIREMENTS_WORDS = 500
MIN_REQUIREMENTS_COUNT = 10
MIN_ACCEPTANCE_WORDS = 300
MIN_ACCEPTANCE_COUNT = 8
MIN_UI_PAGES = 3
MIN_UI_PAGE_WORDS = 1000
MIN_COMPONENTS = 20
MIN_IMPLEMENTATION_STEPS = 50
MIN_VALIDATION_COMMANDS = 10
REQUIRED_STATES = ["empty", "loading", "error", "success"]

GROUNDING_SECTION_HEADERS = {
    "source_truth": ["## Execution Source of Truth", "# Execution Source of Truth"],
    "existing_patterns": ["## Existing Patterns/Reuse", "## Existing Patterns", "# Existing Patterns/Reuse", "# Existing Patterns"],
    "source_anatomy": ["## Source Anatomy", "# Source Anatomy"],
    "reference_map": ["## Reference Map", "# Reference Map"],
    "assumptions": ["## Decisions/Assumptions", "## Assumptions", "# Decisions/Assumptions"],
}

SECTION_HEADERS = {
    "goal": ["## Goal", "# Goal"],
    "non_goals": ["## Non-goals", "## Non Goals", "# Non-goals"],
    "requirements": ["## Requirements", "# Requirements"],
    "acceptance": ["## Acceptance Criteria", "# Acceptance Criteria"],
    "components": ["## Component Inventory", "## Components", "# Component Inventory"],
    "implementation": ["## Implementation Steps", "# Implementation Steps"],
    "validation": ["## Validation Commands", "# Validation Commands"],
}

# Anti-generic patterns that indicate mechanical failures
ANTI_GENERIC_PATTERNS = [
    r"centered gradient hero",
    r"generic.*modern clean",
    r"fake.*dashboard.*metric",
    r"arbitrary.*KPI",
    r"emoji.*icon",
    r"numeric-only.*icon",
    r"placeholder.*imag",
    r"blank.*image.*frame",
    r"repeated.*card.*grid",
    r"card.*spam",
    r"abstract.*blob",
    r"floating.*UI.*card",
    r"CSS.*glass.*panel",
    r"vague.*neon.*blob",
    r"default.*purple.*blue.*glow",
    r"debug.*internal.*copy",
    r"server.*label",
    r"port.*number.*UI",
    r"lorem.*text",
    r"placeholder.*copy",
]

# Design depth keywords that must be present
DESIGN_DEPTH_KEYWORDS = [
    "design read",
    "design_variance",
    "motion_intensity",
    "visual_density",
    "page-by-page",
    "section-level",
    "component inventory",
    "asset/image decision",
    "motion system",
    "reduced-motion",
    "accessibility gate",
    "validation evidence",
]

# Reference pack keywords
REFERENCE_PACK_KEYWORDS = [
    "reference",
    "screenshot",
    "url",
    "visual direction",
    "aesthetic family",
    "layout pattern",
    "component pattern",
    "asset style",
    "image style",
    "motion style",
    "first-principles",
]

GROUNDING_REQUIRED_MARKERS = [
    "confirmed",
    "unverified",
    "assumption",
    "repo-backed",
    "docs-backed",
    "reference-backed",
    "runtime-backed",
]

SPECULATIVE_RISK_PATTERNS = [
    r"\balready exists\b",
    r"\balready running\b",
    r"\balready configured\b",
    r"\bcurrent repo\b",
    r"\bcurrently\b",
    r"\balready updated\b",
]


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def section_body(text: str, headers: list[str]) -> str:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() in headers:
            start = i + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("#"):
            end = j
            break
    return "\n".join(lines[start:end]).strip()


def count_bullets_or_ordered(text: str) -> int:
    count = 0
    for line in text.splitlines():
        s = line.strip()
        if re.match(r"^[-*]\s+", s) or re.match(r"^\d+[.)]\s+", s):
            count += 1
    return count


def extract_ui_pages(text: str) -> list[str]:
    blocks = []
    current = []
    in_page = False
    for line in text.splitlines():
        if re.match(r"^###\s+Page:", line.strip()):
            if current:
                blocks.append("\n".join(current).strip())
            current = [line]
            in_page = True
        elif in_page:
            if line.startswith("## ") and not line.startswith("### "):
                blocks.append("\n".join(current).strip())
                current = []
                in_page = False
            else:
                current.append(line)
    if current:
        blocks.append("\n".join(current).strip())
    return blocks


def count_components(text: str) -> int:
    count = 0
    for line in text.splitlines():
        if re.match(r"^\d+[.)]\s+\*\*.*\*\*", line.strip()) or re.match(r"^\d+[.)]\s+[A-Za-z]", line.strip()):
            count += 1
    return count


def state_coverage_present(text: str) -> bool:
    lower = text.lower()
    return all(state in lower for state in REQUIRED_STATES)


def check_anti_generic_patterns(text: str) -> list[str]:
    """Check for anti-generic patterns. Returns list of matched patterns."""
    lower = text.lower()
    matches = []
    for pattern in ANTI_GENERIC_PATTERNS:
        if re.search(pattern, lower):
            matches.append(pattern)
    return matches


def check_design_depth_keywords(text: str) -> list[str]:
    """Check for design depth keywords. Returns list of missing keywords."""
    lower = text.lower()
    missing = []
    for keyword in DESIGN_DEPTH_KEYWORDS:
        if keyword not in lower:
            missing.append(keyword)
    return missing


def check_reference_pack(text: str) -> tuple[bool, list[str]]:
    """Check for reference pack presence. Returns (has_reference_pack, missing_keywords)."""
    lower = text.lower()
    has_reference = False
    missing = []

    # Check if any reference keyword is present
    for keyword in REFERENCE_PACK_KEYWORDS:
        if keyword in lower:
            has_reference = True
            break

    # Check which reference keywords are missing
    for keyword in REFERENCE_PACK_KEYWORDS:
        if keyword not in lower:
            missing.append(keyword)

    return has_reference, missing


def check_grounding_contract(text: str) -> tuple[bool, list[str]]:
    """Validate plan has explicit grounding sections and confirmed-vs-assumed markers."""
    failures = []

    source_truth = section_body(text, GROUNDING_SECTION_HEADERS["source_truth"])
    existing_patterns = section_body(text, GROUNDING_SECTION_HEADERS["existing_patterns"])
    source_anatomy = section_body(text, GROUNDING_SECTION_HEADERS["source_anatomy"])
    reference_map = section_body(text, GROUNDING_SECTION_HEADERS["reference_map"])
    assumptions = section_body(text, GROUNDING_SECTION_HEADERS["assumptions"])
    lower = text.lower()

    if not source_truth:
        failures.append("missing_execution_source_of_truth")
    if not existing_patterns:
        failures.append("missing_existing_patterns_reuse")
    if not source_anatomy:
        failures.append("missing_source_anatomy")
    if not reference_map:
        failures.append("missing_reference_map")
    if not assumptions:
        failures.append("missing_decisions_assumptions")

    if source_anatomy and word_count(source_anatomy) < 80:
        failures.append("source_anatomy_too_shallow")
    if reference_map and count_bullets_or_ordered(reference_map) < 3:
        failures.append("reference_map_too_shallow")

    if not any(marker in lower for marker in GROUNDING_REQUIRED_MARKERS):
        failures.append("missing_confirmed_vs_assumed_markers")

    if "unverified" not in lower and "assumption" not in lower:
        failures.append("missing_unverified_or_assumption_labels")

    risky = []
    for pattern in SPECULATIVE_RISK_PATTERNS:
        if re.search(pattern, lower):
            risky.append(pattern)
    if risky and ("confirmed" not in lower and "unverified" not in lower):
        failures.append("speculative_operational_claims_without_labels")

    return len(failures) == 0, failures


def main() -> int:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: validate-plan-depth.py <plan.md> [--score]")
        return 2

    path = Path(sys.argv[1])
    score_mode = "--score" in sys.argv
    
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    total_lines = len(text.splitlines())

    goal_text = section_body(text, SECTION_HEADERS["goal"]) + "\n" + section_body(text, SECTION_HEADERS["non_goals"])
    requirements_text = section_body(text, SECTION_HEADERS["requirements"])
    acceptance_text = section_body(text, SECTION_HEADERS["acceptance"])
    components_text = section_body(text, SECTION_HEADERS["components"])
    implementation_text = section_body(text, SECTION_HEADERS["implementation"])
    validation_text = section_body(text, SECTION_HEADERS["validation"])
    ui_pages = extract_ui_pages(text)

    checks = []
    checks.append(("total_lines", total_lines, MIN_TOTAL_LINES, total_lines >= MIN_TOTAL_LINES))
    checks.append(("goal_words", word_count(goal_text), MIN_GOAL_WORDS, word_count(goal_text) >= MIN_GOAL_WORDS))
    checks.append(("requirements_words", word_count(requirements_text), MIN_REQUIREMENTS_WORDS, word_count(requirements_text) >= MIN_REQUIREMENTS_WORDS))
    checks.append(("requirements_count", count_bullets_or_ordered(requirements_text), MIN_REQUIREMENTS_COUNT, count_bullets_or_ordered(requirements_text) >= MIN_REQUIREMENTS_COUNT))
    checks.append(("acceptance_words", word_count(acceptance_text), MIN_ACCEPTANCE_WORDS, word_count(acceptance_text) >= MIN_ACCEPTANCE_WORDS))
    checks.append(("acceptance_count", count_bullets_or_ordered(acceptance_text), MIN_ACCEPTANCE_COUNT, count_bullets_or_ordered(acceptance_text) >= MIN_ACCEPTANCE_COUNT))
    checks.append(("ui_pages", len(ui_pages), MIN_UI_PAGES, len(ui_pages) >= MIN_UI_PAGES))
    min_ui_words_actual = min((word_count(page) for page in ui_pages), default=0)
    checks.append(("ui_page_min_words", min_ui_words_actual, MIN_UI_PAGE_WORDS, min_ui_words_actual >= MIN_UI_PAGE_WORDS))
    checks.append(("components_count", count_components(components_text), MIN_COMPONENTS, count_components(components_text) >= MIN_COMPONENTS))
    checks.append(("implementation_steps", count_bullets_or_ordered(implementation_text), MIN_IMPLEMENTATION_STEPS, count_bullets_or_ordered(implementation_text) >= MIN_IMPLEMENTATION_STEPS))
    checks.append(("validation_commands", count_bullets_or_ordered(validation_text), MIN_VALIDATION_COMMANDS, count_bullets_or_ordered(validation_text) >= MIN_VALIDATION_COMMANDS))
    checks.append(("state_coverage", int(state_coverage_present(components_text)), 1, state_coverage_present(components_text)))
    
    # Phase 2 checks
    anti_generic_matches = check_anti_generic_patterns(text)
    checks.append(("anti_generic_patterns", len(anti_generic_matches), 0, len(anti_generic_matches) == 0))
    
    design_depth_missing = check_design_depth_keywords(text)
    checks.append(("design_depth_keywords", len(DESIGN_DEPTH_KEYWORDS) - len(design_depth_missing), len(DESIGN_DEPTH_KEYWORDS), len(design_depth_missing) == 0))
    
    has_reference_pack, reference_missing = check_reference_pack(text)
    checks.append(("reference_pack", int(has_reference_pack), 1, has_reference_pack))

    # Grounding contract checks
    grounding_ok, grounding_failures = check_grounding_contract(text)
    checks.append(("grounding_contract", int(grounding_ok), 1, grounding_ok))

    failed = [c for c in checks if not c[3]]

    print("PLAN DEPTH REPORT")
    print(f"file: {path}")
    for name, actual, minimum, ok in checks:
        status = "PASS" if ok else "FAIL"
        print(f"- {name}: {actual} / {minimum} => {status}")

    if anti_generic_matches:
        print("\nANTI-GENERIC PATTERNS DETECTED:")
        for pattern in anti_generic_matches:
            print(f"  - {pattern}")

    if design_depth_missing:
        print("\nDESIGN DEPTH KEYWORDS MISSING:")
        for keyword in design_depth_missing:
            print(f"  - {keyword}")

    if not has_reference_pack:
        print("\nREFERENCE PACK MISSING:")
        print("  - No reference screenshots/URLs or first-principles rationale found")

    if grounding_failures:
        print("\nGROUNDING CONTRACT FAILURES:")
        for failure in grounding_failures:
            print(f"  - {failure}")
        print("\nPLAN LACKS CONFIRMED-VS-ASSUMED AUDIT.")
        print("Required sections:")
        print("  - ## Source Anatomy (per subsystem/layer)")
        print("  - ## Reference Map (per feature)")
        print("  - Explicit 'confirmed' / 'unverified' / 'assumption' labels")
        print("Do not speculate about repo state. Verify or label as assumption.")

    if score_mode:
        # Calculate score
        total_checks = len(checks)
        passed_checks = total_checks - len(failed)
        score = (passed_checks / total_checks) * 100
        
        print(f"\nSCORE: {score:.1f}% ({passed_checks}/{total_checks} checks passed)")
        
        # Quality tiers
        if score == 100:
            print("TIER: EXECUTION_READY")
        elif score >= 80:
            print("TIER: NEARLY_READY")
        elif score >= 60:
            print("TIER: NEEDS_WORK")
        elif score >= 40:
            print("TIER: SHALLOW")
        else:
            print("TIER: INADEQUATE")

    if failed:
        print("\nRESULT: NEEDS_DEPTH")
        return 1

    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
