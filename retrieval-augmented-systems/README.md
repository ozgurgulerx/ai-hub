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

## Data quality & retrieval ops (trust killers)

Many RAG failures are “silent” and come from ingestion + retrieval ops, not the LLM:

- encoding / parsing inconsistencies
- irrelevant corpora
- noisy chunking
- stale indexes
- vague user queries routed to the wrong retrieval mode

Deep dive (Noiz summary notes; to verify): `notes/rag-data-quality-retrieval-ops-noiz-summary.md`

### Better RAG through better data (documents, tables, spreadsheets)

For document-heavy RAG, ingestion quality can dominate everything downstream. Hybrid extraction (deterministic CV + VLMs), hard-case eval sets, and retrieval-optimized representations (dynamic chunking, table summaries + section context) are recurring levers.

Deep dive (Noiz summary notes; to verify): `notes/better-rag-through-better-data-reducto-noiz-summary.md`

Scaling note (process + eval + HITL for enterprise doc automation; Noiz summary, to verify): `../ai-product-strategy/notes/document-automation-lessons-at-scale-noiz-summary.md`

### “Hallucinations” are usually data + retrieval failures (production metrics)

In production, many “hallucinations” are better understood as:

- bad/duplicated/outdated/conflicting documents, and/or
- low context relevance / low context usage (“context rot”)

Deep dive (Noiz summary notes; to verify): `notes/production-hallucinations-context-metrics-noiz-summary.md`

## Query understanding (structured routing before retrieval)

For many search/RAG systems, you get big gains by decomposing queries into structured attributes (category/color/brand/recency/location) and routing to the right backend or retrieval mode. The key is to optimize precision vs coverage and avoid high-latency synchronous LLM calls when possible (batch + cache + fallbacks).

Deep dive (Noiz summary notes; to verify): `notes/query-understanding-with-llms-doug-turnbull-noiz-summary.md`

## Typed retrieval: when text embeddings aren’t enough

Many “RAG relevance” failures aren’t about the generator — they’re about retrieval architectures that:

- rely on reranking to paper over weak initial candidate recall
- stringify numbers/lat-long/timestamps into text embeddings (often brittle)
- use boolean filters for *preferences* (hard intersections) instead of modeling them as soft bias signals

A proposed direction is **mixture of encoders** (specialized encoders for text + typed fields + user behavior) with query understanding that outputs:

- embeddings for soft preferences/personalization, and
- filters only for explicit constraints / access control

Deep dive (Noiz summary notes; to verify): `notes/mixture-of-encoders-query-understanding-noiz-summary.md`

## Evaluating embedding models (generative evals)

Public benchmarks can be a weak proxy for your corpus and your users. A practical approach is to generate a **corpus-specific** evaluation set:

- Filter to “queryable” chunks (LLM judge + human calibration).
- Generate realistic, messy queries from your own docs.
- Evaluate retrieval (precision/recall/NDCG) and iterate on the pipeline (reranking, hybrid search, contextualized chunking).

Deep dive (Noiz summary notes; to verify): `notes/generative-evals-embedding-models-noiz-summary.md`

## Production-grade retrieval (metrics, hybrid signals, late interaction)

Treat retrieval as a product system: align precision/recall/latency with business metrics, handle metadata and typed fields deliberately, and choose architectures (hybrid, late interaction, rank fusion) based on measured trade-offs under load.

Deep dive (Noiz summary notes; to verify): `notes/production-grade-retrieval-metrics-and-architectures-noiz-summary.md`

## Self-improving retrieval loops (production signals → better retrieval)

If retrieval is the bottleneck, improvements come from a feedback loop:

- instrument retrieval/ranking and collect **behavior signals**
- run simulations/backtests to compare algorithms safely
- ship changes continuously and re-measure

Deep dive (Noiz summary notes; to verify): `notes/self-improving-retrieval-algolia-noiz-summary.md`

## Reranking vs embedding fine-tuning

Reranking is often the fastest way to improve retrieval quality because it can be added between “candidate retrieval” and “LLM context” without re-embedding/re-indexing your entire corpus. However, rerankers cannot fix missing candidates; treat them as **precision boosters**, not recall miracles.

Deep dive (Noiz summary notes; to verify): `notes/reranking-and-embedding-finetuning-noiz-summary.md`

## Chunking fundamentals

Chunking is a first-order lever for retrieval recall. Default configs often fail; inspect chunk outputs and measure passage-level recall. Prefer semantic boundaries and keep enough context without mixing unrelated info.

Deep dive (Noiz summary notes; to verify): `notes/chunking-strategy-fundamentals-noiz-summary.md`

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

### GraphRAG (Graph RAG / relationship-aware retrieval)
- Uses **graph structure** to surface relationships that similarity search misses.
- Best when questions require **multi-hop** reasoning (“A relates to B via C”) or **global** synthesis across many documents.

#### Graph basics (quick primer)
- A **graph** is a set of **nodes** (entities/things) connected by **edges** (relationships).
- Common graph types:
  - **Directed vs. undirected** edges (A→B vs. A—B)
  - **Weighted** edges (strength/confidence/cost)
  - **Attributed** nodes/edges (metadata like source, timestamps, doc IDs)
- Typical operations used in RAG:
  - **Neighborhood expansion** (get k-hop neighbors around a node)
  - **Path finding** (how is X connected to Y?)
  - **Centrality / importance** (which nodes are “hubs”?)
  - **Community detection / clustering** (themes and subgraphs)

#### How GraphRAG is usually built
- **Extract** entities and relations from text (LLM + rules + NER), producing triples like `(Company) -[acquired]-> (Startup)`.
- **Store** the graph in a graph DB or index (or serialize as adjacency lists) with provenance to source chunks.
- **Link back to text**: keep edges/nodes pointing to the underlying passages so answers remain grounded.

#### Retrieval patterns (what “graph retrieval” means)
- **Entity-first routing**: identify key entities in the query, then retrieve their neighborhoods and associated source chunks.
- **Graph expansion**: expand 1–N hops to gather supporting context, then re-rank with a semantic reranker.
- **Community summaries**: summarize subgraphs (topics/communities) and retrieve summaries first, then drill down to evidence.

#### What matters most in practice (implementation priorities)
Research syntheses of GraphRAG methods consistently point to a few practical levers:

- **Operators > graph type**: ranking/traversal operators (e.g., link traversal + PPR, community ops, clustering) tend to predict retrieval quality more than “richer” graph schemas.
- **Richer graphs ≠ better**: add structure only if it is **discriminative** for your questions; simple trees/KGs can win when operators are strong.
- **Cost has a Pareto frontier**: evaluate accuracy gains against **token + latency** cost; avoid methods that are both slower and worse.
- **Dataset scale + question type drive architecture**: what works for mid-sized corpora and factoid QA may fail for large corpora and abstract cross-document synthesis.
- Deep dive: `notes/graphrag-what-matters.md`

#### Evaluating KG quality (LLM-based extraction)
Classical extraction metrics (NER F1, relation accuracy) often miss what you actually care about in GraphRAG:

- **Knowledge retention**: did the graph capture the important facts in the source text?
- **Downstream usefulness**: does the KG improve retrieval + multi-hop reasoning, or does the LLM “patch over” KG errors?

One practical framing from the KGGen work is **MINE** (Measure of Information in Nodes and Edges):

- **MINE-1 (retention)**: for a set of gold facts, check whether each fact is *recoverable* from a retrieved **two-hop subgraph**, judged semantically (often via an LLM judge).
- **MINE-2 (RAG utility)**: measure QA performance when retrieving **triples + 2-hop expansions**, then grounding back to the source text linked during extraction.
- Deep dive: `notes/kg-evaluation-mine.md`

Design implications:
- Keep **provenance**: every node/edge should link back to the supporting text chunk(s), or GraphRAG degrades fast.
- Invest in **entity/edge resolution** (avoid over-merging and synonym explosions) or multi-hop retrieval becomes noisy.
- Evaluate with both **retention** and **utility** so you can debug extraction vs retrieval vs generation separately.

#### Pitfalls
- **Extraction noise**: bad edges create convincing but wrong chains; keep confidence scores + provenance and validate.
- **Graph bloat**: uncontrolled entity explosion hurts relevance; normalize entities and cap expansion.
- **Grounding drift**: graphs help navigation, but answers should cite the underlying text evidence.

### Multimodal RAG (Video, Movement, “Events”)

Video retrieval adds time and multiple modalities (transcript, visuals, “what happens”). A practical pattern is to keep **separate indexes** (visual embeddings, transcript search, event/highlight summaries) and run **hybrid retrieval** across them, then rerank with richer context.

Deep dive (Noiz summary notes; to verify): `notes/multimodal-video-rag-kino-ai-trellis-noiz-summary.md`

### Ontologies (Semantic Governance for Enterprise RAG)
- An **ontology** is a semantic model of your business world: concepts (entities), relationships, and rules that sit *above* physical tables/files.
- In enterprise RAG, ontologies act as a “semantic contract” so retrieval is not just relevant, but also **authoritative and policy-compliant**.

How ontologies help RAG pipelines:

- **Authority & definitions**: distinguish gold vs. draft sources; standardize metric meanings (“Revenue”, “Active customer”).
- **Lineage-aware grounding**: keep provenance from answers back to governed sources and definitions.
- **Permission-aware retrieval**: enforce concept/attribute classifications (PII, confidential) and user/role policies.
- **Relationship-safe joins**: constrain what can be joined and how (valid relationships, allowed paths, level-of-granularity rules).

Implementation note: many teams prefer “SQL-based ontologies” (governed semantic views + policies in SQL) because they integrate with existing warehouse/lakehouse tooling and can be tested/validated like code.

Epistemology note: ontologies help define meaning and constraints, but **reasoning does not create missing facts**. For hybrid “infer vs validate” thinking (OWL/OWA vs SHACL/CWA) see `../ai-security-and-governance/docs/ai-governance/ontology-epistemology-owl-shacl.md`.

### Context Engineering (Filesystem-backed context for agents)

Context engineering is the practice of filling the context window with the **right minimal subset** of information for the next step. For agentic RAG systems, a filesystem can act as an external, persistent context store: write large intermediate results (search outputs, notes, plans) to disk and selectively re-load only what’s needed.

Deep dives:

- Filesystem as external context store: `notes/context-engineering-filesystem.md`
- “No vibes allowed” (context compaction + RPI workflow): `notes/context-engineering-no-vibes-allowed.md`
- Browser as a controlled data bridge for local/on-prem sources (OpenBB pattern; Noiz summary, to verify): `../projects/agents/agent-protocols/browser-data-bridge/README.md`

### RAG in the age of agents (agentic retrieval)

When retrieval is mediated by an agent loop, the “best” retriever is often the one that works with low friction under iteration. For codebases in particular, simple filesystem tools (`grep`, `find`) plus persistence can outperform heavier embedding retrieval in some regimes; treat embedding retrieval as one tool among many in a hybrid toolbox.

Deep dive (Noiz summary notes; to verify): `notes/rag-in-age-of-agents-agentic-retrieval-noiz-summary.md`

For coding-agent-specific retrieval lessons (including critiques of embedding-RAG over code and workflow alternatives like plan→act and TDD), see: `../ai-coding/notes/retrieval-for-autonomous-coding-agents-cline-noiz-summary.md`

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
