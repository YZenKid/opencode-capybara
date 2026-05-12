import { existsSync, readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";

export function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8"));
}

export function readTextOrNull(file) {
  return existsSync(file) ? readFileSync(file, "utf8") : null;
}

export function extractHeadings(markdown) {
  return markdown
    .split("\n")
    .map((line, index) => ({ line, number: index + 1 }))
    .filter(({ line }) => /^#{1,6}\s+/.test(line))
    .map(({ line, number }) => {
      const [, hashes, text] = line.match(/^(#{1,6})\s+(.*)$/) ?? [];
      return {
        level: hashes.length,
        text: text.trim(),
        line: number,
      };
    });
}

export function hasHeadings(markdown, requiredHeadings) {
  const headings = extractHeadings(markdown).map((heading) => heading.text);
  return requiredHeadings.filter((heading) => !headings.includes(heading));
}

export function parseFrontmatter(markdown) {
  if (!markdown.startsWith("---\n")) return null;
  const end = markdown.indexOf("\n---\n", 4);
  if (end === -1) return null;
  const body = markdown.slice(4, end).split("\n");
  const result = {};
  for (const line of body) {
    const match = line.match(/^([A-Za-z0-9_\-]+):\s*(.*)$/);
    if (!match) continue;
    result[match[1]] = match[2];
  }
  return result;
}

export function missingKeys(obj, requiredKeys) {
  return requiredKeys.filter((key) => !(key in obj));
}

export function evaluateTextRules(content, rule) {
  const missing = (rule.mustInclude ?? []).filter((needle) => !content.includes(needle));
  const forbidden = (rule.mustNotInclude ?? []).filter((needle) => content.includes(needle));
  return { missing, forbidden };
}

export function loadFixtures(fixturesDir) {
  return readdirSync(fixturesDir)
    .filter((file) => file.endsWith(".json"))
    .sort()
    .map((file) => ({ file, fixture: readJson(resolve(fixturesDir, file)) }));
}

export function evaluateTaskFixture(root, fixture) {
  const checks = [];
  let failed = false;

  for (const artifact of fixture.artifacts ?? []) {
    const target = resolve(root, artifact.file);
    const content = readTextOrNull(target);

    if (content === null) {
      failed = true;
      checks.push({
        type: artifact.type ?? "artifact",
        file: artifact.file,
        status: "FAIL",
        reason_code: artifact.reasonCode ?? "missing-artifact",
      });
      continue;
    }

    let missing = [];
    let forbidden = [];

    if (artifact.requiredHeadings) {
      missing = [...missing, ...hasHeadings(content, artifact.requiredHeadings).map((item) => `heading:${item}`)];
    }

    if (artifact.requiredFrontmatterKeys) {
      const frontmatter = parseFrontmatter(content);
      if (frontmatter === null) {
        missing = [...missing, ...artifact.requiredFrontmatterKeys.map((item) => `frontmatter:${item}`)];
      } else {
        missing = [...missing, ...missingKeys(frontmatter, artifact.requiredFrontmatterKeys).map((item) => `frontmatter:${item}`)];
      }
    }

    if (artifact.requiredJsonKeys) {
      const parsed = JSON.parse(content);
      missing = [...missing, ...missingKeys(parsed, artifact.requiredJsonKeys).map((item) => `json:${item}`)];
    }

    const textRuleResult = evaluateTextRules(content, artifact);
    missing = [...missing, ...textRuleResult.missing];
    forbidden = [...forbidden, ...textRuleResult.forbidden];

    if (artifact.expectedReasonCodes) {
      const parsed = JSON.parse(content);
      const actual = new Set(parsed.reason_codes ?? []);
      const missingReasonCodes = artifact.expectedReasonCodes.filter((item) => !actual.has(item));
      missing = [...missing, ...missingReasonCodes.map((item) => `reason_code:${item}`)];
    }

    if (missing.length > 0 || forbidden.length > 0) {
      failed = true;
      checks.push({
        type: artifact.type ?? "artifact",
        file: artifact.file,
        status: "FAIL",
        reason_code: artifact.reasonCode ?? "task-artifact-mismatch",
        missing,
        forbidden,
      });
    } else {
      checks.push({
        type: artifact.type ?? "artifact",
        file: artifact.file,
        status: "PASS",
      });
    }
  }

  return {
    id: fixture.id,
    description: fixture.description,
    category: fixture.category ?? "behavioral-task",
    status: failed ? "FAIL" : "PASS",
    checks,
  };
}

function normalizeTranscriptEvents(events) {
  return (events ?? []).map((event, index) => ({
    index,
    agent: event.agent ?? "unknown",
    action: event.action ?? "unknown",
    fileCount: Number(event.fileCount ?? 0),
    material: Boolean(event.material ?? false),
    nonTrivial: Boolean(event.nonTrivial ?? false),
    delegatedTo: event.delegatedTo ?? null,
    notes: event.notes ?? "",
  }));
}

export function evaluateTranscriptFixture(fixture) {
  const events = normalizeTranscriptEvents(fixture.events);
  const violationChecks = [];
  const actualReasonCodes = new Set();

  const explorerDelegationIndex = events.findIndex(
    (event) => event.agent === "orchestrator" && event.action === "delegate_discovery" && event.delegatedTo === "explorer",
  );

  if (explorerDelegationIndex !== -1) {
    const redundantDiscovery = events.find(
      (event) => event.index > explorerDelegationIndex && event.agent === "orchestrator" && ["read", "discover"].includes(event.action) && event.fileCount > 3,
    );
    if (redundantDiscovery) {
      actualReasonCodes.add("routing-overreach-redundant-orchestrator-discovery");
      violationChecks.push({ type: "transcript-semantics", status: "FAIL", reason_code: "routing-overreach-redundant-orchestrator-discovery", detail: `orchestrator resumed read-heavy discovery after explorer delegation at event ${redundantDiscovery.index}` });
    }
  }

  const directMultiFileEdit = events.find((event) => event.agent === "orchestrator" && event.action === "edit" && event.fileCount >= 2);
  if (directMultiFileEdit) {
    actualReasonCodes.add("routing-overreach-orchestrator-multifile-edit");
    violationChecks.push({ type: "transcript-semantics", status: "FAIL", reason_code: "routing-overreach-orchestrator-multifile-edit", detail: `orchestrator directly edited ${directMultiFileEdit.fileCount} files at event ${directMultiFileEdit.index}` });
  }

  const firstNonTrivialImplementationIndex = events.findIndex(
    (event) => ["orchestrator", "fixer"].includes(event.agent) && event.action === "implement" && (event.nonTrivial || event.fileCount >= 2),
  );
  const plannerIndex = events.findIndex(
    (event) => event.agent === "orchestrator" && event.action === "delegate_plan" && event.delegatedTo === "artifact-planner",
  );
  if (firstNonTrivialImplementationIndex !== -1 && (plannerIndex === -1 || plannerIndex > firstNonTrivialImplementationIndex)) {
    actualReasonCodes.add("routing-overreach-missing-planner-first");
    violationChecks.push({ type: "transcript-semantics", status: "FAIL", reason_code: "routing-overreach-missing-planner-first", detail: `non-trivial implementation started at event ${firstNonTrivialImplementationIndex} before planner-first routing` });
  }

  const materialCompletionIndex = events.findIndex((event) => event.agent === "orchestrator" && event.action === "complete" && event.material);
  if (materialCompletionIndex !== -1) {
    const qualityGateIndex = events.findIndex(
      (event) => event.agent === "orchestrator" && event.action === "delegate_review" && event.delegatedTo === "quality-gate",
    );
    if (qualityGateIndex === -1 || qualityGateIndex > materialCompletionIndex) {
      actualReasonCodes.add("routing-overreach-missing-quality-gate");
      violationChecks.push({ type: "transcript-semantics", status: "FAIL", reason_code: "routing-overreach-missing-quality-gate", detail: `material completion happened at event ${materialCompletionIndex} before quality-gate review` });
    }
  }

  const expectedReasonCodes = (fixture.expectedReasonCodes ?? []).slice().sort();
  const actualReasonCodesSorted = Array.from(actualReasonCodes).sort();
  const missingExpected = expectedReasonCodes.filter((code) => !actualReasonCodesSorted.includes(code));
  const unexpected = actualReasonCodesSorted.filter((code) => !expectedReasonCodes.includes(code));
  const expectationMismatch = missingExpected.length > 0 || unexpected.length > 0;
  const checks = [];

  if (expectationMismatch) {
    checks.push(...violationChecks);
    checks.push({ type: "transcript-expectation", status: "FAIL", reason_code: "transcript-routing-expectation-mismatch", missing: missingExpected, forbidden: unexpected });
  } else if (violationChecks.length > 0) {
    checks.push({
      type: "transcript-expectation",
      status: "PASS",
      detail: `transcript matched expected routing reason codes: ${actualReasonCodesSorted.join(", ")}`,
    });
    checks.push(...violationChecks.map((check) => ({ ...check, status: "PASS" })));
  }

  if (checks.length === 0) {
    checks.push({ type: "transcript-semantics", status: "PASS", detail: "transcript matched expected routing behavior" });
  }

  return {
    id: fixture.id,
    description: fixture.description,
    category: fixture.category ?? "transcript-behavior",
    status: expectationMismatch ? "FAIL" : "PASS",
    checks,
  };
}
