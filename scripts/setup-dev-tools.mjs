#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { platform } from "node:os";

function parseArgs(argv) {
  const flags = {
    check: false,
    force: false,
    skipRtk: false,
    skipCaveman: false,
    help: false,
  };

  for (const arg of argv) {
    if (arg === "--check") flags.check = true;
    else if (arg === "--force") flags.force = true;
    else if (arg === "--skip-rtk") flags.skipRtk = true;
    else if (arg === "--skip-caveman") flags.skipCaveman = true;
    else if (arg === "--help" || arg === "-h") flags.help = true;
    else {
      throw new Error(`Unknown flag: ${arg}`);
    }
  }

  return flags;
}

function run(command, args, options = {}) {
  return spawnSync(command, args, {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    ...options,
  });
}

function commandExists(command, args = ["--version"]) {
  const result = run(command, args);
  return result.status === 0;
}

function printSection(title) {
  process.stdout.write(`\n== ${title} ==\n`);
}

function printLine(message = "") {
  process.stdout.write(`${message}\n`);
}

function printResult(label, status, detail) {
  const prefix = status === "ok" ? "[ok]" : status === "warn" ? "[warn]" : "[action]";
  printLine(`${prefix} ${label}${detail ? ` — ${detail}` : ""}`);
}

function printHelp() {
  printLine("Usage: node scripts/setup-dev-tools.mjs [--check] [--force] [--skip-rtk] [--skip-caveman] [--help]");
  printLine("");
  printLine("Explicitly installs or checks RTK and Caveman for this repo.");
  printLine("- --check: read-only verification only");
  printLine("- --force: reinstall/setup even if tools already exist");
  printLine("- --skip-rtk: skip RTK setup/check");
  printLine("- --skip-caveman: skip Caveman setup/check");
}

function hasUnixLikeSupport() {
  return platform() === "darwin" || platform() === "linux";
}

function hasShell() {
  const result = run("sh", ["-lc", "exit 0"]);
  return result.status === 0;
}

function reportRtkCheckMissing() {
  printResult("RTK", "warn", "not found");
  printLine("  Remediation: run `npm run setup:tools` or install RTK manually.");
}

function installRtk({ check, force }) {
  const pinnedVersion = process.env.RTK_VERSION || "v0.39.0";
  printSection("RTK");
  printLine("Never run `rtk init` with `-g --opencode`.");
  printLine("Use RTK and Caveman together for token compression/context packing when that workflow is needed; they are not either/or alternatives in this repo.");
  printLine(`Pinned fallback version: ${pinnedVersion}`);
  if (check) {
    printLine("Checking: rtk --version");
    if (commandExists("rtk", ["--version"])) {
      printResult("RTK", "ok", "installed");
      return true;
    }
    reportRtkCheckMissing();
    return false;
  }

  if (!force && commandExists("rtk", ["--version"])) {
    printResult("RTK", "ok", "already installed");
    return true;
  }

  if (platform() === "darwin" && commandExists("brew", ["--version"])) {
    printLine("Running: brew install rtk");
    printLine("Note: Homebrew installs the current formula version. Use RTK_VERSION with the pinned script fallback path if you need a deterministic non-Homebrew install.");
    const result = run("brew", ["install", "rtk"], { stdio: "inherit" });
    if (result.status !== 0) {
      printResult("RTK", "warn", "brew install failed");
      printLine("  Remediation: install RTK manually, then rerun `npm run setup:tools`.");
      return false;
    }
    printResult("RTK", "ok", "installed via Homebrew");
    return true;
  }

  if (hasUnixLikeSupport() && commandExists("curl", ["--version"]) && hasShell()) {
    const scriptUrl = `https://raw.githubusercontent.com/rtk-ai/rtk/${pinnedVersion}/install.sh`;
    printLine("Running official RTK install script explicitly because setup was requested.");
    printLine(`Running pinned script: curl -fsSL ${scriptUrl} | RTK_VERSION=${pinnedVersion} sh`);
    const result = spawnSync("sh", ["-lc", `curl -fsSL ${JSON.stringify(scriptUrl)} | RTK_VERSION=${JSON.stringify(pinnedVersion)} sh`], {
      encoding: "utf8",
      stdio: "inherit",
    });
    if (result.status !== 0) {
      printResult("RTK", "warn", "official install script failed");
      printLine("  Remediation: install RTK manually for your platform, then rerun `npm run setup:tools`.");
      return false;
    }
    printResult("RTK", "ok", "installed via official script");
    return true;
  }

  printResult("RTK", "warn", "no automatic installer available for this platform");
  printLine("  Remediation: install RTK manually, then rerun `npm run setup:tools`.");
  return false;
}

function installCaveman({ check, force }) {
  printSection("Caveman");
  const targetCommand = "npx -y skills add JuliusBrussee/caveman -a opencode";
  printLine("Caveman works together with RTK for token compression/context packing in this repo; do not treat it as an alternative path.");

  if (check) {
    const result = run("npx", ["-y", "skills", "--help"]);
    if (result.status === 0) {
      printResult("Caveman", "ok", "skills CLI available");
      printLine(`  Remediation command: ${targetCommand}`);
      return true;
    }
    printResult("Caveman", "warn", "skills CLI not verified");
    printLine(`  Remediation command: ${targetCommand}`);
    return false;
  }

  if (force) {
    printLine(`Running: ${targetCommand}`);
  } else {
    printLine(`Running: ${targetCommand}`);
  }
  const result = spawnSync("npx", ["-y", "skills", "add", "JuliusBrussee/caveman", "-a", "opencode"], {
    encoding: "utf8",
    stdio: "inherit",
  });
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
  try {
    flags = parseArgs(process.argv.slice(2));
  } catch (error) {
    printLine(String(error.message || error));
    process.exitCode = 1;
    return;
  }

  if (flags.help) {
    printHelp();
    return;
  }

  printLine("opencode-capybara tool setup");
  printLine(flags.check ? "Mode: check only" : "Mode: explicit setup");

  let ok = true;
  if (!flags.skipRtk) {
    ok = installRtk(flags) && ok;
  } else {
    printSection("RTK");
    printResult("RTK", "warn", "skipped by request");
  }

  if (!flags.skipCaveman) {
    ok = installCaveman(flags) && ok;
  } else {
    printSection("Caveman");
    printResult("Caveman", "warn", "skipped by request");
  }

  printLine("");
  printLine("Restart OpenCode after installing or checking tools so the new setup is visible in a fresh session.");
  printLine("OpenCode may continue to avoid rtk-prefixed rewriting until you explicitly opt in.");
  if (!ok) {
    process.exitCode = 1;
  }
}

main();
