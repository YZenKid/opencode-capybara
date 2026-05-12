import { existsSync, readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import { normalizeShareExportFixture } from "./share-export-adapter.mjs";

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

function validateTranscriptFixtureSchema(fixture) {
  const errors = [];
  if (!fixture || typeof fixture !== "object") {
    return ["fixture must be a JSON object"];
  }

  if (typeof fixture.id !== "string" || fixture.id.length === 0) {
    errors.push("fixture.id must be a non-empty string");
  }

  if (typeof fixture.description !== "string" || fixture.description.length === 0) {
    errors.push("fixture.description must be a non-empty string");
  }

  const sourceKeys = ["events", "rawTranscript", "rawToolTrace", "shareExport"].filter((key) => key in fixture);
  if (sourceKeys.length !== 1) {
    errors.push("fixture must define exactly one source: events, rawTranscript, rawToolTrace, or shareExport");
  }

  if (fixture.expectedReasonCodes && !Array.isArray(fixture.expectedReasonCodes)) {
    errors.push("fixture.expectedReasonCodes must be an array when present");
  }

  if (fixture.expectedScoreRange) {
    const validRange = Array.isArray(fixture.expectedScoreRange)
      && fixture.expectedScoreRange.length === 2
      && fixture.expectedScoreRange.every((value) => Number.isInteger(value) && value >= 0 && value <= 5)
      && fixture.expectedScoreRange[0] <= fixture.expectedScoreRange[1];
    if (!validRange) {
      errors.push("fixture.expectedScoreRange must be a two-item integer array between 0 and 5");
    }
  }

  if (fixture.releaseCritical != null && typeof fixture.releaseCritical !== "boolean") {
    errors.push("fixture.releaseCritical must be boolean when present");
  }

  return errors;
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

function inferAgent(text) {
  const lower = text.toLowerCase();
  const prefixMatch = lower.match(/^([a-z0-9\-]+)\s*:/);
  if (prefixMatch) return prefixMatch[1];
  if (lower.includes("quality-gate")) return "quality-gate";
  if (lower.includes("artifact-planner") || lower.includes("planner")) return "artifact-planner";
  if (lower.includes("explorer")) return "explorer";
  if (lower.includes("fixer")) return "fixer";
  if (lower.includes("orchestrator")) return "orchestrator";
  return "unknown";
}

function inferDelegatedTo(text) {
  const lower = text.toLowerCase();
  if (lower.includes("quality-gate")) return "quality-gate";
  if (lower.includes("artifact-planner") || lower.includes("planner")) return "artifact-planner";
  if (lower.includes("explorer")) return "explorer";
  if (lower.includes("fixer")) return "fixer";
  return null;
}

function inferAction(text) {
  const lower = text.toLowerCase();
  if (lower.includes("delegate") && lower.includes("discover")) return "delegate_discovery";
  if (lower.includes("delegate") && lower.includes("plan")) return "delegate_plan";
  if (lower.includes("delegate") && (lower.includes("implement") || lower.includes("fixer"))) return "delegate_implementation";
  if (lower.includes("delegate") && (lower.includes("review") || lower.includes("quality-gate"))) return "delegate_review";
  if (lower.includes("discover")) return "discover";
  if (lower.includes("read")) return "read";
  if (lower.includes("edit") || lower.includes("patch")) return "edit";
  if (lower.includes("implement")) return "implement";
  if (lower.includes("review")) return "review";
  if (lower.includes("complete") || lower.includes("done") || lower.includes("final summary")) return "complete";
  if (lower.includes("plan")) return "plan";
  return "unknown";
}

function inferFileCount(text, fallback = 0) {
  const explicit = text.match(/(\d+)\s+files?/i);
  if (explicit) return Number(explicit[1]);
  return Number(fallback ?? 0);
}

function inferMaterial(text) {
  const lower = text.toLowerCase();
  return lower.includes("material") || lower.includes("release") || lower.includes("done") || lower.includes("complete");
}

function inferNonTrivial(text, fallbackFileCount = 0) {
  const lower = text.toLowerCase();
  return lower.includes("non-trivial") || lower.includes("multi-file") || lower.includes("bounded implementation") || fallbackFileCount >= 2;
}

function normalizeRawTranscriptEntry(entry, index) {
  const text = typeof entry === "string" ? entry : JSON.stringify(entry);
  const fileCount = typeof entry === "object" && entry !== null
    ? Number(entry.fileCount ?? (Array.isArray(entry.files) ? entry.files.length : 0))
    : inferFileCount(text);
  return {
    index,
    agent: typeof entry === "object" && entry !== null ? (entry.agent ?? inferAgent(text)) : inferAgent(text),
    action: typeof entry === "object" && entry !== null ? (entry.action ?? inferAction(text)) : inferAction(text),
    fileCount,
    material: typeof entry === "object" && entry !== null ? Boolean(entry.material ?? inferMaterial(text)) : inferMaterial(text),
    nonTrivial: typeof entry === "object" && entry !== null ? Boolean(entry.nonTrivial ?? inferNonTrivial(text, fileCount)) : inferNonTrivial(text, fileCount),
    delegatedTo: typeof entry === "object" && entry !== null ? (entry.delegatedTo ?? inferDelegatedTo(text)) : inferDelegatedTo(text),
    notes: typeof entry === "object" && entry !== null ? (entry.notes ?? text) : text,
  };
}

function normalizeTranscriptFixture(fixture) {
  if (fixture.events) {
    return {
      sourceMode: "normalized-events",
      events: normalizeTranscriptEvents(fixture.events),
    };
  }

  if (fixture.rawTranscript) {
    const entries = Array.isArray(fixture.rawTranscript)
      ? fixture.rawTranscript
      : String(fixture.rawTranscript)
          .split("\n")
          .map((line) => line.trim())
          .filter(Boolean);
    return {
      sourceMode: "raw-transcript",
      events: entries.map((entry, index) => normalizeRawTranscriptEntry(entry, index)),
    };
  }

  if (fixture.rawToolTrace) {
    return {
      sourceMode: "raw-tool-trace",
      events: fixture.rawToolTrace.map((entry, index) => normalizeRawTranscriptEntry(entry, index)),
    };
  }

  if (fixture.shareExport) {
    return normalizeShareExportFixture(fixture.shareExport, normalizeRawTranscriptEntry);
  }

  return {
    sourceMode: "empty",
    events: [],
  };
}

function scoreBandFromValue(score) {
  if (score >= 5) return "excellent";
  if (score >= 4) return "strong";
  if (score >= 3) return "usable";
  if (score >= 1) return "weak";
  return "failed";
}

function confidenceFromSourceMode(sourceMode, eventCount) {
  if (sourceMode === "normalized-events") return "high";
  if (sourceMode === "share-export") return eventCount >= 5 ? "medium" : "low";
  if (sourceMode === "raw-tool-trace") return eventCount >= 5 ? "medium" : "low";
  if (sourceMode === "raw-transcript") return eventCount >= 8 ? "medium" : "low";
  return "low";
}

function computeRoutingScore(context) {
  const sparseTrace = context.events.length < 2;
  const laneFit = !context.actualReasonCodes.has("routing-overreach-redundant-orchestrator-discovery")
    && !context.actualReasonCodes.has("routing-overreach-orchestrator-multifile-edit");
  const thresholdCompliance = !context.events.some(
    (event) => event.agent === "orchestrator" && ((event.action === "edit" && event.fileCount >= 2) || (event.action === "read" && event.fileCount > 3)),
  );
  const plannerFirst = !sparseTrace && !context.actualReasonCodes.has("routing-overreach-missing-planner-first");
  const evidenceLegibilityProxy = context.events.some((event) => event.agent === "orchestrator" && event.action.startsWith("delegate_"));
  const finalGatePresence = !sparseTrace && !context.actualReasonCodes.has("routing-overreach-missing-quality-gate");

  const dimensions = {
    lane_fit: laneFit,
    threshold_compliance: thresholdCompliance,
    planner_first: plannerFirst,
    evidence_legibility_proxy: evidenceLegibilityProxy,
    final_gate_presence: finalGatePresence,
  };

  const score = Object.values(dimensions).filter(Boolean).length;
  return {
    score_0_to_5: score,
    score_band: scoreBandFromValue(score),
    dimensions,
    coverage: {
      event_count: context.events.length,
      source_mode: context.sourceMode,
      has_material_claim: context.events.some((event) => event.material),
      has_non_trivial_work: context.events.some((event) => event.nonTrivial),
      has_delegation: context.events.some((event) => event.action.startsWith("delegate_")),
    },
    confidence: confidenceFromSourceMode(context.sourceMode, context.events.length),
    reasons: Object.entries(dimensions)
      .filter(([, value]) => !value)
      .map(([key]) => key),
  };
}

export function evaluateTranscriptFixture(fixture) {
  const schemaErrors = validateTranscriptFixtureSchema(fixture);
  if (schemaErrors.length > 0) {
    return {
      id: fixture?.id ?? "unknown-transcript-fixture",
      description: fixture?.description ?? "Invalid transcript fixture",
      category: fixture?.category ?? "transcript-behavior",
      transcript_source_mode: "invalid-schema",
      routing_score: {
        score_0_to_5: 0,
        score_band: "failed",
        dimensions: {
          lane_fit: false,
          threshold_compliance: false,
          planner_first: false,
          evidence_legibility_proxy: false,
          final_gate_presence: false,
        },
        coverage: {
          event_count: 0,
          source_mode: "invalid-schema",
          has_material_claim: false,
          has_non_trivial_work: false,
          has_delegation: false,
        },
        confidence: "low",
        reasons: ["invalid_transcript_fixture_schema"],
      },
      release_critical: Boolean(fixture?.releaseCritical),
      fixture_classification: fixture?.classification ?? "invalid",
      status: "FAIL",
      checks: schemaErrors.map((detail) => ({
        type: "transcript-schema",
        status: "FAIL",
        reason_code: "invalid-transcript-fixture-schema",
        detail,
      })),
    };
  }

  const normalized = normalizeTranscriptFixture(fixture);
  const events = normalized.events;
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

  const routingScore = computeRoutingScore({
    events,
    actualReasonCodes,
    sourceMode: normalized.sourceMode,
  });

  if (fixture.expectedScoreRange) {
    const [min, max] = fixture.expectedScoreRange;
    if (routingScore.score_0_to_5 < min || routingScore.score_0_to_5 > max) {
      checks.push({
        type: "transcript-score",
        status: "FAIL",
        reason_code: "transcript-routing-score-out-of-range",
        detail: `routing score ${routingScore.score_0_to_5} was outside expected range ${min}-${max}`,
      });
    }
  }

  const finalStatus = checks.some((check) => check.status === "FAIL") || expectationMismatch ? "FAIL" : "PASS";

  return {
    id: fixture.id,
    description: fixture.description,
    category: fixture.category ?? "transcript-behavior",
    transcript_source_mode: normalized.sourceMode,
    routing_score: routingScore,
    release_critical: Boolean(fixture.releaseCritical),
    fixture_classification: fixture.classification ?? "general",
    status: finalStatus,
    checks,
  };
}
