#!/usr/bin/env node

import { readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

const graphifyPolicyFiles = [
  "AGENTS.md",
  ".opencode/docs/MCP.md",
  ".opencode/docs/TOOL_USAGE.md",
  ".opencode/docs/AGENT_TOOL_ACCESS.md",
  ".opencode/docs/SKILLS.md",
  "skills/graphify-discovery/SKILL.md",
];
const graphifyMarkers = ["## Graphify query-first contract", "query fresh available Graphify first", "narrow query/path/explain", "direct source reading + tests/runtime still required", "missing/stale/unsupported fallback must be recorded", "tiny known-file and non-code skip only with explicit reason"];

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
  const missingGraphify = graphifyMarkers.filter((marker) => !content.toLowerCase().includes(marker.toLowerCase()));
  if (missingGraphify.length > 0) {
    failures += 1;
    console.error(`✗ agents/${file}: missing per-file Graphify query-first contract`);
    for (const marker of missingGraphify) console.error(`  - missing: ${marker}`);
  }
  if (missingSections.length > 0) {
    failures += 1;
    console.error(`✗ agents/${file}: missing structural sections`);
    for (const section of missingSections) console.error(`  - missing: ${section}`);
    console.error("  Structural requirement: All agents must include Workflow, Quality checklist, Anti-patterns, and Output example sections (9.5+ quality standard).");
  }
}

for (const file of graphifyPolicyFiles) {
  const content = readFileSync(resolve(root, file), "utf8");
  const missing = graphifyMarkers.filter((marker) => !content.toLowerCase().includes(marker.toLowerCase()));
  if (missing.length > 0) {
    failures += 1;
    console.error(`✗ ${file}: centralized Graphify policy incomplete`);
    for (const item of missing) console.error(`  - missing: ${item}`);
  }
}

const agentFiles = readdirSync(resolve(root, "agents")).filter((file) => file.endsWith(".md"));
if (agentFiles.length === 0) {
  failures += 1;
  console.error("✗ agents coverage: no local agent files found");
} else if (!graphifyMarkers.every((marker) => readFileSync(resolve(root, "AGENTS.md"), "utf8").toLowerCase().includes(marker.toLowerCase()))) {
  failures += 1;
  console.error("✗ agents coverage: AGENTS.md lacks mandatory Graphify inheritance markers");
} else {
  console.log(`✓ agents coverage: ${agentFiles.length} active agent files inherit mandatory Graphify policy via AGENTS.md`);
}

if (failures > 0) {
  console.error(`\nAgent boundary check failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nAgent boundary check passed.");
