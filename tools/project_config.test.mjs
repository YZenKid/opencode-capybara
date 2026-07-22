import assert from "node:assert/strict"
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises"
import os from "node:os"
import path from "node:path"
import projectConfig, { parseReferences } from "./project_config.mjs"

const root = await mkdtemp(path.join(os.tmpdir(), "project-config-"))
const configPath = path.join(root, "opencode.json")
await writeFile(configPath, JSON.stringify({ existing: { keep: true }, apiKey: "secret-value" }))
assert.deepEqual(parseReferences('{"docs":"docs"}'), { docs: "docs" })
assert.throws(() => parseReferences('{"docs":"/etc"}'), /relative paths/)
const auditOutput = await projectConfig.execute({ action: "audit", projectPath: root })
const audit = JSON.parse(auditOutput)
assert.equal(audit.write, false)
assert.doesNotMatch(auditOutput, /secret-value/)
assert.deepEqual(JSON.parse(await readFile(configPath, "utf8")), { existing: { keep: true }, apiKey: "secret-value" })
await assert.rejects(() => projectConfig.execute({ action: "apply", projectPath: root, confirmation: "wrong" }), /APPLY_PROJECT_CONFIG/)
assert.deepEqual(JSON.parse(await readFile(configPath, "utf8")), { existing: { keep: true }, apiKey: "secret-value" })
const applyOutput = await projectConfig.execute({ action: "apply", projectPath: root, references: '{"docs":"docs"}', confirmation: "APPLY_PROJECT_CONFIG" })
assert.doesNotMatch(applyOutput, /secret-value/)
assert.deepEqual(JSON.parse(await readFile(configPath, "utf8")), { existing: { keep: true }, apiKey: "secret-value", formatter: true, references: { docs: "docs" } })
await rm(root, { recursive: true, force: true })
console.log("project_config safe boundary checks passed")
