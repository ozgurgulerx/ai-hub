# DeepSeek-V3.2

DeepSeek-V3.2 refers to the **DeepSeek-V3** family of base models (and an incremental “.2” revision) that are commonly discussed as strong foundations for **reasoning-tuned** models such as **DeepSeek-R1**.

This note is intentionally **spec-light**: add official links/model cards and verified numbers (context length, sizes, benchmarks) as you collect primary sources.

## What it is (in the reasoning stack)

- A strong **general-purpose base LLM** that can be used as the foundation for reasoning-focused post-training (SFT/RL/verifiers).
- In the DeepSeek ecosystem, V3 is discussed as the base that makes “simple” outcome-reward RL recipes work better than earlier generations.

## What we know (high confidence, from cited sources)

- DeepSeek’s R1 line is described as building reasoning capability primarily via **large-scale reinforcement learning** with **outcome-based / rule-based rewards** on tasks where correctness can be checked (e.g., math/coding). See the R1 paper.
- The notes in `deepseek-r1.pptx` indicate R1-Zero is based on a DeepSeek-V3 base model and highlight the importance of base model quality for RL to “take off”.

## What to verify / fill in for V3.2 (pending primary sources)

Use this as a checklist for completing the model note once you have official material:

- Model family: dense vs MoE; routing design (if MoE); tokenizer; context length.
- Training mix: data sources, multilingual balance, code/math weighting.
- Post-training: instruction tuning recipe, safety alignment, tool-use/function calling.
- Reasoning deltas in “.2”: release notes, eval deltas, and any inference/runtime changes.
- Deployment: supported runtimes (CUDA/ROCm/Ascend), quantization availability, reference serving stack.

## Practical “where it fits”

- If you want a **reasoning model**: treat V3.2 as the base; then evaluate whether you need R1-style post-training, verifiers, and/or test-time techniques (self-consistency, tool use, re-ranking).
- If you want **cost/latency efficiency**: prioritize architecture details (MoE vs dense), quantization support, and serving stack maturity.

## References

- DeepSeek-R1: *Incentivizing Reasoning Capability in LLMs via RL* (paper link referenced in notes): `https://arxiv.org/pdf/2501.17161`
- “RLHF help generalise better” (referenced in notes): `https://arxiv.org/pdf/2310.06452`
- Reproduction effort mentioned in notes: `https://github.com/Jiayi-Pan/TinyZero`

