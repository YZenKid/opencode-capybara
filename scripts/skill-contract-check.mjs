#!/usr/bin/env node

import { readdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const skillsDir = resolve(root, "skills");
let failures = 0;

const intentionallyMissing = new Set(["opencode-build", "opencode-general"]);
const graphifyMarkers = ["## Graphify query-first contract", "query fresh available Graphify first", "narrow query/path/explain", "direct source reading + tests/runtime still required", "missing/stale/unsupported fallback must be recorded", "tiny known-file and non-code skip only with explicit reason"];

// Core structural sections required in every skill
const coreStructuralSections = [
  "## Workflow",
  "## Quality checklist",
  "## Anti-patterns",
  "## Output example"
];

for (const entry of readdirSync(skillsDir, { withFileTypes: true })) {
  if (!entry.isDirectory() || intentionallyMissing.has(entry.name)) continue;
  const file = resolve(skillsDir, entry.name, "SKILL.md");
  try {
    readFileSync(file, "utf8");
  } catch {
    continue;
  }
  const content = readFileSync(file, "utf8");
  const activeCoreSkills = new Set(["opencode-orchestrator", "opencode-artifact-planner", "opencode-fixer", "opencode-designer", "opencode-explorer", "opencode-librarian", "opencode-oracle", "opencode-quality-gate", "opencode-architect", "opencode-visual-context-extractor"]);
  const isCoreSkill = activeCoreSkills.has(entry.name);
  const requirements = content.startsWith("---") ? ["name:", "description:"] : [];
  if (isCoreSkill) {
    requirements.push(/Reference-first|repo evidence|source strategy|source-basis|source-backed/i);
    requirements.push(/assumptions? as (assumptions|facts)|avoid turning them into fake certainty|assumptions? remain|mark assumptions?|uncertainty/i);
    requirements.push("evidence");
  }
  if (entry.name === "opencode-fixer") {
    requirements.push("TDD");
    requirements.push("Validation");
  }
  if (["opencode-architect", "opencode-explorer", "opencode-librarian", "opencode-oracle", "opencode-quality-gate", "opencode-visual-context-extractor"].includes(entry.name)) {
    requirements.push("Read-only");
  }
  const missing = requirements.filter((needle) => needle instanceof RegExp ? !needle.test(content) : !content.includes(needle));
  const missingGraphify = graphifyMarkers.filter((marker) => !content.toLowerCase().includes(marker.toLowerCase()));
  missing.push(...missingGraphify.map((marker) => `Graphify contract: ${marker}`));

  const hasTitle = content.includes("# ");
  const hasContractMarker = /^##\s+.+/m.test(content);

  if (!hasTitle) missing.push("# <title>");
  if (!hasContractMarker) missing.push("contract-section-marker");

  if (isCoreSkill) {
    // Check for core structural sections (9.5+ quality standard)
    for (const section of coreStructuralSections) {
      if (!content.includes(section)) {
        missing.push(`${section} section`);
      }
    }
  }

  if (missing.length > 0) {
    failures += 1;
    console.error(`✗ skills/${entry.name}/SKILL.md: missing contract fields`);
    for (const item of missing) console.error(`  - missing: ${item}`);
    console.error("  Remediation: add minimal frontmatter contract before expanding workflow prose.");
    if (isCoreSkill && missing.some(m => typeof m === "string" && m.includes("section"))) {
      console.error("  Structural requirement: Core skills must include Workflow, Quality checklist, Anti-patterns, and Output example sections (9.5+ quality standard).");
    }
  } else {
    console.log(`✓ skills/${entry.name}/SKILL.md`);
  }
}

const activeSkillDirs = readdirSync(skillsDir, { withFileTypes: true }).filter((entry) => {
  if (!entry.isDirectory() || intentionallyMissing.has(entry.name)) return false;
  try {
    readFileSync(resolve(skillsDir, entry.name, "SKILL.md"), "utf8");
    return true;
  } catch {
    return false;
  }
});
if (activeSkillDirs.length === 0) {
  failures += 1;
  console.error("✗ skills coverage: no active skills found");
} else {
  console.log(`✓ skills coverage: ${activeSkillDirs.length} active skills checked`);
}

if (failures > 0) {
  console.error(`\nSkill contract check failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nSkill contract check passed.");
