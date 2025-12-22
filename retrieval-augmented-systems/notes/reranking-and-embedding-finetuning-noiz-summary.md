# Improving Retrievers with Reranking + Embedding Fine-Tuning — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/QMxCCxBYoaE`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat benchmark numbers, vendor comparisons, and specific failure-rate claims as **to verify** until corroborated by primary sources (talk recording, papers, benchmarks, or reproducible experiments).

## Where reranking fits (claims)

- Reranking is described as a “plug-and-play” layer between retrieval and the LLM context window.
- It is described as the lowest-hanging fruit because it does **not** require re-ingesting billions of database entries (unlike changing the embedding model).

Important caveat (consistent with other notes in this repo):
- Rerankers improve precision over the retrieved candidate set; they cannot recover items that were never retrieved. See also: `mixture-of-encoders-query-understanding-noiz-summary.md`.

## Reranker architectures (claims)

### Cross-encoder rerankers

- Cross-encoders are described as scoring query–document pairs jointly (cross-attention) and producing higher-quality similarity scores.

### ColBERT-style late interaction

- ColBERT is described as splitting work into:
  - offline document embedding
  - online token-level comparison
- This is described as enabling reranking at scale with manageable latency tradeoffs.

## Training rerankers (claims)

### Fine-tuning vs training from scratch

- Fine-tuning existing rerankers is described as yielding **~10–20%** recall improvements with less effort than training from scratch, especially when the dataset drifted from the original training distribution.

### Hard negative mining

- Hard negative mining is described as the key trick:
  - use an independent embedding model to select negatives that are close to the query in embedding space
  - train the reranker to learn meaningful distinctions in that “confusable” region

### Synthetic data cautions

- Synthetic data generation via LLMs is described as potentially hallucinating at high rates (example figure mentioned: **up to 70%**), making it unrecommended early if it degrades dataset quality. (Quantitative claim; to verify.)
- Synthetic generation is described as becoming valuable once you know your use cases and query types, to close the gap between query phrasing and chunks using high-quality examples (not random generation).

## Embedding model fine-tuning (claims)

- Fine-tuning embedding models and LLMs is described as important in specialized domains (legal/healthcare) where proprietary knowledge is absent from general training data.

Operational implication (inference):
- Changing an embedding model typically implies re-embedding/re-indexing content; plan for batch jobs, cost, and backfills. (Inference.)

## Performance/cost tradeoffs (claims)

- “Cohere’s reranking API” is described as outperforming open-source rerankers in benchmarks despite lacking fine-tuning. (Vendor claim; to verify.)
- Using very large models as rankers (example named: GPT‑3) is described as having meaningful maintenance/latency/inference complexity costs; best quality is not always the best system choice.

## System design considerations (claims)

- Hybrid search (full-text + vector) before reranking is described as a major lever for retrieval performance, but complex enough to require deeper discussion.
- Multimodal retrieval (text + images + other modalities) is framed as an important research frontier because it matches how humans interact with information.
- Retrieval quality depends materially on:
  - embedding model
  - vector index choice
  - retrieval architecture (hybrid, multi-feature / multi-index)

## Practical decision guide (distilled)

- Start with:
  - hybrid candidate generation (lexical + vector), if it fits latency/cost
  - reranking (cross-encoder or ColBERT-style) to improve precision
- Move to embedding fine-tuning when:
  - domain mismatch is the dominant failure mode, and
  - you can afford re-embedding/re-indexing operations
- Treat synthetic training data as a late-stage tool: validate your real datasets first.

## Appendix: Raw Notes (Preserved)

- “Re-ranking operates as a plug-and-play layer… no re-ingestion…”
- “Cross-encoder… ColBERT…”
- “Fine-tuning rerankers delivers 10-20% improvements…”
- “Hard negative mining…”
- “Synthetic data… hallucinate up to 70%…”
- “Cohere reranking API…”
