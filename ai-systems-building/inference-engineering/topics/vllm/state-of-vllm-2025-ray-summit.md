# State of vLLM 2025 (Ray Summit 2025) — Notes

Source: “State of vLLM 2025 | Ray Summit 2025” (YouTube): `https://www.youtube.com/watch?v=tN_-nktp1Hk`

This note distills **claims** from the talk summary provided in the prompt (not a verified technical report). Treat specific numbers and feature details as **to-verify** until confirmed in official vLLM docs/release notes.

## Performance & architecture optimization (claims)

- **V1 engine**: described as delivering a **~2× performance boost** by combining:
  - prefix caching
  - speculative decoding
  - CPU offloading
  - a “clean architecture” supporting various degrees of parallelism
- **Quantization**: described as supporting **15+ algorithms**, with hardware acceleration using **FP8/FP4** and **2×–4× performance** improvements “beyond memory savings alone”.
- **Deterministic batch-invariant mode**: described as ensuring **bitwise log probability matching regardless of prompt order**, positioned as enabling accurate RL rollouts with the exact model version used for training.

## Memory & cache management (claims)

- **Hybrid memory allocator**: described as managing KV-cache memory for “non-context reasoning models” with complex attention mechanisms such as:
  - sliding window attention
  - state space models
- **KV connector interface**: described as enabling moving KV cache between **vLLM GPU**, **CPU regions**, and **disk**, and supporting:
  - custom KV connectors
  - sparse attention mechanisms
  - “context parallel decodes”
  - ecosystem integrations mentioned: “LM cache” and “Moon LMD”
- **Agentic / multi-turn tool workflows**: described as optimizing KV cache for multi-turn conversations with external tool calls by keeping requests in a “special KV cache place” for immediate resumption when tool responses return (e.g., web search).

## Ecosystem & integration (claims)

- **Transformers backend (Hugging Face)**: described as enabling serving a broader model set, with additional optimizations including:
  - distributed pipeline parallelism
  - tensor parallelism “through a single flag”
- **Distributed architecture**: described as focusing on:
  - **cluster-in**: parallelism, fault tolerance, elasticity
  - **cluster-out**: routing, caching, operations
  - collaborations referenced: “ALMD” and “Nvidia Dynamo” for out-of-the-box distributed support

## Verification checklist (what to pin down in primary sources)

- What exactly “V1 engine” is (release/version boundary) and how the ~2× figure is measured.
- Which “15+” quantization algorithms are supported and what hardware paths enable FP8/FP4 gains.
- What “deterministic batch-invariant” guarantees cover (logprobs only vs tokens; hardware determinism; seed control).
- How KV connector APIs are exposed, the supported backends, and any constraints on moving KV across device tiers.
- Definitions for “non-context reasoning models”, “context parallel decodes”, “LM cache”, “Moon LMD”, and “ALMD” in vLLM context.

