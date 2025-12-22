# Why Hallucinations Aren’t What You Think (Production Hallucinations + Context Metrics) — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/tQ2uSt-kYYY`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat all percentages, named products/models, and scale claims as **to verify** until corroborated by primary sources (talk recording, docs, or reproduced evaluations).

## Core claim (as described)

Most “production hallucinations” are described as system failures in **data + context**, not mystical model failure:

- The majority (claimed **80–90%**) are attributed to **bad data**: incorrect, outdated, duplicated, or conflicting documents.
- Many are **extrinsic**: the model reasons incorrectly *about the context it was given*.
- “Intrinsic” hallucinations (pure fabrication absent from training) are described as a smaller share in production settings.

## Failure mode: context rot (claims)

- “Context rot” is described as models struggling to parse large or messy context, especially when users supply diverse external data the system doesn’t control.

## Two core metrics for RAG quality (claims)

### 1) Context relevance

- Measure the percent of retrieved documents that are relevant.

### 2) Context usage

- Measure the percent of the model output that is actually grounded in / uses the provided context.

Claimed diagnostic: high values for both indicate higher quality RAG; low values point to retrieval or grounding issues.

## Evaluation approach (claims)

### Reference-free evaluation

- “Reference-free” evaluation is described as essential for dynamic systems where:
  - context changes
  - user queries change
  - golden answers are infeasible to maintain at scale

### Enterprise onboarding audits

- Run exhaustive searches for representative queries during enterprise onboarding to audit the corpus for gaps and conflicts before going live.

## Tool-use hallucinations (agents) (claims)

- Tool-use hallucinations are described as agents fabricating:
  - function names
  - parameters
  - tool usage patterns
…due to incorrect reasoning over real context, leading to incorrect tool calls/arguments.

## Detection patterns (claims)

- Asynchronous hallucination detection is described as enabling thorough checks without adding latency to the main agent flow.
- In-the-loop correction with specialized evaluators is described as important for high-stakes apps (examples named: medical translation, legal research).
- Regulated, high-volume contexts (example: **50–100M monthly API requests**) are described as motivating **custom evaluators** tuned to specific use cases for cost/accuracy tradeoffs.

### Specialized tool-use evaluator model (claim; to verify)

- “Limbic Tool Use” **0.5B** is described as achieving **90%+** accuracy in detecting tool-use errors at **100–200ms** latency, as an open-source guardrail model.

### Output-supported-by-context metric (claim; to verify)

- “Quotient AI” is described as measuring whether agent output is supported by retrieved context, tracking hallucination rate and document relevance as flagship metrics with customizable ROC settings.

## Practical checklist (distilled)

- Treat “hallucinations” as data + retrieval + context-usage problems first.
- Detect and repair corpus issues (conflicts, staleness, duplicates) as part of onboarding and ongoing ops.
- Track context relevance and context usage; use them to locate whether the bottleneck is retrieval or generation grounding.
- Prefer reference-free eval loops for dynamic systems; layer async evaluators where latency is sensitive.
- For tools/agents, add tool-call validation and tool-use error detectors (async or in-loop based on risk).

## Appendix: Raw Notes (Preserved)

- “80–90% of production hallucinations stem from bad data…”
- “Context relevance… context usage…”
- “Context rot…”
- “Limbic Tool Use 0.5B… 90%+… 100–200ms…”
