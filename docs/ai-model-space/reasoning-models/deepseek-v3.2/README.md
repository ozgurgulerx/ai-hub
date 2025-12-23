# DeepSeek-V3.2

DeepSeek-V3.2 refers to the **DeepSeek-V3** family of base models (and an incremental “.2” revision) that are commonly discussed as strong foundations for **reasoning-tuned** models such as **DeepSeek-R1**.

This note is intentionally **spec-light**: add official links/model cards and verified numbers (context length, sizes, benchmarks) as you collect primary sources.

## What it is (in the reasoning stack)

- A strong **general-purpose base LLM** that can be used as the foundation for reasoning-focused post-training (SFT/RL/verifiers).
- In the DeepSeek ecosystem, V3 is discussed as the base that makes “simple” outcome-reward RL recipes work better than earlier generations.

## What we know (high confidence, from cited sources)

- DeepSeek’s R1 line is described as building reasoning capability primarily via **large-scale reinforcement learning** with **outcome-based / rule-based rewards** on tasks where correctness can be checked (e.g., math/coding). See the R1 paper.
- The notes in `deepseek-r1.pptx` indicate R1-Zero is based on a DeepSeek-V3 base model and highlight the importance of base model quality for RL to “take off”.

## Third-party claims to verify (Dec 2025)

This section collects **claims from secondary sources** and should be treated as **unverified** until confirmed in official model cards / technical reports and/or source code.

### Claims (high-level)

- **Long context**: claims **128K-token context** with stable long-context reasoning.
- **Two-stage training for sparsity**: claims (1) dense warm-up to imitate full attention, then (2) sparse training with alignment/consistency losses.
- **Tool-use + “thinking” integration**: claims tool-use is supported in both “thinking” and “non-thinking” modes, with a large synthetic agent-training data program (“1,800+ environments”, “85k+ complex instructions”).
- **Variant naming**: claims a “V3.2-Speciale” variant optimized for maximum reasoning, with higher token usage and “API-only” availability.
- **Benchmark-style claims**: claims “gold-level” results on competition-style tasks and near-frontier performance on coding/reasoning; treat as marketing until pinned to reproducible evals.

Deep dive (preserved notes + verification checklist): `greek-ai-2025-12-03.md`
Related (talk-summary notes): `../../../inference-engineering/reading/how-attention-got-so-efficient-noiz-summary.md`

## DeepSeek Attention (DSA): indexer-selected sparse attention (unverified, code-informed summary)

DeepSeek V3.2 is often described as using a sparse attention mechanism sometimes referred to as **DeepSeek Attention (DSA)** or “dynamic sparse attention”.

Core idea (claimed): introduce a learned **indexer** that selects the **top-k most relevant key tokens** for each query token, making attention sparse and moving scaling toward **O(L × k)** instead of O(L²).

### What’s novel (as described)

- The attention pattern becomes **data-dependent**: the model learns to choose which past tokens are worth attending to.
- The selection can use **indexer heads** that are optimized for *ranking/retrieval* rather than directly reusing the attention Q/K.

### How the indexer is described to work (pseudocode-level)

Described as a 3-step process:

1) Compute **indexer queries** and **indexer keys** across “indexer heads”.
2) Compute a **weight per indexer head** based on relevance to the current query.
3) Compute indexer scores via scaled dot product, then **gate** (ReLU) and **scale** (head weight) to produce token relevancy scores.

The output is an **index mask** (top-k token selection). That mask is then used to replace the usual **causal mask** in the model’s attention implementation (described as “regular MLA attention”), yielding sparse attention.

### Important caveats (as described)

- **Indexer queries** are computed from the *attention queries*, not directly from the hidden states, because the goal is to select tokens relevant to the query vectors that will drive attention.
- **Indexer keys** and **head weights** are computed from hidden states (not from attention keys), to learn ranking/retrieval patterns that may differ from attention key representations.

### Implementation/efficiency notes (as described)

- The indexer and the attention path are described as being computed and cached in **FP8**, with optimizations (e.g., caching scaling factors, rotating activations) intended to reduce quantization loss.

### Open questions to test

- Does the model still show “attention sink” behaviors under sparse selection?
- How sensitive is quality to `k` (top-k size) across tasks (code vs long-doc reasoning)?
- What’s the failure mode: missed long-range dependencies vs noise/over-selection?

## What to verify / fill in for V3.2 (pending primary sources)

Use this as a checklist for completing the model note once you have official material:

- Model family: dense vs MoE; routing design (if MoE); tokenizer; context length.
- Attention mechanism details (if any): whether “dynamic sparse attention / DSA” exists, its selection strategy (e.g., top-k), and what accuracy/latency tradeoffs it introduces.
- Training mix: data sources, multilingual balance, code/math weighting.
- Post-training: instruction tuning recipe, safety alignment, tool-use/function calling.
- Tool-use details: whether tool-use is integrated with a “thinking” mode; what the tool-calling interface and constraints are.
- Long-context behavior: max context, long-context evals, and failure modes (retrieval inside context, truncation sensitivity).
- Reasoning deltas in “.2”: release notes, eval deltas, and any inference/runtime changes.
- Deployment: supported runtimes (CUDA/ROCm/Ascend), quantization availability, reference serving stack.

## Practical “where it fits”

- If you want a **reasoning model**: treat V3.2 as the base; then evaluate whether you need R1-style post-training, verifiers, and/or test-time techniques (self-consistency, tool use, re-ranking).
- If you want **cost/latency efficiency**: prioritize architecture details (MoE vs dense), quantization support, and serving stack maturity.

## References

- DeepSeek-R1: *Incentivizing Reasoning Capability in LLMs via RL* (paper link referenced in notes): `https://arxiv.org/pdf/2501.17161`
- “RLHF help generalise better” (referenced in notes): `https://arxiv.org/pdf/2310.06452`
- Reproduction effort mentioned in notes: `https://github.com/Jiayi-Pan/TinyZero`
- DeepSeek V3.2 landing page (verify model card / license / specs): `https://www.deepseek.com/`
- Hugging Face repo (verify files, license, context, variants): `https://huggingface.co/deepseek-ai/DeepSeek-V3.2/tree/main`
