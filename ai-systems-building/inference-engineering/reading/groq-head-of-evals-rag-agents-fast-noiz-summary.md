# Groq Head of Evals: How to Actually Make RAG & Agents Fast — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/zlo0ctrFBoA`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat specific thresholds, comparative performance claims, and pricing ideas as **to verify** until corroborated by primary sources (talk recording, slides, benchmarks, or reproducible measurements).

## Latency metrics that matter (claims)

### TTFT (Time To First Token)

- TTFT above roughly **500ms–1s** is described as frustrating for users.

### TPS (Tokens Per Second)

- TPS determines how long a response takes after TTFT. Example given: **100 TPS** means a **1000-token** response takes **~10s** to generate *after* TTFT.

### End-to-end latency (the user-perceived number)

- End-to-end latency is described as the total time from “agent call” to the completed answer, including:
  - LLM time (reasoning + generation)
  - tool/API calls
  - parsing/integration of results
  - state management overhead
- Latency is described as compounding in multi-step agents because each decision point can introduce:
  - additional steps
  - retries
  - refinements

## Optimization strategies (claims)

### Parallelism

- Reduce end-to-end latency by running independent steps simultaneously.
  - Example: travel planning can parallelize flights/hotels/activities retrieval.
- Apply both:
  - **task parallelism** (independent tool calls)
  - **data parallelism** (process multiple documents/results concurrently)

### Caching

- Caching is described as a primary lever for cost + latency:
  - **Prefix caching**: structure prompts to maximize cache hits.
  - **Prompt caching**: reuse identical prompts when possible.

Related (in this repo):
- Prefix caching probes (vLLM): `../days/day-007-vllm-runtime-probes/prefix_caching_results.md`
- TTFT probes: `../days/day-007-vllm-runtime-probes/first_token_latency.md`

### Faster core inference → reinvest into quality

- Speed improvements from faster inference (smaller models, quantization, custom silicon, efficient runtimes) can be “reinvested” into quality improvements such as:
  - better reasoning
  - more sampling
  - verification

## UX patterns for perceived speed (claims)

- Stream intermediate steps:
  - quick acknowledgement
  - rough answer
  - iteratively better answers
- This is framed as better UX than a loading bar or blank screen for multi-step agents.

## Business/econ notes (claims)

- Outcome-based pricing (e.g., “closed support tickets”) is described as a possible growth driver vs pure per-token pricing, because teams optimize for results. (Forward-looking; to verify.)
- Optimization should target business objectives within budget constraints (maintenance + inference costs + performance gains vs investment).

## Real-time apps (claims)

- For real-time applications (copilots, code assistants, heads-up displays), prioritize fast models/runtimes to enable interactive updates based on user context.

## Appendix: Raw Notes (Preserved)

- “TTFT over 500ms-1s frustrates users…”
- “End-to-end latency… includes tool calls… parsing… state…”
- “Parallelism… flights/hotels/activities…”
- “Caching… prefix caching… prompt caching…”
- “Stream intermediate steps…”
