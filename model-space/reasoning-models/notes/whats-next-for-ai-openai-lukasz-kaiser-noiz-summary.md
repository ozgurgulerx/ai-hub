# What’s Next for AI? OpenAI’s Łukasz Kaiser (Transformer Co-Author) — Notes

Summary for: https://youtu.be/3K-R4yVjJfU  
Generated from transcript tooling (Noiz): https://noiz.io/tools/download-youtube-transcript  
Status: **To verify**

## Reasoning Models and Chain-of-Thought (Claims)

- GPT-5.1 is described as generating chain-of-thought tokens primarily for its own reasoning (not for users), and using tools (e.g., browsing) during internal thinking to verify facts and extract information. [Unverified]
- Reinforcement learning is described as “differentiating through the reasoning part” and pushing the model toward actions that lead to better answers in verifiable domains (math/coding/science). [Unverified]
- Reasoning models are described as increasing capability faster than pre-training by using more tokens to think, but remaining jagged: strong in some areas, weak in others. [Unverified]
- GPT-5.1 is described as still struggling with some simple logic puzzles (five-year-old math book example), motivating continued human oversight in high-stakes settings. [Unverified]

## Model Training Evolution: GPT-5 → GPT-5.1 (Claims)

- GPT-5 improvements are described as coming from reinforcement learning and synthetic data for reasoning/model quality, while GPT-5.1 post-training focused on safety/tone and reducing hallucinations. [Unverified]
- Pre-training is described as still valuable, and combining it with RL on larger models is described as yielding better results. [Unverified]

## Long-Running Agents and Compaction (Claims)

- “GPT-5.1 Codex Max” is described as designed for long-running workflows spanning days/weeks, using compaction to operate across multiple context windows totaling millions of tokens. [Unverified]
- Compaction is described as summarizing the most important information and forgetting less relevant parts, enabling longer runs by managing attention/memory limits. [Unverified]

## Production Economics and Distillation (Claims)

- Distillation is described as economically necessary for serving very large user bases, because running the largest models for everyday chat is unsustainably expensive. [Unverified]
- Scaling laws and GPU economics are described as shaping research priorities and production model size decisions. [Unverified]

## Interpretability Status (Claims)

- Interpretability progress is described as improving circuit tracing in sparse/smaller models, while larger models remain hard to fully understand. [Unverified]

## Multimodal and Generalization (Claims)

- Multimodal reasoning (text+vision+audio) is described as lagging behind text-only models due to synthetic data generation and base-model retraining costs. [Unverified]
- Reasoning models are described as working best in verifiable domains; subjective domains (e.g., poetry) are described as harder to optimize via RL because “better” is not objective. [Unverified]
- True generalization is described as an open question; it’s unclear whether reasoning-alone yields general generalization. [Unverified]

## Related (In This Repo)

- AI coding notes: `../../../ai-coding/README.md`
- Agent architectures + memory: `../../../projects/agents/README.md`
- EvalOps / verifiable domains framing: `../../../evalops/README.md`

