#!/usr/bin/env node

import { spawnSync } from "node:child_process";

function parseArgs(argv) {
  const flags = { check: false, force: false, skipCaveman: false, help: false };
  for (const arg of argv) {
    if (arg === "--check") flags.check = true;
    else if (arg === "--force") flags.force = true;
    else if (arg === "--skip-caveman") flags.skipCaveman = true;
    else if (arg === "--help" || arg === "-h") flags.help = true;
    else throw new Error(`Unknown flag: ${arg}`);
  }
  return flags;
}

function run(command, args, options = {}) {
  return spawnSync(command, args, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], ...options });
}

function printSection(title) { process.stdout.write(`\n== ${title} ==\n`); }
function printLine(message = "") { process.stdout.write(`${message}\n`); }
function printResult(label, status, detail) {
  const prefix = status === "ok" ? "[ok]" : status === "warn" ? "[warn]" : "[action]";
  printLine(`${prefix} ${label}${detail ? ` — ${detail}` : ""}`);
}
function printHelp() {
  printLine("Usage: node scripts/setup-dev-tools.mjs [--check] [--force] [--skip-caveman] [--help]");
  printLine("");
  printLine("Explicitly installs or checks optional support tooling for this repo.");
  printLine("- --check: read-only verification only");
  printLine("- --force: reinstall/setup even if tools already exist");
  printLine("- --skip-caveman: skip Caveman setup/check");
}

function installCaveman({ check, force }) {
  printSection("Caveman");
  const targetCommand = "npx -y skills add JuliusBrussee/caveman -a opencode";
  printLine("Caveman is optional support for readability and concise communication.");
  if (check) {
    const result = run("npx", ["-y", "skills", "--help"]);
    printResult("Caveman", result.status === 0 ? "ok" : "warn", result.status === 0 ? "skills CLI available" : "skills CLI not verified");
    printLine(`  Remediation command: ${targetCommand}`);
    return result.status === 0;
  }
  printLine(`Running: ${targetCommand}`);
  const result = spawnSync("npx", ["-y", "skills", "add", "JuliusBrussee/caveman", "-a", "opencode"], { encoding: "utf8", stdio: "inherit" });
  if (result.status !== 0) {
    printResult("Caveman", "warn", "setup command failed");
    printLine(`  Remediation: rerun ${targetCommand}`);
    return false;
  }
  printResult("Caveman", "ok", "installed for opencode");
  return true;
}

function main() {
  let flags;
  try { flags = parseArgs(process.argv.slice(2)); } catch (error) { printLine(String(error.message || error)); process.exitCode = 1; return; }
  if (flags.help) { printHelp(); return; }
  printLine("opencode-capybara tool setup");
  printLine(flags.check ? "Mode: check only" : "Mode: explicit setup");
  let ok = true;
  if (!flags.skipCaveman) ok = installCaveman(flags) && ok;
  else { printSection("Caveman"); printResult("Caveman", "warn", "skipped by request"); }
  printLine("");
  printLine("Restart OpenCode after installing or checking tools so the new setup is visible in a fresh session.");
  if (!ok) process.exitCode = 1;
}

main();
