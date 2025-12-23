# Training & Scaling

Notes on the **training stack** behind frontier models: pre-training, post-training, scaling laws, compute economics, and the engineering realities of training at large scale.

## Training Evolution Timeline

| Year | Paradigm | Description |
|------|----------|-------------|
| **202x** | Pre-training (foundation) | Large-scale unsupervised learning on web text |
| **2022** | RLHF + PPO | Reinforcement Learning from Human Feedback with Proximal Policy Optimization |
| **2023** | LoRA SFT | Low-Rank Adaptation for efficient Supervised Fine-Tuning |
| **2024** | Mid-Training | Continued pre-training on domain-specific data |
| **2025** | RLVR + GRPO | RL with Verifiable Rewards + Group Relative Policy Optimization |

## Key Shifts

- **Pre-training → Post-training:** Focus moved from scale to alignment
- **PPO → DPO/GRPO:** Simpler, more stable preference optimization
- **Full fine-tuning → LoRA:** Parameter-efficient adaptation
- **Human feedback → Verifiable rewards:** Automated verification where possible

## Notes

- Anthropic pre-training: scaling laws, distributed training, data quality (Noiz summary, to verify): `notes/anthropic-head-of-pretraining-scaling-laws-compute-economics-noiz-summary.md`

## MoE

- MoE overview: `moe/README.md`
- Why training MoEs is hard (practitioner write-up): `moe/why-training-moes-is-so-hard.md`
