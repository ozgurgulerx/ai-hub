# Day 03 — GRPO Capstone Template (RLVR)

Fill this to define a verifiable GRPO project that can be reproduced and debugged from metrics.

---

## 1) Task (verifiable, unambiguous)

- Task name:
- Domain:
- Why GRPO (not DPO / SFT):
- What “success” means (one sentence):
- What makes it guess-proof:

## 2) Data

- Prompt source:
- Train size / Valid size / Eval size:
- Train/valid/eval split rule:
- Leakage checks:

## 3) Reward / Grader (deterministic)

- Reward range (e.g., 0..1):
- Primary reward (verifiable):
- Shaping (if sparse):
- Anti-cheat constraints (>= 3):
  1.
  2.
  3.
- Fail-closed behaviors (what yields 0 immediately):

## 4) Metrics + logging (what you will plot)

- reward_mean (train/valid):
- success_rate (eval):
- KL to reference:
- entropy / diversity:
- clipfrac:
- length / reasoning tokens (if relevant):

## 5) Training plan (GRPO knobs)

- Base model:
- Reference model:
- Group size K:
- PPO clip ε:
- KL β (or target KL):
- Sampling temperature:
- LR / optimizer:
- Total steps:

## 6) Evaluation plan (must catch hacks)

- Primary eval metric:
- Secondary metrics:
- OOD / adversarial evals:
- Failure-mode table to include:
  - reward hacking
  - KL blow-up / mode collapse
  - thinking tax
  - train/valid divergence (OOD)
  - grader inconsistency

## 7) Ablations (minimum 3)

1.
2.
3.

## 8) Exit criteria (pass/fail)

- Baseline success:
- Target success after GRPO:
- Max acceptable KL:
- “No regression” constraints:

## 9) Artifact checklist (paths to commit)

- Dataset generator:
- Grader implementation:
- Training script/config:
- Eval harness:
- Results report (with plots):
