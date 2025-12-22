# Serving Patterns

Document routing strategies, batching schedulers, and operational playbooks that survive across experiments.

## Latency metrics (agent-aware)

When serving RAG and agents, measure at least:

- **TTFT (time to first token)**: user-visible responsiveness.
- **TPS (tokens per second)**: generation time dominates longer answers.
- **Step latency**: each tool call / decision point / retry adds delay.
- **End-to-end latency**: what users actually experience (LLM + tools + parsing + state).

Deep dive (Noiz summary notes; to verify): `../../reading/groq-head-of-evals-rag-agents-fast-noiz-summary.md`

## Patterns (high leverage)

- **Parallelize independent work**: run independent tool calls concurrently; batch document processing where possible.
- **Cache aggressively**:
  - prefix caching via prompt structure
  - prompt caching for identical calls
- **Stream progress**: acknowledgement → draft → refine (improves perceived speed on multi-step agents).

## TODO

- Add “agent latency budget” templates (TTFT/TPS/E2E targets by app type).
- Add example implementations (async tool fan-out, result aggregation, caching).
