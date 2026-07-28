# 21st discovery overlay source manifest

- Local skill: `skills/21st-discovery-overlay/SKILL.md`
- Upstream project: <https://github.com/21st-dev/skill>
- Selected upstream source: `skills/21st-cli-use/SKILL.md`
- Immutable revision: `a0059e9f3a8ed0310dee8e37bab9fb32ecbf1fa7` (`2026-07-10T22:59:12Z`)
- Raw source: <https://raw.githubusercontent.com/21st-dev/skill/a0059e9f3a8ed0310dee8e37bab9fb32ecbf1fa7/skills/21st-cli-use/SKILL.md>
- License: Apache License, Version 2.0; copyright 2026 21st.dev
- Raw license: <https://raw.githubusercontent.com/21st-dev/skill/a0059e9f3a8ed0310dee8e37bab9fb32ecbf1fa7/LICENSE>
- NOTICE file: none at upstream root as checked through GitHub contents API (`404`, `2026-07-27`)
- Retrieved: `2026-07-27`
- Adaptation: local discovery-only overlay, not raw vendored copy.

## Retained concepts

- Search candidate before writing or importing a matching catalog component.
- Inspect component/theme metadata and code only when separately authorized.
- Track dependency impact and use project package manager for an approved install.

## Pruned or changed

- Removed auto-activation by `components.json`.
- Removed all commands for login, API-key use, install, generation, bookmarks, team/library access, MCP configuration, and publish/manage actions.
- Changed "always search before hand-writing" into conditional discovery after local authority selection.
- Added per-item license requirement, explicit approval boundary, no-secret rule, token/a11y/responsive/reduced-motion review, and no-match fallback.

Apache-2.0 attribution and modification notice retained in this manifest. No upstream source text copied beyond named concepts and source identifiers.
