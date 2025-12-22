# Production-Grade Retrieval (Metrics, Hybrid Signals, Late Interaction) — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/GnY4mdma7TU`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat technical claims and prescriptions as **to verify** until corroborated by primary sources (talk recording, papers, or reproduced experiments).

## Align retrieval metrics to business metrics (claims)

- Establish explicit links between technical metrics (precision/recall/latency) and business outcomes (CTR, ticket resolution).
- Don’t apply expensive techniques (e.g., reranking) everywhere; use them when they move key results and when recall/quality warrants the cost.
- Combine offline eval metrics with production cases to iterate robustly.

## Vector representation techniques (claims)

### Late interaction

- Late interaction is described as keeping token vectors separate and scoring per-token, avoiding pooling/averaging unpredictability.

### Fine-tuning dense encoders (triplet loss)

- Triplet-loss fine-tuning can separate near-opposites (e.g., “good Wi‑Fi” vs “bad Wi‑Fi”).
- Small data can make embeddings closer to cross-encoder rankings. (To verify data requirements.)

### Sparse + dense fusion

- Combine sparse and dense representations; use rank fusion/interleaving and rerank if single-pass scoring isn’t available.

## Data handling and context assembly (claims)

- Treat non-text/non-image data as first-class (don’t stringify timestamps/ids).
- Metadata (authorship, timestamps, org structure) is described as as-important-as content for disambiguation.
- LLMs struggle with timestamps/temporal ordering; explicit retrieval ordering is described as necessary.

## Query optimization (claims)

- Use query templates and have LLMs fill intent slots (recency, popularity, location) using smaller models and parallelization.

## Vector DB tradeoffs (claims)

- Full-scan optimized vector DBs enable flexible scoring (sparse+dense in one pass) but can be compute-expensive.
- Approximate in-memory ANN can have recall issues with metadata boosting; benchmark under concurrent reads/writes.

## Cross-links (in this repo)

- Typed retrieval + encoders: `mixture-of-encoders-query-understanding-noiz-summary.md`
- Reranking vs embedding fine-tuning: `reranking-and-embedding-finetuning-noiz-summary.md`
- Latency for agents: `../inference-engineering/reading/groq-head-of-evals-rag-agents-fast-noiz-summary.md`

