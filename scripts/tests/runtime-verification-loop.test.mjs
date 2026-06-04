#!/usr/bin/env node
import assert from "node:assert/strict";
import { classifyVerificationStatus, computeRunProgress, nextVerificationAction } from "../runtime/verification-loop.mjs";
import { renderRunBoard } from "../runtime/board.mjs";

const tasks = [
  { task_id: "t1", status: "completed" },
  { task_id: "t2", status: "failed" },
];
assert.equal(classifyVerificationStatus({ blocked: false, has_failures: true, all_validations_passed: false }), "NEEDS_FIX");
assert.equal(computeRunProgress(tasks).completed, 1);
assert.equal(nextVerificationAction({ has_failures: true, blocked: false, all_validations_passed: false }), "remediate");
const board = renderRunBoard({ run: { run_id: "run-z", status: "executing", goal: "board" }, tasks, mailbox_summary: { pending: 2, acked: 1 } });
assert.match(board, /run-z/);
assert.match(board, /pending mailbox: 2/);
console.log("runtime-verification-loop.test.mjs: PASS");
