"""Focused DB handoff and routing regressions for agent-context-db-alignment."""
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "scripts" / "subagent-handoff-check.py"
SPEC = importlib.util.spec_from_file_location("handoff_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


BASE = {
    "task_id": "agent-context-db-alignment",
    "plan_id": "agent-context-db-alignment",
    "caller": "orchestrator",
    "callee": "explorer",
    "scope": "Read-only DB context discovery",
    "claim_level": "scoped",
    "claim_scope": "Contract only",
    "source_basis": [".opencode/plans/agent-context-db-alignment.md"],
    "must_preserve": ["No credentials", "No SQL writes"],
    "do_not_touch": [".env", "DB data"],
    "validation": ["focused tests"],
    "exit_criteria": ["Context preserved"],
    "evidence_required": [".opencode/evidence/agent-context-db-alignment/test-results.md"],
    "depends_on": ["A1"],
    "context_bundle": ["source-anatomy.md"],
    "db_target": {"status": "verified", "identifier": "verified-target"},
    "verified_runtime_facts": {
        "current_database": "verified-db",
        "schema": "public",
        "model_table_mapping": "Model -> table",
        "verification_source": "read-only fixture",
        "verification_time": "2026-07-31T00:00:00Z",
    },
    "db_availability": "verified",
    "open_assumptions": ["Engine remains unknown"],
    "evidence_refs": ["db-before", "db-after"],
    "read_only_scope": ["SELECT-only discovery"],
}


class AgentContextDbAlignmentTests(unittest.TestCase):
    def check(self, payload: dict) -> list[str]:
        return validator.validate_one("fixture", payload, ROOT)

    def test_internal_chooser_rejected_direct_route_allowed(self) -> None:
        self.assertEqual([], validator.validate_policy_text("ROUTE_DIRECT; safe read-only discovery", user_facing=True))
        error = validator.validate_policy_text("Please choose investigate, plan, implement, or review.", user_facing=True)
        self.assertEqual(["user-facing internal workflow chooser is forbidden"], error)

    def test_db_context_survives_lane_sequence(self) -> None:
        keys = ("db_target", "verified_runtime_facts", "db_availability", "open_assumptions", "evidence_refs", "read_only_scope")
        payload = json.loads(json.dumps(BASE))
        for callee in ("explorer", "backend", "fixer", "quality-gate"):
            payload["callee"] = callee
            self.assertEqual([], self.check(payload))
            payload = {**payload, **{key: payload[key] for key in keys}}
        self.assertEqual(payload["db_target"]["identifier"], "verified-target")
        self.assertEqual(payload["verified_runtime_facts"]["schema"], "public")

    def test_discovery_write_commands_rejected(self) -> None:
        write_commands = ("INSERT", "UPDATE", "DELETE", "MERGE", "DROP", "ALTER", "TRUNCATE", "migration", "migrate", "reset", "seed")
        for command in write_commands:
            payload = {**BASE, "read_only_scope": [f"SELECT-only discovery; {command} users"]}
            errors = self.check(payload)
            self.assertTrue(any("write SQL or mutation command is forbidden" in error for error in errors), command)
        self.assertEqual([], self.check({**BASE, "validation": ["SELECT current_database and read-only schema mapping"]}))
        self.assertEqual([], self.check({**BASE, "must_preserve": ["no write SQL"]}))

    def test_db_done_claim_requires_evidence_or_unavailable_reason(self) -> None:
        payload = {**BASE, "claim_level": "done", "evidence_refs": []}
        errors = self.check(payload)
        self.assertTrue(any("representative DB evidence" in error for error in errors))
        payload = {**payload, "db_availability": "unavailable", "db_target": {"status": "unavailable"}, "db_unavailable_reason": "local DB unavailable"}
        self.assertEqual([], self.check(payload))

    def test_db_target_availability_mismatch_rejected(self) -> None:
        payload = {**BASE, "db_availability": "unavailable"}
        errors = self.check(payload)
        self.assertTrue(any("db_target.status must match db_availability" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
