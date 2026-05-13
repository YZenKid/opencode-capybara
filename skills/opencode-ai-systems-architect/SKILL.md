# Skill: opencode-ai-systems-architect

Read-only AI systems architecture workflow for production AI features. Use this only when LLMs, RAG, embeddings, tool calling, AI agents, AI evals, face matching, model/provider choices, safety, cost, or AI reliability materially affect the app.

## Trigger / skip

- Trigger for AI assistants, summarizers, recommendations, embeddings/vector search, RAG, multimodal/vision, face matching, tool-calling, AI workflows, AI evals, or model cost/reliability decisions.
- Skip for ordinary non-AI features, simple copywriting, tiny UI polish, or isolated bugfixes without AI behavior.
- For version-sensitive SDK/provider behavior, route docs lookup to `@librarian`.
- For user data, PII, biometric, or tool access, involve `@security-risk-reviewer`.

## Workflow

1. Define AI job-to-be-done and whether AI is necessary.
2. Define input/output contract, grounding sources, tool permissions, and human-review needs.
3. Choose model/provider criteria: quality, latency, cost, privacy, region, multimodal needs, streaming, structured output.
4. Define evals: golden set, negative cases, acceptance thresholds, regression prompts, and observability fields.
5. Define failure handling: fallback, retries, timeouts, abstention, user-facing error states, and cost caps.
6. Identify safety/privacy risks: prompt injection, data leakage, over-retention, hallucination, and unsafe automation.

## Output contract

- AI feature contract and boundaries.
- Provider/model decision criteria.
- Eval plan and telemetry needs.
- Safety/privacy/cost guardrails.
- Fallback and failure-mode strategy.
- Implementation handoff checklist.

## Quality bar

- Do not treat demos as production readiness.
- Every AI feature needs evals and failure behavior.
- Prefer bounded AI capabilities over open-ended agentic behavior.
- Readiness level: `ready-for-blueprint`, `needs-ai-decisions`, or `blocked`.
