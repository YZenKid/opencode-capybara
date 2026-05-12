#!/usr/bin/env node

import { existsSync, readdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { hasHeadings, missingKeys, readJson } from "./evals/lib.mjs";

const root = resolve(import.meta.dirname, "..");
let failures = 0;
const taskIdArg = process.argv.find((arg) => arg.startsWith("--task-id="));
const requestedTaskId = taskIdArg ? taskIdArg.split("=")[1] : null;

function fail(message, details = []) {
  failures += 1;
  console.error(`✗ ${message}`);
  for (const detail of details) console.error(`  - ${detail}`);
}

const quality = readFileSync(resolve(root, ".opencode/docs/QUALITY.md"), "utf8");
const missingQualityHeadings = hasHeadings(quality, ["Evidence contract", "Replay bundle minimum"]);
const required = ["## Evidence", "Command:", "Result:", "## Risks / Limitations", "## Next Steps"];
const missing = required.filter((needle) => !quality.includes(needle));
if (missing.length > 0 || missingQualityHeadings.length > 0) {
  fail(
    ".opencode/docs/QUALITY.md: evidence contract incomplete",
    [
      ...missing.map((item) => `missing: ${item}`),
      ...missingQualityHeadings.map((item) => `missing heading: ${item}`),
    ],
  );
} else {
  console.log("✓ .opencode/docs/QUALITY.md evidence contract");
}

const plansDir = resolve(root, ".opencode", "plans");
const planFiles = readdirSync(plansDir).filter((file) => file.endsWith(".md")).sort();
if (planFiles.length === 0) {
  fail("no plan artifacts found under .opencode/plans/");
} else {
  const selectedPlan = requestedTaskId ? `${requestedTaskId}.md` : planFiles.at(-1);
  const latestPlanPath = resolve(plansDir, selectedPlan);
  if (!existsSync(latestPlanPath)) {
    fail(`selected plan does not exist`, [selectedPlan]);
  }
  const latestPlanContent = readFileSync(latestPlanPath, "utf8");
  const missingSections = hasHeadings(latestPlanContent, ["Goal", "Validation Commands", "Evidence Requirements", "Final Planning Summary"]);
  if (missingSections.length > 0) {
    fail(`selected plan ${selectedPlan}: missing required sections`, missingSections);
  } else {
    console.log(`✓ selected plan ${selectedPlan} includes required evidence-oriented sections`);
  }

  const taskId = selectedPlan.replace(/\.md$/, "");
  const evidenceDir = resolve(root, ".opencode", "evidence", taskId);
  if (!existsSync(evidenceDir)) {
    fail(`evidence directory missing for selected plan ${taskId}`);
  } else {
    const evidenceFiles = readdirSync(evidenceDir).filter((file) => file.endsWith(".md"));
    const requiredEvidenceFiles = ["discovery.md", "verification.md"];
    const missingEvidence = requiredEvidenceFiles.filter((file) => !evidenceFiles.includes(file));
    if (missingEvidence.length > 0) {
      fail(`evidence directory for ${taskId} is incomplete`, missingEvidence.map((item) => `missing: ${item}`));
    } else {
      console.log(`✓ evidence directory for ${taskId} contains discovery and verification artifacts`);
    }

    const manifestPath = resolve(evidenceDir, "index.json");
    if (!existsSync(manifestPath)) {
      fail(`evidence directory for ${taskId} is missing index.json`, ["add a task-scoped evidence manifest"]);
    } else {
      const manifest = readJson(manifestPath);
      const manifestMissing = missingKeys(manifest, ["task_id", "plan_file", "evidence_dir", "required_files", "validation_commands"]);
      if (manifestMissing.length > 0) {
        fail(`evidence manifest for ${taskId} is incomplete`, manifestMissing.map((item) => `missing: ${item}`));
      } else {
        console.log(`✓ evidence manifest for ${taskId} contains task-scoped lookup fields`);
      }
    }
  }
}

const evalReport = resolve(root, ".opencode", "evidence", "harness-evals", "latest", "report.json");
if (!existsSync(evalReport)) {
  fail("missing harness eval report", ["run `npm run eval:harness` to generate replayable eval evidence"]);
} else {
  const report = readJson(evalReport);
  const reportMissing = [
    "task_id",
    "timestamp",
    "harness_version",
    "prompt_or_task_summary",
    "tool_trace_summary",
    "changed_files_summary",
    "files_changed",
    "validation_outputs",
    "verdict",
    "fixture_count",
    "fixture_ids",
    "results",
    "reason_codes",
    "transcript_summary",
    "drift_summary",
    "release_gate_readiness",
  ].filter((key) => !(key in report));
  if (reportMissing.length > 0) {
    fail("harness eval report is missing replay fields", reportMissing.map((item) => `missing: ${item}`));
  } else {
    console.log("✓ harness eval report contains replay metadata");
  }
}

if (failures > 0) {
  console.error(`\nEvidence contract check failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nEvidence contract check passed.");
