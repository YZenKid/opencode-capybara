# Generated: MCP Risk Matrix

Generated from `.opencode/capabilities/registry.json`. Advisory only; configured does not mean usable/authenticated.

- MCP entries: 8

| MCP | Transport | Owner | Auth | Data egress | Write | Allowed lanes | Denied lanes | Fallback | Evidence required | Secret surfaces |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9router | local | @librarian | NINEROUTER_KEY | queries, fetched URLs, prompts, generated image prompts | yes | @librarian, @visual-asset-generator, @orchestrator | @quality-gate, @council | skip external fetch/search/image and use local evidence | source URL/model or asset manifest, no secrets in prompt | NINEROUTER_URL, NINEROUTER_KEY |
| context7 | local | @librarian | CONTEXT7_API_KEY | library name and docs query | no | @librarian, @fixer | @quality-gate, @council | use local docs or package source | library id and query recorded | CONTEXT7_API_KEY |
| github | remote | @orchestrator | GITHUB_PERSONAL_ACCESS_TOKEN | repo metadata, issues, PRs, code, workflow logs | yes | @orchestrator, @fixer, @quality-gate | @council | local git and explicit user handoff | repo, operation, target branch/PR/issue, no secret payload, configured does not mean usable/authenticated | GITHUB_PERSONAL_ACCESS_TOKEN, GITHUB_TOOLSETS |
| grep_app | remote | @librarian | none configured | literal code search patterns | no | @librarian, @fixer | @quality-gate, @council | local grep/glob only | query pattern and repo/path filters | none |
| playwright | local | @designer | browser profile/session state | page URLs, forms, screenshots, network data | yes | @designer, @fixer, @orchestrator | @quality-gate, @council | static review or screenshots supplied by user | URL, action summary, screenshot/console/network result when used | browser cookies, local session |
| semgrep | local | @quality-gate | semgrep login/env optional | repository metadata/findings if app platform used | no | @quality-gate, @fixer, @oracle | @council | manual security review and targeted code search | scan scope and findings summary | Semgrep auth token if configured |
| shadcn | local | @designer | none | registry component names | yes | @designer, @fixer | @quality-gate, @council | manual component implementation from existing project patterns | component names and audit checklist | none |
| time | local | @orchestrator | none | none expected beyond local process | no | @orchestrator, @librarian, @quality-gate | @council | use local system date from environment | record when date/time affects decision | none |
