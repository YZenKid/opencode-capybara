#!/usr/bin/env node
/**
 * Run npm scripts sequentially, report each result, continue on failure.
 * Exits with highest nonzero code. No short-circuit.
 *
 * Usage: node scripts/run-all.mjs <script-name> [script-name ...]
 */
import { spawnSync } from "node:child_process";

const scripts = process.argv.slice(2);
if (scripts.length === 0) {
  console.error("Usage: node scripts/run-all.mjs <script-name> [...]");
  process.exit(2);
}

let highestExit = 0;

for (const name of scripts) {
  const result = spawnSync("npm", ["run", name], {
    stdio: "inherit",
    shell: true,
  });
  const code = result.status ?? 1;
  console.log(`[gate] ${name} exit=${code}`);
  if (code > highestExit) highestExit = code;
}

process.exit(highestExit);
