#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function run(command, args, options = {}) {
  return spawnSync(command, args, {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    ...options,
  });
}

function log(message = "") {
  process.stdout.write(`${message}\n`);
}

function section(title) {
  log(`\n== ${title} ==`);
}

function status(label, state, detail = "") {
  const prefix = state === "pass" ? "[pass]" : state === "warn" ? "[warn]" : "[fail]";
  log(`${prefix} ${label}${detail ? ` — ${detail}` : ""}`);
}

function remediation(command) {
  log(`  Remediation: ${command}`);
}

function checkNode() {
  section("Node runtime");
  log("Read-only environment validation only.");
  const result = run("node", ["--version"]);
  if (result.status === 0) {
    status("Node", "pass", result.stdout.trim());
    return true;
  }
  status("Node", "fail", "not available");
  remediation("install Node.js, then rerun `npm run doctor`");
  return false;
}

function checkNpm() {
  const result = run("npm", ["--version"]);
  if (result.status === 0) {
    status("npm", "pass", result.stdout.trim());
    return true;
  }
  status("npm", "fail", "not available");
  remediation("install npm or a Node.js distribution that includes it");
  return false;
}

function checkRtk() {
  section("RTK");
  log("Checking rtk --version without modifying anything.");
  const result = run("rtk", ["--version"]);
  if (result.status === 0) {
    status("RTK", "pass", result.stdout.trim());
    return true;
  }
  status("RTK", "fail", "missing or not on PATH");
  remediation("run `npm run setup:tools` or install RTK manually, then rerun `npm run doctor`");
  return false;
}

function checkSkills() {
  const result = run("npx", ["-y", "skills", "--help"]);
  if (result.status === 0) {
    status("npx skills", "pass", "available");
    return true;
  }
  status("npx skills", "warn", "could not verify");
  remediation("run `npm run setup:tools -- --skip-rtk` and confirm the skills CLI is available, or rerun `npm run setup:tools`");
  return false;
}

function checkRepoFiles() {
  section("Repository contract");
  const files = [
    ["package.json", true],
    ["README.md", true],
    ["AGENTS.md", true],
    [".opencode/docs/index.md", true],
    [".opencode/docs/AGENT_ROUTING.md", true],
    [".opencode/docs/QUALITY.md", true],
    [".opencode/docs/EVALS.md", true],
    ["scripts/prompt-gate-regression.mjs", true],
    ["scripts/docs-integrity-check.mjs", true],
    ["scripts/sync-agent-models.mjs", true],
    ["scripts/setup-dev-tools.mjs", true],
    ["scripts/doctor.mjs", true],
  ];

  let ok = true;
  for (const [relativePath, required] of files) {
    const path = resolve(root, relativePath);
    const present = existsSync(path);
    if (present) {
      status(relativePath, "pass", "present");
    } else if (required) {
      status(relativePath, "fail", "missing");
      remediation(`restore ${relativePath}`);
      ok = false;
    }
  }

  return ok;
}

function checkPackageLifecycle() {
  section("Package lifecycle safety");
  const pkg = JSON.parse(readFileSync(resolve(root, "package.json"), "utf8"));
  const scripts = pkg.scripts || {};
  const unsafe = ["postinstall", "preinstall", "prepare"].filter((name) => name in scripts);
  if (unsafe.length === 0) {
    status("package lifecycle", "pass", "no unsafe install hooks");
    return true;
  }
  status("package lifecycle", "fail", `unsafe hooks present: ${unsafe.join(", ")}`);
  remediation("remove postinstall/preinstall/prepare install hooks from package.json");
  return false;
}

function checkDocsPolicy() {
  section("Docs and policy");
  const agents = readFileSync(resolve(root, "AGENTS.md"), "utf8");
  const readme = readFileSync(resolve(root, "README.md"), "utf8");
  const docsIndex = readFileSync(resolve(root, ".opencode/docs/index.md"), "utf8");
  const routing = readFileSync(resolve(root, ".opencode/docs/AGENT_ROUTING.md"), "utf8");

  let ok = true;
  const agentsNeedles = [
    "RTK may be installed by explicit setup",
    "OpenCode auto-rewrite/prefix remains opt-in",
    ".opencode/docs/AGENT_ROUTING.md",
    ".opencode/docs/QUALITY.md",
    ".opencode/docs/EVALS.md",
  ];
  for (const needle of agentsNeedles) {
    if (agents.includes(needle)) {
      status(`AGENTS.md: ${needle}`, "pass");
    } else {
      status(`AGENTS.md: ${needle}`, "fail", "missing");
      remediation("update AGENTS.md RTK policy wording to preserve explicit opt-in behavior");
      ok = false;
    }
  }

  const readmeNeedles = ["npm run setup:tools", "npm run doctor", "RTK", "Caveman"];
  for (const needle of readmeNeedles) {
    if (readme.includes(needle)) {
      status(`README.md: ${needle}`, "pass");
    } else {
      status(`README.md: ${needle}`, "fail", "missing");
      remediation("update README.md quick start and RTK/Caveman section");
      ok = false;
    }
  }

  const docsIndexNeedles = [
    "system of record",
    "ARCHITECTURE.md",
    "AGENT_ROUTING.md",
    "QUALITY.md",
    "EVALS.md",
    "GOLDEN_PRINCIPLES.md",
  ];
  for (const needle of docsIndexNeedles) {
    if (docsIndex.includes(needle)) {
      status(`.opencode/docs/index.md: ${needle}`, "pass");
    } else {
      status(`.opencode/docs/index.md: ${needle}`, "fail", "missing");
      remediation("update .opencode/docs/index.md to reflect the canonical documentation map");
      ok = false;
    }
  }

  const routingNeedles = [
    "## Direct-work thresholds for `@orchestrator`",
    "## Routing anti-patterns (and remediation)",
    "## Compact routing quality checklist",
  ];
  for (const needle of routingNeedles) {
    if (routing.includes(needle)) {
      status(`.opencode/docs/AGENT_ROUTING.md: ${needle}`, "pass");
    } else {
      status(`.opencode/docs/AGENT_ROUTING.md: ${needle}`, "fail", "missing");
      remediation("update .opencode/docs/AGENT_ROUTING.md orchestrator thresholds/rubric sections");
      ok = false;
    }
  }

  return ok;
}

function checkEnvWarning() {
  section("Environment file");
  const envPath = resolve(root, ".env");
  if (existsSync(envPath)) {
    status(".env", "warn", "present");
    remediation("do not commit .env; keep secrets local only");
    return true;
  }
  status(".env", "warn", "not present");
  remediation("copy .env.example to .env if you need local credentials");
  return true;
}

function checkOpenChamberSync() {
  section("OpenChamber sync");
  const result = run("node", ["scripts/sync-openchamber-settings.mjs", "--check", "--seed-approved-directories"], { cwd: root });
  if (result.status === 0) {
    status("OpenChamber settings", "pass", "in sync with OpenCode");
    return true;
  }

  const detail = result.stdout.trim() || result.stderr.trim() || "out of sync";
  status("OpenChamber settings", "warn", detail.split("\n").join(" | "));
  remediation("run `npm run sync:openchamber` to align OpenChamber with OpenCode");
  return true;
}

function checkAgentModelSync() {
  section("Agent model sync");
  const result = run("node", ["scripts/sync-agent-models.mjs", "--check"], { cwd: root });
  if (result.status === 0) {
    status("Agent models", "pass", "in sync with .env routing vars");
    return true;
  }

  const detail = result.stdout.trim() || result.stderr.trim() || "out of sync";
  status("Agent models", "warn", detail.split("\n").join(" | "));
  remediation("run `npm run sync:agent-models` after updating OPENCODE_MODEL_* values in .env");
  return true;
}

function checkDefaultModelRouting() {
  section("Default model routing");
  const opencode = JSON.parse(readFileSync(resolve(root, "opencode.json"), "utf8"));
  if (opencode.model === "{env:OPENCODE_MODEL_DEFAULT}") {
    status("opencode.json model", "pass", "uses OPENCODE_MODEL_DEFAULT env routing");
    return true;
  }

  status("opencode.json model", "warn", `expected {env:OPENCODE_MODEL_DEFAULT}, got ${JSON.stringify(opencode.model)}`);
  remediation("set opencode.json model to {env:OPENCODE_MODEL_DEFAULT}");
  return true;
}

function main() {
  log("opencode-capybara doctor");
  log("Read-only checks only; no files will be changed.");

  const results = [
    checkNode(),
    checkNpm(),
    checkRtk(),
    checkSkills(),
    checkRepoFiles(),
    checkPackageLifecycle(),
    checkDocsPolicy(),
    checkEnvWarning(),
    checkDefaultModelRouting(),
    checkAgentModelSync(),
    checkOpenChamberSync(),
  ];

  const failed = results.some((value) => value === false);
  if (failed) {
    process.exitCode = 1;
  } else {
    section("Summary");
    status("Doctor", "pass", "all required checks passed");
  }
}

main();
