#!/usr/bin/env node

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const repoRoot = resolve(import.meta.dirname, "..");

function stripQuotes(value) {
  if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1);
  }
  return value;
}

function parseDotEnv(filePath) {
  if (!existsSync(filePath)) return {};

  const raw = readFileSync(filePath, "utf8");
  const env = {};
  for (const line of raw.split(/\r?\n/u)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const match = trimmed.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/u);
    if (!match) continue;
    const [, key, rawValue] = match;
    env[key] = stripQuotes(rawValue.trim());
  }
  return env;
}

function parseArgs(argv) {
  const flags = {
    check: false,
    help: false,
    opencodeRoot: repoRoot,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--check") {
      flags.check = true;
      continue;
    }
    if (arg === "--help" || arg === "-h") {
      flags.help = true;
      continue;
    }
    if (arg === "--opencode-root") {
      index += 1;
      if (!argv[index]) throw new Error("Missing value for --opencode-root");
      flags.opencodeRoot = resolve(argv[index]);
      continue;
    }
    throw new Error(`Unknown flag: ${arg}`);
  }

  return flags;
}

function log(message = "") {
  process.stdout.write(`${message}\n`);
}

function printHelp() {
  log("Usage: node scripts/sync-agent-models.mjs [--check] [--opencode-root <path>]");
  log("");
  log("Syncs literal agent frontmatter model values from .env OPENCODE_MODEL_* routing vars.");
  log("Flags:");
  log("- --check: read-only comparison, exit non-zero if any agent model is out of sync");
  log("- --opencode-root: override repo root (default: current repo root)");
}

function replaceModel(content, nextModel) {
  const updated = content.replace(/^model:\s.*$/mu, `model: ${nextModel}`);
  if (updated === content) {
    throw new Error("Missing model frontmatter line");
  }
  return updated;
}

function getCurrentModel(content) {
  const match = content.match(/^model:\s*(.+)$/mu);
  if (!match) throw new Error("Missing model frontmatter line");
  return match[1].trim();
}

function main() {
  let flags;
  try {
    flags = parseArgs(process.argv.slice(2));
  } catch (error) {
    log(String(error.message || error));
    process.exitCode = 1;
    return;
  }

  if (flags.help) {
    printHelp();
    return;
  }

  const envPath = resolve(flags.opencodeRoot, ".env");
  const env = parseDotEnv(envPath);

  const modelVars = {
    OPENCODE_MODEL_ORCHESTRATOR: env.OPENCODE_MODEL_ORCHESTRATOR,
    OPENCODE_MODEL_PLANNER: env.OPENCODE_MODEL_PLANNER,
    OPENCODE_MODEL_DESIGN: env.OPENCODE_MODEL_DESIGN,
    OPENCODE_MODEL_REVIEW: env.OPENCODE_MODEL_REVIEW,
    OPENCODE_MODEL_ADVISORY: env.OPENCODE_MODEL_ADVISORY,
    OPENCODE_MODEL_EXECUTION: env.OPENCODE_MODEL_EXECUTION,
    OPENCODE_MODEL_DISCOVERY: env.OPENCODE_MODEL_DISCOVERY,
    OPENCODE_MODEL_DOCUMENTS: env.OPENCODE_MODEL_DOCUMENTS,
    OPENCODE_MODEL_IMPROVEMENT: env.OPENCODE_MODEL_IMPROVEMENT,
  };

  const missing = Object.entries(modelVars)
    .filter(([, value]) => !value)
    .map(([key]) => key);
  if (missing.length > 0) {
    log("Agent model sync");
    log(`- Missing model env vars: ${missing.join(", ")}`);
    log("- Remediation: set every required OPENCODE_MODEL_* value in .env before syncing agent models");
    process.exitCode = 1;
    return;
  }

  const agentModelMap = [
    ["agents/orchestrator.md", env.OPENCODE_MODEL_ORCHESTRATOR],
    ["agents/artifact-planner.md", env.OPENCODE_MODEL_PLANNER],
    ["agents/designer.md", env.OPENCODE_MODEL_DESIGN],
    ["agents/visual-parity-auditor.md", env.OPENCODE_MODEL_DESIGN],
    ["agents/ui-system-architect.md", env.OPENCODE_MODEL_DESIGN],
    ["agents/oracle.md", env.OPENCODE_MODEL_REVIEW],
    ["agents/quality-gate.md", env.OPENCODE_MODEL_REVIEW],
    ["agents/council.md", env.OPENCODE_MODEL_REVIEW],
    ["agents/product-architect.md", env.OPENCODE_MODEL_ADVISORY],
    ["agents/saas-architect.md", env.OPENCODE_MODEL_ADVISORY],
    ["agents/ai-systems-architect.md", env.OPENCODE_MODEL_ADVISORY],
    ["agents/security-privacy-reviewer.md", env.OPENCODE_MODEL_ADVISORY],
    ["agents/release-engineer.md", env.OPENCODE_MODEL_ADVISORY],
    ["agents/mobile-architect.md", env.OPENCODE_MODEL_ADVISORY],
    ["agents/fixer.md", env.OPENCODE_MODEL_EXECUTION],
    ["agents/explorer.md", env.OPENCODE_MODEL_DISCOVERY],
    ["agents/librarian.md", env.OPENCODE_MODEL_DISCOVERY],
    ["agents/motion-specialist.md", env.OPENCODE_MODEL_DISCOVERY],
    ["agents/accessibility-reviewer.md", env.OPENCODE_MODEL_DISCOVERY],
    ["agents/document-specialist.md", env.OPENCODE_MODEL_DOCUMENTS],
    ["agents/skill-improver.md", env.OPENCODE_MODEL_IMPROVEMENT],
  ];

  const changes = [];
  for (const [relativePath, nextModel] of agentModelMap) {
    const filePath = resolve(flags.opencodeRoot, relativePath);
    if (!existsSync(filePath)) {
      throw new Error(`Agent file not found: ${relativePath}`);
    }
    const current = readFileSync(filePath, "utf8");
    const currentModel = getCurrentModel(current);
    if (currentModel !== nextModel) {
      changes.push({ relativePath, currentModel, nextModel, nextContent: replaceModel(current, nextModel) });
    }
  }

  log("Agent model sync");
  log(`- .env path: ${envPath}`);

  if (changes.length === 0) {
    log("- Status: agent models already in sync");
    return;
  }

  for (const change of changes) {
    log(`- ${change.relativePath}: ${change.currentModel} -> ${change.nextModel}`);
  }

  if (flags.check) {
    log("- Check only: no files changed");
    process.exitCode = 1;
    return;
  }

  for (const change of changes) {
    writeFileSync(resolve(flags.opencodeRoot, change.relativePath), change.nextContent);
  }
  log("- Status: updated");
}

main();
