#!/usr/bin/env node

import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const checkOnly = process.argv.includes("--check");
let failures = 0;

function read(file) {
  return readFileSync(resolve(root, file), "utf8");
}

function write(file, content) {
  writeFileSync(resolve(root, file), `${content.trimEnd()}\n`);
}

function normalize(content) {
  return `${content.trimEnd()}\n`;
}

function parseFrontmatter(markdown) {
  if (!markdown.startsWith("---\n")) return {};
  const end = markdown.indexOf("\n---\n", 4);
  if (end === -1) return {};
  const body = markdown.slice(4, end).split("\n");
  const result = {};
  for (const line of body) {
    const match = line.match(/^([A-Za-z0-9_\-]+):\s*(.*)$/);
    if (!match) continue;
    result[match[1]] = match[2];
  }
  return result;
}

function parseArrayLiteral(content, variableName) {
  const startToken = `const ${variableName} = [`;
  const start = content.indexOf(startToken);
  if (start === -1) return [];
  let cursor = start + startToken.length;
  let depth = 1;
  let inString = false;
  let escaped = false;
  let quote = "";

  while (cursor < content.length) {
    const char = content[cursor];

    if (inString) {
      if (escaped) {
        escaped = false;
      } else if (char === "\\") {
        escaped = true;
      } else if (char === quote) {
        inString = false;
      }
      cursor += 1;
      continue;
    }

    if (char === '"' || char === "'") {
      inString = true;
      quote = char;
      cursor += 1;
      continue;
    }

    if (char === "[") depth += 1;
    if (char === "]") depth -= 1;
    cursor += 1;
    if (depth === 0) break;
  }

  const raw = content.slice(start + startToken.length, cursor - 1);
  return Array.from(raw.matchAll(/"([^"]+)"/g)).map((item) => item[1]);
}

function parsePromptGateChecks(content) {
  const checksStart = content.indexOf("const checks = [");
  if (checksStart === -1) return [];

  const lines = content.slice(checksStart).split("\n");
  const gates = [];
  let active = null;

  for (const line of lines) {
    const fileMatch = line.match(/^\s*file:\s*"([^"]+)"/);
    if (fileMatch) {
      active = { file: fileMatch[1], name: null };
      continue;
    }

    if (!active) continue;

    const nameMatch = line.match(/^\s*name:\s*"([^"]+)"/);
    if (nameMatch) {
      active.name = nameMatch[1];
      continue;
    }

    if (/^\s*},?\s*$/.test(line)) {
      if (active.file && active.name) gates.push(active);
      active = null;
    }
  }

  return gates;
}

function renderReport(title, bodyLines) {
  return [...bodyLines].join("\n");
}

function collectAgentMatrix() {
  const agentsDir = resolve(root, "agents");
  const rows = readdirSync(agentsDir)
    .filter((file) => file.endsWith(".md"))
    .sort()
    .map((file) => {
      const content = read(`agents/${file}`);
      const frontmatter = parseFrontmatter(content);
      const agent = file.replace(/\.md$/, "");
      return {
        agent,
        mode: frontmatter.mode || "unknown",
        model: frontmatter.model || "unknown",
        skills: frontmatter.skills || "none",
        description: String(frontmatter.description || "").replace(/\s+/g, " ").trim(),
      };
    });

  const lines = [
    "# Generated: Agent Matrix",
    "",
    "Generated summary of local agent metadata. This file is advisory and must not replace canonical policy in `.opencode/docs/`.",
    "",
    `- Agent count: ${rows.length}`,
    "- Source: `agents/*.md` frontmatter",
    "",
    "| Agent | Mode | Model | Skills | Description |",
    "| --- | --- | --- | --- | --- |",
    ...rows.map((row) => `| ${row.agent} | ${row.mode} | ${row.model} | ${row.skills} | ${row.description || "-"} |`),
  ];

  return renderReport("Agent Matrix", lines);
}

function collectPromptGateReport() {
  const content = read("scripts/prompt-gate-regression.mjs");
  const gates = parsePromptGateChecks(content);
  const uniqueFiles = Array.from(new Set(gates.map((gate) => gate.file))).sort();
  const promptGateDoc = read(".opencode/docs/PROMPT_GATES.md");
  const commands = Array.from(promptGateDoc.matchAll(/-\s+`([^`]+)`/g)).map((match) => match[1]);

  const lines = [
    "# Generated: Prompt Gate Report",
    "",
    "Generated inventory of deterministic prompt-gate checks. This file is advisory and must not replace canonical policy in `.opencode/docs/PROMPT_GATES.md`.",
    "",
    `- Gate count: ${gates.length}`,
    `- Unique files covered: ${uniqueFiles.length}`,
    "- Primary implementation: `scripts/prompt-gate-regression.mjs`",
    "",
    "## Commands referenced",
    ...commands.map((command) => `- \`${command}\``),
    "",
    "## Gate inventory",
    ...gates.map((gate, index) => `${index + 1}. **${gate.name}** — \`${gate.file}\``),
  ];

  return renderReport("Prompt Gate Report", lines);
}

function collectDocsIntegrityReport() {
  const content = read("scripts/docs-integrity-check.mjs");
  const canonicalDocs = parseArrayLiteral(content, "canonicalDocs");
  const generatedFiles = parseArrayLiteral(content, "generatedFiles");
  const referenceFiles = parseArrayLiteral(content, "referenceFiles");

  const lines = [
    "# Generated: Docs Integrity Report",
    "",
    "Generated summary of the docs-integrity contract. This file is advisory and must not replace canonical policy in `.opencode/docs/index.md` and related canonical docs.",
    "",
    `- Canonical docs tracked: ${canonicalDocs.length}`,
    `- Generated docs tracked: ${generatedFiles.length}`,
    `- Reference mirror files tracked: ${referenceFiles.length}`,
    "- Primary implementation: `scripts/docs-integrity-check.mjs`",
    "",
    "## Canonical docs coverage",
    ...canonicalDocs.map((file) => `- \`${file}\``),
    "",
    "## Generated docs coverage",
    ...generatedFiles.map((file) => `- \`${file}\``),
    "",
    "## Reference mirror posture coverage",
    ...referenceFiles.map((file) => `- \`${file}\``),
  ];

  return renderReport("Docs Integrity Report", lines);
}

const outputs = [
  ["docs/generated/agent-matrix.md", collectAgentMatrix()],
  ["docs/generated/prompt-gate-report.md", collectPromptGateReport()],
  ["docs/generated/docs-integrity-report.md", collectDocsIntegrityReport()],
];

for (const [file, content] of outputs) {
  const rendered = normalize(content);
  if (checkOnly) {
    const current = normalize(read(file));
    if (current !== rendered) {
      failures += 1;
      process.stderr.write(`✗ ${file} is stale\n`);
      process.stderr.write(`  - Remediation: run \`npm run docs:generate\` and commit the refreshed file.\n`);
    } else {
      process.stdout.write(`✓ ${file} is current\n`);
    }
    continue;
  }

  write(file, rendered);
}

if (checkOnly) {
  if (failures > 0) {
    process.stderr.write(`\nGenerated docs freshness check failed with ${failures} issue(s).\n`);
    process.exit(1);
  }
  process.stdout.write("\nGenerated docs freshness check passed.\n");
} else {
  process.stdout.write("Generated docs refreshed.\n");
}
