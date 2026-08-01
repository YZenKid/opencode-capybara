"""Deterministic registry for active agent technical IDs and Javanese codenames."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {
    "orchestrator": "Kresna",
    "artifact-planner": "Semar",
    "explorer": "Hanoman",
    "fixer": "Bima",
    "designer": "Arjuna",
    "architect": "Wisanggeni",
    "oracle": "Abiyasa",
    "quality-gate": "Yudhistira",
    "librarian": "Batara Guru",
    "visual-context-extractor": "Sanjaya",
}

files = sorted(path.stem for path in (ROOT / "agents").glob("*.md"))
assert files == sorted(EXPECTED), f"active agent IDs changed: {files}"
for agent, codename in EXPECTED.items():
    content = (ROOT / "agents" / f"{agent}.md").read_text(encoding="utf-8")
    descriptions = re.findall(r"^description:\s*(.*)$", content, re.MULTILINE)
    assert len(descriptions) == 1, f"{agent}: frontmatter description count is {len(descriptions)}"
    assert descriptions[0].startswith(f"{codename} — "), f"{agent}: codename missing"
    assert content.count(codename) == 1, f"{agent}: codename must appear once"
print("agent codename registry passed")
