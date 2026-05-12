#!/usr/bin/env node

import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..", "..");
const reportPath = resolve(root, ".opencode", "evidence", "harness-evals", "latest", "report.json");

if (!existsSync(reportPath)) {
  console.error("✗ missing harness eval report");
  console.error("  - run `npm run eval:harness` before `npm run check:routing-release`");
  process.exit(1);
}

const report = JSON.parse(readFileSync(reportPath, "utf8"));
const transcriptSummary = report.transcript_summary ?? {};
const releaseGate = report.release_gate_readiness ?? {};
const transcriptResults = (report.results ?? []).filter((result) => result.category === "transcript-behavior");
const releaseCritical = transcriptResults.filter((result) => result.release_critical);

const failures = [];
if (transcriptResults.length < 6) {
  failures.push(`expected at least 6 transcript fixtures, found ${transcriptResults.length}`);
}
if (transcriptSummary.average_score_0_to_5 == null) {
  failures.push("missing transcript average score");
}
if (!releaseGate.transcript_fixtures_all_pass) {
  failures.push("not all transcript fixtures passed");
}
if (!releaseGate.release_critical_all_pass) {
  failures.push("not all release-critical transcript fixtures passed");
}
if (releaseGate.release_critical_average_score_0_to_5 != null && releaseGate.release_critical_average_score_0_to_5 < 4.5) {
  failures.push(`release-critical average score below threshold: ${releaseGate.release_critical_average_score_0_to_5} < 4.5`);
}
if (releaseCritical.some((result) => (result.routing_score?.score_0_to_5 ?? 0) < 4)) {
  failures.push("at least one release-critical transcript fixture scored below 4/5");
}

if (failures.length > 0) {
  console.error("✗ transcript release gate failed");
  for (const detail of failures) console.error(`  - ${detail}`);
  process.exit(1);
}

console.log("✓ transcript release gate passed");
console.log(`  - transcript fixtures: ${transcriptResults.length}`);
console.log(`  - release-critical fixtures: ${releaseCritical.length}`);
console.log(`  - release-critical average score: ${releaseGate.release_critical_average_score_0_to_5}`);
