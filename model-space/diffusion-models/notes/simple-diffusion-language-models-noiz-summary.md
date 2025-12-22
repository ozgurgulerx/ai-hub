# Simple Diffusion Language Models — Notes

Source video: https://www.youtube.com/watch?v=WjAUX23vgfg  
Noiz transcript source: https://noiz.io/tools/youtube-video-transcript  
Status: **To verify**

## Core Architecture (Masked Diffusion for Text)

- A masked diffusion language model is described as starting from all blank (masked) tokens and iteratively filling in words using a BERT-style architecture, enabling **parallel** sampling rather than strictly sequential generation. [Unverified]
- Reported performance claim: perplexity 23 vs autoregressive baseline 20.9 on LM1B and OpenWebText. [Unverified]

## Noise Process (Masking Schedule)

- Masking noise is described as flipping a coin for each word with probability (1 − α_t), where α_t is the probability of masking at that location at diffusion step t. [Unverified]
- This defines a stochastic unmasking schedule controlling which tokens are predicted at each step. [Unverified]

## Training Methodology (Denoising Objective)

- Training is described as combining masked language modeling with a denoising objective: sample a noised version of the signal, weight by expected change during denoising, and reconstruct the original signal. [Unverified]
- Generation is described as applying learned denoising functions and remasking predicted words, while never remasking already-predicted tokens. [Unverified]

## Dual-Purpose Capability (Generation + Representation Learning)

- The objective is described as similar to BERT, enabling representation learning alongside generation.
- Claim: significantly better GLUE scores than autoregressive models while retaining full generative capability; framed as superior to other diffusion-based text generation approaches. [Unverified]

