# Reasoning LLMs

This repository focuses on large language models (LLMs) that exhibit reasoning behavior: multi-step problem solving, structured deliberation, and the ability to use tools or intermediate representations to reach an answer.

## What "Reasoning" Means in LLMs

Reasoning in LLMs is typically operationalized as:
- Multi-step decomposition of tasks into intermediate steps.
- Structured representations (e.g., scratchpads, programs, proofs, tables).
- Consistency and verification loops (self-checks, multi-sample voting, tool calls).
- Generalization to novel problems beyond memorized patterns.

## How Reasoning Emerges

Key mechanisms that promote reasoning capability:
- Scale: larger models show stronger emergent reasoning signals.
- Data: curated reasoning corpora, code, math, and multi-step explanations.
- Objectives: training targets that reward intermediate structure, not just final answers.
- Inference: decoding strategies like chain-of-thought prompting, self-consistency, and tool-augmented workflows.

## Pre-Training Methods

Pre-training builds the core world knowledge and language modeling ability.

- Next-token prediction on diverse web, code, math, and scientific data.
- Synthetic reasoning data generation to emphasize stepwise logic.
- Curriculum learning, from short examples to complex multi-hop tasks.
- Filtering and mixture rebalancing to avoid overfitting to shallow patterns.

## Post-Training Methods

Post-training aligns and specializes reasoning behaviors.

- Instruction tuning: supervised fine-tuning on instruction-following and reasoning tasks.
- RLHF/RLAIF: reinforcement learning from human or AI feedback to improve helpfulness and correctness.
- Outcome-based RL: optimizing for final correctness on reasoning benchmarks.
- Process-based supervision: feedback on intermediate steps, not just outcomes.

## Fine-Tuning Methods

Common fine-tuning strategies for reasoning-focused models:
- Supervised fine-tuning (SFT) on reasoning datasets (math, logic, code).
- Multi-task fine-tuning across reasoning, QA, and tool-use data.
- Parameter-efficient tuning (LoRA, adapters, prefix/prompt tuning).
- Distillation: student models learn from larger teacher reasoning traces.

## Inference-Time Techniques

Reasoning improvements that happen at inference time:
- Chain-of-thought prompting and few-shot exemplars.
- Self-consistency: sample multiple reasoning paths, vote on the answer.
- Tool augmentation: calculators, code execution, retrieval, and external APIs.
- Verification loops: critique, refine, or unit-test the reasoning.

## Evaluation

Typical benchmarks and metrics:
- Math and logic: GSM8K, MATH, ARC, AQuA.
- Multi-hop QA: HotpotQA, StrategyQA.
- Coding: HumanEval, MBPP.
- Process evaluation: step-level accuracy and faithfulness.

## Repository Goals

- Curate references, notes, and experiments on reasoning LLMs.
- Track training recipes and fine-tuning strategies.
- Compare inference-time reasoning techniques and evaluation results.

## Suggested Structure (Planned)

- `notes/`: summaries of key papers and methods.
- `experiments/`: small-scale training or inference experiments.
- `datasets/`: links to datasets and benchmarks.
- `prompts/`: prompt patterns and evaluation prompts.

## References (Starter List)

- "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
- "Process Supervision vs. Outcome Supervision for LLMs"
- "Toolformer: Language Models Can Teach Themselves to Use Tools"
- "Training Verifiers for Scalable Supervision"
