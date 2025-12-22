# Better RAG Through Better Data (Reducto CEO) — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/DS4w1CMGJes`

This note distills claims from a **Noiz** YouTube subtitles/summary provided in the prompt. Treat specific performance assertions and product names (“Excel V2”) as **to verify** until corroborated by primary sources (talk recording, docs, or a reproducible implementation).

## Core claim (as described)

For document-heavy RAG, “better data” (ingestion + representation) can dominate model choice: extraction errors and poor structure amplify downstream, especially for tables and complex layouts.

## Hybrid document understanding (claims)

### VLMs + traditional CV

- Vision-language models (VLMs) are described as strong at OCR-like tasks (handwriting, chart extraction) but weak on dense tables and complex layouts.
- A hybrid architecture is described as production-ready:
  - traditional computer vision for deterministic structure (e.g., forms/tables/checkboxes)
  - VLMs as a human-in-the-loop layer (including for sensitive data)

### Binary fields (checkboxes) are brittle

- VLMs are described as arbitrarily deciding checkbox states (≈50/50) for critical binary fields (example: vaccination status), requiring traditional CV for reliable checkbox prediction.

### Real-world layout “edge cases” matter

- Small skew (≈1–2 degrees) is described as a larger robustness issue than expected.
- Watermarks and scattered handwritten notes are described as common ingestion failure sources, motivating fallback pipelines.

## Evaluation and data quality (claims)

- Create **100–200 “hard cases”** to catch long-tail failure modes that are hard to detect in production.
- Ingestion mistakes are described as magnifying downstream impact, especially for tables; therefore table evaluation is emphasized.
- Fine-tuning VLMs with hundreds to ~1,000 examples is described as improving performance, but **label quality must be near-perfect** because small label issues are amplified.

## Output structure optimization (claims)

### Table formatting: HTML vs Markdown

- HTML is described as better for complex tables with merged cells.
- Markdown is described as more token-efficient for simpler tables.
- A heuristic is described: use a “merged-cell threshold” to automatically choose HTML vs Markdown based on table complexity.

### Reading order is critical

- In legal and other multi-column documents, reading order and layout parsing are described as essential because humans also struggle with creative layouts (“visual hodgepodge”).

## Retrieval optimization through better representations (claims)

### Dynamic chunking

- Dynamic chunking is described as preserving paragraphs, tables, and information blocks together.
- Chunk sizes are described as being adapted based on:
  - section information density
  - position
  - embedding similarity
- Relative position is described as a strong proxy for semantic relatedness across large corpora. (Claim; to verify.)

### Table summaries + section context

- A “cheap at scale” optimization is described:
  - generate natural language summaries of table contents
  - add section context to table chunks
- Use smaller language models for this preprocessing, then embed the enriched representation to improve retrieval.

### Separate optimization for embedding vs generation

- Embedding models and LLMs are described as having different limitations; optimize representations for embedding/retrieval specifically (“embedding-optimized representations”).

## Complex spreadsheet handling (“Excel V2”) (claims)

- Large spreadsheets are described as having:
  - information clumps that exceed model context windows
  - clusters with varying density
- A pipeline called “Excel V2” is described as using:
  - a vision model for clustering
  - sliding-window reasoning to find natural breakpoints

## Structured extraction as a multiplier (claims)

- Structured extraction is described as enabling:
  - knowledge graph creation
  - entity mapping
  - clause hierarchy extraction (legal tech)
- Customers are described as mapping extracted data back to parsed outputs for use cases like:
  - drilling manuals
  - multilingual magazines (including vertical text, rotated content)

## Practical checklist (distilled)

- Build a hybrid extractor: deterministic CV for structure + VLMs where they shine.
- Maintain a curated “hard cases” set (100–200) and regress against it.
- Treat tables/forms/checkboxes as first-class evaluation targets.
- Choose output formats based on structure complexity (Markdown vs HTML).
- Preserve layout semantics (reading order) before indexing.
- Use dynamic chunking and add section context; summarize tables for embedding retrieval.

## Appendix: Raw Notes (Preserved)

- “VLMs excel at handwriting and chart extraction but fail on dense tables… hybrid approach…”
- “Checkboxes… 50/50… need traditional CV…”
- “1-2 degree skew… watermarks… handwritten notes…”
- “Create 100-200 hard cases…”
- “HTML better for merge cells… Markdown more token-efficient… threshold…”
- “Dynamic chunking… preserve blocks… position proxies semantics…”
- “Summaries of tables + section context… cheap optimization…”
- “Excel V2… clustering + sliding window reasoning…”
