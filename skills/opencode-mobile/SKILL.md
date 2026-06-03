---
name: opencode-mobile
description: Mobile implementation workflow for React Native, Expo, Flutter, native permissions, navigation, offline, push, camera, deep links, store constraints, and device validation.
---

# OpenCode Mobile Skill

Use for bounded native or hybrid mobile app implementation.

## Duties
- Reuse existing navigation, state, platform config, build, and test patterns.
- Check native permission, offline, push, camera, deep-link, and store-impact boundaries.
- Validate with safe build/test/simulator/device commands when available.

## Forbidden
- Do not add native dependencies without platform impact review.
- Do not handle privacy/biometric/permission final signoff; route `@quality-gate`.
- Do not decide mobile architecture boundaries alone; route `@architect`.

## Senior reference knowledge
- See `.opencode/docs/SENIOR_SKILLS_REFERENCES.md`.
- Relevant reference: `vercel-labs/agent-skills/vercel-react-native-skills` for React Native/Expo only.
- Use as non-authoritative inspiration after stack fit; for Flutter/native, prefer project-local and official docs.

## Workflow
1. Identify stack and platforms.
2. Inspect config, permissions, navigation, and existing modules.
3. Implement minimal app change.
4. Validate with available checks.
5. Record device/runtime limitations and risks.

## Output
Return `summary`, `findings`, `changed_files`, `risks`, `next_actions`, `evidence` plus validation commands/results.
