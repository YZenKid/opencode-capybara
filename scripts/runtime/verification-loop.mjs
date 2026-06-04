export function classifyVerificationStatus({ blocked = false, has_failures = false, all_validations_passed = false, has_risks = false } = {}) {
  if (blocked) return "BLOCKED";
  if (has_failures) return "NEEDS_FIX";
  if (all_validations_passed && has_risks) return "PASS_WITH_RISKS";
  if (all_validations_passed) return "PASS";
  return "NEEDS_FIX";
}

export function nextVerificationAction({ blocked = false, has_failures = false, all_validations_passed = false, has_risks = false } = {}) {
  const status = classifyVerificationStatus({ blocked, has_failures, all_validations_passed, has_risks });
  if (status === "BLOCKED") return "stop";
  if (status === "NEEDS_FIX") return "remediate";
  if (status === "PASS_WITH_RISKS") return "report-risks";
  return "complete";
}

export function computeRunProgress(tasks = []) {
  const summary = {
    total: tasks.length,
    pending: 0,
    claimed: 0,
    completed: 0,
    failed: 0,
    blocked: 0,
    cancelled: 0,
  };

  for (const task of tasks) {
    const status = task?.status ?? "pending";
    if (Object.prototype.hasOwnProperty.call(summary, status)) summary[status] += 1;
    else summary.pending += 1;
  }

  return {
    ...summary,
    completion_ratio: summary.total === 0 ? 0 : summary.completed / summary.total,
    has_failures: summary.failed > 0,
    has_blockers: summary.blocked > 0,
  };
}
