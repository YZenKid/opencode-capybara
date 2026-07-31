---
name: 21st-discovery-overlay
description: 21st.dev component discovery intake overlay. Use only after local DESIGN.md and Open Design catalog selection when evaluating a 21st component, theme, or template for possible adoption; search and inspect before any install, never publish or authenticate automatically.
license: Apache-2.0
metadata:
  upstream: https://github.com/21st-dev/skill
  revision: a0059e9f3a8ed0310dee8e37bab9fb32ecbf1fa7
  adaptation: local-discovery-overlay
---

# 21st Discovery Overlay

Local adaptation of selected `21st-cli-use` intake guidance. Upstream snapshot, Apache-2.0 notice, and revision: [SOURCE.md](./SOURCE.md).

## Authority and boundary

1. User instruction, license/safety, `DESIGN.md`, Open Design citation, local token system, and target stack win.
2. 21st is conditional discovery source, never automatic visual authority.
3. Search/metadata inspection may happen after direction exists. Retrieval, install, code generation, authentication, team access, publishing, editing, and deletion require separately authorized work.

## Workflow

1. Confirm project catalog/design direction, target stack, component boundary, and asset/license requirements.
2. Search candidates. Record item ID/URL, author, item type, visible license/provenance, dependency footprint, and preview evidence.
3. Accept only candidates matching local tokens, responsive behavior, accessibility, reduced-motion policy, and planned anatomy. Adapt through documented deviation; reject otherwise.
4. Before any source retrieval or install, verify per-item license and permission, inspect generated file/dependency diff plan, and obtain separate authorization.
5. Keep no-match outcome valid: use existing primitives or minimal local code when no candidate passes review.

## Quality checklist

- [ ] Design authority selected before 21st search.
- [ ] Candidate record includes provenance, per-item license status, dependencies, and reason.
- [ ] No API key, token, login session, or private library data logged.
- [ ] No retrieval/install/publish/auth action without explicit scoped approval.
- [ ] Candidate passes token, a11y, responsive, motion, and source checks before adoption.
- [ ] Evidence marks component license as unverified until item-level proof exists.

## Anti-patterns

- Auto-activating because `components.json` exists.
- Installing before reviewing target stack, source, license, or dependencies.
- Treating skill Apache-2.0 license as component license.
- Publishing, editing, deleting, team access, or design-theme sync without separate authorization.
- Allowing candidate code to replace `DESIGN.md`/catalog authority.

## Output example

```yaml
candidate:
  id: "21st item ID"
  type: component
  provenance: "21st URL + author"
  item_license: unverified
review:
  token_fit: adapt-required
  a11y: inspect-required
  dependencies: "no retrieval yet"
decision: reject
reason: "license and token parity unavailable"
```

## Graphify query-first contract

For code investigation, debugging, dependency/call-chain tracing, impact analysis, and non-trivial code fixes, query fresh available Graphify first. Use narrow query/path/explain. Direct source reading + tests/runtime still required. Missing/stale/unsupported fallback must be recorded. Tiny known-file and non-code skip only with explicit reason.
