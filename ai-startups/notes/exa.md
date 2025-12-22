# Exa (Web search + crawling for agents) — Notes

Primary site (as provided): `https://exa.ai/exa-api`

Related talk (YouTube): “Future of RAG w/ Exa.ai’s CEO Will Byrk” (Noiz summary): `https://youtu.be/SuR_3sIo_XM`

This note captures descriptions provided in the prompt, including a Noiz summary of a talk. Treat product feature names, internal mechanism claims, and quantitative statements as **to verify** until pinned to official docs or primary material.

## What it is (as described)

- An API-first web search engine + crawler intended for **agent grounding** (search + fetch contents + crawl subpages).

## Why AI search is different (claims; to verify)

- “Search stays necessary” framing: models are finite-sized, while the web is vastly larger, so you can’t “memorize everything” in the model.
- Traditional search engines are framed as optimized for:
  - short keyword queries
  - few results presented to humans
- AI/agent search is framed as needing:
  - long, context-rich queries
  - comprehensive retrieval (the model can process a lot of content quickly)
  - results suitable as *inputs* to downstream reasoning and workflows

Example query pattern (as described): “find me every YC-funded AI startup with details”.

## Claimed differentiators (to verify)

- “Semantic-first retrieval” (embedding-driven relevance) rather than keyword/SEO ranking.
- Search modes tuned for agent workflows (named: `neural`, `deep`, `fast`, `auto`).
- Tight search→content→crawl loop designed for RAG/agent pipelines.

## Architecture (claims; to verify)

- Documents are pre-processed into **embeddings** and ingested into a “custom neural database”.
- Search-time retrieval is described as embedding-based nearest-neighbor search over that index.

## Performance and cost optimizations (claims; to verify)

- **Matryoshka training** (multi-size embeddings) is described as enabling flexible embedding sizes for speed/cost tradeoffs.
- **Clustering** is described as searching only the most relevant clusters close to the query rather than the full corpus.
- **Low-level SIMD CPU optimizations** are described as part of making embedding search fast and cost-effective.

## Relevance signals (claims; to verify)

- The embedding model is described as incorporating **authority**, **relevancy**, and **recency** directly into embeddings, rather than relying only on a separate reranker.

## Search paradigm shifts (claims; to verify)

- “Perfect search” is framed as requiring variable test-time compute: some queries could take seconds (or longer) depending on complexity, unlike traditional “half-second” search expectations.
- Exa is described as exposing more control knobs for product builders (result count, date ranges, domain filters, categories) versus consumer search engines that hide complexity.

## Business model and incentives (claims; to verify)

- Exa is described as charging per query (example pricing mentioned: “$200/month for deep research”) rather than ads, aligning incentives with result quality.
- Embedding-based neural search is described as being more resistant to SEO manipulation than keyword-based retrieval. (Treat as a claim; SEO-adversarial dynamics are complicated in practice.)

## Advanced features (claims; to verify)

- An “answer endpoint” is described as providing quick, streamed answers (not just links/results), targeting AI applications that want concise information.
- Synthetic data generation is described as being used for training and generating complex queries, using techniques compared to frontier LLM training pipelines.

## Where it fits

- Useful when you need **fresh** sources (news, changing docs) and want to ground agent answers in current web content.

## Open questions

- How “meaning-based” ranking is implemented and evaluated (benchmarks, spam resistance).
- Content fetching/crawling policy (robots, rate limits, caching, attribution).
- Cost, latency, and reliability under high-volume agent workloads.
- What “authority/recency in embeddings” means operationally and how it interacts with reranking.
