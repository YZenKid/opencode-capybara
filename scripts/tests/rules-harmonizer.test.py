"""Tests for rules-source-scanner.py and rules-harmonizer.py.

Run: python3 scripts/tests/rules-harmonizer.test.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNER = REPO_ROOT / "scripts" / "rules-source-scanner.py"
HARMONIZER = REPO_ROOT / "scripts" / "rules-harmonizer.py"


def _run(script: Path, *args: str, cwd: Path | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["python3", str(script), *args],
        capture_output=True, text=True, cwd=cwd or REPO_ROOT
    )
    return proc.returncode, proc.stdout, proc.stderr


def _make_project(layout: dict[str, str]) -> Path:
    """Create a temp project with the given {relative_path: content} files."""
    d = Path(tempfile.mkdtemp(prefix="harm-test-", dir="/var/home/ujang"))
    for rel, content in layout.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return d


class TestScanner(unittest.TestCase):
    def test_no_rules_at_all(self):
        d = _make_project({})
        try:
            rc, out, _ = _run(SCANNER, str(d), "--summary-only")
            self.assertEqual(rc, 0)
            self.assertIn("OpenCode native present:  0", out)
            self.assertIn("External rules present:   0", out)
            self.assertIn("No agent-rules files present", out)
        finally:
            import shutil; shutil.rmtree(d)

    def test_only_claude_md(self):
        d = _make_project({"CLAUDE.md": "# Project\n- rule 1\n- rule 2\n"})
        try:
            rc, out, _ = _run(SCANNER, str(d), "--summary-only")
            self.assertEqual(rc, 0)
            self.assertIn("[claude-code] CLAUDE.md", out)
            self.assertIn("External rules present:   1", out)
            self.assertIn("External rules present", out)
        finally:
            import shutil; shutil.rmtree(d)

    def test_both_opencode_and_external(self):
        # Codex also maps AGENTS.md at root, so when AGENTS.md exists
        # alongside CLAUDE.md and .cursorrules, the scanner reports it
        # under BOTH the opencode-native and the codex-external buckets.
        # That is expected: the harmonizer treats AGENTS.md as the canonical
        # OpenCode file and writes the audit-trail noting the overlap.
        d = _make_project({
            "AGENTS.md": "# OpenCode native",
            "CLAUDE.md": "# Claude",
            ".cursorrules": "rule",
        })
        try:
            rc, out, _ = _run(SCANNER, str(d), "--summary-only")
            self.assertEqual(rc, 0)
            self.assertIn("OpenCode native present:  1", out)
            self.assertIn("[claude-code] CLAUDE.md", out)
            self.assertIn("[cursor] .cursorrules", out)
            self.assertIn("--harmonize", out)  # recommendation for both present
        finally:
            import shutil; shutil.rmtree(d)

    def test_json_output(self):
        d = _make_project({"CLAUDE.md": "x"})
        try:
            rc, out, _ = _run(SCANNER, str(d), "--json")
            data = json.loads(out)
            self.assertIn("hits", data)
            self.assertIn("external_rules_present", data)
            self.assertIn("CLAUDE.md", data["external_rules_present"])
        finally:
            import shutil; shutil.rmtree(d)


class TestHarmonizer(unittest.TestCase):
    def test_no_external_no_rules(self):
        d = _make_project({})
        try:
            rc, out, _ = _run(HARMONIZER, str(d))
            self.assertEqual(rc, 0)
            self.assertIn("no external rules found", out)
            audit = d / ".opencode" / "docs" / "SOURCE_RULES.md"
            self.assertTrue(audit.exists())
            self.assertIn("No external rules files were detected", audit.read_text())
        finally:
            import shutil; shutil.rmtree(d)

    def test_claude_md_creates_audit(self):
        d = _make_project({
            "CLAUDE.md": (
                "# Project\n\n"
                "## Routing\n"
                "- Use @orchestrator first\n"
                "## Style\n"
                "- Use tabs (4-wide)\n"
                "## Security\n"
                "- Never commit .env\n"
            ),
        })
        try:
            rc, out, _ = _run(HARMONIZER, str(d))
            self.assertEqual(rc, 0)
            self.assertIn("3 rule(s)", out)
            audit = d / ".opencode" / "docs" / "SOURCE_RULES.md"
            text = audit.read_text()
            self.assertIn("### routing", text)
            self.assertIn("### style_format", text)
            self.assertIn("### security_secrets", text)
        finally:
            import shutil; shutil.rmtree(d)

    def test_apply_appends_to_agents_md(self):
        d = _make_project({
            "AGENTS.md": "# Existing\n\n## Risk Triggers\n- x\n",
            "CLAUDE.md": "- use tabs\n",
        })
        try:
            rc, out, _ = _run(HARMONIZER, str(d), "--apply")
            self.assertEqual(rc, 0)
            self.assertIn("appended Source Rules section", out)
            ag = (d / "AGENTS.md").read_text()
            self.assertIn("## Source Rules", ag)
            self.assertIn("`claude-code`", ag)
        finally:
            import shutil; shutil.rmtree(d)

    def test_apply_skipped_when_no_agents_md(self):
        d = _make_project({"CLAUDE.md": "- use tabs\n"})
        try:
            rc, out, _ = _run(HARMONIZER, str(d), "--apply")
            self.assertEqual(rc, 0)
            # No AGENTS.md to append to; the script should silently skip
            self.assertFalse((d / "AGENTS.md").exists())
        finally:
            import shutil; shutil.rmtree(d)

    def test_forward_creates_mirrors(self):
        d = _make_project({"CLAUDE.md": "- use tabs\n- run tests\n"})
        try:
            rc, out, _ = _run(HARMONIZER, str(d), "--forward-to", "codex,cursor")
            self.assertEqual(rc, 0)
            self.assertTrue((d / ".codex" / "AGENTS.md").exists())
            self.assertTrue((d / ".cursor" / "rules" / "OPENCODE_HARMONIZED.md").exists())
            codex = (d / ".codex" / "AGENTS.md").read_text()
            self.assertIn("OpenCode-derived", codex)
            self.assertIn("style_format", codex)
        finally:
            import shutil; shutil.rmtree(d)

    def test_idempotent_forward(self):
        d = _make_project({"CLAUDE.md": "- use tabs\n- run tests\n"})
        try:
            _run(HARMONIZER, str(d), "--forward-to", "claude")
            _run(HARMONIZER, str(d), "--forward-to", "claude")
            _run(HARMONIZER, str(d), "--forward-to", "claude")
            # Claude.md should not have grown: forward skips "already mirrored"
            claude_text = (d / "CLAUDE.md").read_text()
            self.assertEqual(claude_text.count("OpenCode-derived"), 1)
            # Audit file should have consistent rule count
            audit = d / ".opencode" / "docs" / "SOURCE_RULES.md"
            text = audit.read_text()
            self.assertIn("Total rules imported: 2", text)
        finally:
            import shutil; shutil.rmtree(d)

    def test_dry_run_does_not_write(self):
        d = _make_project({"CLAUDE.md": "- use tabs\n"})
        try:
            rc, out, _ = _run(HARMONIZER, str(d), "--dry-run", "--apply")
            self.assertEqual(rc, 0)
            self.assertIn("DRY RUN", out)
            # No file should be written
            self.assertFalse((d / ".opencode" / "docs" / "SOURCE_RULES.md").exists())
        finally:
            import shutil; shutil.rmtree(d)

    def test_categorization_correct(self):
        d = _make_project({
            "CLAUDE.md": (
                "- use tabs (style)\n"
                "- run npm test (build/test)\n"
                "- never commit .env (security)\n"
                "- commit to main (git workflow)\n"
                "- use @orchestrator (routing)\n"
                "- npm install axios (dependency)\n"
                "- deploy to vercel (deployment)\n"
                "- update README (docs)\n"
                "- select from postgres (data)\n"
                "- shadcn button (ui)\n"
            ),
        })
        try:
            rc, _, _ = _run(HARMONIZER, str(d))
            self.assertEqual(rc, 0)
            text = (d / ".opencode" / "docs" / "SOURCE_RULES.md").read_text()
            for cat in ("routing", "build_test", "style_format", "security_secrets",
                       "git_workflow", "dependency", "deployment", "docs", "data_db",
                       "ui_design"):
                self.assertIn(f"### {cat}", text, f"missing category {cat}")
        finally:
            import shutil; shutil.rmtree(d)


class TestStackSuggester(unittest.TestCase):
    """Smoke tests for stack-resource-suggester.py on synthetic projects."""

    def test_laravel_high_confidence(self):
        d = _make_project({
            "composer.json": '{"require":{"laravel/framework":"^11.0"}}',
            "artisan": "",
            ".env": "APP_KEY=base64:test\n",
        })
        (d / "app").mkdir()
        (d / "routes").mkdir()
        try:
            proc = subprocess.run(
                ["python3", str(REPO_ROOT / "scripts" / "stack-resource-suggester.py"),
                 str(d), "--json"],
                capture_output=True, text=True
            )
            data = json.loads(proc.stdout)
            laravel = next((m for m in data["matches"] if m["stack_id"] == "laravel"), None)
            self.assertIsNotNone(laravel, "Laravel should be detected")
            self.assertEqual(laravel["confidence"], "high")
        finally:
            import shutil; shutil.rmtree(d)

    def test_empty_project_no_match(self):
        d = _make_project({})
        try:
            proc = subprocess.run(
                ["python3", str(REPO_ROOT / "scripts" / "stack-resource-suggester.py"),
                 str(d), "--json"],
                capture_output=True, text=True
            )
            data = json.loads(proc.stdout)
            self.assertEqual(data["matches"], [])
        finally:
            import shutil; shutil.rmtree(d)

    def test_list_stacks(self):
        proc = subprocess.run(
            ["python3", str(REPO_ROOT / "scripts" / "stack-resource-suggester.py"),
             "--list-stacks"],
            capture_output=True, text=True
        )
        self.assertIn("laravel", proc.stdout)
        self.assertIn("nextjs", proc.stdout)
        self.assertIn("postgres", proc.stdout)

    def test_show_laravel(self):
        proc = subprocess.run(
            ["python3", str(REPO_ROOT / "scripts" / "stack-resource-suggester.py"),
             "--show", "laravel"],
            capture_output=True, text=True
        )
        data = json.loads(proc.stdout)
        self.assertIn("skills", data)
        self.assertGreater(len(data["skills"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
