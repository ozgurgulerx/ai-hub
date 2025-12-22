# GraphRAG Foundations — 2 Years of KGs and GenAI (Recap) — Notes

Summary for: https://youtu.be/IlI3uNjquKI  
Generated from summary tooling (Noiz): https://noiz.io/tools/youtube-summary  
Status: **To verify**

## Why “Vectors + Graphs”

- Vectors are described as capturing semantic similarity, while graphs add **explainability** and **structured proximity** through relationships/topology.
- The recap emphasizes contextualizing retrieval by understanding **why** items are similar (relationships/structure), not only that they are similar.

## Document Graphs + Domain Graphs

- A pattern described: represent source structure as a document graph (chapters/subchapters/fragments) and combine with a domain graph (entities/relationships) to enable multiple navigation paths.
- Combine vector search with graph traversals enriched by schemas/ontologies to explore context both “blind” (semantic) and “explicit” (entities/relations).

## Ontology-Driven Construction

- Ontologies/target schemas are described as prerequisites for building manageable/queryable KGs, improving terminology consistency and alignment.
- Practical approach described: map structured data (tables/relational exports) to an ontology, then add unstructured extraction iteratively with post-processing and feedback.

## LLM-Assisted Domain Modeling (With Human Refinement)

- LLMs are described as helping generate initial graph models from structured data and iteratively improving them with feedback (including critique loops).
- The recap frames this as enabling faster modeling at scale, with validation/refinement by domain experts.

## Agentic Patterns

- Agentic apps can offer multiple retrieval techniques as tools, with an LLM reasoner selecting tools based on the question and dynamically loading new tools from ontology stored in the graph (as described).

