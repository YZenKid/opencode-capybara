#!/usr/bin/env python3
"""
Project knowledge memory system with archive, dedup, and proposals.

Usage:
  project-memory.py --save --task <task-id> --category <category> --lesson <text> [--context <text>] [--tags <tag1,tag2>] [--importance high|medium|low] [--skip-dedup]
  project-memory.py --list [--category <category>] [--limit N]
  project-memory.py --search <keyword>
  project-memory.py --load --context <task-context> [--tags <tag1,tag2>] [--limit N] [--importance high|medium|low]
  project-memory.py --cleanup [--archive-old]
  project-memory.py --archive --id <memory-id>
  project-memory.py --export
  project-memory.py --propose --task <task-id> --category <category> --lesson <text> [--context <text>] [--tags <tag1,tag2>] [--importance high|medium|low]
  project-memory.py --list-proposals
  project-memory.py --apply-proposal --id <proposal-id>
  project-memory.py --use --id <memory-id>

Memory structure:
- Active memories: .opencode/memory/knowledge.json
- Archived memories: .opencode/memory/archive.json
- Proposals: .opencode/memory/proposals.json
"""

import json
import sys
import argparse
import difflib
from pathlib import Path
from datetime import datetime, timedelta

MEMORY_DIR = Path(".opencode/memory")
MEMORY_FILE = MEMORY_DIR / "knowledge.json"
ARCHIVE_FILE = MEMORY_DIR / "archive.json"
PROPOSALS_FILE = MEMORY_DIR / "proposals.json"


def load_memories() -> list[dict]:
    if not MEMORY_FILE.exists():
        return []
    return json.loads(MEMORY_FILE.read_text())


def save_memories(memories: list[dict]):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memories, indent=2))


def load_archive() -> list[dict]:
    if not ARCHIVE_FILE.exists():
        return []
    return json.loads(ARCHIVE_FILE.read_text())


def save_archive(archive: list[dict]):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_FILE.write_text(json.dumps(archive, indent=2))


def load_proposals() -> list[dict]:
    if not PROPOSALS_FILE.exists():
        return []
    return json.loads(PROPOSALS_FILE.read_text())


def save_proposals(proposals: list[dict]):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    PROPOSALS_FILE.write_text(json.dumps(proposals, indent=2))


def find_similar_memories(lesson: str, context: str = None, threshold: float = 0.6) -> list[dict]:
    """Find memories similar to the given lesson/context using difflib."""
    memories = load_memories()
    if not memories:
        return []
    
    similar = []
    for m in memories:
        # Compare lesson text
        lesson_similarity = difflib.SequenceMatcher(
            None, 
            lesson.lower(), 
            m.get("lesson", "").lower()
        ).ratio()
        
        # Compare context if provided
        context_similarity = 0
        if context and m.get("context"):
            context_similarity = difflib.SequenceMatcher(
                None,
                context.lower(),
                m.get("context", "").lower()
            ).ratio()
        
        # Combined similarity
        combined = lesson_similarity * 0.7 + context_similarity * 0.3 if context else lesson_similarity
        
        if combined >= threshold:
            similar.append({
                "memory": m,
                "similarity": combined,
                "lesson_sim": lesson_similarity,
                "context_sim": context_similarity
            })
    
    # Sort by similarity desc
    similar.sort(key=lambda x: x["similarity"], reverse=True)
    return similar[:3]  # Return top 3 most similar


def save_memory(task_id: str, category: str, lesson: str, context: str = None, tags: list[str] = None, importance: str = "medium", skip_dedup: bool = False):
    """Save a new memory entry with dedup check."""
    memories = load_memories()
    
    # Dedup check
    if not skip_dedup:
        similar = find_similar_memories(lesson, context, threshold=0.6)
        if similar:
            print("⚠️  Similar memories found:")
            for s in similar:
                m = s["memory"]
                print(f"  - {m['id']} (similarity: {s['similarity']:.2f})")
                print(f"    Lesson: {m['lesson']}")
                if m.get("context"):
                    print(f"    Context: {m['context']}")
            print("\nUse --skip-dedup to save anyway, or --update to replace existing.")
            return None
    
    # Generate new ID
    all_memories = memories + load_archive()
    new_id = f"mem-{len(all_memories) + 1:04d}"
    
    entry = {
        "id": new_id,
        "task_id": task_id,
        "category": category,
        "lesson": lesson,
        "context": context,
        "tags": tags or [],
        "importance": importance,
        "created": datetime.now().isoformat(),
        "used_count": 0,
        "last_used": None,
    }
    
    memories.append(entry)
    save_memories(memories)
    print(f"✓ Saved memory: {new_id} (category: {category}, importance: {importance})")
    return entry


def list_memories(category: str = None, limit: int = None):
    """List memories, optionally filtered by category."""
    memories = load_memories()
    
    if category:
        memories = [m for m in memories if m.get("category") == category]
    
    # Sort by importance then created desc
    importance_order = {"high": 3, "medium": 2, "low": 1}
    memories.sort(key=lambda m: (
        importance_order.get(m.get("importance", "medium"), 2),
        m.get("created", "")
    ), reverse=True)
    
    if limit:
        memories = memories[:limit]
    
    print(f"## Project Knowledge Memory ({len(memories)} entries)\n")
    
    for m in memories:
        tags_str = ", ".join(m.get("tags", [])) if m.get("tags") else "none"
        importance = m.get("importance", "medium")
        used_count = m.get("used_count", 0)
        print(f"### {m['id']} ({m['category']}) [importance: {importance}, used: {used_count}x]")
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
        importance = m.get("importance", "medium")
        print(f"### {m['id']} ({m['category']}) [importance: {importance}]")
        print(f"Task: {m['task_id']}")
        print(f"Tags: {tags_str}")
        if m.get("context"):
            print(f"Context: {m['context']}")
        print(f"Lesson: {m['lesson']}")
        print()


def load_relevant(context: str, tags: list[str] = None, limit: int = 10, min_importance: str = "medium"):
    """Load memories relevant to current task context, filtered by importance."""
    memories = load_memories()
    context_lower = context.lower()
    tags_set = set(t.lower() for t in tags) if tags else set()
    
    # Filter by importance
    importance_order = {"high": 3, "medium": 2, "low": 1}
    min_importance_level = importance_order.get(min_importance, 2)
    memories = [m for m in memories if importance_order.get(m.get("importance", "medium"), 2) >= min_importance_level]
    
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
        
        # Boost by importance
        score += (importance_order.get(m.get("importance", "medium"), 2) - 1) * 2
        
        # Boost by usage count (prefer frequently used)
        score += min(m.get("used_count", 0), 5) * 0.5
        
        if score > 0:
            scored.append((score, m))
    
    # Sort by score desc, then by importance desc, then by created desc
    scored.sort(key=lambda x: (x[0], importance_order.get(x[1].get("importance", "medium"), 2), x[1].get("created", "")), reverse=True)
    
    if limit:
        scored = scored[:limit]
    
    print(f"## Relevant Memories for: '{context[:100]}...' (min importance: {min_importance})\n")
    print(f"Found {len(scored)} relevant entries (showing top {min(limit, len(scored))}):\n")
    
    for score, m in scored:
        tags_str = ", ".join(m.get("tags", [])) if m.get("tags") else "none"
        importance = m.get("importance", "medium")
        print(f"### {m['id']} ({m['category']}) [importance: {importance}, relevance: {score:.1f}]")
        print(f"Task: {m['task_id']}")
        print(f"Tags: {tags_str}")
        if m.get("context"):
            print(f"Context: {m['context']}")
        print(f"Lesson: {m['lesson']}")
        print()


def cleanup_memories(archive_old: bool = False):
    """Remove low-importance memories, optionally archive old unused ones."""
    memories = load_memories()
    archive = load_archive() if archive_old else []
    original_count = len(memories)
    
    # Separate by importance
    low_importance = [m for m in memories if m.get("importance", "medium") == "low"]
    kept = [m for m in memories if m.get("importance", "medium") != "low"]
    
    # Find old unused memories (>90 days, used_count=0)
    cutoff = datetime.now() - timedelta(days=90)
    old_unused = []
    still_kept = []
    
    for m in kept:
        created = datetime.fromisoformat(m.get("created", datetime.now().isoformat()))
        if created < cutoff and m.get("used_count", 0) == 0:
            old_unused.append(m)
        else:
            still_kept.append(m)
    
    # Archive old unused if requested
    if archive_old and old_unused:
        for m in old_unused:
            m["archived"] = datetime.now().isoformat()
        archive.extend(old_unused)
        save_archive(archive)
        kept = still_kept
    
    # Save active memories
    save_memories(kept)
    
    print(f"## Memory Cleanup Report\n")
    print(f"Original count: {original_count}")
    print(f"Removed (low importance): {len(low_importance)}")
    if archive_old:
        print(f"Archived (old unused): {len(old_unused)}")
    print(f"Remaining active: {len(kept)}")
    if archive_old:
        print(f"Total in archive: {len(archive)}")
    
    if not archive_old and old_unused:
        print(f"\n⚠️  {len(old_unused)} old unused memories found. Use --archive-old to move them to archive.")


def archive_memory(memory_id: str):
    """Move a specific memory to archive."""
    memories = load_memories()
    archive = load_archive()
    
    target = None
    remaining = []
    for m in memories:
        if m.get("id") == memory_id:
            target = m
        else:
            remaining.append(m)
    
    if not target:
        print(f"✗ Memory {memory_id} not found", file=sys.stderr)
        sys.exit(1)
    
    target["archived"] = datetime.now().isoformat()
    archive.append(target)
    save_archive(archive)
    save_memories(remaining)
    
    print(f"✓ Archived memory {memory_id}")


def propose_memory(task_id: str, category: str, lesson: str, context: str = None, tags: list[str] = None, importance: str = "medium"):
    """Create a memory proposal for review."""
    proposals = load_proposals()
    
    # Generate proposal ID
    all_memories = load_memories() + load_archive() + proposals
    proposal_id = f"prop-{len(all_memories) + 1:04d}"
    
    proposal = {
        "id": proposal_id,
        "task_id": task_id,
        "category": category,
        "lesson": lesson,
        "context": context,
        "tags": tags or [],
        "importance": importance,
        "proposed": datetime.now().isoformat(),
        "status": "pending",
        "reason": f"Proposed from task {task_id}",
    }
    
    proposals.append(proposal)
    save_proposals(proposals)
    
    print(f"✓ Proposed memory: {proposal_id}")
    print(f"  Category: {category}")
    print(f"  Importance: {importance}")
    print(f"  Lesson: {lesson}")
    if context:
        print(f"  Context: {context}")
    
    # Check for similar memories
    similar = find_similar_memories(lesson, context, threshold=0.5)
    if similar:
        print(f"\n⚠️  Note: Similar memories exist:")
        for s in similar:
            m = s["memory"]
            print(f"  - {m['id']} (similarity: {s['similarity']:.2f})")
    
    return proposal


def list_proposals():
    """List all memory proposals."""
    proposals = load_proposals()
    pending = [p for p in proposals if p.get("status") == "pending"]
    
    print(f"## Memory Proposals ({len(pending)} pending)\n")
    
    if not pending:
        print("No pending proposals.")
        return
    
    for p in pending:
        tags_str = ", ".join(p.get("tags", [])) if p.get("tags") else "none"
        print(f"### {p['id']} ({p['category']}) [importance: {p['importance']}]")
        print(f"Task: {p['task_id']}")
        print(f"Proposed: {p['proposed']}")
        print(f"Tags: {tags_str}")
        if p.get("context"):
            print(f"Context: {p['context']}")
        print(f"Lesson: {p['lesson']}")
        print(f"Reason: {p['reason']}")
        print()


def apply_proposal(proposal_id: str):
    """Convert a proposal into an actual memory."""
    proposals = load_proposals()
    
    target = None
    remaining = []
    for p in proposals:
        if p.get("id") == proposal_id:
            target = p
        else:
            remaining.append(p)
    
    if not target:
        print(f"✗ Proposal {proposal_id} not found", file=sys.stderr)
        sys.exit(1)
    
    # Save as actual memory
    result = save_memory(
        task_id=target["task_id"],
        category=target["category"],
        lesson=target["lesson"],
        context=target.get("context"),
        tags=target.get("tags", []),
        importance=target["importance"],
        skip_dedup=False
    )
    
    if result:
        # Mark proposal as applied
        target["status"] = "applied"
        target["applied_as"] = result["id"]
        target["applied_at"] = datetime.now().isoformat()
        remaining.append(target)
        save_proposals(remaining)
        
        print(f"\n✓ Proposal {proposal_id} applied as memory {result['id']}")
    else:
        print(f"\n✗ Failed to apply proposal (duplicate detected)")


def mark_used(memory_id: str):
    """Mark a memory entry as used (increment used_count, update last_used)."""
    memories = load_memories()
    for m in memories:
        if m.get("id") == memory_id:
            m["used_count"] = m.get("used_count", 0) + 1
            m["last_used"] = datetime.now().isoformat()
            save_memories(memories)
            print(f"✓ Marked {memory_id} as used (count: {m['used_count']})")
            return
    print(f"✗ Memory {memory_id} not found", file=sys.stderr)


def export_memories():
    """Export all memories as markdown."""
    memories = load_memories()
    archive = load_archive()
    
    print(f"# Project Knowledge Base\n")
    print(f"Active entries: {len(memories)}")
    print(f"Archived entries: {len(archive)}\n")
    
    if memories:
        print("## Active Memories\n")
        
        # Group by category
        by_category = {}
        for m in memories:
            cat = m.get("category", "uncategorized")
            by_category.setdefault(cat, []).append(m)
        
        for category in sorted(by_category.keys()):
            print(f"\n### {category.replace('_', ' ').title()}\n")
            for m in by_category[category]:
                tags_str = ", ".join(m.get("tags", [])) if m.get("tags") else "none"
                importance = m.get("importance", "medium")
                print(f"#### {m['id']} (from task: {m['task_id']}) [importance: {importance}]")
                print(f"- Created: {m['created']}")
                print(f"- Tags: {tags_str}")
                print(f"- Used: {m.get('used_count', 0)}x")
                if m.get("context"):
                    print(f"- Context: {m['context']}")
                print(f"- **Lesson**: {m['lesson']}")
                print()
    
    if archive:
        print("\n## Archived Memories\n")
        
        # Group by category
        by_category = {}
        for m in archive:
            cat = m.get("category", "uncategorized")
            by_category.setdefault(cat, []).append(m)
        
        for category in sorted(by_category.keys()):
            print(f"\n### {category.replace('_', ' ').title()}\n")
            for m in by_category[category]:
                tags_str = ", ".join(m.get("tags", [])) if m.get("tags") else "none"
                print(f"#### {m['id']} (from task: {m['task_id']})")
                print(f"- Created: {m['created']}")
                print(f"- Archived: {m.get('archived', 'unknown')}")
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
    group.add_argument("--cleanup", action="store_true", help="Remove low-importance memories")
    group.add_argument("--archive", action="store_true", help="Archive a specific memory")
    group.add_argument("--propose", action="store_true", help="Propose a memory for review")
    group.add_argument("--list-proposals", action="store_true", help="List all proposals")
    group.add_argument("--apply-proposal", metavar="PROPOSAL_ID", help="Apply a proposal")
    group.add_argument("--use", action="store_true", help="Mark memory as used")
    group.add_argument("--export", action="store_true", help="Export as markdown")
    
    parser.add_argument("--task", help="Task ID (for --save)")
    parser.add_argument("--category", choices=["pitfall", "pattern", "decision", "workaround", "architecture", "testing", "deployment", "performance", "security", "ux"], help="Memory category (for --save or --list)")
    parser.add_argument("--lesson", help="The lesson learned (for --save)")
    parser.add_argument("--context", help="Context/situation (for --save or --load)")
    parser.add_argument("--tags", help="Comma-separated tags (for --save or --load)")
    parser.add_argument("--importance", choices=["high", "medium", "low"], default="medium", help="Importance level (for --save or --load filter)")
    parser.add_argument("--limit", type=int, default=10, help="Max entries to show (for --list or --load)")
    parser.add_argument("--archive-old", action="store_true", help="Archive old unused memories during cleanup")
    parser.add_argument("--id", help="Memory ID (for --archive or --use)")
    parser.add_argument("--skip-dedup", action="store_true", help="Skip dedup check when saving")
    
    args = parser.parse_args()
    
    if args.save:
        if not args.task or not args.category or not args.lesson:
            print("Error: --task, --category, and --lesson required for --save", file=sys.stderr)
            sys.exit(1)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        save_memory(args.task, args.category, args.lesson, args.context, tags, args.importance, args.skip_dedup)
    
    elif args.list:
        list_memories(args.category, args.limit)
    
    elif args.search:
        search_memories(args.search)
    
    elif args.load:
        if not args.context:
            print("Error: --context required for --load", file=sys.stderr)
            sys.exit(1)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        load_relevant(args.context, tags, args.limit, args.importance)
    
    elif args.cleanup:
        cleanup_memories(args.archive_old)
    
    elif args.archive:
        if not args.id:
            print("Error: --id required for --archive", file=sys.stderr)
            sys.exit(1)
        archive_memory(args.id)
    
    elif args.propose:
        if not args.task or not args.category or not args.lesson:
            print("Error: --task, --category, and --lesson required for --propose", file=sys.stderr)
            sys.exit(1)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        propose_memory(args.task, args.category, args.lesson, args.context, tags, args.importance)
    
    elif args.list_proposals:
        list_proposals()
    
    elif args.apply_proposal:
        apply_proposal(args.apply_proposal)
    
    elif args.use:
        if not args.id:
            print("Error: --id required for --use", file=sys.stderr)
            sys.exit(1)
        mark_used(args.id)
    
    elif args.export:
        export_memories()


if __name__ == "__main__":
    main()
