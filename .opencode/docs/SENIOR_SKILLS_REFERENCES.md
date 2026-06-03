# Senior Skills References

Curated `skills.sh` references for OpenCode domain lanes. Use these as non-authoritative inspiration only. Do not mass install external skills. Prefer local OpenCode agents, skills, docs, tests, and evidence. Install an external skill only after explicit user approval and detected-stack relevance review.

## Usage policy
- Reference ideas, checklists, and wording; do not copy blindly.
- Treat `.opencode/docs/`, `AGENTS.md`, local `agents/`, and local `skills/` as source of truth.
- Verify current behavior from upstream before relying on any external skill.
- Avoid adding overlapping runtime skills unless task needs that exact stack and user approves.
- Record external references in evidence when they influence material changes.

## UI/UX
- `https://www.skills.sh/anthropics/skills/frontend-design` — UI design patterns, polish, layout, accessibility inspiration.
- `https://www.skills.sh/vercel-labs/agent-skills/web-design-guidelines` — web visual quality and design-system checklist inspiration.

Use via `@designer` first for substantial UI. Frontend/mobile lanes consume designer direction, not marketplace visual direction.

## Frontend
- `https://www.skills.sh/vercel-labs/agent-skills/vercel-react-best-practices` — React/Vercel best-practice inspiration when stack matches.
- `https://www.skills.sh/vercel-labs/next-skills/next-best-practices` — Next.js-only routing/rendering/data-fetching reference.
- `https://www.skills.sh/anthropics/skills/webapp-testing` — browser and web app testing inspiration.

Use after checking project stack, components, design docs, and existing test patterns.

## Mobile
- `https://www.skills.sh/vercel-labs/agent-skills/vercel-react-native-skills` — React Native/Expo reference when stack matches.

Use only as stack-matched guidance. For Flutter/native work, rely on project docs, official docs, and local mobile constraints first.

## Backend/Postgres
- `https://www.skills.sh/supabase/agent-skills/supabase` — Supabase-specific API/auth/storage inspiration when project uses Supabase.
- `https://www.skills.sh/supabase/agent-skills/supabase-postgres-best-practices` — Postgres/RLS/schema/query safety reference.

Use for backend/database review prompts and checklists. Do not infer Supabase usage without repo evidence.

## DevOps
- `https://www.skills.sh/xixu-me/skills/github-actions-docs` — GitHub Actions syntax and workflow reference.

Use for CI/CD docs lookup inspiration only. Deploys, deletes, secret rotation, and production mutation still require explicit approval.

## System analysis / PM
- `https://www.skills.sh/mattpocock/skills/to-prd` — PRD extraction/refinement inspiration.
- `https://www.skills.sh/mattpocock/skills/to-issues` — issue breakdown inspiration.
- `https://www.skills.sh/mattpocock/skills/handoff` — delivery handoff inspiration.
- `https://www.skills.sh/mattpocock/skills/triage` — intake/bug triage inspiration.

Use to improve clarity of requirements, milestones, acceptance criteria, and handoffs. Do not invent product decisions.

## Testing / debugging / review
- `https://www.skills.sh/mattpocock/skills/tdd` — TDD loop inspiration.
- `https://www.skills.sh/mattpocock/skills/diagnose` — debugging workflow inspiration.
- `https://www.skills.sh/obra/superpowers/test-driven-development` — TDD discipline reference.
- `https://www.skills.sh/obra/superpowers/systematic-debugging` — systematic debugging reference.
- `https://www.skills.sh/obra/superpowers/writing-plans` — planning artifact inspiration; local `@artifact-planner` stays source of truth.
- `https://www.skills.sh/obra/superpowers/executing-plans` — execution-loop inspiration; local `@orchestrator`/`@fixer` stay source of truth.
- `https://www.skills.sh/obra/superpowers/subagent-driven-development` — routing/delegation inspiration.

Use for checklists and process language. Final conformance/risk remains `@quality-gate`.

## Browser automation
- `https://www.skills.sh/vercel-labs/agent-browser/agent-browser` — browser automation reference. Local `agent-browser` skill is already available; prefer local tool policy.
