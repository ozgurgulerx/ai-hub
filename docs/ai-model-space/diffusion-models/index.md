# Diffusion Models

This section focuses on diffusion-based generative models and how they compare to (and can complement) transformer LLMs.

## What A Diffusion Model Is

Diffusion models learn to generate data by reversing a gradual noising process:
- **Forward process**: corrupt data step-by-step (add noise / mask / replace tokens)
- **Reverse process**: learn to denoise step-by-step to recover samples from noise

## Why Diffusion for Text

- **Global editing / infilling**: naturally supports filling missing spans
- **Better controllability**: conditioning applied throughout denoising
- **Alternative decoding**: not strictly left-to-right

## Key Trade-offs vs Transformers

- **Inference cost**: many denoising steps (can be slower)
- **Tooling maturity**: fewer production patterns for text diffusion

## Notes

- [Simple diffusion language models](notes/simple-diffusion-language-models-noiz-summary.md)
