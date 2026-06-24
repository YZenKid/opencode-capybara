#!/usr/bin/env python3
"""
Project knowledge memory system.

Stores lessons learned from completed tasks for reuse in future work.
Memory is per-project at `.opencode/memory/`.

Usage:
  project-memory.py --save --task <task-id> --category <category> --lesson <text> [--context <text>] [--tags <tag1,tag2>]
  project-memory.py --list [--category <category>] [--limit N]
  project-memory.py --search <keyword>
  project-memory.py --load --context <task-context> [--tags <tag1,tag2>] [--limit N]
  project-memory.py --export
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path(".opencode/memory")
MEMORY_FILE = MEMORY_DIR / "knowledge.json"


def load_memories() -> list[dict]:
    if not MEMORY_FILE.exists():
        return []
    return json.loads(MEMORY_FILE.read_text())


def save_memories(memories: list[dict]):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memories, indent=2))


def save_memory(task_id: str, category: str, lesson: str, context: str = None, tags: list[str] = None):
    """Save a new memory entry."""
    memories = load_memories()

    entry = {
        "id": f"mem-{len(memories) + 1:04d}",
        "task_id": task_id,
        "category": category,
        "lesson": lesson,
        "context": context,
        "tags": tags or [],
        "created": datetime.now().isoformat(),
    }

    memories.append(entry)
    save_memories(memories)
    print(f"Saved memory: {entry['id']} ({category})")
    return entry


def list_memories(category: str = None, limit: int = None):
    """List memories, optionally filtered by category."""
    memories = load_memories()

    if category:
        memories = [m for m in memories if m.get("category") == category]

    # Sort by created desc
    memories.sort(key=lambda m: m.get("created", ""), reverse=True)

    if limit:
        memories = memories[:limit]

    print(f"## Project Knowledge Memory ({len(memories)} entries)\n")

    for m in memories:
        tags_str = ", ".join(m.get("tags", [])) if m.get("tags") else "none"
        print(f"### {m['id']} ({m['category']})")
        print(f"Task: {m['task_id']}")
        print(f"Created: {m['created']}")
        print(f"Tags: {tags_str}")
        if m.get("context"):
            print(f"Context: {m['context']}")
        print(f"Lesson: {m['lesson']}")
        print()


def search_memories(keyword: str):
    """Search memories by keyword in lesson/context/tags."""
    memories = load_memories()
    keyword_lower = keyword.lower()

    matches = []
    for m in memories:
        searchable = f"{m.get('lesson', '')} {m.get('context', '')} {' '.join(m.get('tags', []))}".lower()
        if keyword_lower in searchable:
            matches.append(m)

    print(f"## Search: '{keyword}' ({len(matches)} matches)\n")

    for m in matches:
        tags_str = ", ".join(m.get("tags", [])) if m.get("tags") else "none"
        print(f"### {m['id']} ({m['category']})")
        print(f"Task: {m['task_id']}")
        print(f"Tags: {tags_str}")
        if m.get("context"):
            print(f"Context: {m['context']}")
        print(f"Lesson: {m['lesson']}")
        print()


def load_relevant(context: str, tags: list[str] = None, limit: int = 10):
    """Load memories relevant to current task context."""
    memories = load_memories()
    context_lower = context.lower()
    tags_set = set(t.lower() for t in tags) if tags else set()

    scored = []
    for m in memories:
        score = 0
        searchable = f"{m.get('lesson', '')} {m.get('context', '')}".lower()

        # Context keyword match
        for word in context_lower.split():
            if len(word) > 3 and word in searchable:
                score += 1

        # Tag match
        memory_tags = set(t.lower() for t in m.get("tags", []))
        if tags_set and memory_tags:
            overlap = len(tags_set & memory_tags)
            score += overlap * 2

        if score > 0:
            scored.append((score, m))

    # Sort by score desc, then by created desc
    scored.sort(key=lambda x: (x[0], x[1].get("created", "")), reverse=True)

    if limit:
        scored = scored[:limit]

    print(f"## Relevant Memories for: '{context[:100]}...'\n")
    print(f"Found {len(scored)} relevant entries (showing top {min(limit, len(scored))}):\n")

    for score, m in scored:
        tags_str = ", ".join(m.get("tags", [])) if m.get("tags") else "none"
        print(f"### {m['id']} ({m['category']}) [relevance: {score}]")
        print(f"Task: {m['task_id']}")
        print(f"Tags: {tags_str}")
        if m.get("context"):
            print(f"Context: {m['context']}")
        print(f"Lesson: {m['lesson']}")
        print()


def export_memories():
    """Export all memories as markdown."""
    memories = load_memories()
    print(f"# Project Knowledge Base\n")
    print(f"Total entries: {len(memories)}\n")

    # Group by category
    by_category = {}
    for m in memories:
        cat = m.get("category", "uncategorized")
        by_category.setdefault(cat, []).append(m)

    for category in sorted(by_category.keys()):
        print(f"\n## {category.replace('_', ' ').title()}\n")
        for m in by_category[category]:
            tags_str = ", ".join(m.get("tags", [])) if m.get("tags") else "none"
            print(f"### {m['id']} (from task: {m['task_id']})")
            print(f"- Created: {m['created']}")
            print(f"- Tags: {tags_str}")
            if m.get("context"):
                print(f"- Context: {m['context']}")
            print(f"- **Lesson**: {m['lesson']}")
            print()


def main():
    parser = argparse.ArgumentParser(description="Project knowledge memory system")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--save", action="store_true", help="Save a new memory")
    group.add_argument("--list", action="store_true", help="List all memories")
    group.add_argument("--search", metavar="KEYWORD", help="Search memories")
    group.add_argument("--load", action="store_true", help="Load relevant memories")
    group.add_argument("--export", action="store_true", help="Export as markdown")

    parser.add_argument("--task", help="Task ID (for --save)")
    parser.add_argument("--category", choices=["pitfall", "pattern", "decision", "workaround", "architecture", "testing", "deployment", "performance", "security", "ux"], help="Memory category (for --save or --list)")
    parser.add_argument("--lesson", help="The lesson learned (for --save)")
    parser.add_argument("--context", help="Context/situation (for --save or --load)")
    parser.add_argument("--tags", help="Comma-separated tags (for --save or --load)")
    parser.add_argument("--limit", type=int, default=10, help="Max entries to show (for --list or --load)")

    args = parser.parse_args()

    if args.save:
        if not args.task or not args.category or not args.lesson:
            print("Error: --task, --category, and --lesson required for --save", file=sys.stderr)
            sys.exit(1)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        save_memory(args.task, args.category, args.lesson, args.context, tags)

    elif args.list:
        list_memories(args.category, args.limit)

    elif args.search:
        search_memories(args.search)

    elif args.load:
        if not args.context:
            print("Error: --context required for --load", file=sys.stderr)
            sys.exit(1)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        load_relevant(args.context, tags, args.limit)

    elif args.export:
        export_memories()


if __name__ == "__main__":
    main()
