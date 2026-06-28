"""Insert '## Pre-flight Skill & MCP Discovery' block into all 22 agent files
and 22 skill files (skills/opencode-*/SKILL.md) if not already present.

Idempotent: re-running the script is a no-op.
"""
import re
import sys
from pathlib import Path

REPO = Path("/var/home/ujang/.config/opencode")

AGENT_PREFLIGHT = """## Pre-flight Skill & MCP Discovery
Before the first substantial answer, diagnosis, plan, or implementation step on non-trivial work:
- Load the lane's primary skill first and name it explicitly (`Skill I'm using: ...`).
- Scan `.opencode/docs/MCP.md`, task shape, and stack docs to decide which MCPs are applicable; state that explicitly (`MCPs I'm using: ...`, `What I'm checking first: ...`).
- If an MCP is obviously applicable (multi-issue debugging -> `sequential-thinking`; version-sensitive docs/API/framework -> `context7`; broad code search -> `grep_app`; repo/PR/remote state -> `github`; static pattern/security scan -> `semgrep`; browser/runtime UI flow -> `playwright`), use it or record a concrete skip reason.
- If you loaded a skill, it must change execution in at least one concrete way (command, pattern, test, risk callout, MCP choice). Loaded-but-unused skill is a process defect.

ponytail: Textual contract first; mechanical transcript audit via `scripts/session-trace-audit.py` is the upgrade path.

"""

SKILL_PREFLIGHT = """## Pre-flight Skill & MCP Discovery
Before the first substantial answer, diagnosis, route, or implementation step on non-trivial work:
- Name the skill explicitly (`Skill I'm using: ...`).
- Decide MCP applicability explicitly (`MCPs I'm using: ...`, `What I'm checking first: ...`).
- If an MCP is obviously applicable, use it or record a concrete skip reason. Silent skip is a defect.
- At final summary time, name one concrete thing this skill changed about execution. Loaded-but-unused skill is a process defect.

ponytail: This is a behavioral contract. Use `scripts/session-trace-audit.py` as the advisory checker until transcript hooks become first-class.

"""

MARKER = "## Pre-flight Skill & MCP Discovery"


def patch_agent(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    if MARKER in text:
        return False
    if "\n## Workflow\n" in text:
        new = text.replace("\n## Workflow\n", "\n" + AGENT_PREFLIGHT + "## Workflow\n", 1)
        path.write_text(new, encoding="utf-8")
        return True
    return False


def patch_skill(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    if MARKER in text:
        return False
    if "\n## Workflow\n" in text:
        new = text.replace("\n## Workflow\n", "\n" + SKILL_PREFLIGHT + "## Workflow\n", 1)
    elif "\n## Sequential Thinking MCP Gate\n" in text:
        new = text.replace("\n## Sequential Thinking MCP Gate\n", "\n" + SKILL_PREFLIGHT + "## Sequential Thinking MCP Gate\n", 1)
    else:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    agents = sorted(REPO.glob("agents/*.md"))
    skills = sorted(REPO.glob("skills/opencode-*/SKILL.md"))

    agent_changed = [str(p) for p in agents if patch_agent(p)]
    skill_changed = [str(p) for p in skills if patch_skill(p)]

    print(f"agent files scanned:  {len(agents)}")
    print(f"agent files changed:  {len(agent_changed)}")
    for p in agent_changed:
        print(f"  A {p}")
    print()
    print(f"skill files scanned:  {len(skills)}")
    print(f"skill files changed:  {len(skill_changed)}")
    for p in skill_changed:
        print(f"  S {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
