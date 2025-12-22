# Retrieval-Augmented Systems (Advanced RAG + Secure RAG Lab)

This folder combines:

- A hands-on **secure RAG baseline** (Day001) with an attack harness and small defenses.
- A curated set of **advanced retrieval notes** (sparse/hybrid/graph/multimodal, evaluation, and ops).

Some material references a local PDF (`/Users/ozgurguler/Downloads/2511 RAG Optimisation with Sparse Retrieval Methods.pdf`) that is not stored in-repo.

## Start here

- Secure RAG lab: `docs/day001/README.md`
- Advanced notes index: `notes/README.md`

## Day001 (Secure RAG baseline)

Day001 adds a deliberately vulnerable RAG+tool mini-app plus an attack harness so you can measure security regressions.

```bash
python3 eval/harness/run_attack_pack.py --compare
```

Start here: `docs/day001/README.md`

## What usually breaks (failure map)

- **Bad data**: outdated/duplicate/conflicting documents and ingestion errors.
- **Bad retrieval**: missing candidates (recall), noisy candidates (precision), stale indexes.
- **Bad representation**: chunking and typed fields (numbers/timestamps) mishandled.
- **Bad agent loops**: latency compounding, context rot, wrong tool choice.

Use `notes/README.md` to jump to the relevant deep dive.

## Notes index (start here for concepts)

The main README stays short; the full topic map lives in `notes/README.md`.

## Recommended pipeline (from the source)
1) Hybrid search + semantic reranker
   - Combine BM25 and vector search, then re-rank top candidates.
2) Add advanced retrieval methods as needed
   - RAPTOR for hierarchy, ColBERT-v2 for token precision,
     SPLADE-v2 for sparse-dense coverage, GraphRAG for relationships.
3) Add live web grounding when recency matters
   - For “what changed recently?” or missing internal sources, add a web search + content fetch layer and treat results as untrusted inputs.
   - Example provider notes: `../ai-startups/notes/exa.md`
4) Make latency a first-class constraint (agents)
   - Multi-step agents compound latency across tool calls and retries; measure TTFT/TPS/end-to-end and optimize with parallelism + caching.
   - Inference notes (Noiz summary; to verify): `../inference-engineering/reading/groq-head-of-evals-rag-agents-fast-noiz-summary.md`

## Source
- `Downloads/2511 RAG Optimisation with Sparse Retrieval Methods.pdf`
