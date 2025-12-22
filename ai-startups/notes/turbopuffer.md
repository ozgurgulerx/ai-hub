# turbopuffer (Object-storage-first vector + hybrid search) — Notes

Primary site (as provided earlier in conversation): `https://turbopuffer.com/`

Talk source (YouTube; Noiz summary): “Billion Scale Vector Storage for RAG”: `https://youtu.be/l2N4DT35PKg`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat all numbers and customer claims as **to verify** until corroborated by primary sources (docs, benchmarks, case studies).

## What it is (as described)

- turbopuffer is described as a vector storage/search system designed for very large scale, emphasizing:
  - object storage (S3/GCS/Azure Blob) as the default persistence layer
  - caching to achieve low latency
  - hybrid search (semantic + full text) plus filtering/faceting/aggregations

## Architecture claims (to verify)

### “Pufferfish” + object storage-first

- Stores data on object storage by default (S3/GCS/Azure Blob).
- Uses JIT-style caching to turn ~**500ms** cold queries into **sub-10ms** hot queries in RAM by caching at ~**1GB+/sec**.
- Framing: enables trillion-scale vector search economically.

### Cost claim

- Object-storage-first is described as ~**10× cheaper** than SSD-based storage for large indices.

## Production impact claims (to verify)

- Cursor is described as reducing costs by **95%** and indexing much larger repos with “unlimited horizontal scaling” across many namespaces.
- Notion is described as saving millions and handling **10B+ vectors**, large write peaks, and millions of namespaces with minimal operational overhead.

## Bottleneck claim: embedding latency dominates

- Embedding model latency is described as a critical bottleneck for real-time search (example cited: OpenAI embeddings at ~**300ms P50**).
- Low-latency embedding alternatives are named (Cohere, Gemini, “Vina”). (To verify models and measurements.)

## Search capabilities (claims)

- Hybrid search is described as combining semantic + full-text search with:
  - filtering
  - faceting
  - aggregations
- Use case framing: enables “context engineering” without loading everything into the context window (filter by color/size/price; summarize aggregates).

## Consistency tradeoffs (claims)

- Strong consistency is described as simplifying reasoning (“immediately available after write”).
- It can be disabled for performance; eventual consistency is described as enabling **sub-10ms P99** latency. (To verify.)

## Late interaction and index optimizations (claims)

- Supports late interaction models by sending top-K vectors per token and doing a second-layer query for term cover. (To verify mechanics and economics.)
- Quantization and clustering are described as improving economics (smaller vectors reduce storage and export costs).

## Practical adoption checklist (distilled)

- Measure end-to-end latency: embedding generation often dominates DB latency.
- Benchmark hot vs cold query performance and cache behavior.
- Validate hybrid search needs (filters/facets/aggs) vs pure ANN.
- Validate consistency requirements for your app and multi-tenant namespaces.

