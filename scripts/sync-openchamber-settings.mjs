#!/usr/bin/env node

import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

const repoRoot = resolve(import.meta.dirname, "..");

function stripQuotes(value) {
  if (
    (value.startsWith('"') && value.endsWith('"')) ||
    (value.startsWith("'") && value.endsWith("'"))
  ) {
    return value.slice(1, -1);
  }
  return value;
}

function parseDotEnv(filePath) {
  if (!existsSync(filePath)) {
    return {};
  }

  const raw = readFileSync(filePath, "utf8");
  const env = {};

  for (const line of raw.split(/\r?\n/u)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }

    const match = trimmed.match(/^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/u);
    if (!match) {
      continue;
    }

    const [, key, rawValue] = match;
    env[key] = stripQuotes(rawValue.trim());
  }

  return env;
}

function parseArgs(argv) {
  const flags = {
    check: false,
    help: false,
    openchamberSettings: resolve(process.env.HOME || "~", ".config/openchamber/settings.json"),
    opencodeRoot: repoRoot,
    seedApprovedDirectories: false,
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
    if (arg === "--seed-approved-directories") {
      flags.seedApprovedDirectories = true;
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

function printHelp() {
  log("Usage: node scripts/sync-openchamber-settings.mjs [--check] [--seed-approved-directories] [--opencode-root <path>] [--openchamber-settings <path>]");
  log("");
  log("Syncs OpenChamber settings with the current OpenCode config.");
  log("Fields synced:");
  log("- homeDirectory <- OpenCode config root");
  log("- defaultModel <- OPENCODE_MODEL_ORCHESTRATOR for new OpenChamber sessions");
  log("- defaultAgent <- opencode.json default_agent");
  log("- zenModel <- OPENCODE_MODEL_DISCOVERY or OPENCODE_MODEL_IMPROVEMENT or opencode.json model");
  log("- opencodeAgentModelMap <- metadata mirror of OpenCode per-agent model routing");
  log("");
  log("Flags:");
  log("- --check: read-only comparison, exit non-zero if out of sync");
  log("- --seed-approved-directories: append OpenCode root to approvedDirectories if missing");
  log("- --opencode-root: override OpenCode config root (default: current repo root)");
  log("- --openchamber-settings: override OpenChamber settings path");
}

function resolveEnvTemplate(value, env) {
  if (typeof value !== "string") return value;
  const match = value.match(/^\{env:([A-Za-z_][A-Za-z0-9_]*)\}$/u);
  if (!match) return value;
  return env[match[1]] || value;
}

function buildOpencodeAgentModelMap(env) {
  return {
    orchestrator: env.OPENCODE_MODEL_ORCHESTRATOR,
    "artifact-planner": env.OPENCODE_MODEL_PLANNER,
    designer: env.OPENCODE_MODEL_DESIGN,
    oracle: env.OPENCODE_MODEL_REVIEW,
    "quality-gate": env.OPENCODE_MODEL_REVIEW,
    council: env.OPENCODE_MODEL_REVIEW,
    architect: env.OPENCODE_MODEL_ADVISORY,
    fixer: env.OPENCODE_MODEL_EXECUTION,
    explorer: env.OPENCODE_MODEL_DISCOVERY,
    librarian: env.OPENCODE_MODEL_DISCOVERY,
    "skill-improver": env.OPENCODE_MODEL_IMPROVEMENT,
  };
}

function stableStringify(value) {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    return `[${value.map((item) => stableStringify(item)).join(",")}]`;
  }
  const entries = Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`);
  return `{${entries.join(",")}}`;
}

function valuesEqual(left, right) {
  if (left && right && typeof left === "object" && typeof right === "object") {
    return stableStringify(left) === stableStringify(right);
  }
  return left === right;
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

  const opencodeJsonPath = resolve(flags.opencodeRoot, "opencode.json");
  const opencodeEnvPath = resolve(flags.opencodeRoot, ".env");
  const openchamberSettingsPath = flags.openchamberSettings;

  const opencodeConfig = readJson(opencodeJsonPath, "OpenCode config");
  const opencodeEnv = parseDotEnv(opencodeEnvPath);
  const openchamberSettings = readJson(openchamberSettingsPath, "OpenChamber settings");

  const zenModel =
    opencodeEnv.OPENCODE_MODEL_DISCOVERY ||
    opencodeEnv.OPENCODE_MODEL_IMPROVEMENT ||
    opencodeEnv.OPENCODE_MODEL_DEFAULT ||
    resolveEnvTemplate(opencodeConfig.model, opencodeEnv);

  const defaultModel =
    opencodeEnv.OPENCODE_MODEL_ORCHESTRATOR ||
    opencodeEnv.OPENCODE_MODEL_DEFAULT ||
    resolveEnvTemplate(opencodeConfig.model, opencodeEnv);

  const opencodeAgentModelMap = buildOpencodeAgentModelMap(opencodeEnv);

  const desired = {
    homeDirectory: flags.opencodeRoot,
    defaultModel,
    defaultAgent: opencodeConfig.default_agent,
    zenModel,
    opencodeAgentModelMap,
  };

  const changes = [];
  for (const [key, nextValue] of Object.entries(desired)) {
    if (typeof nextValue === "undefined") {
      continue;
    }
    const currentValue = openchamberSettings[key];
    if (!valuesEqual(currentValue, nextValue)) {
      changes.push({ key, currentValue, nextValue });
    }
  }

  log("OpenChamber sync");
  log(`- OpenCode root: ${flags.opencodeRoot}`);
  log(`- OpenCode config: ${opencodeJsonPath}`);
  log(`- OpenChamber settings: ${openchamberSettingsPath}`);

  if (changes.length === 0) {
    log("- Status: already in sync");
    return;
  }

  for (const change of changes) {
    log(`- ${change.key}: ${JSON.stringify(change.currentValue)} -> ${JSON.stringify(change.nextValue)}`);
  }

  let approvedDirectoriesNeedsSeed = false;
  if (flags.seedApprovedDirectories) {
    const approvedDirectories = Array.isArray(openchamberSettings.approvedDirectories)
      ? openchamberSettings.approvedDirectories
      : [];
    approvedDirectoriesNeedsSeed = !approvedDirectories.includes(flags.opencodeRoot);
    if (approvedDirectoriesNeedsSeed) {
      log(`- approvedDirectories: append ${JSON.stringify(flags.opencodeRoot)}`);
    }
  }

  if (flags.check) {
    log("- Check only: no files changed");
    if (changes.length > 0 || approvedDirectoriesNeedsSeed) {
      process.exitCode = 1;
    }
    return;
  }

  const nextSettings = { ...openchamberSettings };
  for (const change of changes) {
    nextSettings[change.key] = change.nextValue;
  }

  if (flags.seedApprovedDirectories) {
    const approvedDirectories = Array.isArray(nextSettings.approvedDirectories)
      ? [...nextSettings.approvedDirectories]
      : [];
    if (!approvedDirectories.includes(flags.opencodeRoot)) {
      approvedDirectories.push(flags.opencodeRoot);
      nextSettings.approvedDirectories = approvedDirectories;
    }
  }

  if (!existsSync(dirname(openchamberSettingsPath))) {
    throw new Error(`OpenChamber config directory not found: ${dirname(openchamberSettingsPath)}`);
  }

  writeFileSync(openchamberSettingsPath, `${JSON.stringify(nextSettings, null, 2)}\n`);
  log("- Status: updated");
}

main();
