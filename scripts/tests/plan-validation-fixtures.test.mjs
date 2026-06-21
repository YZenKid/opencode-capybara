#!/usr/bin/env node
import { resolve } from "node:path";
import { execSync } from "node:child_process";

const root = resolve(import.meta.dirname, "../..");
const validatorScript = resolve(root, "scripts/validate-plan-depth.py");
const fixturesDir = resolve(root, "scripts/evals/fixtures/plans");

const fixtures = [
  {
    name: "bad-shallow-plan.md",
    shouldPass: false,
    expectedFailures: ["total_lines", "goal_words", "requirements_count", "acceptance_count", "components_count", "implementation_steps", "validation_commands"],
  },
  {
    name: "bad-generic-ui-plan.md",
    shouldPass: false,
    expectedFailures: ["anti_generic_patterns"],
  },
  {
    name: "EXAMPLE_PLAN.md",
    shouldPass: true,
    expectedFailures: [],
  },
];

let failures = 0;

for (const fixture of fixtures) {
  const planPath = fixture.name === "EXAMPLE_PLAN.md"
    ? resolve(root, ".opencode/docs/EXAMPLE_PLAN.md")
    : resolve(fixturesDir, fixture.name);

  try {
    const output = execSync(`python3 ${validatorScript} ${planPath}`, {
      encoding: "utf-8",
      cwd: root,
    });

    const passed = output.includes("RESULT: PASS");

    if (fixture.shouldPass && !passed) {
      console.error(`✗ ${fixture.name}: expected PASS but got NEEDS_DEPTH`);
      failures += 1;
    } else if (!fixture.shouldPass && passed) {
      console.error(`✗ ${fixture.name}: expected NEEDS_DEPTH but got PASS`);
      failures += 1;
    } else {
      console.log(`✓ ${fixture.name}: ${passed ? "PASS" : "NEEDS_DEPTH"} (expected)`);
    }

    // Check for expected failure patterns
    if (!fixture.shouldPass && !passed) {
      for (const expected of fixture.expectedFailures) {
        if (!output.includes(expected)) {
          console.error(`  ✗ Missing expected failure: ${expected}`);
          failures += 1;
        }
      }
    }
  } catch (error) {
    if (error.status === 1) {
      // Script returned 1 = NEEDS_DEPTH
      const output = error.stdout || "";
      const passed = output.includes("RESULT: PASS");

      if (fixture.shouldPass && !passed) {
        console.error(`✗ ${fixture.name}: expected PASS but got NEEDS_DEPTH`);
        failures += 1;
      } else if (!fixture.shouldPass && passed) {
        console.error(`✗ ${fixture.name}: expected NEEDS_DEPTH but got PASS`);
        failures += 1;
      } else {
        console.log(`✓ ${fixture.name}: ${passed ? "PASS" : "NEEDS_DEPTH"} (expected)`);
      }

      // Check for expected failure patterns
      if (!fixture.shouldPass && !passed) {
        for (const expected of fixture.expectedFailures) {
          if (!output.includes(expected)) {
            console.error(`  ✗ Missing expected failure: ${expected}`);
            failures += 1;
          }
        }
      }
    } else {
      console.error(`✗ ${fixture.name}: script error - ${error.message}`);
      failures += 1;
    }
  }
}

if (failures > 0) {
  console.error(`\nPlan validation fixtures failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nAll plan validation fixtures passed.");
