# Continual Learning (LLMs & Agents)

Continual learning is about **updating a model over time** (new tasks, new domains, new preferences) without losing previously learned capabilities (**catastrophic forgetting**). In production, this shows up as “we improved X, but broke Y”.

This folder is a home for methods, mental models, and evaluation patterns for continual learning in LLMs and agentic systems.

## Where This Fits In AI Hub

- **This folder (weight updates):** continual fine-tuning, RL/RLHF-style updates, distillation, replay, and regression control.
- **Not weight updates (often better):** retrieval + memory + tooling to incorporate new knowledge without changing weights:
  - RAG: `retrieval-augmented-systems/`
  - Agent memory patterns: `projects/agents/` and `workshops/03-agents-on-azure-ai-foundry-tools-memory-orchestration/`

## Key Problems

- **Catastrophic forgetting:** improving a behavior shifts the policy/model and erodes general instruction following, safety, or other skills.
- **Distribution shift:** new data/tasks differ from the original training distribution; naive fine-tuning overfits.
- **Reward hacking / over-optimization:** RL-style updates can produce brittle policies that regress elsewhere.
- **Evaluation debt:** without regression suites, you don’t notice what you broke until users do.

## Approaches (Scaffold)

- **Rehearsal / replay**: mix in prior data (or synthetic replay) while learning new tasks.
- **Regularization**: constrain updates to preserve important parameters/behaviors (e.g., EWC/LwF-style ideas).
- **Parameter isolation**: adapters/LoRA modules per domain, routing, or sparse MoE-style specialization.
- **Distillation**: preserve behaviors by matching a reference model (teacher) while learning new skills.
- **RL + distillation hybrids**: teach a new skill via RL in a specialist teacher, then transfer it into a generalist student while limiting forgetting.

## Notes

- On-policy distillation for continual learning: `on-policy-distillation.md`
- Reinforcement distillation (RLAIF-style): `reinforcement-distillation.md`

## What To Add Next

- A minimal regression harness (capability suite + “do not regress” gates)
- A checklist for “continual learning in enterprise” (data governance, approvals, rollback)
- Examples of adapter-based continual updates vs. full fine-tunes
