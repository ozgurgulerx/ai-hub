# AI Startups

A curated list of AI startups worth tracking across the AI stack (models, inference, agents, eval, security, data, and apps).

## Curation Rules

- Prefer **primary sources**: product docs, papers, repos, benchmarks, or customer case studies.
- Avoid “hype-only” entries; include a short **why it matters** and **evidence** link(s).
- Keep claims precise; if something is uncertain, label it as **Unverified**.
- Update entries when the product changes (add a “Last verified” date).

## Listing Format

Add one row per startup:

| Startup | Category | What it does (1 line) | Why it matters | Evidence / Links | Last verified |
| --- | --- | --- | --- | --- | --- |
| Exa | Retrieval / RAG / memory | API-first web search + crawling for agent grounding | Fresh, source-backed context for agents without building a crawler/search stack | `notes/exa.md`, `https://exa.ai/exa-api`, `https://youtu.be/SuR_3sIo_XM` | Unverified |
| LanceDB | Retrieval / RAG / memory | Vector DB / “multimodal lakehouse” built on the Lance format | Single store for vectors + large blob data; claims focus on random-access + multimodal scale | `notes/lancedb.md`, `https://lancedb.com/`, `https://youtu.be/y5g7u3sWyrk` | Unverified |
| Reducto | Data tooling (ingestion) | Document ingestion/extraction for RAG (tables, layouts, spreadsheets) | “Better data” can dominate RAG quality; ingestion errors amplify downstream | `notes/reducto.md`, `https://youtu.be/DS4w1CMGJes` | Unverified |
| turbopuffer | Retrieval / RAG / memory | Object-storage-first vector + hybrid search (cache-heavy) | Makes billion/trillion-scale vector storage economically plausible; adds filtering/facets/aggs | `notes/turbopuffer.md`, `https://turbopuffer.com/`, `https://youtu.be/l2N4DT35PKg` | Unverified |
| Braintrust | EvalOps / safety evals | Eval + observability platform for LLM apps | Makes evaluation and iteration repeatable; turns “vibes” into measured engineering | `notes/braintrust.md`, `https://www.braintrust.dev/` | Unverified |

## Categories (Suggested)

- Models & training
- Inference & serving
- Agents & orchestration
- Retrieval / RAG / memory
- EvalOps / safety evals
- Security & governance
- Data tooling (labeling, quality, lineage)
- Developer tooling (IDE, code review, docs)
- Enterprise apps (support, sales, operations)

## Big Ideas

Visionary themes, narratives, and contrarian theses (not company lists). Use these to track “where the world is going” and then link to startups that embody each idea.

- Index: `big-ideas/README.md`

## Patterns

Cross-cutting patterns that help interpret startup/company moves (funding dynamics, distribution shifts, stack-layer consolidation).

- Index: `patterns/README.md`

## Notes

- If you want deeper writeups per company, add `ai-startups/notes/<startup>.md` and link it from the table.
  - Tooling-first entries should also capture the “layer” they sit in (grounding, vector store, ingestion, eval, safety, execution, inference).
