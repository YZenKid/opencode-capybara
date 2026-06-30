#!/usr/bin/env python3
"""Project-local MCP memory wrapper with bounded replace/archive lifecycle.

This wraps the official MCP memory server (`@modelcontextprotocol/server-memory`)
but keeps storage local to each project under `.opencode/mcp-memory/`.

Goals:
- final-task project memory is persisted before `@orchestrator` gives the final summary
- memory is project-local, not global chat memory
- memory does not grow forever: dedup, replace, archive, cap

Storage:
- MCP graph jsonl: `.opencode/mcp-memory/<project-key>/memory.jsonl`
- index/meta: `.opencode/mcp-memory/<project-key>/index.json`
- archive log: `.opencode/mcp-memory/<project-key>/archive.json`

This script is intentionally boring:
- if the MCP package is unavailable, it falls back to local bounded JSON writes
- destructive delete tools are not exposed in finalize mode
- replace policy is entity-name based inside category namespace

Usage:
  python3 scripts/mcp-memory-store.py --project-root . --finalize \
    --task landing-2026-06-30 \
    --summary "Shipped landing hero using dashboard tokens" \
    --decision "Use dashboard template tokens as source of truth" \
    --decision "Do not reuse Trafalgar template directly (N19)" \
    --file resources/js/pages/welcome.tsx \
    --file templates/dashboard/src/index.css \
    --claim-level done

  python3 scripts/mcp-memory-store.py --project-root . --search tailwind
  python3 scripts/mcp-memory-store.py --project-root . --graph

Exit codes:
  0 = ok
  1 = validation/finalize issue
  2 = mcp invocation / io failure
  4 = invocation error
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MAX_ACTIVE_DEFAULT = 200
DATE_FMT = "%Y-%m-%dT%H:%M:%SZ"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime(DATE_FMT)


def slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._-]+", "-", s.strip().lower()).strip("-")
    return s or "unknown"


def project_key(project_root: Path) -> str:
    digest = hashlib.sha256(str(project_root.resolve()).encode("utf-8")).hexdigest()[:16]
    return f"{slug(project_root.name)}-{digest}"


def bundle_root(project_root: Path) -> Path:
    return project_root / ".opencode" / "mcp-memory" / project_key(project_root)


def memory_file(project_root: Path) -> Path:
    return bundle_root(project_root) / "memory.jsonl"


def index_file(project_root: Path) -> Path:
    return bundle_root(project_root) / "index.json"


def archive_file(project_root: Path) -> Path:
    return bundle_root(project_root) / "archive.json"


def ensure_dirs(project_root: Path) -> None:
    bundle_root(project_root).mkdir(parents=True, exist_ok=True)


def read_json(path: Path, fallback: Any) -> Any:
    if not path.is_file():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return fallback


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


@dataclass
class MemoryRecord:
    entity_name: str
    entity_type: str
    summary: str
    task_id: str
    claim_level: str
    decisions: "list[str]"
    files: "list[str]"
    status: str = "active"
    importance: str = "medium"
    created_at: str = ""
    updated_at: str = ""
    last_used_at: str = ""
    revision: int = 1
    supersedes: "str | None" = None
    archived_reason: "str | None" = None

    def to_observations(self) -> list[str]:
        obs = [
            f"summary: {self.summary}",
            f"task_id: {self.task_id}",
            f"claim_level: {self.claim_level}",
            f"status: {self.status}",
            f"importance: {self.importance}",
            f"revision: {self.revision}",
            f"updated_at: {self.updated_at}",
        ]
        obs.extend(f"decision: {x}" for x in self.decisions)
        obs.extend(f"file: {x}" for x in self.files)
        if self.supersedes:
            obs.append(f"supersedes: {self.supersedes}")
        if self.archived_reason:
            obs.append(f"archived_reason: {self.archived_reason}")
        return obs


def load_index(project_root: Path) -> dict[str, Any]:
    return read_json(index_file(project_root), {"records": [], "project_root": str(project_root.resolve())})


def save_index(project_root: Path, data: dict[str, Any]) -> None:
    write_json(index_file(project_root), data)


def load_archive(project_root: Path) -> list[dict[str, Any]]:
    return read_json(archive_file(project_root), [])


def save_archive(project_root: Path, data: list[dict[str, Any]]) -> None:
    write_json(archive_file(project_root), data)


def entity_name_for_task(task_id: str) -> str:
    return f"task::{slug(task_id)}"


def local_finalize(
    project_root: Path,
    task_id: str,
    summary: str,
    decisions: list[str],
    files: list[str],
    claim_level: str,
    max_active: int,
) -> dict[str, Any]:
    ensure_dirs(project_root)
    idx = load_index(project_root)
    archive = load_archive(project_root)
    now = now_iso()
    name = entity_name_for_task(task_id)
    records = idx.get("records") or []

    existing = next((r for r in records if r.get("entity_name") == name and r.get("status") == "active"), None)
    supersedes = None
    revision = 1
    if existing:
        existing["status"] = "archived"
        existing["archived_reason"] = "replaced_by_newer_task_memory"
        existing["last_used_at"] = now
        archive.append(existing.copy())
        supersedes = existing.get("task_id")
        revision = int(existing.get("revision") or 1) + 1

    rec = MemoryRecord(
        entity_name=name,
        entity_type="project_task_memory",
        summary=summary.strip(),
        task_id=task_id,
        claim_level=claim_level,
        decisions=[x.strip() for x in decisions if x.strip()],
        files=[x.strip() for x in files if x.strip()],
        created_at=now,
        updated_at=now,
        last_used_at=now,
        revision=revision,
        supersedes=supersedes,
    )

    records = [r for r in records if not (r.get("entity_name") == name and r.get("status") == "active")]
    records.append(asdict(rec))
    active = [r for r in records if r.get("status") == "active"]
    if len(active) > max_active:
        active_sorted = sorted(
            active,
            key=lambda r: (
                {"high": 2, "medium": 1, "low": 0}.get(str(r.get("importance") or "medium"), 1),
                str(r.get("last_used_at") or ""),
            ),
        )
        overflow = len(active) - max_active
        to_archive = active_sorted[:overflow]
        for r in to_archive:
            r["status"] = "archived"
            r["archived_reason"] = "cap_exceeded"
            archive.append(r.copy())

    idx["records"] = records
    idx["updated_at"] = now
    save_index(project_root, idx)
    save_archive(project_root, archive)
    return {
        "ok": True,
        "backend": "local",
        "project_key": project_key(project_root),
        "record": asdict(rec),
        "active_count": len([r for r in idx["records"] if r.get("status") == "active"]),
        "archived_count": len(archive),
    }


def call_mcp_memory(project_root: Path, tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    memfile = memory_file(project_root)
    ensure_dirs(project_root)
    env = os.environ.copy()
    env["MEMORY_FILE_PATH"] = str(memfile)
    # ponytail: direct stdio JSON-RPC to npx server-memory. If protocol changes,
    # upgrade by swapping this bridge to a dedicated MCP client helper.
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool, "arguments": payload},
    }
    init = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "opencode-mcp-memory-store", "version": "1.0.0"},
        },
    }
    proc = subprocess.run(
        ["npx", "-y", "@modelcontextprotocol/server-memory"],
        input=json.dumps(init) + "\n" + json.dumps(req) + "\n",
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or f"npx exited {proc.returncode}")
    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip().startswith("{")]
    if not lines:
        raise RuntimeError("no JSON-RPC response from memory server")
    parsed = [json.loads(line) for line in lines]
    final = next((x for x in parsed if x.get("id") == 1), parsed[-1])
    if "error" in final:
        raise RuntimeError(json.dumps(final["error"], ensure_ascii=False))
    return final.get("result") or {}


def mcp_finalize(
    project_root: Path,
    task_id: str,
    summary: str,
    decisions: list[str],
    files: list[str],
    claim_level: str,
    max_active: int,
) -> dict[str, Any]:
    result = local_finalize(project_root, task_id, summary, decisions, files, claim_level, max_active)
    rec = result["record"]
    entity = {
        "name": rec["entity_name"],
        "entityType": rec["entity_type"],
        "observations": [f"task_id: {rec['task_id']}"]
    }
    try:
        call_mcp_memory(project_root, "create_entities", {"entities": [entity]})
        call_mcp_memory(
            project_root,
            "add_observations",
            {"observations": [{"entityName": rec["entity_name"], "contents": rec["summary"]}, *[
                {"entityName": rec["entity_name"], "contents": x} for x in MemoryRecord(**rec).to_observations()
            ]]},
        )
        result["backend"] = "mcp+local"
    except Exception as e:
        result["backend"] = "local-fallback"
        result["mcp_error"] = str(e)
    return result


def search_local(project_root: Path, query: str) -> dict[str, Any]:
    idx = load_index(project_root)
    q = query.lower()
    hits = []
    for r in idx.get("records") or []:
        blob = json.dumps(r, ensure_ascii=False).lower()
        if q in blob:
            hits.append(r)
    return {"ok": True, "backend": "local", "query": query, "hits": hits[:20]}


def graph_local(project_root: Path) -> dict[str, Any]:
    idx = load_index(project_root)
    return {"ok": True, "backend": "local", "records": idx.get("records") or []}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--task")
    ap.add_argument("--summary")
    ap.add_argument("--decision", action="append", default=[])
    ap.add_argument("--file", action="append", default=[])
    ap.add_argument("--claim-level", default="done")
    ap.add_argument("--max-active", type=int, default=MAX_ACTIVE_DEFAULT)
    ap.add_argument("--finalize", action="store_true")
    ap.add_argument("--search")
    ap.add_argument("--graph", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    try:
        if args.finalize:
            if not args.task or not args.summary:
                print("error: --finalize requires --task and --summary", file=sys.stderr)
                return 4
            out = mcp_finalize(
                root,
                args.task,
                args.summary,
                args.decision,
                args.file,
                args.claim_level,
                args.max_active,
            )
        elif args.search:
            out = search_local(root, args.search)
        elif args.graph:
            out = graph_local(root)
        else:
            print("error: choose one of --finalize, --search, or --graph", file=sys.stderr)
            return 4
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(out, ensure_ascii=False))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
