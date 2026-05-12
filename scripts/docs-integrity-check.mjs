#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

const canonicalDocs = [
  ".opencode/docs/index.md",
  ".opencode/docs/ARCHITECTURE.md",
  ".opencode/docs/AGENT_ROUTING.md",
  ".opencode/docs/AGENT_LEGIBILITY.md",
  ".opencode/docs/QUALITY.md",
  ".opencode/docs/QUALITY_SCORE.md",
  ".opencode/docs/SECURITY.md",
  ".opencode/docs/PROMPT_GATES.md",
  ".opencode/docs/SKILLS.md",
  ".opencode/docs/MCP.md",
  ".opencode/docs/TOOL_USAGE.md",
  ".opencode/docs/AGENT_TOOL_ACCESS.md",
  ".opencode/docs/EVALS.md",
  ".opencode/docs/GOLDEN_PRINCIPLES.md",
  ".opencode/docs/DECISIONS.md",
  ".opencode/docs/RELEASE.md",
  ".opencode/docs/GC_WORKFLOW.md",
];

let failures = 0;

function abs(file) {
  return resolve(root, file);
}

function read(file) {
  const path = abs(file);
  if (!existsSync(path)) {
    failures += 1;
    console.error(`✗ missing required file: ${file}`);
    return null;
  }
  return readFileSync(path, "utf8");
}

function checkCanonicalFilesExist() {
  for (const file of canonicalDocs) {
    const content = read(file);
    if (content !== null) {
      console.log(`✓ ${file}`);
    }
  }
}

function checkIndexCoverage() {
  const index = read(".opencode/docs/index.md");
  if (index === null) return;

  const missing = canonicalDocs.filter((file) => file !== ".opencode/docs/index.md").filter((file) => !index.includes(file.replace(".opencode/docs/", "./")) && !index.includes(file.replace(".opencode/docs/", "")));

  if (missing.length > 0) {
    failures += 1;
    console.error("✗ .opencode/docs/index.md is missing canonical doc links:");
    for (const item of missing) console.error(`  - ${item}`);
  } else {
    console.log("✓ .opencode/docs/index.md canonical coverage");
  }
}

function checkAgentsPointers() {
  const agents = read("AGENTS.md");
  if (agents === null) return;

  const required = [
    ".opencode/docs/AGENT_ROUTING.md",
    ".opencode/docs/ARCHITECTURE.md",
    ".opencode/docs/QUALITY.md",
    ".opencode/docs/EVALS.md",
    ".opencode/docs/SECURITY.md",
    ".opencode/docs/PROMPT_GATES.md",
    ".opencode/docs/SKILLS.md",
    ".opencode/docs/GOLDEN_PRINCIPLES.md",
    ".opencode/docs/AGENT_LEGIBILITY.md",
    ".opencode/docs/DECISIONS.md",
    ".opencode/docs/RELEASE.md",
    ".opencode/docs/QUALITY_SCORE.md",
    ".opencode/docs/GC_WORKFLOW.md",
  ];

  const missing = required.filter((needle) => !agents.includes(needle));
  if (missing.length > 0) {
    failures += 1;
    console.error("✗ AGENTS.md is missing required docs pointers:");
    for (const item of missing) console.error(`  - ${item}`);
  } else {
    console.log("✓ AGENTS.md docs pointers");
  }
}

function checkGeneratedDocsLabel() {
  const generatedFiles = [
    "docs/generated/agent-matrix.md",
    "docs/generated/prompt-gate-report.md",
    "docs/generated/docs-integrity-report.md",
  ];

  for (const file of generatedFiles) {
    const content = read(file);
    if (content === null) continue;
    if (!content.includes("Generated")) {
      failures += 1;
      console.error(`✗ ${file}: missing generated marker`);
    } else {
      console.log(`✓ ${file} generated marker`);
    }
  }
}

function checkReferenceMirrorPosture() {
  const referenceFiles = [
    "docs/index.md",
    "docs/ARCHITECTURE.md",
    "docs/DECISIONS.md",
    "docs/QUALITY.md",
    "docs/QUALITY_SCORE.md",
    "docs/references/opencode.md",
    "docs/references/mcp.md",
  ];

  const forbiddenClaims = [
    "`docs/` is the repository system of record",
    "`docs/` is the durable policy/reference layer",
    "Prefer `docs/MCP.md` and `opencode.json` as the canonical sources.",
    "canonical docs in `docs/`",
  ];

  for (const file of referenceFiles) {
    const content = read(file);
    if (content === null) continue;

    const hits = forbiddenClaims.filter((needle) => content.includes(needle));
    if (hits.length > 0) {
      failures += 1;
      console.error(`✗ ${file}: reference-only mirror still claims canonical authority`);
      for (const item of hits) console.error(`  - forbidden: ${item}`);
    } else {
      console.log(`✓ ${file} reference-only posture`);
    }
  }
}

function checkMirrorPolicyBloat() {
  const agents = read("AGENTS.md");
  const readme = read("README.md");
  if (agents === null || readme === null) return;

  const forbiddenInAgents = [
    "Page-by-page UX blueprint",
    "Section-level visual specification",
    "Motion system",
    "Interaction and state design",
    "Validation evidence",
  ].filter((needle) => agents.includes(needle));

  if (forbiddenInAgents.length > 0) {
    failures += 1;
    console.error("✗ AGENTS.md has absorbed long-form policy that should live in docs:");
    for (const item of forbiddenInAgents) console.error(`  - ${item}`);
  } else {
    console.log("✓ AGENTS.md remains map-like and does not absorb long-form design policy");
  }

  const forbiddenInReadme = [
    "Page-by-page UX blueprint",
    "Section-level visual specification",
    "Interaction and state design",
  ].filter((needle) => readme.includes(needle));

  if (forbiddenInReadme.length > 0) {
    failures += 1;
    console.error("✗ README.md mirrors long-form policy that should remain canonical in docs:");
    for (const item of forbiddenInReadme) console.error(`  - ${item}`);
  } else {
    console.log("✓ README.md stays onboarding-oriented and does not mirror long-form policy");
  }
}

function checkDecisionAdjacency() {
  try {
    const changed = execFileSync("git", ["diff", "--name-only", "HEAD"], {
      cwd: root,
      encoding: "utf8",
    })
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);

    const guarded = changed.filter((file) =>
      file === "AGENTS.md" ||
      file === "README.md" ||
      file.startsWith(".opencode/docs/") ||
      file.startsWith("scripts/")
    );

    if (guarded.length === 0) {
      console.log("✓ no guarded docs/scripts changes requiring decision adjacency");
      return;
    }

    const decisions = read(".opencode/docs/DECISIONS.md");
    if (decisions === null) return;
    const hasDecisionHeading = /##\s+\d{4}-\d{2}-\d{2}\s+—\s+/.test(decisions);
    if (!hasDecisionHeading) {
      failures += 1;
      console.error("✗ .opencode/docs/DECISIONS.md does not reflect the active guarded docs/scripts changes");
      console.error("  - Remediation: add or update a dated decision entry when docs/scripts policy changes materially.");
    } else {
      console.log("✓ .opencode/docs/DECISIONS.md provides decision adjacency for current guarded changes");
    }
  } catch {
    console.log("! skipped decision adjacency git-diff check (git context unavailable)");
  }
}

checkCanonicalFilesExist();
checkIndexCoverage();
checkAgentsPointers();
checkGeneratedDocsLabel();
checkReferenceMirrorPosture();
checkMirrorPolicyBloat();
checkDecisionAdjacency();

if (failures > 0) {
  console.error(`\nDocs integrity check failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nDocs integrity check passed.");
