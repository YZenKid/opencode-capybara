"""Tests for 21st adoption provenance checks in scripts/visual-audit-check.py.

Run:
    python3 scripts/tests/visual-audit-check.test.py
"""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "visual-audit-check.py"
SPEC = importlib.util.spec_from_file_location("visual_audit_check", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

BASE_CONTRACT = """# Visual Quality Contract

### Must Show
- real thing

### Must NOT Show
- placeholder

### Reject If
- missing real thing
"""

INCOMPLETE_21ST = BASE_CONTRACT + """
## External Component Provenance
21st_adoption: true
component: accordion-42
source: https://21st.dev/components/accordion-42
"""

COMPLETE_21ST = BASE_CONTRACT + """
## External Component Provenance
21st_adoption: true
component: accordion-42
source: https://21st.dev/components/accordion-42
license: MIT
dependencies: none
token_mapping: mapped
validation: https://example.test/evidence/accordion-42.md
"""


class VisualAuditCheckTests(unittest.TestCase):
    def _findings(self, content: str) -> list[dict]:
        with tempfile.TemporaryDirectory() as temp_dir:
            contract = Path(temp_dir) / "visual-quality-contract.md"
            contract.write_text(content, encoding="utf-8")
            return MODULE.audit_contract_v2(contract)

    def test_no_21st_adoption_preserves_existing_behavior(self) -> None:
        self.assertFalse(any(finding["severity"] == "high" for finding in self._findings(BASE_CONTRACT)))

    def test_declared_21st_adoption_requires_complete_metadata(self) -> None:
        codes = {finding["issue"] for finding in self._findings(INCOMPLETE_21ST)}
        self.assertIn("external_component_provenance_incomplete", codes)

    def test_complete_21st_adoption_passes(self) -> None:
        self.assertFalse(any(finding["severity"] == "high" for finding in self._findings(COMPLETE_21ST)))


if __name__ == "__main__":
    unittest.main()
