# AI Infrastructure Startups: Reference Guide

This guide profiles key AI infrastructure companies across the stack—from data quality to vector storage to web search. Use it as a reference when evaluating tools for your AI systems.

---

## The AI Infrastructure Stack

| Layer | Function | Example Companies |
|-------|----------|-------------------|
| **Data Quality** | Labeling, preference data, verifiers | Surge AI |
| **Document Ingestion** | Parsing, extraction, chunking | Reducto |
| **Vector Storage** | Embeddings, hybrid search | LanceDB, turbopuffer |
| **Web Search** | Agent grounding, real-time retrieval | Exa |
| **EvalOps** | Evaluation, observability, iteration | Braintrust |
| **Vertical AI** | Domain-specific applications | Harvey (legal) |

---

## Surge AI — Data Quality & Human Evaluation

**What it is:** Human data labeling and evaluation platform focused on teaching models "taste" and subtle quality notions.

### Core Thesis

- Expert human evaluation is a better progress measure than noisy benchmarks
- Data quality goes beyond checkbox labeling—includes uniqueness, imagery, emotional impact
- Benchmarks are often flawed, enabling hill-climbing without solving real problems

### Products

- Rubrics and verifiers
- Preference data
- RL environments (simulating real-world scenarios with tools, objectives, multi-turn)
- Trajectory data (including failures and inefficient paths as training signals)

### Notable Claims

- $1B revenue in under 4 years with <100 employees (bootstrapped)
- Operates more like a research lab than typical startup
- Contrarian GTM: minimal social promotion, no VC funding

### Key Insight

Reaching very high reliability (99% → 99.9%) takes much longer than automating large fractions of tasks—the last mile is the hardest.

---

## Exa — Web Search for Agents

**What it is:** API-first web search engine + crawler for agent grounding (search + fetch + crawl).

### Why AI Search Is Different

| Traditional Search | AI/Agent Search |
|-------------------|-----------------|
| Short keyword queries | Long, context-rich queries |
| Few results for humans | Comprehensive retrieval |
| Results as endpoints | Results as inputs to reasoning |

### Architecture

- Documents pre-processed into embeddings
- Custom neural database for nearest-neighbor search
- Semantic-first retrieval vs keyword/SEO ranking

### Search Modes

- `neural` — Embedding-based semantic search
- `deep` — Comprehensive retrieval
- `fast` — Quick results
- `auto` — Adaptive selection

### Performance Optimizations

- **Matryoshka training** — Multi-size embeddings for speed/cost tradeoffs
- **Clustering** — Search only relevant clusters
- **SIMD optimizations** — Fast, cost-effective embedding search

### Relevance Signals

Authority, relevancy, and recency incorporated directly into embeddings (not just reranker).

### Business Model

Per-query pricing (not ads) aligns incentives with result quality. Embedding-based search claimed more resistant to SEO manipulation.

---

## LanceDB — Multimodal Lakehouse

**What it is:** Vector database built on Lance format, positioned as "multimodal lakehouse" (vectors + large blob assets).

### Lance Format Advantages

- **2D data layout** — ~100× faster random access vs traditional formats
- **Blob + tabular** — Images/videos alongside tabular data in one table
- **Zero-copy evolution** — Add feature columns/embeddings without copying original data
- **Petabyte scale** — Tens to hundreds of petabytes of blob assets

### AI Data Characteristics

- ~6× larger than traditional tabular data
- Generated ~100× faster by models than humans
- Heterogeneous (prompts, audio, video, embeddings)

### Industry Trends Driving Design

- "Carsonization" — JVM projects rewritten in Rust
- Multimodal as first-class citizen
- Agent experience via MCP servers

### When to Consider

- Managing large blob assets alongside embeddings
- Need schema evolution without backfills
- Existing data lakehouse investment

---

## turbopuffer — Object-Storage-First Vector Search

**What it is:** Vector storage/search designed for very large scale on object storage (S3/GCS/Azure Blob).

### Architecture: "Pufferfish"

- Object storage as default persistence layer
- JIT-style caching: ~500ms cold → sub-10ms hot queries
- Cache throughput: ~1GB+/sec

### Economics

- ~10× cheaper than SSD-based storage for large indices
- Enables trillion-scale vector search economically

### Production Claims

| Customer | Impact |
|----------|--------|
| **Cursor** | 95% cost reduction, unlimited horizontal scaling |
| **Notion** | 10B+ vectors, millions of namespaces, minimal ops overhead |

### Search Capabilities

- Hybrid search (semantic + full-text)
- Filtering, faceting, aggregations
- Late interaction model support
- Quantization and clustering for economics

### Key Insight

**Embedding latency dominates:** OpenAI embeddings at ~300ms P50 can be the bottleneck, not DB latency. Consider low-latency alternatives (Cohere, Gemini).

### Consistency Options

- Strong consistency (immediately available after write)
- Eventual consistency for sub-10ms P99 latency

---

## Braintrust — EvalOps & Observability

**What it is:** AI observability/EvalOps platform for evaluations, logging/tracing, and iteration loops.

### Core Capabilities

- Evaluations
- Logging and tracing
- Datasets and experiments
- Prompt/model iteration

### Why It Matters

"Measure → iterate → win" depends on repeatable evals and production traces, not vibes.

### Questions to Evaluate

- What primitives are first-class (traces, datasets, eval runs, graders)?
- What integrations exist (LLM SDKs, RAG frameworks, CI/CD)?
- Self-hosting and data residency options?
- Pricing and operational overhead at scale?

---

## Harvey — Legal AI

**What it is:** AI platform for law firms, focused on enabling firms rather than competing with them.

### Shared Playbooks

- Package proven contract language and market intelligence
- Deliver first-pass contract reviews in minutes
- Enable redlines "with a few clicks"

### Real-Time Synchronization

When firm updates rules, client playbooks sync automatically—no manual distribution.

### Secure Collaboration

"Shared Spaces" provide branded, secure environment for firm↔client collaboration.

### Strategy

Making every law firm AI-first > building a single AI-first law firm (avoids conflicts of interest).

---

## Reducto — Document Ingestion

**What it is:** Document ingestion platform for RAG pipelines.

### Core Capabilities

- Hybrid extraction (layout + OCR + VLM)
- Table handling with intelligent formatting
- Dynamic chunking preserving document structure

*See RAG Comprehensive Guide for detailed ingestion patterns.*

---

## Quick Reference: When to Use What

| Need | Consider |
|------|----------|
| High-quality human labels/preference data | Surge AI |
| Agent grounding with fresh web content | Exa |
| Large-scale multimodal data + embeddings | LanceDB |
| Cost-effective trillion-scale vector search | turbopuffer |
| Eval loops and production observability | Braintrust |
| Complex document parsing for RAG | Reducto |
| Legal document automation | Harvey |

---

## Evaluation Checklist

Before adopting any tool:

1. **Benchmark on your workload** — Vendor claims may not match your use case
2. **Measure end-to-end latency** — Often dominated by embedding generation, not DB
3. **Understand pricing model** — Per-query, per-vector, per-GB, or subscription
4. **Check integration story** — Connectors, SDKs, existing tooling compatibility
5. **Validate consistency requirements** — Strong vs eventual, multi-tenant isolation
6. **Assess operational overhead** — Self-hosting options, data residency, scaling complexity
