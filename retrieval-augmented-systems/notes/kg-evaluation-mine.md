# Evaluating LLM-Extracted Knowledge Graphs for GraphRAG (KGGen / MINE-1, MINE-2)

LLM-generated knowledge graphs are increasingly used for **GraphRAG** and multi-hop retrieval. The hard part isn’t “can we extract triples?”—it’s **can we measure whether the graph is good enough to trust and useful enough to keep**.

This note distills a practical evaluation split highlighted in the KGGen work: evaluate (1) **knowledge retention** and (2) **RAG usefulness**.

## Why classic metrics aren’t enough

- **NER F1 / RE accuracy** measure local extraction correctness, but not whether the KG captures the *information content* of the document.
- **Downstream QA-only** is confounded: a strong LLM can answer despite a weak KG, masking extraction failures.

## Common failure modes in LLM KG extraction

- **Over-merging**: collapsing distinct entities (“Type 1” vs “Type 2”) because strings/embeddings look similar.
- **Predicate explosion**: unbounded relation phrases create many near-duplicates (“acquired”, “bought”, “purchased”) and fragment retrieval.
- **Disconnected graphs**: lots of isolated triples that don’t support multi-hop inference.
- **Ungrounded edges**: triples without pointers back to supporting text make QA brittle and debugging painful.

## Two-level evaluation: retention vs usefulness

### MINE (Measure of Information in Nodes and Edges)

**MINE** evaluates whether the KG preserves and exposes information in a way that supports inference.

### MINE-1: Knowledge retention

Goal: “How much of the source text’s knowledge is recoverable from the KG?”

High-level protocol:

1) Start from documents with a small set of **gold facts**.
2) Extract a KG from the documents.
3) For each fact, retrieve relevant nodes/edges (often via embeddings), then extract a **two-hop subgraph** around them.
4) Use a semantic judge (often an LLM judge) to decide whether the fact can be **inferred** from the subgraph.
5) Score = fraction of recoverable facts.

Why it’s useful: it rewards graphs that are **well-connected** and **semantically faithful**, not just syntactically similar.

### MINE-2: KG-assisted RAG usefulness

Goal: “Does the KG improve retrieval + reasoning in a QA workflow?”

High-level protocol:

1) Build a KG over a corpus used for QA.
2) For each question, retrieve relevant **triples** (text + embedding retrieval), then expand with **two-hop** neighbors.
3) Retrieve the **grounding text** linked to those triples (provenance is mandatory).
4) Answer with LLM using the retrieved triples + grounding text.
5) Judge correctness (often LLM-as-judge with calibration to human samples).

Why it’s useful: it measures whether the KG adds **structured inductive bias** that helps multi-hop retrieval.

## Pipeline pattern that tends to work (KGGen-style)

Many successful systems look “hybrid”: LLMs for extraction + deterministic components for scaling and consistency.

- **Stage 1 (LLM)**: extract entities, then extract triples constrained to those entities (reduces schema drift vs one-shot triple generation).
- **Stage 2 (non-LLM)**: aggregate across documents (normalize strings, dedupe obvious duplicates) to form a global graph.
- **Stage 3 (hybrid)**: entity/edge resolution at scale
  - cluster by embeddings
  - retrieve candidates (BM25 + embedding similarity)
  - use an LLM to decide “same or different”
  - choose a canonical form + aliases; iterate

## Engineering implications (what these evals force you to build)

- **Grounded triples**: every edge needs pointers to source spans/chunks, or you can’t debug and MINE-2 collapses.
- **Entity/edge resolution**: avoid both
  - **over-merging** (“Type 1” ≠ “Type 2”), and
  - synonym bloat (duplicate nodes/predicates).
- **Embedding choice matters**: both protocols rely on retrieval over facts/questions and nodes/triples.
- **Separate concerns**: measure extraction (MINE-1) separately from retrieval utility (MINE-2) to locate bottlenecks.
- **LLM-as-judge**: treat judging as a component you must harden (deterministic prompting, calibration vs human samples, regression tests).
- **Operator design still dominates**: even a “good” KG needs the right traversal/ranking/subgraph operators and cost budgets to be useful at query time. See `graphrag-what-matters.md`.
- **Inference vs completeness**: don’t expect reasoning to “fill in” missing data; separate inferred consequences from unknowns and validate completeness explicitly when needed. See `../../ai-security-and-governance/docs/ai-governance/ontology-epistemology-owl-shacl.md`.

## References (TODO)

- KGGen paper (arXiv): add link
- KGGen repo: add link
