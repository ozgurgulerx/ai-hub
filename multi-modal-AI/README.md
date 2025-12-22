# Multi‑Modal AI

This folder is for notes and references on building AI systems that operate over **multiple modalities** (text, images, audio, video, structured data, and sensor/telemetry).

## What This Should Cover

- **Modalities + representations**: text tokens, vision embeddings, audio features, video time-series.
- **Fusion patterns**: early fusion vs late fusion, cross-attention, two-tower models, mixture-of-encoders.
- **Multimodal retrieval (RAG)**:
  - indexing strategies (separate vs joint indexes)
  - “events/highlights” for video
  - hybrid retrieval across transcript + visuals + metadata
- **Evaluation**: modality-specific metrics and end-to-end task evals; failure taxonomy.
- **Data + labeling**: weak supervision, alignment, quality pitfalls (OCR, tables, layouts).
- **Serving**: latency, caching, batching, and cost tradeoffs for multimodal pipelines.
- **Safety**: prompt injection via multimodal content, PII in images/audio, logging/retention.

## Suggested Structure (Planned)

- `notes/` — distilled notes and reading summaries
- `patterns/` — reusable architectures (pipelines, index layouts, fusion strategies)
- `examples/` — small demos (if/when added)
- `references/` — primary sources (papers, docs)

## Related (In This Repo)

- Multimodal video RAG notes: `../retrieval-augmented-systems/notes/multimodal-video-rag-kino-ai-trellis-noiz-summary.md`
- Document-heavy multimodal ingestion (VLM + CV): `../retrieval-augmented-systems/notes/better-rag-through-better-data-reducto-noiz-summary.md`
- Typed retrieval / mixture of encoders: `../retrieval-augmented-systems/notes/mixture-of-encoders-query-understanding-noiz-summary.md`

