# LanceDB (Lance format + “multimodal lakehouse”) — Notes

Primary site: `https://lancedb.com/`

Talk summary source (Noiz): “Keynote: The Post-Modern Data Stack for AI: Open Source Foundations for a Multimodal La...” (Chang She): `https://youtu.be/y5g7u3sWyrk`

This note distills claims from the prompt, including a Noiz summary of a keynote. Treat quantitative claims and benchmark-like statements as **to verify** until backed by primary sources (docs, papers, reproducible benchmarks).

## What it is (as described)

- LanceDB is described as a vector database built on **Lance**, positioned as a “multimodal lakehouse” (vectors + large blob assets such as images/videos) rather than “embeddings-in-a-table”.

## Keynote claims (to verify)

### Data infrastructure evolution

- **Lance format 2D layout**: described as enabling **~100× faster random access** for search versus “traditional formats”, while maintaining fast scan performance like Parquet/Iceberg.
- **Blob + tabular in one table**: described as efficiently managing large blob data (images/videos) alongside tabular data.
- **Zero-copy evolution**: described as allowing incremental addition of feature columns/embeddings without copying original data (avoiding backfills).
- **Multimodal lakehouse scale**: described as scaling to **tens to hundreds of petabytes** of blob assets while keeping a “single source of truth” through open-source format integration with existing tooling.
- **Legacy search constraints**: Elasticsearch is described as lacking compute-storage separation, making it costly at AI data scale; managing multiple systems for different data types is described as reducing research productivity.

### AI data characteristics (as described)

- AI data is described as:
  - **~6× larger** than traditional tabular data (embeddings/images/videos).
  - Generated **~100× faster** by models than humans.
  - Heterogeneous (long prompts, audio, video, embeddings).

### Industry trends (as described)

- “carsonization”: JVM projects rewritten in Rust.
- Multimodal data treated as a first-class citizen from inception.
- Designing for “agent experience” via better integration primitives such as **MCP servers**.

## Practical questions to verify before adopting

- What “100× random access” is measured against (workload, hardware, dataset, dtype).
- How Lance compares to Parquet/Iceberg for:
  - scans vs random reads
  - indexing + vector search workloads
  - schema evolution and adding embeddings
- How blobs are stored and retrieved (layout, caching, partial reads).
- How LanceDB integrates with existing data tooling (connectors, compute engines, catalogs).

## Appendix: Raw Notes (Preserved)

- “Lance format introduces 2D data layout enabling 100x faster random access…”
- “Zero-copy data evolution… adding new feature columns and embeddings without copying…”
- “LanceDB's multimodal lakehouse architecture scales to tens to hundreds of petabytes…”
- “Three key AI infrastructure trends… carsonization… multimodal… agent experience (MCP servers)…”
