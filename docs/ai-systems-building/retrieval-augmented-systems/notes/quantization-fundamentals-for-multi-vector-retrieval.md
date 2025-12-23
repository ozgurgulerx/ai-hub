# Quantization Fundamentals for Multi-Vector Retrieval

Multi-vector retrieval (e.g., ColBERT-style late interaction) stores **many embeddings per document** (often token-level). This improves precision (less semantic drift; better “needle” retrieval), but explodes index size and memory bandwidth requirements. **Quantization** is what makes multi-vector indexing practical at scale.

Primary reference:
- Isaac Flath, “Quantization Fundamentals for Multi-Vector Retrieval” (2025-12-01): https://isaacflath.com/writing/QuantizationFundamentalsForMultiVectorRetrieval

## Why this matters for agents

Coding and tool-using agents benefit disproportionately from high-recall, high-precision retrieval:
- Better retrieval → fewer retries, fewer tool calls, fewer tokens in downstream synthesis.
- Multi-vector retrieval tends to improve “local alignment” (identifiers, APIs, symbols) that single-vector chunk embeddings often miss.

The catch: token-level vectors mean **orders of magnitude** more vectors to store and search.

## Quantization: the core tradeoff

Quantization compresses numeric representations (e.g., FP32/FP16 → int8 / bit-packed codes), trading a small amount of accuracy for:
- smaller indexes (fits in RAM/VRAM)
- faster search (memory bandwidth is often the bottleneck)
- cheaper infra (fewer GPUs / smaller instances)

## Levels of quantization used in retrieval

### 1) Scalar (uniform) quantization

Quantize each scalar value into a small number of discrete levels (e.g., 256 levels for 8-bit). This is the simplest mental model:
- choose `min`/`max` (or calibration stats)
- map float → integer bucket
- reconstruct approximately when needed

Works well for intuition but can accumulate error across high-dimensional embeddings.

### 2) Vector quantization (VQ)

Instead of quantizing each dimension independently:
- cluster vectors (often k-means)
- store **cluster id** per vector
- store **centroids** as the codebook

Pros: captures correlation across dimensions.  
Cons: needs many centroids for high fidelity (codebook size grows fast).

### 3) Product quantization (PQ)

PQ is the workhorse for large-scale embedding compression:
- split each embedding into `m` sub-vectors (subspaces)
- run k-means separately per subspace (often `k=256`, giving 8 bits per sub-vector)
- store `m` small codes instead of the full float vector

Why it’s powerful:
- you get high compression without a single gigantic codebook
- distances can be approximated efficiently via lookup tables

Key knobs to tune:
- `m` (number of sub-vectors): higher → better fidelity, more compute
- `k` / bits per sub-vector: higher → better fidelity, larger codes and codebooks
- normalization + similarity choice (cosine vs dot/L2): affects calibration and error sensitivity

### 4) Residual / “extreme” quantization (ColBERT-style)

Some systems quantize:
1) a coarse representation (PQ), then
2) the **residual** (what’s left after subtracting the centroid) using very low-bit encoding

The post highlights a common pattern:
- bucketize residual values into small integer bins
- extract bits for each bin (bitwise operations)
- **pack bits** densely into bytes for storage efficiency

This is how multi-vector indexes can store many token embeddings while staying tractable.

## Practical evaluation checklist (don’t guess)

When adopting PQ / residual quantization for multi-vector retrieval:
- Measure retrieval quality: `Recall@k`, `MRR`, `nDCG` on your query set (including “ID/needle” queries).
- Measure end-to-end utility: agent task success rate, time-to-fix, token usage, tool-call count.
- Measure infra: index size, QPS, P95 latency, memory bandwidth utilization, GPU utilization.

## Where this fits in the RAG stack

- If you’re using **ColBERT / late interaction**, quantization is often the difference between “prototype” and “production”.
- If you’re on single-vector embeddings, quantization still matters (ANN indexes), but the pressure is usually lower than token-level indexing.

