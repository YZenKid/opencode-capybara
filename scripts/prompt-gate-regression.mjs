#!/usr/bin/env node

import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

const checks = [
  {
    file: "oh-my-opencode-slim.json",
    name: "council plugin disable gate",
    mustInclude: [
      '"disabled_agents": [',
      '"council"',
    ],
  },
  {
    file: "agents/council.md",
    name: "local council subagent gate",
    mustInclude: [
      'mode: subagent',
      'hidden: false',
      'description: Multi-LLM consensus engine for high-confidence answers',
      'model: cliproxyapi/gpt-5.5',
      'opencode-council',
      'council_session: allow',
    ],
  },
  {
    file: "opencode.json",
    name: "agent architecture selection gate",
    mustInclude: [
      '"default_agent": "orchestrator"',
      '"plan": {',
      '"explore": {',
    ],
  },
  {
    file: "AGENTS.md",
    name: "global anti-slop and parity gates",
    mustInclude: [
      "numeric-only service icons",
      "blank image frames",
      "visual density",
      "production-like screenshots",
      "designer signoff",
      "generic hover-only motion is not enough",
      "reference/current/final evidence",
      "designer pass/fail review",
      "assume it is image-heavy until the designer proves otherwise",
      "image generation decision",
      "legal style-equivalent generation",
      "CSS placeholders",
    ],
  },
  {
    file: "AGENTS.md",
    name: "quality gate routing gate",
    mustInclude: [
      "@quality-gate",
      "final conformance/risk gate",
      "non-trivial/risky",
      "prompt/config changes",
      "security-sensitive changes",
      "task trivial",
    ],
  },
  {
    file: "agents/artifact-planner.md",
    name: "artifact planner design readiness gate",
    mustInclude: [
      "mode: primary",
      '"*": deny',
      "explorer: allow",
      "librarian: allow",
      "oracle: allow",
      "council: allow",
      "observer: allow",
      "document-specialist: allow",
      "bash: ask",
      "apply_patch: deny",
      "write:",
      ".opencode/plans/",
      ".opencode/draft/",
      ".opencode/evidence/",
      "Design Readiness Gate",
      "motion storyboard",
      "icon matrix",
      "visual density rubric",
      "asset manifest summary",
      "image generation decision",
      "reference/current captures",
      "generated-assets.md",
      "final-designer-review.md",
      "assume image-heavy until the visual spec proves otherwise",
      "legal style-equivalent generation by default",
      "informational, read-only, research, and documentation subagents",
      "fixer, designer, or visual-asset-generator",
      "write the plan and stop",
    ],
  },
  {
    file: "skills/opencode-artifact-planner/SKILL.md",
    name: "artifact planner standalone skill gate",
    mustInclude: [
      "informational, read-only, research, and documentation subagents",
      "fixer, designer, or visual-asset-generator",
      "write the plan and stop",
      "Design Readiness Gate",
      "motion storyboard",
      "icon matrix",
      "visual density rubric",
      "asset manifest",
      "image generation decision",
      "reference/current captures",
      "generated-assets.md",
      "final designer review",
      "visual-comparison.md",
      "assume image-heavy until proven otherwise",
      "no-generation-needed",
    ],
  },
  {
    file: "agents/orchestrator.md",
    name: "orchestrator primary mode gate",
    mustInclude: [
      "mode: primary",
      "router/integrator",
      "direct edits only when the change is tiny",
      "do not issue a final completion claim",
      "@skill-improver",
      "@quality-gate",
    ],
  },
  {
    file: "agents/quality-gate.md",
    name: "quality gate subagent gate",
    mustInclude: [
      "mode: subagent",
      "hidden: false",
      "Final conformance and risk gate for non-trivial OpenCode work",
      "model: cliproxyapi/gpt-5.5",
      "opencode-quality-gate",
      "apply_patch: deny",
      "task: deny",
      "bash: ask",
      "external_directory:",
      "{env:HOME}/.config/opencode/skills/opencode-quality-gate/*",
      "PASS_WITH_RISKS",
      "NEEDS_FIX",
      "BLOCKED",
    ],
  },
  {
    file: "agents/build.md",
    name: "build subagent retired gate",
    mustInclude: [
      "mode: subagent",
      "hidden: true",
      "retired",
    ],
  },
  {
    file: "agents/skill-improver.md",
    name: "skill improver subagent gate",
    mustInclude: [
      "mode: subagent",
      "hidden: true",
      "opencode-skill-improver",
      "bounded post-task skill improvement subagent",
      "secret",
      "prompt bloat",
      "blind external updates",
    ],
  },
  {
    file: "skills/opencode-skill-improver/SKILL.md",
    name: "skill improver standalone skill gate",
    mustInclude: [
      "skill-creator",
      "post-task improvement checkpoint",
      "baseline",
      "with-skill",
      "evals",
      "prompt bloat",
      "secret",
      "blind external updates",
      "instruction conflicts",
      "trigger description optimization",
    ],
  },
  {
    file: "skills/opencode-designer/SKILL.md",
    name: "designer signoff contract",
    mustInclude: [
      "ready",
      "blocked",
      "needs-polish",
      "motion storyboard",
      "icon system matrix",
      "visual density checklist",
      "asset manifest",
      "image generation decision",
      "final pass/fail comparison",
      "assume image-heavy until proven otherwise",
      "legal style-equivalent generation by default",
      "dev overlays",
      "blank image frames",
      "numeric-only service icons",
      "missing planned sections",
      "Generated asset art direction gate",
      "art direction brief",
      "style board",
      "visual thesis",
      "reference traits",
      "composition notes",
      "generic AI aesthetics",
      "floating UI cards without domain meaning",
      "same-looking thumbnails",
    ],
  },
  {
    file: "agents/orchestrator.md",
    name: "orchestrator UI hard stop",
    mustInclude: [
      "reference/current/final evidence",
      "motion storyboard",
      "icon strategy",
      "asset manifest",
      "image generation decision",
      "visual-asset-generator",
      "assume image-heavy",
      "final designer pass/fail review",
      "draft",
      "blocked",
      "do not issue a final completion claim",
    ],
  },
  {
    file: "skills/opencode-orchestrator/SKILL.md",
    name: "orchestrator standalone parity contract",
    mustInclude: [
      "motion storyboard",
      "icon strategy",
      "visual density checks",
      "image generation decision",
      "visual-asset-generator",
      "assume image-heavy",
      "designer signoff",
      "evidence paths",
      "draft",
      "inspired by",
      "style-equivalent",
      "close parity",
      "@skill-improver",
      "@quality-gate",
    ],
  },
  {
    file: "skills/opencode-quality-gate/SKILL.md",
    name: "quality gate standalone skill",
    mustInclude: [
      "final reviewer read-only",
      "plan/evidence/diff/validation",
      "security/secrets/dependency",
      "docs/config drift",
      "UI/release gate",
      "PASS_WITH_RISKS",
      "NEEDS_FIX",
      "BLOCKED",
      "No edit, no autofix",
    ],
  },
  {
    file: "agents/build.md",
    name: "build agent UI pause gates",
    mustInclude: [
      "hover-only polish",
      "production-like screenshots",
      "section-by-section review",
      "draft vs reference-ready status",
      "motion storyboard",
      "icon strategy",
      "asset manifest",
      "image generation decision",
      "numeric-only icons",
      "blank frames",
      "fake controls",
      "CSS-only placeholders",
    ],
  },
  {
    file: "skills/opencode-build/SKILL.md",
    name: "build skill UI pause gates",
    mustInclude: [
      "production-like screenshots",
      "visual comparison notes",
      "draft vs reference-ready status",
      "motion storyboard",
      "icon strategy",
      "asset manifest",
      "image generation decision",
      "generic gradients",
      "blank frames",
      "generic hover-only effects",
    ],
  },
  {
    file: "skills/opencode-fixer/SKILL.md",
    name: "fixer skill UI pause gates",
    mustInclude: [
      "production-like evidence",
      "icon audit",
      "motion audit",
      "draft vs reference-ready status",
      "motion storyboard",
      "icon system",
      "asset manifest",
      "image generation decision",
      "numeric-only icons",
      "fake controls",
      "blank image frames",
      "generic gradients",
      "generic hover-only motion",
    ],
  },
  {
    file: "agents/visual-asset-generator.md",
    name: "visual asset generator manifest and icon rules",
    mustInclude: [
      "icon strategy",
      "image generation decision",
      "section-aware palette notes",
      "legal notes",
      "reject manifests",
      "executable jobs",
      "CSS placeholders",
      "proper icon library",
      "generic generated symbols",
      "art direction",
      "style board",
      "reference traits",
      "composition notes",
      "quality_bar",
      "reject_if",
      "differentiator",
      "professional art director",
      "generic tech dashboard",
      "futuristic",
      "cyberpunk",
      "abstract UI",
    ],
  },
  {
    file: "skills/opencode-visual-asset-generator/SKILL.md",
    name: "visual asset generator standalone manifest rules",
    mustInclude: [
      "icon strategy",
      "image generation decision",
      "art direction",
      "style board",
      "reference traits",
      "composition notes",
      "quality_bar",
      "reject_if",
      "differentiator",
      "professional art director",
      "explicit legal notes",
      "return error instead of guessing",
      "return executable jobs",
      "no-generation-needed",
      "Generated icons are only acceptable for decorative badges",
      "proper icon library",
      "designer review before visual parity claims",
    ],
  },
  {
    file: "README.md",
    name: "skill improver documentation gate",
    mustInclude: [
      "@skill-improver",
      "non-trivial",
      "repeated failures",
      "policy gaps",
      "explicit request",
      "no blind external updates",
      "build retired",
      "general retired",
      "@quality-gate",
      "PASS_WITH_RISKS",
      "NEEDS_FIX",
      "BLOCKED",
    ],
  },
  {
    file: "oh-my-opencode-slim.json",
    name: "quality gate preset gate",
    mustInclude: [
      "quality-gate",
      "opencode-quality-gate",
      "github",
      "semgrep",
      "playwright",
      "grep_app",
    ],
  },
];

const portabilityChecks = [
  "AGENTS.md",
  "agents/orchestrator.md",
  "agents/build.md",
  "agents/artifact-planner.md",
  "agents/general.md",
  "agents/visual-asset-generator.md",
  "skills/opencode-orchestrator/SKILL.md",
  "skills/opencode-visual-asset-generator/SKILL.md",
  "skills/opencode-build/SKILL.md",
  "skills/opencode-fixer/SKILL.md",
  "skills/opencode-artifact-planner/SKILL.md",
  "opencode.json",
  "scripts/prompt-gate-regression.mjs",
];

const duplicates = [
  {
    file: "skills/opencode-build/SKILL.md",
    text: "If the motion storyboard, icon strategy, or asset manifest is missing on a substantial UI task",
    max: 1,
  },
  {
    file: "skills/opencode-fixer/SKILL.md",
    text: "For substantial UI/reference/image-heavy work, do not close on screenshots alone",
    max: 1,
  },
];

const forbiddenPaths = ["/home/" + "ujang", "/Users/" + "ujang"];

let failures = 0;

function read(file) {
  const absolute = resolve(root, file);
  if (!existsSync(absolute)) {
    failures += 1;
    console.error(`✗ ${file}: file missing`);
    return null;
  }
  return readFileSync(absolute, "utf8");
}

function checkPortability() {
  for (const file of portabilityChecks) {
    const content = read(file);
    if (content === null) continue;

    for (const forbidden of forbiddenPaths) {
      if (content.includes(forbidden)) {
        failures += 1;
        console.error(`✗ ${file}: contains hardcoded path ${forbidden.replace("ujang", "<user>")}`);
      }
    }

    if (file === "opencode.json" && content.includes("./bin/image-asset-mcp.mjs")) {
      failures += 1;
      console.error(`✗ ${file}: image-asset-generator still uses ./bin/image-asset-mcp.mjs`);
    }

    if (
      ["agents/visual-asset-generator.md", "skills/opencode-visual-asset-generator/SKILL.md"].includes(file)
    ) {
      const requiredPhrases = [
        "Never hardcode device-specific absolute paths",
        "active workspace/project root",
        "OpenCode config root",
        "target app `project_root`",
        "target_path` relative to that root",
      ];
      const missing = requiredPhrases.filter((phrase) => !content.includes(phrase));
      if (missing.length > 0) {
        failures += 1;
        console.error(`✗ ${file}: missing portability phrases:`);
        for (const phrase of missing) console.error(`  - ${phrase}`);
      }
    }
  }
}

function checkRootFilesForPortability() {
  const rootFiles = ["AGENTS.md", "agents/orchestrator.md", "agents/build.md", "agents/artifact-planner.md", "agents/general.md", "agents/visual-asset-generator.md", "skills/opencode-orchestrator/SKILL.md", "skills/opencode-visual-asset-generator/SKILL.md", "scripts/prompt-gate-regression.mjs", "opencode.json"];
  for (const file of rootFiles) {
    const content = read(file);
    if (content === null) continue;
    for (const forbidden of forbiddenPaths) {
      if (content.includes(forbidden)) {
        failures += 1;
        console.error(`✗ ${file}: contains hardcoded path ${forbidden.replace("ujang", "<user>")}`);
      }
    }
  }
}

for (const check of checks) {
  const content = read(check.file);
  if (content === null) continue;

  const missing = check.mustInclude.filter((needle) => !content.includes(needle));
  if (missing.length > 0) {
    failures += 1;
    console.error(`✗ ${check.file} (${check.name}) missing:`);
    for (const item of missing) console.error(`  - ${item}`);
  } else {
    console.log(`✓ ${check.file} (${check.name})`);
  }
}

for (const check of duplicates) {
  const content = read(check.file);
  if (content === null) continue;
  const count = content.split(check.text).length - 1;
  if (count > check.max) {
    failures += 1;
    console.error(`✗ ${check.file}: duplicate phrase appears ${count} times (max ${check.max})`);
    console.error(`  - ${check.text}`);
  } else {
    console.log(`✓ ${check.file} duplicate guard (${count}/${check.max})`);
  }
}

checkPortability();
checkRootFilesForPortability();

if (failures > 0) {
  console.error(`\nPrompt gate regression failed with ${failures} issue(s).`);
  process.exit(1);
}

console.log("\nPrompt gate regression passed.");
