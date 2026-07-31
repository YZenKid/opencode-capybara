import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const checkPlan = readFileSync("commands/check-plan.md", "utf8");
const fixPlan = readFileSync("commands/fix-plan.md", "utf8");
const startWork = readFileSync("commands/start-work.md", "utf8");

for (const term of ["@plan-validator", "check-and-fix", "--fix-only", "auto_fixes", "plan_remediation_loop", "may edit", "may be edited"]) {
  assert.equal(checkPlan.includes(term), false, `check-plan contains forbidden term: ${term}`);
}
for (const term of ["strictly read-only", "never edits", "validate-plan-depth.py", "plan-compliance-check.py", "subagent-handoff-check.py", "/fix-plan"]) {
  assert.equal(checkPlan.includes(term), true, `check-plan missing contract: ${term}`);
}
assert.match(fixPlan, /@artifact-planner/);
assert.doesNotMatch(fixPlan, /@plan-validator|plan-validator/);
assert.match(startWork, /\/check-plan/);
assert.match(startWork, /\/fix-plan/);
assert.match(startWork, /@artifact-planner/);
assert.doesNotMatch(startWork, /@plan-validator|plan-validator/);
console.log("A4 command contract passed");
