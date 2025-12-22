# Cheating at Query Understanding with LLMs (Doug Turnbull) — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/UfHoLV674do`

This note distills claims from a **Noiz** summary provided in the prompt. Treat framework names (“Hydantic”) and prescriptions as **to verify** until corroborated by primary sources (talk recording, docs, or reproduced experiments).

## What “query understanding” means (claims)

- Decompose natural language queries into structured properties (e.g., category, color, brand).
- Route to specialized backends depending on which properties are present (e.g., product reviews vs news).
- Goal: more precise retrieval than treating the query as unstructured text.

## Why LLMs change the economics (claims)

- “Simple LLMs” are described as now doing reliable NLP tasks (e.g., color extraction) that historically required large specialized NLP efforts.

## Evaluation metrics (claims)

- Measure:
  - **precision** (label correctness)
  - **coverage** (percent of queries labeled)
- Precision is emphasized to avoid harmful wrong labels.

## Embedding and retrieval pitfalls (claims)

- “Embedding collapse / hubness” can happen with generic models (example: CLIP) in specific domains, causing irrelevant items to cluster.
- Use fallback paths when attributes are absent:
  - lexical retrieval
  - vector retrieval

## Production patterns (claims)

- Avoid calling large LLMs (e.g., GPT‑4 class) synchronously for latency-sensitive query understanding.
- Preferred pattern:
  - run query understanding as nightly batch jobs
  - cache results
  - use fallback mechanisms for cache misses

### Fast iteration

- Use feature flags to iterate on query understanding safely in production.

## Enrichment for downstream retrieval (claims)

- Content enrichment: add structured attributes (company names, fiscal years, etc.) to documents so queries can filter/select the right set.
- Multimodal/structured signals (popularity, numeric, categorical, hierarchical data) require extraction to support first-pass retrieval and filtering.

## Schemas for constrained extraction (claims)

- “Hydantic schemas” are described as enforcing specific label extraction (e.g., color) so outputs match query intent.

## Future-looking claim (agents)

- Reasoning agents may learn optimal query understanding settings via trial-and-error and persist what works.

## Cross-links (in this repo)

- Typed retrieval and mixture-of-encoders perspective: `mixture-of-encoders-query-understanding-noiz-summary.md`
- RAG ops checklist (staleness, metadata, evaluation): `rag-data-quality-retrieval-ops-noiz-summary.md`

