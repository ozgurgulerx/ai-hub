# Reasoning Models

LLMs that exhibit reasoning behavior: multi-step problem solving, structured deliberation, and tool use.

## What "Reasoning" Means

- Multi-step decomposition into intermediate steps
- Structured representations (scratchpads, programs, proofs)
- Consistency and verification loops (self-checks, voting, tool calls)
- Generalization to novel problems

## Models

| Model | Focus |
|-------|-------|
| **[DeepSeek V3](deepseek-v3/index.md)** | Base for R1, MoE, long context |
| **[GPT-5](gpt-5/index.md)** | Code quality, agentic reliability |
| **[Kimi K2](kimi-k2/index.md)** | Long context, Chinese+English |
| **[MiniMax M2](minimax2/index.md)** | Efficiency, self-hosted |
| **[OLMo](olmo/index.md)** | Transparent training reports, architecture notes |
| **[Sakana CTM](sakana-ctm/index.md)** | Temporal reasoning, backtracking |

## Key Methods

### Pre-Training
- Next-token prediction on web, code, math data
- Synthetic reasoning data generation
- Curriculum learning

### Post-Training
- Instruction tuning (SFT)
- RLHF/RLAIF for helpfulness and correctness
- Outcome-based RL, process-based supervision

### Inference-Time
- Chain-of-thought prompting
- Self-consistency (sample multiple paths, vote)
- Tool augmentation (code execution, retrieval)

## Notes

- [Reasoning Models Comprehensive Guide](notes/reasoning-models-comprehensive-guide.md)
