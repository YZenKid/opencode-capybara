# Generated: External Comparison

Generated from `.opencode/capabilities/registry.json`. External repos are comparators only, not active capabilities or source imports.

- Comparators: 4

| Comparator | Status | License | Decision | Patterns | Reason | Risk |
| --- | --- | --- | --- | --- | --- | --- |
| oh-my-claudecode | external-comparator | unverified in local evidence | adapt | skill lifecycle, smoke tests, install/migration/security docs | Comparable governance ideas only; local harness remains canonical. | prompt-bloat, tooling-mismatch |
| oh-my-codex | external-comparator | unverified in local evidence | adapt | clarify-plan-execute-verify, doctor/exec style checks | Use workflow pattern only; no source import in MVP. | cargo-cult, license-unknown |
| oh-my-openagent | external-comparator | SUL-1.0 per plan | reject | layered core/adapters, edition split, compatibility matrix | Source reuse blocked by license review; comparator only. | license, external-overreach |
| oh-my-pi | external-comparator | unverified in local evidence | defer | typed subagent outputs, hashline/content-hash anchors, LSP/AST-first | Good future fit, but MVP limits scope to registry and deterministic checks. | overengineering, prompt-bloat |
