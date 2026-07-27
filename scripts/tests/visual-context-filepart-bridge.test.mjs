import assert from "node:assert/strict";
import { mkdtemp, readFile, stat } from "node:fs/promises";
import { join } from "node:path";
import { tmpdir } from "node:os";
import createPlugin from "../../plugins/visual-context-filepart-bridge.js";

const configText = await readFile(new URL("../../opencode.json", import.meta.url), "utf8");
const config = JSON.parse(configText);
assert.deepEqual(config.plugin, ["./plugins/visual-context-filepart-bridge.js"]);
assert.equal(await stat(new URL("../../plugins/visual-context-filepart-bridge.js", import.meta.url)).then(() => true), true);

const worktree = await mkdtemp(join(tmpdir(), "visual-worktree-"));
const fixture = `data:image/png;base64,${Buffer.from("png").toString("base64")}`;
const part = { type: "file", mime: "image/png", url: fixture };
const orchestratorDoc = await readFile(new URL("../../agents/orchestrator.md", import.meta.url), "utf8");
assert.match(orchestratorDoc, /built-in `task`.*interceptor/s);
assert.match(orchestratorDoc, /@\.opencode\/visual-attachments/);
assert.match(orchestratorDoc, /direct task without plugin remains unavailable/);
const hooks = await createPlugin({ worktree });
assert.equal(typeof hooks["tool.execute.before"], "function");
assert.equal(typeof hooks["tool.execute.after"], "function");
assert.equal(hooks.tool, undefined);
const sessionID = "session-test";
await hooks["chat.message"]({ sessionID }, { parts: [part] });
const output = { args: { subagent_type: "visual-context-extractor", prompt: "inspect" } };
await hooks["tool.execute.before"]({ tool: "task", callID: "call-test", sessionID }, output);
assert.match(output.args.prompt, /^inspect\n@\.opencode\/visual-attachments\/[^/]+\/image\.png$/);
const relative = output.args.prompt.slice("inspect\n@".length);
const materializedPath = join(worktree, relative);
assert.equal(await stat(materializedPath).then(() => true), true);
await hooks["tool.execute.after"]({ callID: "call-test" });
assert.equal(await stat(materializedPath).catch(() => null), null);

const unchanged = { args: { subagent_type: "other", prompt: "inspect" } };
await hooks["tool.execute.before"]({ tool: "task", callID: "call-other", sessionID }, unchanged);
assert.deepEqual(unchanged.args, { subagent_type: "other", prompt: "inspect" });

console.log("visual-context-filepart-bridge tests passed");
