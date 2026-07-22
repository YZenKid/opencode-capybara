# Auto-fixes — graphify-discovery-coverage

- Normalized `## Existing Patterns / Reuse` to `## Existing Patterns/Reuse` for validator-recognized heading match.
- Normalized `## Decisions / Assumptions` to `## Decisions/Assumptions` for validator-recognized heading match.
- Expanded `## Grounding Contract` label list to include full validator-recognized claim labels.
- Updated maintenance validation references from `--mode auto` to `--mode maintenance` in acceptance criteria, quality-gate handoff, validation commands, and routing note.
- Rewrote 4 embedded handoff YAML blocks so schema-required fields live at YAML root instead of under nested `handoff:` key.
- Added evidence note for `.opencode/evidence/graphify-discovery-coverage/check-plan/*.txt`.
- Renamed execution/readiness task IDs from `GC1..GC4` to `G1..G4` across worklist, handoff blocks, `start_with`, and progress task_map for parser-safe `^[A-Z]\d+$` compliance.

No implementation docs, skills, scripts, config, generated files, or runtime state changed.
