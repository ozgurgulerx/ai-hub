# Advanced RAG Optimization (Sparse + Hybrid Retrieval)

This repo focuses on advanced RAG methods for LLMs with an emphasis on sparse retrieval
and hybrid pipelines. It is based on the material in
`/Users/ozgurguler/Downloads/2511 RAG Optimisation with Sparse Retrieval Methods.pdf`.

## Day001 (Secure RAG baseline)

Day001 adds a deliberately vulnerable RAG+tool mini-app plus an attack harness so you can measure security regressions.

```bash
python3 eval/harness/run_attack_pack.py --compare
```

Start here: `docs/day001/README.md`

## Why baseline RAG breaks
- Fragmentation: facts are correct but scattered across documents, so answers are incomplete.
- Semantic drift: dense similarity returns thematically related chunks that do not answer intent.
- Lexical brittleness: dense misses IDs and rare tokens; BM25 misses paraphrases.
- Proximity blindness: single-vector chunks lose token-level alignment.
- Global search: abstract queries need structure, not isolated leaves.

## Failure patterns mapped to remedies
- Fragmentation -> RAPTOR: hierarchical summaries and recursive retrieval.
- Semantic drift -> Hybrid retrieval + reranking, ColBERT-v2: intent-aligned re-ranking.
- Lexical brittleness -> SPLADE-v2: sparse-dense hybrid with learned term expansion.
- Proximity blindness -> ColBERT-v2: late interaction token matching.
- Global search -> GraphRAG or RAPTOR: clustered or hierarchical retrieval.

## Core methods in this repo
### RAPTOR (recursive abstractive processing for tree retrieval)
- Builds a summary tree: root overview -> section summaries -> leaf chunks.
- Replaces flat indexes with a hierarchical index to address fragmentation.
- Retrieval modes:
  - Summary-first routing (top-down beam search) for broad or multi-hop questions.
  - Hybrid leaf retrieval (summary + leaf union + rerank) for crisp, needle queries.
- Best for long technical docs, policies, specs, legal/scientific literature, and limited context budgets.

### ColBERT-v2 (late interaction retrieval)
- Token-level matching with MaxSim instead of whole-query similarity.
- Solves semantic drift and single-vector brittleness for complex queries.
- Practical at scale with compressed multi-vector indexes.
- Fit for legal, medical, and technical QA where precision matters.

### SPLADE-v2 (learned sparse retrieval)
- Learned lexical weights and term expansion on an inverted index (Lucene/OpenSearch).
- Exact match matters for entities, IDs, and rare terms while preserving recall.
- Combines sparse and dense signals for robust coverage across paraphrases and OOD queries.

### GraphRAG (relationship-aware retrieval)
- Uses graph structure to surface relationships that similarity misses.
- Supports multi-hop reasoning and global theme discovery.

## Recommended pipeline (from the source)
1) Hybrid search + semantic reranker
   - Combine BM25 and vector search, then re-rank top candidates.
2) Add advanced retrieval methods as needed
   - RAPTOR for hierarchy, ColBERT-v2 for token precision,
     SPLADE-v2 for sparse-dense coverage, GraphRAG for relationships.

## Source
- `Downloads/2511 RAG Optimisation with Sparse Retrieval Methods.pdf`
