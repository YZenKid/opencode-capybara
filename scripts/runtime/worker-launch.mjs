import { pickDefaultBackend, validateWorkerSpec } from "./worker-contracts.mjs";

function buildBackendCommand(spec, backend) {
  const prompt = spec.prompt;
  switch (backend) {
    case "opencode-subagent":
      return { command: "opencode", args: ["run", "--agent", spec.lane, prompt] };
    case "opencode-session":
      return { command: "opencode", args: ["--agent", spec.lane] };
    case "external-cli-codex":
      return { command: "codex", args: [prompt] };
    case "external-cli-claude":
      return { command: "claude", args: [prompt] };
    case "external-cli-gemini":
      return { command: "gemini", args: [prompt] };
    default:
      throw new Error(`unsupported backend: ${backend}`);
  }
}

export function buildWorkerLaunchPlan(spec = {}) {
  const backend = spec.backend ?? pickDefaultBackend(spec.lane);
  const validation = validateWorkerSpec({ ...spec, backend });
  if (!validation.ok) {
    throw new Error(`invalid worker spec: ${validation.errors.join('; ')}`);
  }

  const cwd = spec.worktree_path ?? spec.project_root;
  const backendCommand = buildBackendCommand(spec, backend);
  return {
    worker_name: spec.worker_name,
    lane: spec.lane,
    backend,
    cwd,
    command: backendCommand.command,
    args: backendCommand.args,
    command_preview: [backendCommand.command, ...backendCommand.args.map((arg) => JSON.stringify(arg))].join(" "),
    metadata: {
      run_id: spec.run_id,
      project_root: spec.project_root,
      workspace_mode: spec.workspace_mode ?? (spec.worktree_path ? "worktree" : "single"),
      worktree_path: spec.worktree_path ?? null,
      worktree_branch: spec.worktree_branch ?? null,
      worktree_repo_root: spec.project_root,
    },
  };
}
