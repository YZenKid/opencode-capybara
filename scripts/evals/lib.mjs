import { copyFileSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { execFileSync, spawn } from "node:child_process";
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

function ensureDir(dir) {
  mkdirSync(dir, { recursive: true });
}

function copyTree(sourceDir, targetDir) {
  ensureDir(targetDir);
  for (const entry of readdirSync(sourceDir)) {
    const sourcePath = resolve(sourceDir, entry);
    const targetPath = resolve(targetDir, entry);
    const stats = statSync(sourcePath);
    if (stats.isDirectory()) {
      copyTree(sourcePath, targetPath);
    } else {
      ensureDir(resolve(targetPath, ".."));
      copyFileSync(sourcePath, targetPath);
    }
  }
}

function listFilesRecursive(dir, baseDir = dir) {
  if (!existsSync(dir)) return [];
  const files = [];
  for (const entry of readdirSync(dir)) {
    const entryPath = resolve(dir, entry);
    const stats = statSync(entryPath);
    if (stats.isDirectory()) {
      files.push(...listFilesRecursive(entryPath, baseDir));
    } else {
      files.push(entryPath.replace(`${baseDir}/`, ""));
    }
  }
  return files.sort();
}

const initHarnessCanonicalDocs = [
  "index.md",
  "ARCHITECTURE.md",
  "AGENT_ROUTING.md",
  "AGENT_LEGIBILITY.md",
  "QUALITY.md",
  "QUALITY_SCORE.md",
  "SECURITY.md",
  "PROMPT_GATES.md",
  "SKILLS.md",
  "MCP.md",
  "TOOL_USAGE.md",
  "AGENT_TOOL_ACCESS.md",
  "EVALS.md",
  "GOLDEN_PRINCIPLES.md",
  "DECISIONS.md",
  "RELEASE.md",
  "GC_WORKFLOW.md",
];

const initHarnessGeneratedAgents = `# AGENTS.md

## Start Here
- Routing rules: \`.opencode/docs/AGENT_ROUTING.md\`
- Architecture: \`.opencode/docs/ARCHITECTURE.md\`
- Quality and evidence: \`.opencode/docs/QUALITY.md\`
- Harness evals and replayability: \`.opencode/docs/EVALS.md\`
- Project stack and tool detection: \`.opencode/docs/PROJECT_STACK.md\`, \`.opencode/docs/PROJECT_DETECTED_TOOLS.md\` when present
- Project framework commands/playbook: \`.opencode/docs/PROJECT_COMMANDS.md\`, \`.opencode/docs/FRAMEWORK_PLAYBOOK.md\` when present
- Security policy: \`.opencode/docs/SECURITY.md\`
- Prompt gates: \`.opencode/docs/PROMPT_GATES.md\`
- Skills index: \`.opencode/docs/SKILLS.md\`
- MCP overview: \`.opencode/docs/MCP.md\`
- Golden principles: \`.opencode/docs/GOLDEN_PRINCIPLES.md\`
- Agent legibility: \`.opencode/docs/AGENT_LEGIBILITY.md\`
- Decisions log: \`.opencode/docs/DECISIONS.md\`
- Release and operational readiness: \`.opencode/docs/RELEASE.md\`
- Quality score and GC workflow: \`.opencode/docs/QUALITY_SCORE.md\`, \`.opencode/docs/GC_WORKFLOW.md\`

## Non-negotiable Rules
- Use \`@orchestrator\` for routing and integration.
- Use \`@quality-gate\` for material changes, including non-trivial/risky work, prompt/config changes, and security-sensitive changes.
- Harness Preflight Gate: before non-trivial work, \`@orchestrator\` must verify the target project has a current root \`AGENTS.md\`, canonical \`.opencode/docs/\`, and root \`DESIGN.md\` when UI/design work is involved.
- For framework-managed artifacts, follow project-local \`.opencode/docs/PROJECT_STACK.md\`, \`.opencode/docs/PROJECT_COMMANDS.md\`, \`.opencode/docs/FRAMEWORK_PLAYBOOK.md\`, and \`.opencode/docs/PROJECT_DETECTED_TOOLS.md\` before manual edits when those docs are present.
- If harness guidance is missing/stale, run \`/init-harness\` first, or ask the user to run \`/init-harness\` when command execution is unavailable. Skip only for tiny, read-only, or emergency tasks and record the skip reason in the final summary.
- Prefer evidence over assertion.
- Prefer references over assumptions.
- Prefer repo-local docs over chat memory.
- Keep this file short and map-like.

## Default Flow
User intent → \`@orchestrator\` → specialist agents → validation → \`@quality-gate\` → final summary.

## Harness Posture
- \`.opencode/docs/\` is the repository knowledge system of record.
- \`AGENTS.md\` is the map, not the encyclopedia.
- Plans are first-class artifacts under \`.opencode/plans/\`.
- Runtime state lives under \`.opencode/state/\` for durable runs, task queues, mailbox, memory, and worktree metadata.
- Evidence is required for material changes.
- \`@orchestrator\` routes, decomposes, and integrates; do not let all implementation collapse into direct orchestrator execution.

## Risk Triggers
- Product/SaaS/platform/AI/UI-system architecture ambiguity → \`@architect\`
- Security/privacy/accessibility/visual-parity final signoff → \`@quality-gate\`
- User-facing UI/reference/animation/accessibility/design-system design direction → \`@designer\`
- Shared tokens/primitives/themes/component APIs → \`@design-system-engineer\`
- Current library/API docs lookup when local context is insufficient → supporting \`@librarian\` research lane

## Notes
- Future operators should read \`.opencode/docs/index.md\` first, then follow the canonical docs by concern.
- Keep this file short and map-like.
`;

function runShell(script, cwd) {
  return execFileSync("sh", ["-lc", script], {
    cwd,
    encoding: "utf8",
    stdio: "pipe",
    timeout: 300000,
  });
}

function prepareInitHarnessTempRepo(root, fixture) {
  const seedRoot = resolve(root, fixture.execute.seedRoot);
  const tempRoot = mkdtempSync(join(tmpdir(), "opencode-init-harness-"));
  copyTree(seedRoot, tempRoot);

  const docsTargetDir = resolve(tempRoot, ".opencode", "docs");
  ensureDir(docsTargetDir);
  for (const file of initHarnessCanonicalDocs) {
    copyFileSync(resolve(root, ".opencode", "docs", file), resolve(docsTargetDir, file));
  }

  const designTemplate = resolve(root, "skills", "opencode-designer", "references", "DESIGN-MD-TEMPLATE.md");
  const registryTemplate = resolve(root, "skills", "opencode-design-system-engineer", "references", "DESIGN-SYSTEM-REGISTRY-TEMPLATE.md");
  const designTarget = resolve(tempRoot, "DESIGN.md");
  const registryTarget = resolve(tempRoot, ".opencode", "design-system", "registry.md");
  const catalogTarget = resolve(tempRoot, ".opencode", "design-system", "catalog.json");
  if (!existsSync(designTarget) && existsSync(designTemplate)) {
    copyFileSync(designTemplate, designTarget);
  }
  if (!existsSync(registryTarget) && existsSync(registryTemplate)) {
    ensureDir(resolve(tempRoot, ".opencode", "design-system"));
    copyFileSync(registryTemplate, registryTarget);
  }
  if (!existsSync(catalogTarget)) {
    ensureDir(resolve(tempRoot, ".opencode", "design-system"));
    writeFileSync(catalogTarget, '{\n  "tokens": [],\n  "primitives": [],\n  "components": [],\n  "patterns": [],\n  "sources": {}\n}\n');
  }

  writeFileSync(resolve(tempRoot, "AGENTS.md"), initHarnessGeneratedAgents);

  return {
    fixtureRoot: tempRoot,
    execution: {
      mode: fixture.execute.mode,
      seed_root: fixture.execute.seedRoot,
      generated_files: listFilesRecursive(tempRoot),
      limitation: "Eval-only temp-repo scaffold adapter; does not execute the real /init-harness slash-command runtime.",
    },
    cleanup() {
      rmSync(tempRoot, { recursive: true, force: true });
    },
  };
}

function prepareInitHarnessRuntimeTempRepo(root, fixture) {
  const seedRoot = resolve(root, fixture.execute.seedRoot);
  const tempRoot = mkdtempSync(join(tmpdir(), "opencode-init-harness-runtime-"));
  copyTree(seedRoot, tempRoot);

  const port = 43000 + Math.floor(Math.random() * 1000);
  const logFile = resolve(tempRoot, ".opencode-runtime.log");
  const stdoutFile = resolve(tempRoot, ".opencode-run.stdout.log");
  const stderrFile = resolve(tempRoot, ".opencode-run.stderr.log");
  const runtimeMessage = fixture.execute.runtimeMessage ?? "/init-harness";
  const serverUrl = `http://127.0.0.1:${port}`;
  const logHandle = writeFileSync(logFile, "");
  const logFd = readFileSync(logFile, "utf8");
  void logHandle;
  void logFd;
  const server = spawn("opencode", ["serve", "--pure", "--hostname", "127.0.0.1", "--port", String(port)], {
    cwd: root,
    detached: false,
    stdio: ["ignore", "ignore", "ignore"],
  });

  let ready = false;
  for (let attempt = 0; attempt < 100; attempt += 1) {
    try {
      const output = execFileSync("sh", ["-lc", `curl -fsS ${JSON.stringify(serverUrl)} >/dev/null`], {
        cwd: root,
        encoding: "utf8",
        stdio: "pipe",
        timeout: 2000,
      });
      void output;
      ready = true;
      break;
    } catch {
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 200);
    }
  }

  if (!ready) {
    server.kill("SIGTERM");
    throw new Error(`opencode serve did not become ready at ${serverUrl}`);
  }

  const stdout = execFileSync("opencode", [
    "run",
    "--pure",
    "--dangerously-skip-permissions",
    "--attach",
    serverUrl,
    "--dir",
    tempRoot,
    runtimeMessage,
  ], {
    cwd: root,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    timeout: 300000,
  });
  writeFileSync(stdoutFile, stdout);
  writeFileSync(stderrFile, "");
  server.kill("SIGTERM");

  return {
    fixtureRoot: tempRoot,
    execution: {
      mode: fixture.execute.mode,
      seed_root: fixture.execute.seedRoot,
      server_url: serverUrl,
      runtime_message: runtimeMessage,
      generated_files: listFilesRecursive(tempRoot),
      stdout: readTextOrNull(stdoutFile) ?? "",
      stderr: readTextOrNull(stderrFile) ?? "",
      limitation: "Uses the real local opencode runtime via serve+attach in a temp repo, but still depends on the locally installed runtime version and environment.",
    },
    cleanup() {
      server.kill("SIGTERM");
      rmSync(tempRoot, { recursive: true, force: true });
    },
  };
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

function prepareScriptRunTempRepo(root, fixture) {
  const seedRoot = resolve(root, fixture.execute.seedRoot);
  const tempRoot = mkdtempSync(join(tmpdir(), "opencode-script-run-"));
  copyTree(seedRoot, tempRoot);
  const command = fixture.execute.command;
  let stdout = "";
  let stderr = "";
  let exit_code = 0;
  try {
    stdout = execFileSync("sh", ["-lc", command], {
      cwd: tempRoot,
      encoding: "utf8",
      stdio: "pipe",
      timeout: fixture.execute.timeoutMs ?? 20000,
    });
  } catch (error) {
    stdout = error.stdout ?? "";
    stderr = error.stderr ?? "";
    exit_code = error.status ?? 1;
    const allowed = fixture.execute.allowedExitCodes ?? [0, 1];
    if (!allowed.includes(exit_code)) {
      throw error;
    }
  }
  return {
    fixtureRoot: tempRoot,
    execution: {
      mode: fixture.execute.mode,
      seed_root: fixture.execute.seedRoot,
      command,
      stdout,
      stderr,
      exit_code,
      generated_files: listFilesRecursive(tempRoot),
      limitation: "Eval-only temp-repo script execution; uses local scripts and seed fixture files.",
    },
    cleanup() {
      rmSync(tempRoot, { recursive: true, force: true });
    },
  };
}

export function evaluateTaskFixture(root, fixture) {
  let fixtureRoot = fixture.root ? resolve(root, fixture.root) : root;
  let execution = null;
  let cleanup = null;
  if (fixture.execute?.mode === "init-harness-scaffold") {
    const prepared = prepareInitHarnessTempRepo(root, fixture);
    fixtureRoot = prepared.fixtureRoot;
    execution = prepared.execution;
    cleanup = prepared.cleanup;
  } else if (fixture.execute?.mode === "opencode-runtime-init-harness") {
    const prepared = prepareInitHarnessRuntimeTempRepo(root, fixture);
    fixtureRoot = prepared.fixtureRoot;
    execution = prepared.execution;
    cleanup = prepared.cleanup;
  } else if (fixture.execute?.mode === "script-run") {
    const prepared = prepareScriptRunTempRepo(root, fixture);
    fixtureRoot = prepared.fixtureRoot;
    execution = prepared.execution;
    cleanup = prepared.cleanup;
  }
  const checks = [];
  let failed = false;

  try {
    for (const artifact of fixture.artifacts ?? []) {
      const target = resolve(fixtureRoot, artifact.file);
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
  } finally {
    cleanup?.();
  }

  return {
    id: fixture.id,
    description: fixture.description,
    category: fixture.category ?? "behavioral-task",
    status: failed ? "FAIL" : "PASS",
    checks,
    execution,
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
    userFacing: event.userFacing == null ? null : Boolean(event.userFacing),
    internalOnly: event.internalOnly == null ? null : Boolean(event.internalOnly),
    blockerClass: event.blockerClass ?? null,
    advisoryStatus: event.advisoryStatus ?? null,
    continuationClass: event.continuationClass ?? null,
    violationCodes: Array.isArray(event.violationCodes) ? event.violationCodes : [],
    taskSize: event.taskSize ?? null,
    taskType: event.taskType ?? null,
    versionSensitive: Boolean(event.versionSensitive ?? false),
    sourceLookedUp: Boolean(event.sourceLookedUp ?? false),
    skippedSourceRationale: Boolean(event.skippedSourceRationale ?? false),
    broadUnknownScope: Boolean(event.broadUnknownScope ?? false),
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
    userFacing: typeof entry === "object" && entry !== null && entry.userFacing != null ? Boolean(entry.userFacing) : null,
    internalOnly: typeof entry === "object" && entry !== null && entry.internalOnly != null ? Boolean(entry.internalOnly) : null,
    blockerClass: typeof entry === "object" && entry !== null ? (entry.blockerClass ?? null) : null,
    advisoryStatus: typeof entry === "object" && entry !== null ? (entry.advisoryStatus ?? null) : null,
    continuationClass: typeof entry === "object" && entry !== null ? (entry.continuationClass ?? null) : null,
    violationCodes: typeof entry === "object" && entry !== null && Array.isArray(entry.violationCodes) ? entry.violationCodes : [],
    taskSize: typeof entry === "object" && entry !== null ? (entry.taskSize ?? null) : null,
    taskType: typeof entry === "object" && entry !== null ? (entry.taskType ?? null) : null,
    versionSensitive: typeof entry === "object" && entry !== null ? Boolean(entry.versionSensitive ?? false) : false,
    sourceLookedUp: typeof entry === "object" && entry !== null ? Boolean(entry.sourceLookedUp ?? false) : false,
    skippedSourceRationale: typeof entry === "object" && entry !== null ? Boolean(entry.skippedSourceRationale ?? false) : false,
    broadUnknownScope: typeof entry === "object" && entry !== null ? Boolean(entry.broadUnknownScope ?? false) : false,
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
    && !context.actualReasonCodes.has("routing-overreach-orchestrator-multifile-edit")
    && !context.actualReasonCodes.has("finish-first-premature-advisory-stop");
  const thresholdCompliance = !context.events.some(
    (event) => event.agent === "orchestrator" && ((event.action === "edit" && event.fileCount >= 2) || (event.action === "read" && event.fileCount > 3)),
  ) && !context.actualReasonCodes.has("final-output-raw-internal-passthrough");
  const plannerFirst = !sparseTrace && !context.actualReasonCodes.has("routing-overreach-missing-planner-first");
  const evidenceLegibilityProxy = context.events.some((event) => event.agent === "orchestrator" && event.action.startsWith("delegate_"))
    && !context.actualReasonCodes.has("final-output-raw-internal-passthrough");
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

  const tinyPlannerOveruse = events.find((event) => {
    if (event.agent !== "orchestrator" || event.action !== "delegate_plan" || event.delegatedTo !== "artifact-planner") return false;
    const note = String(event.notes ?? "").toLowerCase();
    return event.taskSize === "tiny" || note.includes("tiny typo") || note.includes("single-file reversible") || note.includes("one-file reversible");
  });
  if (tinyPlannerOveruse) {
    actualReasonCodes.add("routing-drift-planner-overuse-tiny-task");
    violationChecks.push({ type: "transcript-semantics", status: "FAIL", reason_code: "routing-drift-planner-overuse-tiny-task", detail: `artifact-planner used for tiny reversible task at event ${tinyPlannerOveruse.index}` });
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

  const broadFullstackCatchall = events.find((event) => {
    if (!(event.agent === "orchestrator" && event.action === "delegate_implementation" && event.delegatedTo === "fullstack")) return false;
    const note = String(event.notes ?? "").toLowerCase();
    return event.broadUnknownScope || note.includes("broad") || note.includes("unknown contract") || note.includes("catch-all") || note.includes("multiple bounded slices");
  });
  if (broadFullstackCatchall) {
    actualReasonCodes.add("routing-drift-fullstack-catchall");
    violationChecks.push({ type: "transcript-semantics", status: "FAIL", reason_code: "routing-drift-fullstack-catchall", detail: `fullstack used as broad catch-all at event ${broadFullstackCatchall.index}` });
  }

  const versionSensitiveWithoutSource = events.find((event) => {
    const note = String(event.notes ?? "").toLowerCase();
    const versionSensitive = event.versionSensitive || note.includes("version-sensitive") || note.includes("current api") || note.includes("sdk version") || note.includes("library api");
    const hasSource = event.sourceLookedUp || event.skippedSourceRationale || note.includes("source lookup") || note.includes("official docs") || note.includes("repo-local evidence") || note.includes("skipped-source rationale");
    return versionSensitive && !hasSource;
  });
  if (versionSensitiveWithoutSource) {
    actualReasonCodes.add("source-strategy-missing-for-version-sensitive-work");
    violationChecks.push({ type: "transcript-semantics", status: "FAIL", reason_code: "source-strategy-missing-for-version-sensitive-work", detail: `version-sensitive decision without source strategy at event ${versionSensitiveWithoutSource.index}` });
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

  const advisoryStopIndex = events.findIndex((event) => {
    if (event.agent !== "orchestrator") return false;
    if (!["complete", "review", "unknown"].includes(event.action)) return false;
    if (event.advisoryStatus === "advisory_only_stop" || event.blockerClass === "soft_blocker") return true;
    const note = String(event.notes ?? "").toLowerCase();
    return note.includes("needs-architect-decisions") || note.includes("material block exists") || note.includes("soft blocker") || note.includes("advisory_only") || note.includes("advisory stop") || note.includes("blocked by advisory");
  });
  const hasAdvisoryStopSignal = advisoryStopIndex !== -1;
  const hasSafeContinuation = advisoryStopIndex !== -1 && events.some((event) => {
    if (event.index <= advisoryStopIndex) return false;
    if (event.continuationClass === "safe_subset_continue") return true;
    if (event.agent === "orchestrator") {
      return ["implement", "edit", "discover", "delegate_implementation", "delegate_discovery"].includes(event.action);
    }
    return ["fixer", "explorer", "designer"].includes(event.agent) && ["implement", "edit", "discover"].includes(event.action);
  });
  const hasHardStopSignal = events.some((event) => {
    if (event.agent !== "orchestrator") return false;
    if (event.blockerClass === "hard_stop") return true;
    const note = String(event.notes ?? "").toLowerCase();
    return note.includes("hard_stop") || note.includes("destructive") || note.includes("irreversible") || note.includes("security boundary") || note.includes("privacy boundary") || note.includes("secrets boundary") || note.includes("missing required access") || note.includes("contradictory requirements");
  });
  if (hasAdvisoryStopSignal && !hasSafeContinuation && !hasHardStopSignal) {
    actualReasonCodes.add("finish-first-premature-advisory-stop");
    violationChecks.push({ type: "transcript-semantics", status: "FAIL", reason_code: "finish-first-premature-advisory-stop", detail: "orchestrator stopped after advisory soft blocker without safe subset continuation" });
  }

  const hasRawInternalPassthrough = events.some((event) => {
    if (event.agent !== "orchestrator") return false;
    if (event.userFacing === true && event.internalOnly === true) return true;
    const note = String(event.notes ?? "");
    const lower = note.toLowerCase();
    return ["task_result", "changed_files", "next_actions", "summary:", "findings:", "needs-architect-decisions", "status:"].some((token) => lower.includes(token));
  });
  if (hasRawInternalPassthrough) {
    actualReasonCodes.add("final-output-raw-internal-passthrough");
    violationChecks.push({ type: "transcript-semantics", status: "FAIL", reason_code: "final-output-raw-internal-passthrough", detail: "raw internal/subagent fields leaked into user-facing orchestrator output" });
  }

  const hasIndonesianFinal = events.some((event) => {
    if (event.agent !== "orchestrator") return false;
    if (event.action !== "complete") return false;
    const lower = String(event.notes ?? "").toLowerCase();
    return lower.includes("ringkasan") || lower.includes("lanjut") || lower.includes("risiko") || lower.includes("langkah");
  });
  if (!hasRawInternalPassthrough && hasIndonesianFinal) {
    violationChecks.push({ type: "transcript-semantics", status: "PASS", detail: "user-facing final output showed Indonesian normalization without raw internal fields" });
  }

  for (const event of events) {
    for (const violationCode of event.violationCodes ?? []) {
      if (typeof violationCode === "string" && violationCode.length > 0) {
        actualReasonCodes.add(violationCode);
      }
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
