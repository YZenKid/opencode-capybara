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
const requiredSentinelIds = [
  "drift-planner-default-tax-negative",
  "drift-maintenance-overgated-negative",
  "drift-designer-frontend-boundary-negative",
  "drift-fullstack-catchall-negative",
  "drift-source-strategy-skip-negative",
  "drift-quality-gate-remediation-positive",
  "drift-visual-asset-boundary-negative",
  "drift-readonly-advisor-write-negative",
];
const releaseCriticalSentinelIds = [
  "drift-planner-default-tax-negative",
  "drift-designer-frontend-boundary-negative",
  "drift-fullstack-catchall-negative",
  "drift-quality-gate-remediation-positive",
  "drift-readonly-advisor-write-negative",
];
const requiredClassifications = ["good", "bad", "borderline", "fallback-valid", "source-strategy", "domain-boundary", "quality-gate", "planner-boundary"];
const requiredSourceModes = ["normalized-events", "raw-tool-trace"];
const requiredTranscriptFixtureCount = 21;
const resultIds = new Set(transcriptResults.map((result) => result.id));
const classifications = new Set(transcriptResults.map((result) => result.fixture_classification ?? "general"));
const sourceModes = new Set(transcriptResults.map((result) => result.transcript_source_mode));

const failures = [];
if (transcriptResults.length < requiredTranscriptFixtureCount) {
  failures.push(`expected at least ${requiredTranscriptFixtureCount} transcript fixtures, found ${transcriptResults.length}`);
}
const missingSentinelIds = requiredSentinelIds.filter((id) => !resultIds.has(id));
if (missingSentinelIds.length > 0) failures.push(`missing required drift sentinel fixture ids: ${missingSentinelIds.join(", ")}`);
const missingCriticalSentinelIds = releaseCriticalSentinelIds.filter((id) => !releaseCritical.some((result) => result.id === id));
if (missingCriticalSentinelIds.length > 0) failures.push(`missing release-critical drift sentinel ids: ${missingCriticalSentinelIds.join(", ")}`);
const missingClassifications = requiredClassifications.filter((classification) => !classifications.has(classification));
if (missingClassifications.length > 0) failures.push(`missing transcript classifications: ${missingClassifications.join(", ")}`);
const missingSourceModes = requiredSourceModes.filter((sourceMode) => !sourceModes.has(sourceMode));
if (missingSourceModes.length > 0) failures.push(`missing transcript source modes: ${missingSourceModes.join(", ")}`);
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
if (failures.length > 0) {
  console.error("✗ transcript release gate failed");
  for (const detail of failures) console.error(`  - ${detail}`);
  process.exit(1);
}

console.log("✓ transcript release gate passed");
console.log(`  - transcript fixtures: ${transcriptResults.length}`);
console.log(`  - release-critical fixtures: ${releaseCritical.length}`);
console.log(`  - release-critical average score: ${releaseGate.release_critical_average_score_0_to_5}`);
console.log(`  - required drift sentinels: ${requiredSentinelIds.length}`);
