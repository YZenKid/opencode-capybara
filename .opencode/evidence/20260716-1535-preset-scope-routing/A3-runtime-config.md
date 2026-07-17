# A3 runtime and config compatibility

- task_id: `20260716-1535-preset-scope-routing`
- claim_scope: local resolved config and static candidate audits
- config disposition: `no_change`

## Local proof

`opencode debug agent orchestrator` resolved:

- `model.providerID`: `9router`
- `model.modelID`: `high`
- `steps`: `null`

`opencode.json` parses as JSON. Static config inspection shows:

- default model: `{env:OPENCODE_MODEL_DEFAULT}`
- registered `9router/fast` model ID: `cx/gpt-5.4-mini`
- explicit agent model overrides: none

`opencode debug config` is available but emitted expanded configured agent/prompt data rather than a small task-class routing diagnostic. No local command demonstrated semantic routing from `read_only` intent to `9router/fast` within primary `orchestrator`.

## Decision

- `confirmed_runtime`: current primary `orchestrator` resolves to `9router/high`; `steps` is unset.
- `confirmed_repo`: `9router/fast` is registered in `opencode.json`, while default model remains env-based and no static agent override exists.
- `unverified`: automatic task-class selection of `9router/fast`.
- No `opencode.json` modification. No `steps` configuration.

## Safety

- No credential, `.env`, or provider key was read.
- `git diff -- opencode.json` produced no output.
- Runtime performance/latency is not claimed.
