# Diffusion Models (for Generative Modeling)

This section focuses on diffusion-based generative models and how they compare to (and can complement) transformer LLMs. While diffusion is dominant in image/video generation, diffusion-style approaches for **text and sequences** are an active research area.

## What A Diffusion Model Is

Diffusion models learn to generate data by reversing a gradual noising process:
- **Forward process**: corrupt data step-by-step (add noise / mask / replace tokens).
- **Reverse process**: learn to denoise step-by-step to recover samples from noise.

For language, diffusion is often implemented in one of two broad styles:
- **Continuous-space diffusion** over embeddings/latents (then decode to text).
- **Discrete diffusion / masking** over tokens (categorical transitions).

## Why Diffusion for Text (Potential Upsides)

- **Global editing / infilling**: naturally supports filling missing spans and iterative refinement.
- **Better controllability**: conditioning can be applied throughout denoising steps.
- **Alternative decoding**: not strictly left-to-right next-token generation.

## Key Trade-offs vs. Transformers

- **Inference cost**: diffusion typically requires many denoising steps (can be slower than autoregressive decoding).
- **Quality/throughput**: strong results exist, but frontier LLM ecosystems largely optimize for autoregressive.
- **Tooling maturity**: fewer standard eval harnesses and production patterns for text diffusion.

## What To Learn Here

- Diffusion fundamentals: objectives, schedules, sampling, guidance, distillation.
- Discrete diffusion for sequences: token transition kernels, masking strategies.
- Hybrid systems: diffusion components combined with transformers (or used for editing).
- Evaluation: quality, controllability, latency/cost trade-offs, safety.

## Suggested Structure (Planned)

- `notes/`: paper summaries (text diffusion, discrete diffusion, sampling speedups)
- `experiments/`: small demos (infilling, editing, controllable generation)
- `benchmarks/`: tasks + evaluation notes for diffusion vs. autoregressive
- `assets/`: diagrams and visuals

## References (Starter List)

- "Diffusion-LM: ... for Text Generation" (text diffusion approaches)
- "D3PM: Discrete Denoising Diffusion Probabilistic Models" (categorical/discrete diffusion)
- "DiffuSeq / SeqDiffuSeq" (sequence-to-sequence diffusion variants)

