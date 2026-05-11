#!/usr/bin/env node

import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

const checks = [
  {
    file: "agents/quality-gate.md",
    mustInclude: ["apply_patch: deny", "task: deny", "Do not use when", "Do not edit files"],
  },
  {
    file: "agents/oracle.md",
    mustInclude: ["apply_patch: deny", "task: deny"],
  },
  {
    file: "agents/explorer.md",
    mustInclude: ["apply_patch: deny", "task: deny"],
  },
  {
    file: "agents/librarian.md",
    mustInclude: ["apply_patch: deny", "task: deny"],
  },
  {
    file: "agents/accessibility-reviewer.md",
    mustInclude: ["apply_patch: deny", "task: deny"],
  },
  {
    file: "agents/motion-specialist.md",
    mustInclude: ["apply_patch: deny", "task: deny"],
  },
  {
    file: "agents/ui-system-architect.md",
    mustInclude: ["apply_patch: deny", "task: deny"],
  },
  {
    file: "agents/visual-parity-auditor.md",
    mustInclude: ["apply_patch: deny", "task: deny"],
  },
];

let failures = 0;

for (const check of checks) {
  const content = readFileSync(resolve(root, check.file), "utf8");
  const missing = check.mustInclude.filter((needle) => !content.includes(needle));
  if (missing.length > 0) {
    failures += 1;
    console.error(`✗ ${check.file}: boundary contract incomplete`);
    for (const item of missing) console.error(`  - missing: ${item}`);
    console.error("  Remediation: restore explicit read-only contract and keep implementation in @fixer or @designer.");
  } else {
    console.log(`✓ ${check.file}`);
  }
}

if (failures > 0) {
  console.error(`\nAgent boundary check failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nAgent boundary check passed.");
