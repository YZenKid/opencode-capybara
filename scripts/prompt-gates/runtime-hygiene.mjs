export const portabilityChecks = [
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

export const duplicateChecks = [
  {
    file: "skills/opencode-fixer/SKILL.md",
    text: "For substantial UI/reference/image-heavy work, do not close on screenshots alone",
    max: 1,
  },
];

export const forbiddenPaths = ["/home/" + "ujang", "/Users/" + "ujang"];

export function runPortabilityChecks({ read, state }) {
  for (const file of portabilityChecks) {
    const content = read(file);
    if (content === null) continue;

    for (const forbidden of forbiddenPaths) {
      if (content.includes(forbidden)) {
        state.failures += 1;
        console.error(`✗ ${file}: contains hardcoded path ${forbidden.replace("ujang", "<user>")}`);
      }
    }

    if (file === "opencode.json" && content.includes("./bin/image-asset-mcp.mjs")) {
      state.failures += 1;
      console.error(`✗ ${file}: image-asset-generator still uses ./bin/image-asset-mcp.mjs`);
    }
  }

  for (const file of [
    "agents/visual-asset-generator.md",
    "skills/opencode-visual-asset-generator/SKILL.md",
  ]) {
    const content = read(file);
    if (content === null) continue;
    const requiredPhrases = [
      "Never hardcode device-specific absolute paths",
      "active workspace/project root",
      "OpenCode config root",
      "target app `project_root`",
      "target_path` relative to that root",
    ];
    const missing = requiredPhrases.filter((phrase) => !content.includes(phrase));
    if (missing.length > 0) {
      state.failures += 1;
      console.error(`✗ ${file}: missing portability phrases:`);
      for (const phrase of missing) console.error(`  - ${phrase}`);
    }
  }
}
