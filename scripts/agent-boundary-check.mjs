#!/usr/bin/env node

import { readFileSync, readdirSync } from "node:fs";
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
    file: "agents/architect.md",
    mustInclude: ["apply_patch: deny", "task: deny"],
  },
  {
    file: "agents/council.md",
    mustInclude: ["apply_patch: deny", "task: deny"],
  },
  {
    file: "agents/system-analyst.md",
    mustInclude: ["apply_patch: deny", "task: deny", "Read-only", "do not patch source files"],
  },
  {
    file: "agents/project-manager.md",
    mustInclude: ["apply_patch: deny", "task: deny", "Read-only", "do not patch source files"],
  },
  {
    file: "agents/artifact-planner.md",
    mustInclude: [".opencode/plans/**", ".opencode/draft/**", ".opencode/evidence/**", "artifact", "app source files"],
  },
  {
    file: "agents/orchestrator.md",
    mustInclude: ["tiny", "<=1 file", "delegate", "@fixer", "@quality-gate"],
  },
];

const coreStructuralSections = [
  "## Workflow",
  "## Quality checklist",
  "## Anti-patterns",
  "## Output example"
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

for (const file of readdirSync(resolve(root, "agents"))) {
  if (!file.endsWith(".md")) continue;
  const content = readFileSync(resolve(root, "agents", file), "utf8");
  const missingSections = coreStructuralSections.filter((section) => !content.includes(section));
  if (missingSections.length > 0) {
    failures += 1;
    console.error(`✗ agents/${file}: missing structural sections`);
    for (const section of missingSections) console.error(`  - missing: ${section}`);
    console.error("  Structural requirement: All agents must include Workflow, Quality checklist, Anti-patterns, and Output example sections (9.5+ quality standard).");
  }
}

if (failures > 0) {
  console.error(`\nAgent boundary check failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nAgent boundary check passed.");
