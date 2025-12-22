# Retrieval-Augmented Systems

This folder contains a comprehensive guide to building production RAG systems, plus a hands-on secure RAG lab.

## Start Here

| Resource | Description |
|----------|-------------|
| **[RAG Comprehensive Guide](notes/RAG-comprehensive-guide.md)** | Complete reference covering data quality, chunking, embeddings, retrieval architectures, reranking, GraphRAG, context engineering, evaluation, and security |
| [Secure RAG Lab](docs/day001/README.md) | Hands-on vulnerable RAG app + attack harness for testing defenses |

## What Usually Breaks

- **Bad data** — Outdated, duplicate, or conflicting documents; ingestion/parsing errors
- **Bad retrieval** — Missing candidates (recall), noisy results (precision), stale indexes
- **Bad representation** — Poor chunking, typed fields (numbers/timestamps) mishandled
- **Bad context** — Token bloat, context rot, distractors degrading model performance

## Recommended Pipeline

1. **Hybrid search + reranking** — Combine BM25 and vector search, rerank top candidates
2. **Advanced retrieval as needed** — RAPTOR (hierarchy), ColBERT (precision), SPLADE (sparse-dense), GraphRAG (relationships)
3. **Context discipline** — Small relevant windows, frequent compaction, recall before precision
4. **Continuous evaluation** — Reference-free evals, corpus-specific benchmarks, end-to-end metrics

## Lab

Run the attack harness against the secure RAG baseline:

```bash
python3 lab/eval/harness/run_attack_pack.py --compare
```

See `docs/day001/README.md` for setup and details.
