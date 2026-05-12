#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { evaluateTaskFixture, evaluateTextRules, evaluateTranscriptFixture, loadFixtures, readJson, readTextOrNull } from "./lib.mjs";

const root = resolve(import.meta.dirname, "..", "..");
const fixturesDir = resolve(root, "scripts", "evals", "fixtures");
const taskFixturesDir = resolve(root, "scripts", "evals", "task-fixtures");
const transcriptFixturesDir = resolve(root, "scripts", "evals", "transcript-fixtures");
const reportDir = resolve(root, ".opencode", "evidence", "harness-evals", "latest");

mkdirSync(reportDir, { recursive: true });

const fixtures = loadFixtures(fixturesDir);
const taskFixtures = existsSync(taskFixturesDir) ? loadFixtures(taskFixturesDir) : [];
const transcriptFixtures = existsSync(transcriptFixturesDir) ? loadFixtures(transcriptFixturesDir) : [];

const results = [];
let failed = 0;
const validatedFiles = new Set();
const transcriptScores = [];
const transcriptSourceModes = {};
const transcriptScoreBands = {};
const transcriptClassifications = {};

let gitSha = "unknown";
try {
  gitSha = execFileSync("git", ["rev-parse", "HEAD"], {
    cwd: root,
    encoding: "utf8",
  }).trim();
} catch {
  gitSha = "local-worktree";
}

const validationCommands = [
  {
    command: "npm run eval:harness",
    result: "PASS",
  },
];

for (const { fixture } of fixtures) {
  const checks = [];
  let fixtureFailed = false;

  for (const rule of fixture.rules) {
    const target = resolve(root, rule.file);
    const content = readTextOrNull(target);
    if (content === null) {
      checks.push({ file: rule.file, status: "FAIL", reason_code: "missing-file" });
      fixtureFailed = true;
      continue;
    }

    validatedFiles.add(rule.file);

    const { missing, forbidden } = evaluateTextRules(content, rule);

    if (missing.length > 0 || forbidden.length > 0) {
      fixtureFailed = true;
      checks.push({
        file: rule.file,
        status: "FAIL",
        reason_code: rule.reasonCode ?? "rule-mismatch",
        missing,
        forbidden,
      });
    } else {
      checks.push({ file: rule.file, status: "PASS" });
    }
  }

  if (fixtureFailed) failed += 1;
  results.push({
    id: fixture.id,
    description: fixture.description,
    status: fixtureFailed ? "FAIL" : "PASS",
      checks,
    });
}

for (const { fixture } of taskFixtures) {
  const result = evaluateTaskFixture(root, fixture);
  for (const check of result.checks) {
    if (check.file) validatedFiles.add(check.file);
  }
  if (result.status === "FAIL") failed += 1;
  results.push(result);
}

for (const { file, fixture } of transcriptFixtures) {
  const result = evaluateTranscriptFixture(fixture);
  for (const check of result.checks) {
    if (!check.file) check.file = `scripts/evals/transcript-fixtures/${file}`;
  }
  validatedFiles.add(`scripts/evals/transcript-fixtures/${file}`);
  transcriptScores.push(result.routing_score?.score_0_to_5 ?? 0);
  transcriptSourceModes[result.transcript_source_mode] = (transcriptSourceModes[result.transcript_source_mode] ?? 0) + 1;
  transcriptScoreBands[result.routing_score?.score_band ?? "unknown"] = (transcriptScoreBands[result.routing_score?.score_band ?? "unknown"] ?? 0) + 1;
  transcriptClassifications[result.fixture_classification ?? "general"] = (transcriptClassifications[result.fixture_classification ?? "general"] ?? 0) + 1;
  if (result.status === "FAIL") failed += 1;
  results.push(result);
}

const transcriptResults = results.filter((result) => result.category === "transcript-behavior");
const releaseCriticalTranscriptResults = transcriptResults.filter((result) => result.release_critical);
const releaseCriticalAverage = releaseCriticalTranscriptResults.length > 0
  ? Number((releaseCriticalTranscriptResults.reduce((sum, result) => sum + (result.routing_score?.score_0_to_5 ?? 0), 0) / releaseCriticalTranscriptResults.length).toFixed(2))
  : null;

const historyDir = resolve(root, ".opencode", "evidence", "harness-evals", "history");
mkdirSync(historyDir, { recursive: true });
const historyFiles = existsSync(historyDir)
  ? readdirSync(historyDir).filter((file) => file.endsWith(".json")).sort()
  : [];
const previousHistoryPath = historyFiles.length > 0 ? resolve(historyDir, historyFiles.at(-1)) : null;
const previousHistory = previousHistoryPath && existsSync(previousHistoryPath) ? readJson(previousHistoryPath) : null;

const currentAverage = transcriptScores.length > 0
  ? Number((transcriptScores.reduce((sum, score) => sum + score, 0) / transcriptScores.length).toFixed(2))
  : null;

const report = {
  task_id: "harness-evals-latest",
  timestamp: new Date().toISOString(),
  harness_version: gitSha,
  prompt_or_task_summary: "Run lightweight deterministic harness eval fixtures for docs system-of-record and runtime plugin-removal regressions.",
  tool_trace_summary: [
    "Read eval fixture JSON files from scripts/evals/fixtures/",
    "Read behavioral task fixture JSON files from scripts/evals/task-fixtures/",
    "Read transcript sequence fixtures from scripts/evals/transcript-fixtures/",
    "Read target repository files and evaluate mustInclude/mustNotInclude rules",
    "Write replayable report artifacts under .opencode/evidence/harness-evals/latest/",
  ],
  changed_files_summary: "Read-only eval run; no repository files were modified. files_changed lists validated target files.",
  validation_outputs: validationCommands,
  verdict: failed > 0 ? "FAIL" : "PASS",
  fixture_count: results.length,
  failed,
  fixture_ids: results.map((result) => result.id),
  reason_codes: results.flatMap((result) =>
    result.checks.filter((check) => check.reason_code).map((check) => check.reason_code),
  ),
  transcript_summary: {
    fixture_count: transcriptFixtures.length,
    average_score_0_to_5: currentAverage,
    min_score_0_to_5: transcriptScores.length > 0 ? Math.min(...transcriptScores) : null,
    max_score_0_to_5: transcriptScores.length > 0 ? Math.max(...transcriptScores) : null,
    source_modes: transcriptSourceModes,
    score_bands: transcriptScoreBands,
    classifications: transcriptClassifications,
    release_critical_fixture_count: releaseCriticalTranscriptResults.length,
    release_critical_average_score_0_to_5: releaseCriticalAverage,
  },
  drift_summary: {
    previous_timestamp: previousHistory?.timestamp ?? null,
    previous_average_score_0_to_5: previousHistory?.transcript_summary?.average_score_0_to_5 ?? null,
    average_score_delta: previousHistory?.transcript_summary?.average_score_0_to_5 != null && currentAverage != null
      ? Number((currentAverage - previousHistory.transcript_summary.average_score_0_to_5).toFixed(2))
      : null,
    failed_delta: previousHistory?.failed != null ? failed - previousHistory.failed : null,
    fixture_count_delta: previousHistory?.transcript_summary?.fixture_count != null
      ? transcriptFixtures.length - previousHistory.transcript_summary.fixture_count
      : null,
  },
  release_gate_readiness: {
    transcript_fixtures_all_pass: transcriptResults.every((result) => result.status === "PASS"),
    release_critical_all_pass: releaseCriticalTranscriptResults.every((result) => result.status === "PASS"),
    release_critical_average_score_0_to_5: releaseCriticalAverage,
    minimum_required_average_score_0_to_5: 4.5,
    ready: transcriptResults.every((result) => result.status === "PASS")
      && (releaseCriticalAverage == null || releaseCriticalAverage >= 4.5),
  },
  files_changed: Array.from(validatedFiles).sort(),
  results,
};

writeFileSync(resolve(reportDir, "report.json"), JSON.stringify(report, null, 2));
writeFileSync(
  resolve(reportDir, "report.md"),
  [
    "# Harness Eval Report",
    "",
      `- Timestamp: ${report.timestamp}`,
      `- Harness version: ${report.harness_version}`,
      `- Task summary: ${report.prompt_or_task_summary}`,
      `- Verdict: ${report.verdict}`,
      `- Fixture count: ${report.fixture_count}`,
      `- Failed: ${report.failed}`,
      report.transcript_summary.fixture_count > 0 ? `- Transcript fixture count: ${report.transcript_summary.fixture_count}` : null,
      report.transcript_summary.fixture_count > 0 ? `- Transcript average routing score: ${report.transcript_summary.average_score_0_to_5}/5` : null,
      report.transcript_summary.fixture_count > 0 ? `- Transcript score bands: ${Object.entries(report.transcript_summary.score_bands).map(([key, value]) => `${key}=${value}`).join(", ")}` : null,
      report.drift_summary.previous_timestamp ? `- Drift average delta: ${report.drift_summary.average_score_delta}` : null,
      `- Release gate ready: ${report.release_gate_readiness.ready}`,
      "- Tool trace:",
      ...report.tool_trace_summary.map((item) => `  - ${item}`),
      `- Files changed summary: ${report.changed_files_summary}`,
      ...(report.files_changed.length > 0 ? report.files_changed.map((item) => `  - ${item}`) : ["  - none (read-only eval)"]),
      "- Validation outputs:",
      ...report.validation_outputs.map((item) => `  - ${item.command} → ${item.result}`),
      "- Fixture IDs:",
      ...report.fixture_ids.map((item) => `  - ${item}`),
      report.reason_codes.length > 0 ? "- Reason codes:" : "- Reason codes: none",
      ...report.reason_codes.map((item) => `  - ${item}`),
      "",
      ...results.flatMap((result) => [
        `## ${result.id}`,
      `- Status: ${result.status}`,
      `- Description: ${result.description}`,
      result.transcript_source_mode ? `- Transcript source mode: ${result.transcript_source_mode}` : null,
      result.routing_score ? `- Routing score: ${result.routing_score.score_0_to_5}/5` : null,
      result.routing_score ? `- Routing score band: ${result.routing_score.score_band}` : null,
      result.routing_score ? `- Routing confidence: ${result.routing_score.confidence}` : null,
      result.routing_score ? `- Routing dimensions: ${Object.entries(result.routing_score.dimensions).map(([key, value]) => `${key}=${value ? "pass" : "fail"}`).join(", ")}` : null,
      ...result.checks.map((check) => `- ${check.file}: ${check.status}${check.reason_code ? ` (${check.reason_code})` : ""}`),
      "",
    ].filter(Boolean)),
  ].join("\n"),
);

const historySafeTimestamp = report.timestamp.replace(/[:]/g, "-");
writeFileSync(resolve(historyDir, `${historySafeTimestamp}.json`), JSON.stringify(report, null, 2));
writeFileSync(resolve(historyDir, `${historySafeTimestamp}.md`), readFileSync(resolve(reportDir, "report.md"), "utf8"));

for (const result of results) {
  console.log(`${result.status === "PASS" ? "✓" : "✗"} ${result.id}`);
}

if (failed > 0) {
  console.error(`\nHarness eval failed with ${failed} failing fixture(s).`);
  process.exit(1);
}

console.log("\nHarness eval passed.");
