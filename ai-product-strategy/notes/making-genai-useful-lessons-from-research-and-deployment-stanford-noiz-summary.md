# Making GenAI Useful: Lessons from Research and Deployment (Stanford Webinar) — Notes

Summary for: https://youtu.be/9-eXLFvAoKM  
Generated from transcript tooling (Noiz): https://noiz.io/tools/download-youtube-transcript  
Status: **To verify**

## Capabilities + Post-Training

- Base models are described as more capable than expected, but often require context engineering to surface capabilities.
- Continued pre-training and supervised fine-tuning are described as key post-training processes.
- Emergent capabilities are described as often unplanned.

## Evaluation and Improvement

- Internal evals based on production use cases/feedback are described as more effective than external evals for “usefulness”.
- Steerability and instruction-following are highlighted as important (format, negative/ordered instructions, content constraints).
- Grounding is emphasized as central to truthfulness/reliability; correctness is not guaranteed by “sounding grounded”.

## Alignment + Model Specification

- A model specification is described as important for intended behavior alignment; it should be open-sourced, updated, and receive diverse feedback to reduce internal bias (as described).
- Default behavior should accommodate diverse applications (chat vs API UX differences are mentioned as an example).

## Infra + System Design

- Build surrounding systems to remain adaptable to changing model capabilities (avoid brittle infra assumptions).
- There are described opportunities beyond copywriting/coding in enterprise/support use cases.

