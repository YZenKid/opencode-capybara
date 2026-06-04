#!/usr/bin/env node
import assert from "node:assert/strict";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createRun } from "../runtime/run-store.mjs";
import { sendMessage, listMessages, ackMessage, requeueMessage } from "../runtime/mailbox-store.mjs";

const projectRoot = mkdtempSync(join(tmpdir(), "opencode-runtime-mailbox-"));
createRun(projectRoot, { run_id: "run-mail", goal: "mailbox test", mode: "maintenance", status: "executing" });
const msg = sendMessage(projectRoot, "run-mail", { from: "orchestrator", to: "fixer-1", type: "task", payload: { task_id: "task-1" } });
assert.equal(listMessages(projectRoot, "run-mail", "fixer-1").length, 1);
ackMessage(projectRoot, "run-mail", "fixer-1", msg.message_id, "fixer-1");
assert.equal(listMessages(projectRoot, "run-mail", "fixer-1").length, 0);
requeueMessage(projectRoot, "run-mail", "fixer-1", msg.message_id, "orchestrator");
assert.equal(listMessages(projectRoot, "run-mail", "fixer-1").length, 1);
console.log("runtime-mailbox.test.mjs: PASS");
