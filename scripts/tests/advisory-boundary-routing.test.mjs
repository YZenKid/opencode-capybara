#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const fixture = JSON.parse(readFileSync(resolve(root, "scripts/evals/fixtures/advisory-boundary-routing.json"), "utf8"));
const routingDoc = readFileSync(resolve(root, ".opencode/docs/AGENT_ROUTING.md"), "utf8");
const skillsDoc = readFileSync(resolve(root, ".opencode/docs/SKILLS.md"), "utf8");

const expectationMap = {
  "@architect": ["@architect", "architecture boundaries"],
  "@oracle": ["@oracle", "deep review", "simplification"],
  "@artifact-planner": ["@artifact-planner", "requirements", "acceptance criteria"],
  "@artifact-planner": ["@artifact-planner", "milestones", "release checklist"],
  "@fixer": ["@fixer", "small vertical slice"],
  "@artifact-planner": ["@artifact-planner", "multi-phase", "ambiguous"],
};

let failures = 0;
for (const f of fixture.fixtures) {
  const expectedSignals = expectationMap[f.expected_lane] || [f.expected_lane];
  const haystack = `${routingDoc}\n${skillsDoc}`;
  const pass = expectedSignals.every((s) => haystack.includes(s));
  if (!pass) {
    console.error(`✗ ${f.id}: expected routing signals for ${f.expected_lane} missing`);
    failures += 1;
  } else {
    console.log(`✓ ${f.id}: expected routing signals for ${f.expected_lane} present`);
  }
  if (f.id === "fullstack-forbidden-catchall") {
    const guard = haystack.includes("@fixer` is never catch-all/default") || haystack.includes("@fixer must not become catch-all");
    if (!guard) {
      console.error(`✗ ${f.id}: missing explicit catch-all guard for @fixer`);
      failures += 1;
    } else {
      console.log(`✓ ${f.id}: explicit catch-all guard present`);
    }
  }
}

if (failures > 0) {
  console.error(`\nAdvisory boundary routing failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nAdvisory boundary routing passed.");
