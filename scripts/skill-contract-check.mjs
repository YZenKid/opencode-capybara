#!/usr/bin/env node

import { readdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const skillsDir = resolve(root, "skills");
let failures = 0;

const intentionallyMissing = new Set(["opencode-build", "opencode-general"]);

for (const entry of readdirSync(skillsDir, { withFileTypes: true })) {
  if (!entry.isDirectory() || !entry.name.startsWith("opencode-") || intentionallyMissing.has(entry.name)) continue;
  const file = resolve(skillsDir, entry.name, "SKILL.md");
  const content = readFileSync(file, "utf8");
  const requirements = content.startsWith("---") ? ["name:", "description:"] : ["## Workflow", "## Output contract"];
  const missing = requirements.filter((needle) => !content.includes(needle));

  const hasTitle = content.includes("# ");
  const hasContractMarker = /^##\s+.+/m.test(content);

  if (!hasTitle) missing.push("# <title>");
  if (!hasContractMarker) missing.push("contract-section-marker");

  if (missing.length > 0) {
    failures += 1;
    console.error(`✗ skills/${entry.name}/SKILL.md: missing contract fields`);
    for (const item of missing) console.error(`  - missing: ${item}`);
    console.error("  Remediation: add minimal frontmatter contract before expanding workflow prose.");
  } else {
    console.log(`✓ skills/${entry.name}/SKILL.md`);
  }
}

if (failures > 0) {
  console.error(`\nSkill contract check failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nSkill contract check passed.");
