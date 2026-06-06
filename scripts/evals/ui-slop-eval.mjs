#!/usr/bin/env node

import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { basename, join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "../..");
const fixtureDir = join(root, "scripts/evals/ui-slop-fixtures");
const evidenceDir = join(root, ".opencode/evidence/ui-slop/latest");
const reasonMeta = {
  "requested-aesthetic-mismatch": ["HIGH", "style_fidelity", "Translate requested aesthetic into concrete material tokens and remove conflicting style families."],
  "material-grammar-missing": ["HIGH", "style_fidelity", "Add requested material grammar: surfaces, depth, translucency, shadows, and color roles."],
  "card-spam-repetition": ["HIGH", "layout_variety", "Replace repeated card-grid anatomy with purpose-specific hierarchy and section composition."],
  "generic-neon-glass-overuse": ["MEDIUM", "style_fidelity", "Remove generic neon/glow/glass defaults unless requested and domain-relevant."],
  "fake-metric": ["BLOCKER", "content_humanity", "Remove arbitrary metrics or label data as real source-backed/demo-only with context."],
  "debug-copy-user-facing": ["BLOCKER", "debug_artifact_hygiene", "Remove localhost, TODO, debug, mock, internal state, and implementation copy from user-facing UI."],
  "abstract-hero-filler": ["BLOCKER", "hero_specificity", "Replace generic blobs/floating cards with product/domain-specific hero composition."],
  "placeholder-visual": ["HIGH", "hero_specificity", "Replace placeholder visual content with domain-specific imagery, illustration, or honest empty state."],
  "missing-state-evidence": ["MEDIUM", "state_accessibility_evidence", "Add visible loading/empty/error/success state evidence for substantial UI."],
  "missing-accessibility-evidence": ["MEDIUM", "state_accessibility_evidence", "Add accessible labels, semantic headings, and state descriptions."],
  "missing-screenshot-evidence-for-visual-claim": ["LOW", "state_accessibility_evidence", "Capture screenshot evidence before making visual completion claims."],
};

const categories = [...new Set(Object.values(reasonMeta).map(([, category]) => category))];
const args = process.argv.slice(2);
const mode = args.includes("check") || args.includes("--check") ? "check" : "eval";
const url = args.find((arg) => arg.startsWith("--url="))?.slice("--url=".length);
const expectUrlFail = args.includes("--expect-url-fail");

function stripTags(html) {
  return html.replace(/<script[\s\S]*?<\/script>/gi, " ").replace(/<style[\s\S]*?<\/style>/gi, " ").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
}

function pushFinding(findings, source, reason_code, detail, hint = "document") {
  const [severity, category, remediation] = reasonMeta[reason_code];
  findings.push({ fixture_id: source.id, source_id: source.id, reason_code, severity, category, remediation, hint, detail });
}

function evaluateSource(source) {
  const html = source.html ?? "";
  const visibleText = stripTags(html);
  const text = visibleText.toLowerCase();
  const markupHaystack = `${source.surface ?? ""} ${html} ${visibleText}`.toLowerCase();
  const haystack = `${source.requestedAesthetic ?? ""} ${markupHaystack}`.toLowerCase();
  const findings = [];
  const requestedClayGlass = /clay|glass/.test((source.requestedAesthetic ?? "").toLowerCase());
  const hasClayGrammar = /clay|soft-clay|rounded-3xl|shadow-inner|raised|cream|muted|soft/.test(markupHaystack);
  const neonHits = (haystack.match(/neon|glow|cyan|electric|gradient|orb/g) ?? []).length;
  const glassHits = (haystack.match(/glass|frosted|translucent|blur|backdrop/g) ?? []).length;
  const cardHits = (html.match(/class=['"][^'"]*(card|article)[^'"]*['"]/gi) ?? []).length;
  const articleHits = (html.match(/<article\b/gi) ?? []).length;
  const repeatedCardClassHits = (html.match(/class=['"][^'"]*(card neon|border-cyan|glass card)[^'"]*['"]/gi) ?? []).length;
  const repeatedCardRisk = repeatedCardClassHits >= 4 || (cardHits >= 6 && /grid|cards|card-list|pricing|feature-card/.test(html.toLowerCase()));
  const hasMetricFraming = /real|actual|source|verified|current|selected|record|invoice|order|analytics|from api|sample data|demo-only/.test(text);

  if (requestedClayGlass && neonHits >= 3 && !hasClayGrammar) pushFinding(findings, source, "requested-aesthetic-mismatch", "Requested clay/glass aesthetic is dominated by neon/glow language.", "style/class tokens");
  if (requestedClayGlass && !hasClayGrammar) pushFinding(findings, source, "material-grammar-missing", "Requested material family lacks soft clay/glass grammar tokens.", "style/class tokens");
  if (repeatedCardRisk) pushFinding(findings, source, "card-spam-repetition", `Repeated card anatomy count: ${Math.max(cardHits, articleHits, repeatedCardClassHits)}.`, "card grid");
  if (neonHits >= 4 && glassHits >= 1) pushFinding(findings, source, "generic-neon-glass-overuse", `Generic neon/glass token count: ${neonHits + glassHits}.`, "style/class tokens");
  if (/localhost|debug|todo|mock=true|state dump|wire real api|component state|implementation note/.test(text)) pushFinding(findings, source, "debug-copy-user-facing", "Internal/debug copy appears in user-facing text.", "text copy");
  if (/demo data|placeholder metric|\$999,?999|123%|420%|99%|10k\+|\$1m|87%/.test(text) && !hasMetricFraming) pushFinding(findings, source, "fake-metric", "Arbitrary metric or demo number appears without source framing.", "metrics text");
  if (/abstract|blob|gradient-orb|floating-card|beautiful tools for modern teams|transform your workflow/.test(haystack) && /hero|landing/.test(haystack)) pushFinding(findings, source, "abstract-hero-filler", "Hero relies on generic abstract composition rather than domain-specific content.", "hero section");
  if (/placeholder|lorem|generic visual|stock blob/.test(haystack)) pushFinding(findings, source, "placeholder-visual", "Placeholder visual/copy remains in UI.", "visual placeholder");
  if ((source.surface ?? "").includes("dashboard") && !/empty|loading|error|success|filter|selected date|current/.test(text)) pushFinding(findings, source, "missing-state-evidence", "Dashboard lacks visible state or data-scope evidence.", "dashboard state copy");
  if (!/aria-label|aria-labelledby|<h1\b|<button[^>]+aria-label/.test(html)) pushFinding(findings, source, "missing-accessibility-evidence", "Markup lacks basic accessible labels/headings evidence.", "semantic/accessibility markup");

  const highCount = findings.filter((f) => f.severity === "HIGH").length;
  const blockerCount = findings.filter((f) => f.severity === "BLOCKER").length;
  const scoreByCategory = Object.fromEntries(categories.map((category) => {
    const penalty = findings.filter((f) => f.category === category).reduce((sum, f) => sum + (f.severity === "BLOCKER" ? 2 : f.severity === "HIGH" ? 1.25 : f.severity === "MEDIUM" ? 0.75 : 0.25), 0);
    return [category, Math.max(1, Number((5 - penalty).toFixed(2)))];
  }));
  const averageScore = Number((Object.values(scoreByCategory).reduce((a, b) => a + b, 0) / categories.length).toFixed(2));
  const status = blockerCount > 0 || highCount > 2 || averageScore < 3.5 ? "FAIL" : "PASS";
  return { ...source, status, averageScore, scoreByCategory, findings };
}

async function loadFixtures() {
  const names = (await readdir(fixtureDir)).filter((name) => name.endsWith(".json") && name !== "schema.json").sort();
  const fixtures = [];
  for (const name of names) fixtures.push(JSON.parse(await readFile(join(fixtureDir, name), "utf8")));
  return fixtures;
}

async function loadUrlSource(targetUrl) {
  if (!targetUrl) return [];
  const response = await fetch(targetUrl);
  const html = await response.text();
  return [{ id: `url:${targetUrl}`, description: `Best-effort URL source ${targetUrl}`, requestedAesthetic: "unspecified", surface: "url", expectedStatus: expectUrlFail ? "FAIL" : undefined, expectedReasonCodes: [], advisory: !expectUrlFail, html }];
}

function buildReport(results) {
  const failures = [];
  for (const result of results) {
    const codes = new Set(result.findings.map((f) => f.reason_code));
    const missing = (result.expectedReasonCodes ?? []).filter((code) => !codes.has(code));
    if (result.advisory) continue;
    if (result.expectedStatus && result.status !== result.expectedStatus) failures.push(`${result.id}: expected ${result.expectedStatus}, got ${result.status}`);
    if (missing.length > 0) failures.push(`${result.id}: missing expected reason codes ${missing.join(", ")}`);
  }
  return {
    schema_version: 1,
    generated_at: new Date().toISOString(),
    mode,
    fixture_count: results.length,
    status: failures.length === 0 ? "PASS" : "FAIL",
    failures,
    results: results.map(({ html, ...rest }) => rest),
  };
}

function markdown(report) {
  const lines = ["# UI Slop Evaluation Report", "", `Status: ${report.status}`, `Mode: ${report.mode}`, `Fixtures/sources: ${report.fixture_count}`, ""];
  for (const result of report.results) {
    lines.push(`## ${result.id}`, "", `Status: ${result.status}`, `Expected: ${result.expectedStatus ?? "n/a"}`, `Average score: ${result.averageScore}`, "", "Findings:");
    if (result.findings.length === 0) lines.push("- none");
    for (const f of result.findings) lines.push(`- ${f.severity} ${f.reason_code} (${f.category}) [${f.hint}]: ${f.detail} Remediation: ${f.remediation}`);
    lines.push("");
  }
  if (report.failures.length) lines.push("## Check failures", "", ...report.failures.map((f) => `- ${f}`), "");
  return `${lines.join("\n")}\n`;
}

const sources = [...await loadFixtures(), ...await loadUrlSource(url)];
const results = sources.map(evaluateSource);
const report = buildReport(results);
await mkdir(evidenceDir, { recursive: true });
await writeFile(join(evidenceDir, "report.json"), `${JSON.stringify(report, null, 2)}\n`);
await writeFile(join(evidenceDir, "report.md"), markdown(report));

console.log(`UI slop ${mode}: ${report.status}`);
console.log(`Report: ${join(".opencode/evidence/ui-slop/latest", "report.json")}`);
for (const result of report.results) console.log(`- ${basename(result.id)} ${result.status} findings=${result.findings.length} score=${result.averageScore}`);
if (mode === "check" && report.status !== "PASS") {
  for (const failure of report.failures) console.error(`✗ ${failure}`);
  process.exit(1);
}
