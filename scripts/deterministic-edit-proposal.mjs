#!/usr/bin/env node

import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { resolve, relative, sep, extname } from "node:path";

const EXIT = {
  OK: 0,
  STALE_HASH: 10,
  ANCHOR_NOT_FOUND: 11,
  AMBIGUOUS_ANCHOR: 12,
  NO_CHANGE: 13,
  PATH_OUT_OF_SCOPE: 14,
  UNSUPPORTED_FILE: 15,
  WRITE_FORBIDDEN: 16,
  INVALID_INPUT: 17,
};

const ALLOWED_EXT = new Set([".md", ".txt", ".json", ".mjs", ".js", ".ts", ".tsx", ".yml", ".yaml"]);

function fail(code, reason, extra = {}) {
  const out = { ok: false, code, reason, ...extra };
  process.stdout.write(`${JSON.stringify(out, null, 2)}\n`);
  process.exit(code);
}

function sha256(input) {
  return createHash("sha256").update(input).digest("hex");
}

function parseArgs(argv) {
  const arg = argv[2];
  if (!arg) fail(EXIT.INVALID_INPUT, "missing-json-payload");
  let parsed;
  try {
    parsed = JSON.parse(arg);
  } catch {
    fail(EXIT.INVALID_INPUT, "invalid-json-payload");
  }
  return parsed;
}

function assertRepoRelativePath(repoRoot, relPath) {
  if (typeof relPath !== "string" || relPath.length === 0) {
    fail(EXIT.INVALID_INPUT, "missing-path");
  }
  if (relPath.startsWith("/") || relPath.includes("..")) {
    fail(EXIT.PATH_OUT_OF_SCOPE, "path-out-of-scope", { path: relPath });
  }
  const abs = resolve(repoRoot, relPath);
  const rel = relative(repoRoot, abs);
  if (rel.startsWith("..") || rel.includes(`..${sep}`)) {
    fail(EXIT.PATH_OUT_OF_SCOPE, "path-out-of-scope", { path: relPath });
  }
  return abs;
}

function findUniqueExactBlock(content, anchor) {
  const first = content.indexOf(anchor);
  if (first === -1) return { kind: "not-found" };
  const second = content.indexOf(anchor, first + anchor.length);
  if (second !== -1) return { kind: "ambiguous" };
  return { kind: "ok", index: first };
}

function makeSimpleUnifiedDiff(filename, before, after) {
  const beforeLines = before.split("\n");
  const afterLines = after.split("\n");
  
  const header = [
    `--- ${filename} (before)`,
    `+++ ${filename} (proposal)`,
    "@@ -1,1 +1,1 @@"
  ];
  
  const diffLines = [];
  
  // Minimal diff for anchor substitution
  let bIdx = 0;
  let aIdx = 0;
  while (bIdx < beforeLines.length || aIdx < afterLines.length) {
    if (beforeLines[bIdx] === afterLines[aIdx]) {
      if (beforeLines[bIdx] !== undefined) {
        diffLines.push(` ${beforeLines[bIdx]}`);
      }
      bIdx++;
      aIdx++;
    } else {
      // Find mismatch
      const oldChunk = [];
      const newChunk = [];
      while (bIdx < beforeLines.length && beforeLines[bIdx] !== afterLines[aIdx]) {
        oldChunk.push(`-${beforeLines[bIdx]}`);
        bIdx++;
      }
      while (aIdx < afterLines.length && (bIdx >= beforeLines.length || beforeLines[bIdx] !== afterLines[aIdx])) {
        newChunk.push(`+${afterLines[aIdx]}`);
        aIdx++;
      }
      diffLines.push(...oldChunk, ...newChunk);
    }
  }
  
  return [...header, ...diffLines].join("\n");
}

function main() {
  const repoRoot = process.cwd();
  const payload = parseArgs(process.argv);
  
  if (payload.apply === true || payload.mode === "apply") {
    fail(EXIT.WRITE_FORBIDDEN, "write-forbidden");
  }

  const path = payload.path;
  const expectedSha256 = payload.expected_sha256;
  const oldBlock = payload.old_block;
  const newBlock = payload.new_block;

  if (!expectedSha256 || !oldBlock || typeof newBlock !== "string") {
    fail(EXIT.INVALID_INPUT, "missing-required-fields", { required: ["path", "expected_sha256", "old_block", "new_block"] });
  }

  const absPath = assertRepoRelativePath(repoRoot, path);
  if (!ALLOWED_EXT.has(extname(absPath))) fail(EXIT.UNSUPPORTED_FILE, "unsupported-file", { path });
  if (!existsSync(absPath)) fail(EXIT.UNSUPPORTED_FILE, "file-not-found", { path });

  const before = readFileSync(absPath, "utf8");
  const actualSha = sha256(before);
  if (actualSha !== expectedSha256) {
    fail(EXIT.STALE_HASH, "stale-hash", { path, expected_sha256: expectedSha256, actual_sha256: actualSha });
  }

  const match = findUniqueExactBlock(before, oldBlock);
  if (match.kind === "not-found") fail(EXIT.ANCHOR_NOT_FOUND, "anchor-not-found", { path });
  if (match.kind === "ambiguous") fail(EXIT.AMBIGUOUS_ANCHOR, "ambiguous-anchor", { path });

  const after = `${before.slice(0, match.index)}${newBlock}${before.slice(match.index + oldBlock.length)}`;
  if (after === before) fail(EXIT.NO_CHANGE, "no-change", { path });

  const diff = makeSimpleUnifiedDiff(path, before, after);
  const out = {
    ok: true,
    code: EXIT.OK,
    mode: "proposal-only",
    write_attempted: false,
    path,
    expected_sha256: expectedSha256,
    actual_sha256: actualSha,
    proposed_sha256: sha256(after),
    diff,
  };
  process.stdout.write(`${JSON.stringify(out, null, 2)}\n`);
}

main();
