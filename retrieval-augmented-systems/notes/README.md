# Advanced RAG Notes — Index

This folder is the “knowledge base” part of `retrieval-augmented-systems/`: distilled notes, design patterns, and evaluation ideas for building retrieval systems that hold up in production.

All `*-noiz-summary.md` notes are **claims-to-verify** summaries from provided transcripts; treat them as hypotheses until pinned to primary sources or reproduced.

## Start here

- If you want a hands-on **secure RAG baseline**: `../docs/day001/README.md`
- If you want the “what to build next” mental model: start with:
  - Data + ops: `rag-data-quality-retrieval-ops-noiz-summary.md`
  - Evaluation: `generative-evals-embedding-models-noiz-summary.md`
  - Latency for agents: `../../inference-engineering/reading/groq-head-of-evals-rag-agents-fast-noiz-summary.md`

## 1) Data, ingestion, and “trust killers”

- `rag-data-quality-retrieval-ops-noiz-summary.md` — ingestion pitfalls, staleness, vague queries, evaluation tactics
- `better-rag-through-better-data-reducto-noiz-summary.md` — document-heavy ingestion (tables/layouts/spreadsheets), dynamic chunking, table summaries
- `production-hallucinations-context-metrics-noiz-summary.md` — production hallucinations as data/context failures; context relevance/usage metrics

## 2) Chunking and representation

- `chunking-strategy-fundamentals-noiz-summary.md` — chunking principles, semantic vs heuristic chunking, recall-first debugging
- `mixture-of-encoders-query-understanding-noiz-summary.md` — typed retrieval and “mixture of encoders” framing (text vs numbers/lat-long/timestamps)

## 3) Query understanding and routing

- `query-understanding-with-llms-doug-turnbull-noiz-summary.md` — structured attribute extraction + routing; precision vs coverage; batch/caching patterns

## 4) Retrieval architectures and optimization

- `production-grade-retrieval-metrics-and-architectures-noiz-summary.md` — align retrieval metrics to business metrics; hybrid signals; late interaction; DB tradeoffs
- `reranking-and-embedding-finetuning-noiz-summary.md` — reranking vs embedding fine-tuning; hard negatives; synthetic data cautions
- `self-improving-retrieval-algolia-noiz-summary.md` — production feedback loops (signals → backtests → ship → re-measure)

## 4a) Core retrieval methods (quick primer)

These show up repeatedly across modern RAG stacks:

- **RAPTOR**: hierarchical summaries + top-down retrieval for fragmentation/multi-hop.
- **ColBERT (late interaction)**: token-level matching to reduce semantic drift and improve precision.
- **SPLADE (learned sparse)**: lexical coverage (IDs/rare tokens) with learned term expansion; often combined with dense retrieval.
- **GraphRAG**: relationship-aware retrieval when questions require multi-hop/global synthesis.

## 5) Graph RAG and knowledge graphs

- `graphrag-what-matters.md` — operators, cost/perf tradeoffs, what matters in GraphRAG implementations
- `kg-evaluation-mine.md` — evaluating KG extraction quality (MINE-1/2 framing)

## 6) Multimodal RAG

- `multimodal-video-rag-kino-ai-trellis-noiz-summary.md` — video RAG patterns (visual/transcript/highlight indexes, hybrid retrieval, reranking)

## 7) Agents, context engineering, and long-context limits

- `limits-of-long-context-models-kelly-hong-noiz-summary.md` — why “more context” can reduce reliability; distractors/context rot
- `context-engineering-filesystem.md` — filesystem-backed context engineering patterns
- `context-engineering-no-vibes-allowed.md` — compaction + RPI workflow for big codebases
- `rag-in-age-of-agents-agentic-retrieval-noiz-summary.md` — agentic retrieval: start simple (`grep`/`find`) and iterate end-to-end

## 8) Security-specific notes

- `day001_lit_review.md` — “minimum viable canon” reading bullets for Secure RAG Day001

## 9) Enterprise governance (related)

- Ontologies + epistemology (meaning vs validation; OWL vs SHACL): `../../ai-security-and-governance/docs/ai-governance/ontology-epistemology-owl-shacl.md`
