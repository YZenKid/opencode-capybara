#!/usr/bin/env node

import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const upstreamPresetName = ["oh", "my", "opencode", "slim"].join("-");
const pluginPackageName = ["@opencode-ai", "plugin"].join("/");
const disabledAgentsKey = ["disabled", "agents"].join("_");

const checks = [
  {
    file: ".env.example",
    name: "model routing env example gate",
    mustInclude: [
      "OPENCODE_MODEL_DEFAULT=",
      "OPENCODE_MODEL_ORCHESTRATOR=",
      "OPENCODE_MODEL_PLANNER=",
      "OPENCODE_MODEL_DESIGN=",
      "OPENCODE_MODEL_REVIEW=",
      "OPENCODE_MODEL_ADVISORY=",
      "OPENCODE_MODEL_EXECUTION=",
      "OPENCODE_MODEL_DISCOVERY=",
      "OPENCODE_MODEL_DOCUMENTS=",
      "OPENCODE_MODEL_IMPROVEMENT=",
      "IMAGE_ASSET_MODEL=",
    ],
  },
  {
    file: "commands/init-design.md",
    name: "project design init command gate",
    mustInclude: [
      "Arguments from user",
      "$ARGUMENTS",
      "DESIGN.md",
      "design-system/DESIGN.md",
      "Visual Theme & Atmosphere",
      "Color Palette & Roles",
      "Typography Rules",
      "Component Stylings",
      "Layout Principles",
      "Depth & Elevation",
      "Do's and Don'ts",
      "Responsive Behavior",
      "Agent Prompt Guide",
      "ask before overwriting",
      "project-local",
    ],
  },
  {
    file: "agents/council.md",
    name: "local council subagent gate",
    mustInclude: [
      'mode: subagent',
      'hidden: false',
      'description: Multi-LLM consensus engine for high-confidence answers',
      'model: cliproxyapi/gpt-5.4',
      'opencode-council',
      'council_session: allow',
    ],
  },
  {
    file: "opencode.json",
    name: "agent architecture selection gate",
    mustInclude: [
      '"default_agent": "orchestrator"',
      '"model": "cliproxyapi/gpt-5.3-codex"',
      '"plan": {',
      '"explore": {',
    ],
  },
  {
    file: "AGENTS.md",
    name: "global anti-slop and parity gates",
    mustInclude: [
      "First inspect the target project's `DESIGN.md`",
      "design-system/DESIGN.md",
      "suggest `/init-design`",
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
    name: "global general design readiness gate",
    mustInclude: [
      "General Design Readiness Gate",
      "The target project's own `DESIGN.md` is the first design authority",
      "high-level visual direction is not enough",
      "UI/UX Design Blueprint",
      "Experience direction",
      "Page-by-page UX blueprint",
      "Section-level visual specification",
      "Component system plan",
      "Visual system",
      "Asset and image decision",
      "Motion system",
      "Interaction and state design",
      "Responsive plan",
      "Accessibility gate",
      "Validation evidence",
      "blocked`, `needs-polish`, or `draft`, not `done`",
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
    file: "AGENTS.md",
    name: "auto-commit policy gate",
    mustInclude: [
      "Default auto-commit is ON for local commits only",
      "plan-bound, non-trivial task",
      "validation has passed",
      "PASS_WITH_RISKS",
      "Never push automatically",
      "Never stage `.env`, secrets, tokens, credentials",
      "Never use `--no-verify`, `--no-gpg-sign`, `amend`",
      "stop and ask",
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
    file: "README.md",
    name: "model routing documentation gate",
    mustInclude: [
      "### Model routing table",
      "OPENCODE_MODEL_DEFAULT",
      "OPENCODE_MODEL_ORCHESTRATOR",
      "OPENCODE_MODEL_PLANNER",
      "OPENCODE_MODEL_DESIGN",
      "OPENCODE_MODEL_REVIEW",
      "OPENCODE_MODEL_ADVISORY",
      "OPENCODE_MODEL_EXECUTION",
      "OPENCODE_MODEL_DISCOVERY",
      "OPENCODE_MODEL_DOCUMENTS",
      "OPENCODE_MODEL_IMPROVEMENT",
      "Copy `.env.example` to `.env`",
      "Missing env vars resolve to an empty string",
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
    file: "agents/designer.md",
    name: "designer workflow gate",
    mustInclude: [
      "Before any UI/design direction",
      "target project's `DESIGN.md`",
      "design-system/DESIGN.md",
      "suggest `/init-design`",
      "artifact-first UI workflow",
      "DESIGN.md awareness",
      "artifact-mode output",
    ],
  },
  {
    file: "agents/orchestrator.md",
    name: "orchestrator primary mode gate",
    mustInclude: [
      "mode: primary",
      "router/integrator",
      "OPENCODE_MODEL_ORCHESTRATOR",
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
      "model: cliproxyapi/gpt-5.4",
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
    name: "redundant build agent removed gate",
    mustBeMissing: true,
  },
  {
    file: "agents/general.md",
    name: "redundant general agent removed gate",
    mustBeMissing: true,
  },
  {
    file: "agents/skill-improver.md",
    name: "skill improver subagent gate",
    mustInclude: [
      "mode: subagent",
      "hidden: true",
      "opencode-skill-improver",
      "OPENCODE_MODEL_IMPROVEMENT",
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
    file: "skills/opencode-designer/SKILL.md",
    name: "designer design-guide contract",
    mustInclude: [
      "Inspect the target project's `DESIGN.md`",
      "project's own `DESIGN.md` is the first design authority",
      "design-system/DESIGN.md",
      "/init-design",
      "project-local design guide",
    ],
  },
  {
    file: "skills/opencode-designer/SKILL.md",
    name: "designer general design readiness gate",
    mustInclude: [
      "General Design Readiness Gate",
      "high-level visual intent alone",
      "end-to-end UI/UX Design Blueprint",
      "Experience direction",
      "Page-by-page UX blueprint",
      "Section-level visual specification",
      "Component system plan",
      "Visual system",
      "Asset and image decision",
      "Motion system",
      "Interaction and state design",
      "Responsive plan",
      "Accessibility gate",
      "Validation evidence",
      "do not mark the design `ready`",
    ],
  },
  {
    file: "agents/orchestrator.md",
    name: "orchestrator UI hard stop",
    mustInclude: [
      "target project's `DESIGN.md`",
      "design-system/DESIGN.md",
      "suggest `/init-design`",
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
    file: "agents/orchestrator.md",
    name: "orchestrator general design blueprint hard stop",
    mustInclude: [
      "Project-local design guidance wins over generic taste",
      "high-level visual direction is insufficient",
      "general end-to-end UI/UX Design Blueprint",
      "experience direction",
      "page-by-page UX blueprint",
      "section-level visual specification",
      "component system plan",
      "visual system",
      "asset and image decision",
      "motion system",
      "interaction/state design",
      "responsive plan",
      "accessibility gate",
      "validation evidence",
      "final status must be `blocked`, `needs-polish`, or `draft`, not `done`",
    ],
  },
  {
    file: "agents/orchestrator.md",
    name: "orchestrator auto-commit gate",
    mustInclude: [
      "Default auto-commit is ON for local commits only",
      "plan-bound, non-trivial task",
      "@quality-gate returns `PASS` or `PASS_WITH_RISKS`",
      "Never push automatically",
      "Never stage `.env`, secrets, tokens, credentials",
      "Never use `--no-verify`, `--no-gpg-sign`, `amend`",
      "If scope or staging is unclear, stop and ask",
    ],
  },
  {
    file: "skills/opencode-orchestrator/SKILL.md",
    name: "orchestrator standalone parity contract",
    mustInclude: [
      "target project's `DESIGN.md`",
      "design-system/DESIGN.md",
      "/init-design",
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
    file: "skills/opencode-orchestrator/SKILL.md",
    name: "orchestrator standalone general design blueprint gate",
    mustInclude: [
      "The target project's own `DESIGN.md` is the first design authority",
      "high-level visual direction is insufficient",
      "general end-to-end UI/UX Design Blueprint",
      "experience direction",
      "page-by-page UX blueprint",
      "section-level visual specification",
      "component system plan",
      "visual system",
      "asset and image decision",
      "motion system",
      "interaction/state design",
      "responsive plan",
      "accessibility gate",
      "validation evidence",
      "final status must be `blocked`, `needs-polish`, or `draft`, not `done`",
    ],
  },
  {
    file: "skills/opencode-orchestrator/SKILL.md",
    name: "orchestrator auto-commit skill gate",
    mustInclude: [
      "Auto-commit default is ON for local commits only",
      "never push automatically",
      "plan-bound non-trivial task",
      "validation has passed",
      "PASS",
      "PASS_WITH_RISKS",
    ],
  },
  {
    file: "skills/opencode-quality-gate/SKILL.md",
    name: "quality gate standalone skill",
    mustInclude: [
      "final reviewer read-only",
      "plan/evidence/diff/validation",
      "Project design-guide conformance",
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
    file: "skills/opencode-build/SKILL.md",
    name: "redundant build skill removed gate",
    mustBeMissing: true,
  },
  {
    file: "skills/opencode-general/SKILL.md",
    name: "redundant general skill removed gate",
    mustBeMissing: true,
  },
  {
    file: "skills/opencode-fixer/SKILL.md",
    name: "fixer skill UI pause gates",
    mustInclude: [
      "target project's `DESIGN.md`",
      "design-system/DESIGN.md",
      "do not silently override it",
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
    file: "skills/opencode-ui-system-architect/SKILL.md",
    name: "ui system architect skill gate",
    mustInclude: [
      "Inspect the target project's `DESIGN.md`",
      "Project-local design guidance wins over generic taste",
      "/init-design",
      "tokens",
      "component anatomy",
      "do not edit files",
    ],
  },
  {
    file: "agents/product-architect.md",
    name: "product architect subagent gate",
    mustInclude: [
      "mode: subagent",
      "description: PRD-to-production product architecture specialist",
      "opencode-product-architect",
      "apply_patch: deny",
      "task: deny",
      "PRD/product strategy/roadmap/MVP ambiguity",
      "tiny UI polish",
      "isolated bugfixes",
    ],
  },
  {
    file: "agents/saas-architect.md",
    name: "saas architect subagent gate",
    mustInclude: [
      "mode: subagent",
      "description: SaaS architecture specialist",
      "opencode-saas-architect",
      "apply_patch: deny",
      "task: deny",
      "multi-tenant apps",
      "billing, or permission risk",
    ],
  },
  {
    file: "agents/ai-systems-architect.md",
    name: "ai systems architect subagent gate",
    mustInclude: [
      "mode: subagent",
      "description: AI systems specialist",
      "opencode-ai-systems-architect",
      "apply_patch: deny",
      "task: deny",
      "LLM/RAG/embedding/tool-calling",
      "AI data or reliability risk",
    ],
  },
  {
    file: "agents/security-privacy-reviewer.md",
    name: "security privacy reviewer subagent gate",
    mustInclude: [
      "mode: subagent",
      "description: Read-only security and privacy reviewer",
      "opencode-security-privacy-reviewer",
      "apply_patch: deny",
      "task: deny",
      "biometric/face/photo data",
      "AI data leakage",
      "risk trigger applies",
    ],
  },
  {
    file: "agents/release-engineer.md",
    name: "release engineer subagent gate",
    mustInclude: [
      "mode: subagent",
      "description: Release engineering specialist",
      "opencode-release-engineer",
      "apply_patch: deny",
      "task: deny",
      "CI/CD, environment validation, deployment",
      "release risk is involved",
    ],
  },
  {
    file: "agents/mobile-architect.md",
    name: "mobile architect subagent gate",
    mustInclude: [
      "mode: subagent",
      "description: Mobile and hybrid app architecture specialist",
      "opencode-mobile-architect",
      "apply_patch: deny",
      "task: deny",
      "React Native/Expo, Flutter, Capacitor/PWA",
      "responsive web-only polish",
    ],
  },
  {
    file: "skills/opencode-product-architect/SKILL.md",
    name: "product architect skill gate",
    mustInclude: [
      "PRD-to-production product architecture workflow",
      "MVP cut",
      "user journeys",
      "acceptance criteria",
      "ready-for-blueprint",
      "needs-product-decisions",
    ],
  },
  {
    file: "skills/opencode-saas-architect/SKILL.md",
    name: "saas architect skill gate",
    mustInclude: [
      "multi-tenant production apps",
      "tenancy model",
      "workspace/org model",
      "billing/subscription model",
      "tenant isolation",
      "needs-saas-decisions",
    ],
  },
  {
    file: "skills/opencode-ai-systems-architect/SKILL.md",
    name: "ai systems architect skill gate",
    mustInclude: [
      "production AI features",
      "LLMs, RAG, embeddings",
      "evals",
      "cost caps",
      "prompt injection",
      "needs-ai-decisions",
    ],
  },
  {
    file: "skills/opencode-security-privacy-reviewer/SKILL.md",
    name: "security privacy reviewer skill gate",
    mustInclude: [
      "PII, auth/session",
      "biometric/face matching",
      "tenant isolation",
      "webhook verification",
      "prompt injection",
      "needs-fix",
    ],
  },
  {
    file: "skills/opencode-release-engineer/SKILL.md",
    name: "release engineer skill gate",
    mustInclude: [
      "production readiness",
      "CI/CD",
      "migration rollout",
      "rollback",
      "Monitoring/logging/alerting",
      "production-candidate",
    ],
  },
  {
    file: "skills/opencode-mobile-architect/SKILL.md",
    name: "mobile architect skill gate",
    mustInclude: [
      "mobile and hybrid app architecture",
      "Expo/React Native",
      "offline sync",
      "camera/QR scanner",
      "app-store constraints",
      "needs-mobile-decisions",
    ],
  },
  {
    file: "agents/orchestrator.md",
    name: "conditional domain specialist routing gate",
    mustInclude: [
      "@product-architect",
      "@saas-architect",
      "@ai-systems-architect",
      "@security-privacy-reviewer",
      "@release-engineer",
      "@mobile-architect",
      "Conditional domain specialist routing",
      "Skip domain specialists for tiny UI polish and isolated bugfixes unless risk triggers apply",
      "Domain specialists do not replace @designer for UI direction, @fixer for implementation, @oracle for deep tradeoff review, or @quality-gate for final conformance",
    ],
  },
  {
    file: "skills/opencode-orchestrator/SKILL.md",
    name: "orchestrator conditional domain skill gate",
    mustInclude: [
      "@product-architect",
      "@saas-architect",
      "@ai-systems-architect",
      "@security-privacy-reviewer",
      "@release-engineer",
      "@mobile-architect",
      "Skip domain specialists for tiny UI polish and isolated bugfixes unless risk triggers apply",
      "Domain specialists do not replace `@designer`, `@fixer`, `@oracle`, or `@quality-gate`",
    ],
  },
  {
    file: "agents/artifact-planner.md",
    name: "artifact planner domain advisory gate",
    mustInclude: [
      "product-architect: allow",
      "saas-architect: allow",
      "ai-systems-architect: allow",
      "security-privacy-reviewer: allow",
      "release-engineer: allow",
      "mobile-architect: allow",
      "PRD to Production Blueprint Mode",
      "Skip domain specialists for tiny UI polish and isolated bugfixes unless risk triggers apply",
    ],
  },
  {
    file: "skills/opencode-artifact-planner/SKILL.md",
    name: "artifact planner production blueprint skill gate",
    mustInclude: [
      "PRD to Production Blueprint",
      "product-architect, saas-architect, ai-systems-architect, security-privacy-reviewer, release-engineer, and mobile-architect",
      "Production Blueprint Summary",
      "Skip domain specialists for tiny UI polish and isolated bugfixes unless risk triggers apply",
    ],
  },
  {
    file: "AGENTS.md",
    name: "global conditional domain specialist gate",
    mustInclude: [
      "PRD/product blueprint work",
      "SaaS architecture",
      "AI system design",
      "Security/privacy review",
      "Release/ops readiness",
      "Mobile/hybrid architecture",
      "Skip domain specialists for tiny UI polish and isolated bugfixes unless risk triggers apply",
    ],
  },
  {
    file: "README.md",
    name: "readme conditional domain specialist gate",
    mustInclude: [
      "@product-architect",
      "@saas-architect",
      "@ai-systems-architect",
      "@security-privacy-reviewer",
      "@release-engineer",
      "@mobile-architect",
      "Domain specialists bersifat conditional",
      "Tiny UI polish tetap ke `@designer`",
      "isolated bugfix tetap ke `@fixer`",
    ],
  },
  {
    file: "package.json",
    name: "tool setup script contract gate",
    mustInclude: [
      '"setup:tools"',
      '"setup:tools:check"',
      '"doctor"',
      '"test:prompt-gates"',
    ],
    mustNotInclude: [
      '"postinstall": "',
      '"preinstall": "',
      '"prepare": "',
    ],
  },
  {
    file: "README.md",
    name: "rtk caveman onboarding docs gate",
    mustInclude: [
      "npm run setup:tools",
      "npm run doctor",
      "RTK",
      "Caveman",
      "manual fallback",
      "no unsafe lifecycle install hooks policy",
      "OpenCode command rewriting",
      "opt-in",
    ],
    mustNotInclude: [
      "hidden postinstall",
    ],
  },
  {
    file: "AGENTS.md",
    name: "rtk opt-in policy gate",
    mustInclude: [
      "RTK may be installed",
      "OpenCode/OpenChamber auto-rewrite/prefix remains opt-in",
      "unless user explicitly asks",
      "Do not prefix shell commands with `rtk`",
    ],
  },
  {
    file: "scripts/setup-dev-tools.mjs",
    name: "setup-dev-tools contract gate",
    mustInclude: [
      "--check",
      "--force",
      "--skip-rtk",
      "--skip-caveman",
      "--help",
      "JuliusBrussee/caveman",
      "-a opencode",
      "Checking: rtk --version",
      "brew install rtk",
      "https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh",
      "official RTK install script",
      "Never run `rtk init` with `-g --opencode`",
      "Restart OpenCode",
    ],
    mustNotInclude: [
      "--all",
      "rtk init with -g --opencode",
      "JuliusBrussee/rtk",
    ],
  },
  {
    file: "scripts/doctor.mjs",
    name: "doctor read-only contract gate",
    mustInclude: [
      "Read-only",
      "Node",
      "npm",
      "rtk --version",
      "npx skills",
      "AGENTS.md",
      "README.md",
      "package lifecycle",
      "remediation",
      "warn",
      ".env",
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
    file: "skills/opencode-orchestrator/SKILL.md",
    name: "orchestrator auto-commit skill gate",
    mustInclude: [
      "Auto-commit default is ON for local commits only",
      "plan-bound non-trivial task completes",
      "@quality-gate returns `PASS` or `PASS_WITH_RISKS`",
      "concise subject plus bullet-point body",
      "never push automatically",
      "Never stage `.env`, secrets, tokens, credentials",
      "Never use `--no-verify`, `--no-gpg-sign`, `amend`",
      "stop and ask",
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
      "Redundant `build` and `general` local agents have been removed",
      "@quality-gate",
      "PASS_WITH_RISKS",
      "NEEDS_FIX",
      "BLOCKED",
    ],
  },
  {
    file: "README.md",
    name: "auto-commit policy readme gate",
    mustInclude: [
      "Auto-commit default ON untuk local commits only",
      "never push automatically",
      "plan-bound non-trivial selesai",
      "validation lulus",
      "PASS",
      "PASS_WITH_RISKS",
      "Review `git status`/`git diff`",
      "stage hanya file relevan",
      "subject singkat plus body bullet-point",
      "Jangan stage `.env`, secrets, tokens, credentials",
      "Jangan gunakan `--no-verify`, `--no-gpg-sign`, `amend`",
      "Kalau scope atau staging meragukan, berhenti dan tanya",
    ],
  },
  {
    file: "agents/explorer.md",
    name: "explorer agent gate",
    mustInclude: [
      "mode: subagent",
      "description:",
      "model: cliproxyapi/gpt-5.4-mini",
      "opencode-explorer",
      "apply_patch: deny",
      "task: deny",
      "*.env",
      "deny",
    ],
  },
  {
    file: "agents/librarian.md",
    name: "librarian agent gate",
    mustInclude: [
      "mode: subagent",
      "description:",
      "model: cliproxyapi/gpt-5.4-mini",
      "opencode-librarian",
      "apply_patch: deny",
      "task: deny",
      "*.env",
      "deny",
    ],
  },
  {
    file: "agents/oracle.md",
    name: "oracle agent gate",
    mustInclude: [
      "mode: subagent",
      "description:",
      "model: cliproxyapi/gpt-5.4",
      "opencode-oracle",
      "apply_patch: deny",
      "task: deny",
      "*.env",
      "deny",
    ],
  },
  {
    file: "agents/designer.md",
    name: "designer agent gate",
    mustInclude: [
      "mode: subagent",
      "description:",
      "model: cliproxyapi/gpt-5.4",
      "opencode-designer",
      "Stitch",
      "visual parity",
      "apply_patch: allow",
      "task: deny",
      "*.env",
      "deny",
    ],
  },
  {
    file: "agents/fixer.md",
    name: "fixer agent gate",
    mustInclude: [
      "mode: subagent",
      "description:",
      "model: cliproxyapi/gpt-5.3-codex",
      "opencode-fixer",
      "apply_patch: allow",
      "task: deny",
      "*.env",
      "deny",
    ],
  },
  {
    file: "README.md",
    name: "standalone identity gate",
    mustInclude: [
      "# opencode-capybara",
      "Standalone OpenCode multi-agent configuration",
      "assets/opencode-capybara-icon.png",
      "## Kenapa capybara?",
      "Calm orchestration",
      "Capybara bukan simbol",
    ],
  },
  {
    file: "agents/artifact-planner.md",
    name: "artifact planner env routing gate",
    mustInclude: [
      "model: cliproxyapi/gpt-5.3-codex",
    ],
  },
  {
    file: "agents/document-specialist.md",
    name: "document specialist env routing gate",
    mustInclude: [
      "model: cliproxyapi/gpt-5.4-mini",
    ],
  },
  {
    file: "package.json",
    name: "package identity gate",
    mustInclude: [
      '"name": "opencode-capybara"',
      '"private": true',
    ],
  },
  {
    file: "opencode.json",
    name: "runtime plugin removal gate",
    mustInclude: [],
    mustNotInclude: [
      upstreamPresetName,
      pluginPackageName,
    ],
  },
  {
    file: "package.json",
    name: "runtime dependency removal gate",
    mustInclude: [],
    mustNotInclude: [
      upstreamPresetName,
      pluginPackageName,
    ],
  },
  {
    file: "package-lock.json",
    name: "lockfile dependency removal gate",
    mustInclude: [],
    mustNotInclude: [
      upstreamPresetName,
      pluginPackageName,
    ],
  },
  {
    file: "tui.json",
    name: "tui plugin removal gate",
    mustInclude: [],
    mustNotInclude: [
      upstreamPresetName,
    ],
  },
  {
    file: "README.md",
    name: "runtime plugin wording gate",
    mustInclude: [],
    mustNotInclude: [
      upstreamPresetName,
      pluginPackageName,
      disabledAgentsKey,
      "Install dependency plugin",
      "plugin-generated",
      "plugin dependency",
      "npm install " + pluginPackageName,
      upstreamPresetName + " is required",
      "required for core routing",
      upstreamPresetName + ".json",
      "previous plugin preset",
    ],
  },
  {
    file: "bun.lock",
    name: "obsolete bun lockfile removed gate",
    mustBeMissing: true,
  },
  {
    file: "commands/commit-message.md",
    name: "manual commit message format gate",
    mustInclude: [
      "concise subject line followed by a bullet-point body",
      "summarizes the most important changes",
      "If auto-commit guidance or repo style suggests a multi-line message",
      "Keep commit messages themselves in English",
    ],
  },
  {
    file: "commands/tdd.md",
    name: "retired workflow command removed gate",
    mustBeMissing: true,
  },
  {
    file: "commands/replicate-ui.md",
    name: "retired UI workflow command removed gate",
    mustBeMissing: true,
  },
  {
    file: "commands/revamp-like.md",
    name: "retired revamp workflow command removed gate",
    mustBeMissing: true,
  },
  {
    file: "agents/visual-parity-auditor.md",
    name: "visual parity agent gate",
    mustInclude: [
      "mode: subagent",
      "hidden: false",
      "apply_patch: deny",
      "task: deny",
      "*.env",
      "deny",
      "opencode-visual-parity-auditor",
    ],
  },
  {
    file: "agents/motion-specialist.md",
    name: "motion specialist agent gate",
    mustInclude: [
      "mode: subagent",
      "hidden: false",
      "apply_patch: deny",
      "task: deny",
      "*.env",
      "deny",
      "opencode-motion-specialist",
    ],
  },
  {
    file: "agents/accessibility-reviewer.md",
    name: "accessibility reviewer agent gate",
    mustInclude: [
      "mode: subagent",
      "hidden: false",
      "apply_patch: deny",
      "task: deny",
      "*.env",
      "deny",
      "opencode-accessibility-reviewer",
    ],
  },
  {
    file: "agents/ui-system-architect.md",
    name: "ui system architect agent gate",
    mustInclude: [
      "mode: subagent",
      "hidden: false",
      "apply_patch: deny",
      "task: deny",
      "*.env",
      "deny",
      "opencode-ui-system-architect",
    ],
  },
  {
    file: "skills/opencode-visual-parity-auditor/SKILL.md",
    name: "visual parity skill gate",
    mustInclude: [
      "visual parity audits",
      "read-only",
      "do not edit files",
    ],
  },
  {
    file: "skills/opencode-motion-specialist/SKILL.md",
    name: "motion specialist skill gate",
    mustInclude: [
      "motion direction",
      "reduced-motion",
      "do not edit files",
    ],
  },
  {
    file: "skills/opencode-accessibility-reviewer/SKILL.md",
    name: "accessibility reviewer skill gate",
    mustInclude: [
      "keyboard access",
      "focus-visible",
      "do not edit files",
    ],
  },
];

const portabilityChecks = [
  "AGENTS.md",
  "agents/orchestrator.md",
  "agents/artifact-planner.md",
  "agents/visual-asset-generator.md",
  "skills/opencode-orchestrator/SKILL.md",
  "skills/opencode-visual-asset-generator/SKILL.md",
  "skills/opencode-fixer/SKILL.md",
  "skills/opencode-artifact-planner/SKILL.md",
  "opencode.json",
  "scripts/prompt-gate-regression.mjs",
];

const duplicates = [
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
  const rootFiles = ["AGENTS.md", "agents/orchestrator.md", "agents/artifact-planner.md", "agents/visual-asset-generator.md", "skills/opencode-orchestrator/SKILL.md", "skills/opencode-visual-asset-generator/SKILL.md", "scripts/prompt-gate-regression.mjs", "opencode.json"];
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
  if (check.mustBeMissing) {
    const absolute = resolve(root, check.file);
    if (existsSync(absolute)) {
      failures += 1;
      console.error(`✗ ${check.file} (${check.name}) should be removed`);
    } else {
      console.log(`✓ ${check.file} (${check.name})`);
    }
    continue;
  }

  const content = read(check.file);
  if (content === null) continue;
  const mustInclude = check.mustInclude ?? [];
  const mustNotInclude = check.mustNotInclude ?? [];

  const missing = mustInclude.filter((needle) => !content.includes(needle));
  const forbiddenHits = mustNotInclude.filter((needle) => content.includes(needle));

  if (missing.length > 0 || forbiddenHits.length > 0) {
    failures += 1;
    console.error(`✗ ${check.file} (${check.name}) ${missing.length > 0 ? "missing" : "forbidden"}:`);
    for (const item of missing) console.error(`  - missing: ${item}`);
    for (const item of forbiddenHits) console.error(`  - forbidden: ${item}`);
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
