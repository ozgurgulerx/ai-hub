# “We’re Ahead of Where I Thought We’d Be” — Gemini 3 & the Future of AI — Notes

Summary for: https://youtu.be/cNGDAqFXvew  
Generated from transcript tooling (Noiz): https://noiz.io/tools/download-youtube-transcript  
Status: **To verify**

## Architecture & Training Philosophy

- Gemini 3 improvements are framed as the culmination of many changes (pre-training + post-training) by a large team, shifting from “single model training” to full system building. [Unverified]
- Mixture of Experts (MoE) is described as decoupling compute from parameters via expert routing, building on older research. [Unverified]
- Native multimodality is described as processing text/images/audio in one model but increasing complexity and compute costs (esp. large images). [Unverified]

## Data Regime & Synthetic Data

- Gemini 3 is described as operating in a data-limited regime; synthetic data from strong models is used to train future models. [Unverified]
- Synthetic data is framed as powerful but dangerous; requires controls to avoid degradation loops. [Unverified]
- Pre-training mix is described as multimodal from the ground up with diverse sources. [Unverified]

## Evaluation & Alignment

- Evaluation is framed as one of the hardest/most underrated problems; benchmark contamination is highlighted. [Unverified]
- Two eval gaps are described:
  1) predicting scaled-up performance from smaller pre-trained models,
  2) proxying post-training performance from pre-training evals. [Unverified]
- Alignment is framed as primarily post-training, but pre-training needs negative examples to learn to avoid harmful behavior. [Unverified]

## Long Context & Retrieval

- Long-context improvements are described as ongoing with more innovation expected. [Unverified]
- RETRO is referenced as retrieval-augmented architecture work that combines with pre-training improvements. [Unverified]

## Advanced Reasoning & Workflows

- “Deep Think” is described as hypothesis generation/testing, tool use, and search calls (not just deeper compute). [Unverified]
- Agentic workflows are framed as accelerating research by automating infra work like running/babysitting experiments and analysis, not fully automating research. [Unverified]

## Trajectory

- Next 2–3 years framed as containing potential for scientific discoveries and rapid improvements. [Unverified]
- Continual learning is described as externalizing knowledge via search/retrieval and expanding context in pre-training. [Unverified]

