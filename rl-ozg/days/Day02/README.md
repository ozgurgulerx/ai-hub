# Day 02 — DPO + PPO (Azure DPO, PPO as RLHF baseline)

Azure AI Foundry exposes **DPO** as a first-class customization method.

Azure AI Foundry does **not** expose “PPO” as a first-class fine-tuning method in the same “choose method” UI (you get SFT / DPO / RFT). So Day02 covers PPO as the RLHF algorithm you’d run yourself (e.g., TRL), and shows how to map that mental model to Foundry’s RFT/GRPO.

**What you will be able to do after Day02**

1) Build a *high-signal* preference dataset for DPO (what-to-keep vs what-to-avoid).
2) Run **DPO fine-tuning in Azure AI Foundry / Azure OpenAI** (portal or REST).
3) Evaluate and debug preference alignment (offline + online).
4) Understand PPO deeply enough to implement/run it via TRL, and know when PPO beats DPO (and vice versa).
5) Build a “decision table” for SFT vs DPO vs PPO vs RFT (GRPO).

Files:

- `THEORY.md`  — dense theory + operational rules.
- `LAB.md`     — practical drills, scripts, and failure-mode ablations.
- `data/`      — preference JSONL examples and generation notes.
- `eval/`      — eval harness templates (pairwise win rate + regression tests).
- `scripts/`   — dataset generators and validators.
