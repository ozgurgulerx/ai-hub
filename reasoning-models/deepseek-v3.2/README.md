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

The following points are **claims from a secondary writeup** and should be treated as **unverified** until confirmed in official model cards / technical reports:

- **Long context**: claims **128K-token context** with stable long-context reasoning.
- **Dynamic sparse attention**: claims a learned “indexer” selects top-k relevant past tokens (≈2,048) so scaling is closer to **O(L × k)** rather than O(L²).
- **Two-stage training for sparsity**: claims (1) dense warm-up to imitate full attention, then (2) sparse training with alignment/consistency losses.
- **Tool-use + “thinking” integration**: claims tool-use is supported in both “thinking” and “non-thinking” modes, with a large synthetic agent-training data program (“1,800+ environments”, “85k+ complex instructions”).
- **Variant naming**: claims a “V3.2-Speciale” variant optimized for maximum reasoning, with higher token usage and “API-only” availability.
- **Benchmark-style claims**: claims “gold-level” results on competition-style tasks and near-frontier performance on coding/reasoning; treat as marketing until pinned to reproducible evals.
- **Attention variants (GQA/MLA/DSA)**: a separate talk-summary claims DeepSeek V3/R1 uses GQA (16 groups) and MLA (576-d latent compression), and that “DeepSeek Sparse Attention (DSA)” reduced compute/cost by 50% (Sep 2025); verify against primary sources.

Deep dive (preserved notes + verification checklist): `greek-ai-2025-12-03.md`
Related (talk-summary notes): `../../inference-engineering/reading/how-attention-got-so-efficient-noiz-summary.md`

## What to verify / fill in for V3.2 (pending primary sources)

Use this as a checklist for completing the model note once you have official material:

- Model family: dense vs MoE; routing design (if MoE); tokenizer; context length.
- Attention mechanism details (if any): whether “dynamic sparse attention” exists, its selection strategy (e.g., top-k), and what accuracy/latency tradeoffs it introduces.
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
