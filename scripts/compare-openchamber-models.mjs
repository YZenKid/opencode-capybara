#!/usr/bin/env node

import { existsSync, readFileSync } from "node:fs";
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

function readJson(filePath, label) {
  if (!existsSync(filePath)) {
    throw new Error(`${label} not found: ${filePath}`);
  }
  try {
    return JSON.parse(readFileSync(filePath, "utf8"));
  } catch (error) {
    throw new Error(`Failed to parse ${label}: ${filePath}\n${error.message}`);
  }
}

function parseArgs(argv) {
  const flags = {
    help: false,
    openchamberSettings: resolve(process.env.HOME || "~", ".config/openchamber/settings.json"),
    opencodeRoot: repoRoot,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--help" || arg === "-h") {
      flags.help = true;
      continue;
    }
    if (arg === "--openchamber-settings") {
      index += 1;
      if (!argv[index]) throw new Error("Missing value for --openchamber-settings");
      flags.openchamberSettings = resolve(argv[index]);
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
  log("Usage: node scripts/compare-openchamber-models.mjs [--opencode-root <path>] [--openchamber-settings <path>]");
  log("");
  log("Prints a side-by-side comparison of OpenCode model routing and OpenChamber settings.");
}

function pad(value, width) {
  const text = String(value);
  return text.length >= width ? text : `${text}${" ".repeat(width - text.length)}`;
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

  const env = parseDotEnv(resolve(flags.opencodeRoot, ".env"));
  const opencodeConfig = readJson(resolve(flags.opencodeRoot, "opencode.json"), "OpenCode config");
  const openchamber = readJson(flags.openchamberSettings, "OpenChamber settings");

  const rows = [
    [
      "defaultModel",
      env.OPENCODE_MODEL_ORCHESTRATOR || env.OPENCODE_MODEL_DEFAULT || opencodeConfig.model,
      openchamber.defaultModel || "-",
    ],
    ["defaultAgent", opencodeConfig.default_agent || "-", openchamber.defaultAgent || "-"],
    [
      "zenModel",
      env.OPENCODE_MODEL_DISCOVERY || env.OPENCODE_MODEL_IMPROVEMENT || env.OPENCODE_MODEL_DEFAULT || opencodeConfig.model,
      openchamber.zenModel || "-",
    ],
    ["homeDirectory", flags.opencodeRoot, openchamber.homeDirectory || "-"],
  ];

  const agentMap = {
    orchestrator: env.OPENCODE_MODEL_ORCHESTRATOR || "-",
    "artifact-planner": env.OPENCODE_MODEL_PLANNER || "-",
    designer: env.OPENCODE_MODEL_DESIGN || "-",
    oracle: env.OPENCODE_MODEL_REVIEW || "-",
    "quality-gate": env.OPENCODE_MODEL_REVIEW || "-",
    council: env.OPENCODE_MODEL_REVIEW || "-",
    architect: env.OPENCODE_MODEL_ADVISORY || "-",
    fixer: env.OPENCODE_MODEL_EXECUTION || "-",
    explorer: env.OPENCODE_MODEL_DISCOVERY || "-",
    librarian: env.OPENCODE_MODEL_DISCOVERY || "-",
    "skill-improver": env.OPENCODE_MODEL_IMPROVEMENT || "-",
  };

  const mirroredMap = openchamber.opencodeAgentModelMap || {};

  log("OpenCode vs OpenChamber model settings");
  log(`- OpenCode root: ${flags.opencodeRoot}`);
  log(`- OpenChamber settings: ${flags.openchamberSettings}`);
  log("");

  log(`${pad("Field", 18)} ${pad("OpenCode", 32)} OpenChamber`);
  log(`${"-".repeat(18)} ${"-".repeat(32)} ${"-".repeat(32)}`);
  for (const [field, left, right] of rows) {
    log(`${pad(field, 18)} ${pad(left, 32)} ${right}`);
  }

  log("");
  log("Per-agent model mirror (metadata only in OpenChamber)");
  log(`${pad("Agent", 18)} ${pad("OpenCode", 32)} OpenChamber mirror`);
  log(`${"-".repeat(18)} ${"-".repeat(32)} ${"-".repeat(32)}`);
  for (const [agent, model] of Object.entries(agentMap)) {
    log(`${pad(agent, 18)} ${pad(model, 32)} ${mirroredMap[agent] || "-"}`);
  }
}

main();
