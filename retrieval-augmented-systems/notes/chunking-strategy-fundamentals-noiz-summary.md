# Chunking Strategy Fundamentals — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/GYj4Ay7SdWw`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat prescriptions and “best” defaults as **to verify** until corroborated by primary sources (talk recording or reproduced experiments).

## Why chunking exists (claims)

- Chunking allows retrieving specific passages across documents, enabling multi-doc evidence assembly that document-level retrieval misses.

## Two principles (claims)

- Use as much of the embedding model’s context window as is helpful for accuracy.
- Avoid grouping unrelated or “semantically similar-but-different” information that degrades retrieval.

## Implementation approaches (claims)

### Heuristic chunking

- Split by separators (newlines, punctuation).
- Described as brittle and dependent on clean pre-processing.

### Semantic chunking

- Use embeddings to identify meaning-based boundaries.
- Claimed advantage: less brittle; produces embedding-optimal chunks when using the same model for chunking and retrieval.

## Evaluation and debugging (claims)

- Recall of relevant passage retrieval is described as the primary metric for chunking.
- Default chunking configurations are described as frequently poor; inspect actual chunk outputs (look for too-short chunks due to bad delimiters).

## Cross-links (in this repo)

- RAG ops and chunking pitfalls: `rag-data-quality-retrieval-ops-noiz-summary.md`
- Generative evals for retrievers: `generative-evals-embedding-models-noiz-summary.md`

