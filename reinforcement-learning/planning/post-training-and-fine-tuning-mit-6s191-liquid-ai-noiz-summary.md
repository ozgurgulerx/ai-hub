# Post-Training and Fine-Tuning (MIT 6.S191 / Liquid AI: Large Language Models) — Notes

Source video: https://www.youtube.com/watch?v=_HfdncCbMOE  
Transcript summary source (Noiz): https://noiz.io/tools/youtube-video-transcript  
Status: **To verify**

## Post-Training: What It Tries To Do

- Post-training is framed as transforming base models into useful assistants via supervised fine-tuning and preference alignment. [Unverified]
- Preference alignment is described as teaching the model to maximize the gap between chosen and rejected responses. [Unverified]

## Fine-Tuning Types (Use-Case Framing)

- General-purpose fine-tuning: make a versatile assistant. [Unverified]
- Domain-specific fine-tuning: embed specialized-field knowledge. [Unverified]
- Task-specific fine-tuning: focus on a single function (e.g., summarization). [Unverified]

## Fine-Tuning Data: What “Good” Looks Like (As Described)

- Balance accuracy, diversity, and complexity. [Unverified]
- Include correct answers, wide-ranging interactions, and challenging step-by-step reasoning examples. [Unverified]

## Data Generation and Quality Techniques

- Back-translation, scoring/filtering, and duplication removal are described as key for high-quality training data and avoiding test contamination. [Unverified]
- Preference data generation: query multiple LLMs, score with a judge LLM, then select best/worst as chosen/rejected pairs. [Unverified]

## Libraries and Techniques Mentioned

- Fine-tuning libraries mentioned:
  - TRL (positioned as “up-to-date research”). [Unverified]
  - “Axel” (YAML configs; name/identity to verify). [Unverified]
  - Unsloth (efficient single-GPU fine-tuning). [Unverified]
- LoRA is described as fine-tuning a small fraction of parameters (~0.5%), reducing VRAM/hardware cost. [Unverified]
- DPO is described as a cheaper/faster alternative to PPO for preference alignment, requiring two models instead of three. [Unverified]
- “Kilo” is mentioned as a parameter-efficient technique (details to verify). [Unverified]

## Model Merging

- Model merging is described as combining parameters from different models to add specific skills without compromising general capabilities. [Unverified]

## Evaluation (Benchmarks + Human + LLM Judges)

- Automated benchmarks (e.g., MMLU) are described as scalable and cost-effective. [Unverified]
- Human eval (e.g., Chatbot Arena) is described as providing real-world usability signal. [Unverified]
- “LLMs judging LLMs” is described as scaling evaluation via more samples and direct feedback, correlating with human ratings but requiring validation of judge quality. [Unverified]
- A combined approach (benchmarks + human + LLM judges + model comparisons) is described as necessary for robust evaluation. [Unverified]

## Optimization and Scaling Loops

- Test-time compute scaling is described as improving quality by generating multiple answers and selecting the best (e.g., best-of-n, process reward models). [Unverified]
- A post-training loop is described as spending roughly one-third of time each on data creation, model training, and evaluation. [Unverified]

## Multi-Turn Preference Alignment (Constraint)

- Multi-turn preference alignment is described as important; single-turn instruction following may not generalize well to more complex interactions. [Unverified]
- Create evaluation datasets early (before fine-tuning) and iterate based on model answers. [Unverified]

## Related (In This Repo)

- RLFT / RFT notes: `rlft_concepts.md`
- EvalOps (evaluation practice): `../../evalops/README.md`

