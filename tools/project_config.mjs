import { readFile, stat, writeFile } from "node:fs/promises"
import path from "node:path"
import { tool } from "@opencode-ai/plugin"

const confirmation = "APPLY_PROJECT_CONFIG"

function parseReferences(raw) {
  if (raw === undefined || raw === "") return {}
  let references
  try {
    references = JSON.parse(raw)
  } catch {
    throw new Error("references must be valid JSON")
  }
  if (!references || Array.isArray(references) || typeof references !== "object") {
    throw new Error("references must be a JSON object")
  }
  for (const [alias, value] of Object.entries(references)) {
    if (!/^[a-zA-Z0-9._-]+$/.test(alias) || typeof value !== "string" || value.length === 0) {
      throw new Error("references must contain portable aliases and non-empty strings")
    }
    if (path.isAbsolute(value) || value.startsWith("~") || value.split(/[\\/]/).includes("..")) {
      throw new Error("references must use relative paths or repository names")
    }
  }
  return references
}

async function projectConfig(projectPath) {
  if (typeof projectPath !== "string" || projectPath.length === 0 || !path.isAbsolute(projectPath)) {
    throw new Error("projectPath must be an absolute existing project directory")
  }
  try {
    if (!(await stat(projectPath)).isDirectory()) throw new Error("not a directory")
  } catch {
    throw new Error("projectPath must be an absolute existing project directory")
  }
  return path.join(projectPath, "opencode.json")
}

export default tool({
  description: "Audit or explicitly apply project-local formatter and reference settings.",
  args: {
    action: tool.schema.enum(["audit", "apply"]).default("audit"),
    projectPath: tool.schema.string().describe("Absolute project directory to inspect"),
    references: tool.schema.string().optional().describe("JSON object of relative or repository reference aliases"),
    confirmation: tool.schema.string().optional().describe("Required exact value for apply: APPLY_PROJECT_CONFIG"),
  },
  async execute(args) {
    const configPath = await projectConfig(args.projectPath)
    const references = parseReferences(args.references)
    let current = {}
    try {
      current = JSON.parse(await readFile(configPath, "utf8"))
    } catch (error) {
      if (error.code !== "ENOENT") throw new Error("target opencode.json must contain valid JSON")
    }
    const next = { ...current, formatter: true }
    if (Object.keys(references).length > 0) next.references = { ...(current.references ?? {}), ...references }
    const summary = {
      projectPath: args.projectPath,
      configPath,
      formatterEnabled: current.formatter === true,
      referenceAliases: Object.keys(current.references ?? {}),
      proposedFormatter: true,
      proposedReferenceAliases: Object.keys(references),
    }
    if (args.action !== "apply") {
      return JSON.stringify({ action: "audit", ...summary, write: false }, null, 2)
    }
    if (args.confirmation !== confirmation) throw new Error(`apply requires confirmation: ${confirmation}`)
    await writeFile(configPath, `${JSON.stringify(next, null, 2)}\n`, "utf8")
    return JSON.stringify({ action: "apply", ...summary, write: true }, null, 2)
  },
})

export { parseReferences, projectConfig }
