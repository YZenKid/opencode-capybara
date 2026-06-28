#!/usr/bin/env node
// Wrapper for scripts/verify-before-claim-check.py with practical defaults
// for the most common orchestrator-side usage.
//
// Modes:
//   (default)        : scan most recent .opencode/evidence/*/summary.md (or the
//                       newest .md under .opencode/evidence/ if no summary.md).
//                       Exit 0 even if flagged (advisory).
//   --strict         : same as default, but exit 1 if any claim is flagged.
//   --file <path>    : scan a specific file (relative or absolute).
//   --stdin          : read text from stdin instead of a file.
//   --recent         : same as default mode (explicit).
//   --json           : emit JSON output instead of text.
//   --all-evidence   : scan every .md file under .opencode/evidence/.
//   --help           : show usage.
//
// Examples:
//   node scripts/verify-claim-cli.mjs
//   node scripts/verify-claim-cli.mjs --strict
//   node scripts/verify-claim-cli.mjs --file .opencode/evidence/20260528-foo/summary.md
//   node scripts/verify-claim-cli.mjs --all-evidence --json
import { spawnSync } from "node:child_process";
import { existsSync, readdirSync, statSync } from "node:fs";
import { join, resolve, basename } from "node:path";

const repoRoot = process.cwd();
const evidenceRoot = join(repoRoot, ".opencode", "evidence");

function listMarkdownFiles(root) {
  if (!existsSync(root)) return [];
  const out = [];
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;
    const dir = join(root, entry.name);
    for (const f of readdirSync(dir, { withFileTypes: true })) {
      if (f.isFile() && f.name.endsWith(".md")) {
        out.push(join(dir, f.name));
      }
    }
  }
  return out;
}

function newestByMtime(files) {
  return files
    .map((f) => ({ f, m: statSync(f).mtimeMs }))
    .sort((a, b) => b.m - a.m)[0]?.f;
}

function pickDefaultTarget() {
  const files = listMarkdownFiles(evidenceRoot);
  if (!files.length) return null;
  // Prefer summary.md if present in the most recent task folder
  const summaryFirst = files.find((f) => basename(f) === "summary.md");
  if (summaryFirst) return summaryFirst;
  return newestByMtime(files);
}

function usage() {
  return [
    "Usage: node scripts/verify-claim-cli.mjs [options]",
    "",
    "Options:",
    "  --strict         exit non-zero on any flagged claim",
    "  --file <path>    scan a specific file",
    "  --stdin          read text from stdin",
    "  --recent         scan most recent evidence file (default mode)",
    "  --all-evidence   scan every .md under .opencode/evidence/",
    "  --json           emit JSON output",
    "  --help           show this help",
    "",
    "Defaults to --recent when no target flag is provided.",
    "Run with no target and no evidence dir present to see this help.",
  ].join("\n");
}

function runPython(args, input) {
  return spawnSync("python3", ["scripts/verify-before-claim-check.py", ...args], {
    input: input ?? undefined,
    cwd: repoRoot,
    encoding: "utf-8",
    stdio: ["pipe", "pipe", "pipe"],
  });
}

function main() {
  const argv = process.argv.slice(2);
  if (argv.includes("--help") || argv.includes("-h")) {
    console.log(usage());
    process.exit(0);
  }

  const isStrict = argv.includes("--strict");
  const isJson = argv.includes("--json");
  const fileIdx = argv.indexOf("--file");
  const isStdin = argv.includes("--stdin");
  const isAll = argv.includes("--all-evidence");

  const args = [];
  if (isJson) args.push("--json");
  if (isStrict) args.push("--strict");

  if (isStdin) {
    const res = runPython(["-", ...args], "");
    process.stdout.write(res.stdout);
    if (res.stderr) process.stderr.write(res.stderr);
    process.exit(res.status ?? 0);
  }

  if (fileIdx !== -1 && argv[fileIdx + 1]) {
    const file = resolve(argv[fileIdx + 1]);
    if (!existsSync(file)) {
      console.error(`verify-claim-cli: file not found: ${file}`);
      process.exit(2);
    }
    const res = runPython([file, ...args]);
    process.stdout.write(res.stdout);
    if (res.stderr) process.stderr.write(res.stderr);
    process.exit(res.status ?? 0);
  }

  const files = listMarkdownFiles(evidenceRoot);
  if (isAll) {
    if (!files.length) {
      console.log("verify-claim-cli: no .md files under .opencode/evidence/");
      process.exit(0);
    }
    let total = 0;
    let totalFlagged = 0;
    for (const f of files) {
      const res = runPython([f, ...args]);
      process.stdout.write(res.stdout + "\n");
      const m = res.stdout.match(/flagged \(no verify\):\s+(\d+)/);
      if (m) {
        total += Number(m[1]);
        totalFlagged += Number(m[1]);
      }
    }
    console.log(
      `verify-claim-cli: scanned ${files.length} files, ${total} flagged claims`,
    );
    process.exit(isStrict && totalFlagged > 0 ? 1 : 0);
  }

  // Default: most recent
  const target = pickDefaultTarget();
  if (!target) {
    console.log(usage());
    console.log(
      "\nNo .opencode/evidence/ found. Provide --file <path> or create evidence first.",
    );
    process.exit(0);
  }
  console.log(`verify-claim-cli: scanning ${target}`);
  const res = runPython([target, ...args]);
  process.stdout.write(res.stdout);
  if (res.stderr) process.stderr.write(res.stderr);
  process.exit(res.status ?? 0);
}

main();
