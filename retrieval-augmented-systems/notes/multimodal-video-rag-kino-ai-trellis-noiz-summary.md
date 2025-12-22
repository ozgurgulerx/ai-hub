# How RAG Changes When You Add Video, Emotion, and Movement — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/hmDGrFNTGxk`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat specifics (time intervals, model names, product architecture) as **to verify** until corroborated by primary sources (talk recording, docs, or a reproducible implementation).

## Problem framing (as described)

Video RAG adds a temporal + multimodal retrieval problem:

- Users may remember *what was said*, *what was seen*, or *what happened* (actions/movement), and want to locate moments across large corpora (hundreds of hours).
- Embeddings can be noisy across modalities; success comes from giving multiple retrieval axes and then reranking with richer context.

## Core architecture (claims)

### “Video as 4D data” with a Trellis-like hierarchy

- A “Trellis” framework is described as treating video as “4D data” by separating:
  - what’s said (transcript)
  - what’s seen (visual content)
  - what happens (events/movement)
- This is described as being represented in a hierarchical tree structure to locate moments quickly across large footage collections.

Note: another note in this repo uses “Trellis” to describe bucketing an AI app’s output space for monitoring/workflows. It’s **unclear** whether the same framework/name is being referenced. (Unverified.)

### Multi-index strategy

The ingestion/indexing pipeline is described as producing multiple indexes:

- **Visual index**: multimodal embeddings computed every **10–15 seconds**, capturing things like hand movements, object interactions, prominent colors, zooms, and transitions.
- **Transcript index**: text embeddings / sparse text indexing over speech-to-text transcripts.
- **Highlight index**: “core events” summarized into highlights spanning **~10 seconds to 1 minute**, aggregating multimodal + text embeddings.

## Retrieval strategy (claims)

### Hybrid retrieval across modalities

- Retrieval is described as searching **visual, transcript, and highlight** indexes simultaneously.
- Results are described as aggregated based on:
  - embedding quality and/or confidence (conceptually)
  - user-defined modality weights

### Modality tradeoffs

- Visual embeddings are described as excelling for purely visual searches.
- Text embeddings are described as more reliable (“battle-tested”) for text-based queries due to lower noise.

### Prompt decomposition for low-noise searches

- Query decomposition is described as extracting core components (e.g., person + object of interest) and using:
  - sparse text indexing when users know what was said
  - semantic embeddings when users know what was seen/happened

## Advanced processing (claims)

### LLM reranking with long context

- Large-context language models (example named: “GPT‑4.11”) are described as serving as rerankers to determine what the video contains, using transcripts + highlights as context.

### Graph databases for entity relationships

- Graph databases are described as relating entities across footage (example: sunglasses worn by different people), enabling:
  - auto-tagging
  - relationship-aware retrieval and reasoning

Related: GraphRAG overview and evaluation notes: `../README.md`, `graphrag-what-matters.md`, `kg-evaluation-mine.md`

## Technical risks / gotchas (claims)

- Multimodal embeddings are described as requiring high-quality training data and careful handling of temporal features; fusing visual/audio/text across time can lose context/meaning.

## Design implication (as described)

- “Recall-based search” is prioritized for expert users (e.g., filmmakers) who know the footage but need help locating specific moments; pre-indexing and keeping visual vs text cues separate is described as improving retrieval.

## Appendix: Raw Notes (Preserved)

- “Trellis framework treats video as 4D data by separating what's said, what's seen, and what happens…”
- “Multimodal embeddings index video every 10-15 seconds…”
- “Highlight indexing creates concise representations… 10 seconds to 1 minute…”
- “Hybrid retrieval searches across visual, transcript, and highlight indexes… weights…”
- “LLMs with large context windows like GPT-4.11 serve as rerankers…”
- “Graph databases relate entities across footage…”
