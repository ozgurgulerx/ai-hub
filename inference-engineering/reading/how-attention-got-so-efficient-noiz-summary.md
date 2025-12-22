# How Attention Got So Efficient (MQA / GQA / MLA / DSA) — Noiz summary notes

Source video (YouTube): `https://www.youtube.com/watch?v=Y-o545eYjXM`

This note distills claims from a **Noiz** YouTube summary provided in the prompt. Treat quantitative figures and implementation details as **to verify** until confirmed via primary sources (papers, official model docs, or reproducible benchmarks).

## Attention fundamentals (as described)

- Attention is described as computing token relationships via **dot products** between **query** and **key** vectors, then applying **softmax** to normalize scores into attention weights.
- Tokenization is described as mapping text pieces to unique IDs and d-dimensional embedding vectors, with semantically similar words clustering in that space.

## Memory efficiency evolution (claims)

### Multi-Head Attention (baseline context)

The summary uses “Multi-Head Attention” as the baseline for KV-cache memory costs.

### Multi-Query Attention (MQA)

- Mechanism claim: share a **single** key and value vector across many query heads.
- Claimed impact: **128×** memory reduction (example framing: “4MB per token → 31kB per token”) at the cost of reduced expressive power.

### Grouped-Query Attention (GQA)

- Mechanism claim: split heads into **groups**; each group shares key/value pairs across multiple heads.
- Claimed DeepSeek usage: “16 groups in DeepSeek V3/R1”.
- Claimed impact: **8×** memory reduction vs Multi-Head Attention, while preserving model quality better than MQA.

### Multi-head Latent Attention (MLA)

- Mechanism claim: compress query/key/value representations into a lower-dimensional latent vector.
- Claimed DeepSeek usage: “576-dimensional compressed vector in DeepSeek V3/R1”.
- Claimed impact: **57×** reduction vs Multi-Head Attention, with a “slight performance improvement” attributed to learned compression.

## Production impact (claims)

### DeepSeek Sparse Attention (DSA)

- Claim: “DeepSeek Sparse Attention (DSA)” released in **September 2025** matches earlier model performance while cutting compute costs and API pricing by **50%** via a novel sparse attention variant.

## Verification checklist (what to pin down)

- What baseline is used for the memory ratios (per-token KV cache, which dtypes, which head counts, which sequence lengths).
- MQA:
  - what “single KV” means operationally (number of KV heads) and quality tradeoffs by task.
- GQA:
  - what “group” means (KV heads count vs Q heads count) and the exact configuration for DeepSeek.
- MLA:
  - formal definition of the “latent” compression and how it is trained/integrated.
  - whether “576-d” is constant across layers or configurable.
- DSA:
  - whether it is a standalone attention mechanism or part of a broader inference/training stack.
  - reproducible evidence for “50%” compute/cost reduction while matching quality.

## Related (in this repo)

- DeepSeek V3.2 note (third-party claims to verify): `../../reasoning-models/deepseek-v3.2/README.md`
- vLLM internals (KV cache and attention kernels): `../books/inference-engineering/chapters/03-vllm-architecture.md`

## Appendix: Raw Notes (Preserved)

- “MQA achieves 128x memory reduction…”
- “GQA… 16 groups in DeepSeek V3/R1… 8-fold memory reduction…”
- “MLA… 576-dimensional compressed vector in DeepSeek V3/R1… 57-fold reduction…”
- “DeepSeek Sparse Attention (DSA)… September 2025… cut compute costs and API pricing by 50%…”
