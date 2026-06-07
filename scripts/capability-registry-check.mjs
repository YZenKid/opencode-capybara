#!/usr/bin/env node

import { existsSync, readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const registry = readJson(".opencode/capabilities/registry.json");
const config = readJson("opencode.json");
let failures = 0;

function readJson(file) {
  return JSON.parse(readFileSync(resolve(root, file), "utf8"));
}

function fail(message) {
  failures += 1;
  console.error(`✗ ${message}`);
}

function pass(message) {
  console.log(`✓ ${message}`);
}

function requireGovernance(kind, item) {
  for (const field of ["owner_lane", "fallback", "source"]) {
    if (!item[field] || typeof item[field] !== "string") fail(`${kind} ${item.name}: missing ${field}`);
  }
  for (const field of ["risk", "evidence"]) {
    if (!Array.isArray(item[field]) || item[field].length === 0) fail(`${kind} ${item.name}: missing ${field}`);
  }
}

function extractFrontmatterList(content, key) {
  const match = content.match(new RegExp(`^${key}:\\n((?:  - .+\\n)+)`, "m"));
  if (!match) return [];
  return match[1].split("\n").map((line) => line.trim().replace(/^-\s*/, "")).filter(Boolean);
}

const activeAgents = readdirSync(resolve(root, "agents"))
  .filter((file) => file.endsWith(".md"))
  .map((file) => file.replace(/\.md$/, ""))
  .filter((name) => !["build", "general"].includes(name))
  .sort();
const activeSkills = activeAgents.map((agent) => `opencode-${agent}`);
const configuredMcp = Object.entries(config.mcp ?? {}).filter(([, value]) => value.enabled !== false).map(([name]) => name).sort();

for (const agent of activeAgents) {
  const row = registry.agents.find((item) => item.name === agent && item.status === "active");
  if (!row) fail(`active agent missing from registry: ${agent}`);
  else {
    requireGovernance("agent", row);
    const content = readFileSync(resolve(root, `agents/${agent}.md`), "utf8");
    const skills = extractFrontmatterList(content, "skills");
    if (row.skill && !skills.includes(row.skill)) fail(`agent ${agent}: registry skill ${row.skill} not in frontmatter`);
    if (row.skill && row.skill !== `opencode-${agent}`) fail(`agent ${agent}: registry skill must preserve 1:1 mapping, found ${row.skill}`);
  }
}
pass("active agents checked against registry");

for (const skill of activeSkills) {
  const row = registry.skills.find((item) => item.name === skill && item.status === "active");
  if (!row) fail(`active skill missing from registry: ${skill}`);
  else requireGovernance("skill", row);
  if (!existsSync(resolve(root, `skills/${skill}/SKILL.md`))) fail(`active skill file missing: skills/${skill}/SKILL.md`);
}
pass("active skills checked against registry");

for (const name of configuredMcp) {
  const row = registry.mcp.find((item) => item.name === name && item.status === "configured");
  if (!row) fail(`configured MCP missing from registry: ${name}`);
  else {
    requireGovernance("mcp", row);
    for (const field of ["transport", "auth", "data_egress", "write_capability", "allowed_lanes", "denied_lanes", "evidence_required", "secret_surfaces"]) {
      if (row[field] === undefined || row[field] === null || (Array.isArray(row[field]) && row[field].length === 0 && field !== "secret_surfaces")) {
        fail(`mcp ${name}: missing ${field}`);
      }
    }
    if (row.transport !== config.mcp[name].type) fail(`mcp ${name}: transport ${row.transport} != opencode.json type ${config.mcp[name].type}`);
  }
}
pass("configured MCP checked against registry");

for (const item of [...registry.agents, ...registry.skills, ...registry.mcp]) {
  if (item.status === "external-comparator") fail(`${item.name}: external comparator listed as active capability`);
}
for (const comparator of registry.external_comparators) {
  if (comparator.status !== "external-comparator") fail(`external comparator ${comparator.name}: wrong status`);
  if (!["adopt", "adapt", "reject", "defer"].includes(comparator.decision)) fail(`external comparator ${comparator.name}: invalid decision`);
}
pass("external comparators are not active capabilities");

if (failures > 0) {
  console.error(`\nCapability registry check failed with ${failures} issue(s).`);
  process.exit(1);
}
console.log("\nCapability registry check passed.");
