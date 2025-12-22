# Reinforcement Distillation (RLAIF-Style “Teacher as Reward Model”)

Reinforcement distillation is a simple but useful pattern:

- A **small student** model produces an action/answer.
- A **strong teacher** (often an LLM) acts as a **reward model**, returning a score (sometimes just `+1/-1`).
- The student is trained with **reinforcement learning** to maximize that reward.

This is a minimal, practical form of **RLAIF (Reinforcement Learning from AI Feedback)** and can be seen as “distillation without labeled datasets”: you’re distilling the teacher’s *judgments* rather than its logits.

## How It Differs From Classic Distillation

- **Classic distillation**: student learns to match teacher outputs/distribution (KL / cross-entropy on logits).
- **Reinforcement distillation**: student learns to maximize a **teacher-scored reward**; the teacher need not provide the “right answer”, only an evaluation.

## Minimal Recipe (Distilled)

1) **Constrain the action space** (especially for toy demos): pick from a fixed set of answers/actions (lower variance, more stable RL).
2) **Sample from the student policy** `π(a|x)` for input `x`.
3) **Query teacher-as-judge** to score `(x, a)` vs a target spec (or ground truth), returning reward `r` (e.g., `+1/-1`).
4) **Update student with policy gradients** (REINFORCE):
   - `L_rl = - log π(a|x) * r`
5) Optionally add a **stabilizer** when `r > 0`:
   - a supervised “lock-in” term that increases the probability of the rewarded action.

## Why It’s Impactful

- **No labeled dataset required** (in the simplest setup): the teacher provides the supervision signal.
- **Local / on-prem friendly**: the teacher can be a local model (e.g., via Ollama) to keep data inside your environment.
- **Bridges to real systems**: same shape as production RLAIF/RLHF pipelines—just stripped down.

## Integrity Notes / Common Pitfalls

- **Reward hacking**: the student can learn to exploit judge weaknesses; you must validate with held-out evals.
- **High-variance learning**: binary rewards (`+1/-1`) are noisy; use baselines, larger batches, or richer scoring where possible.
- **Judge alignment**: if the teacher’s evaluation rubric is inconsistent, the student learns inconsistently.
- **Spec vs. imitation**: you’re distilling a preference/criterion. If the rubric is wrong, the student becomes confidently wrong.
- **Action-space mismatch**: fixed answer sets make demos work; open-ended generation needs more careful credit assignment and evaluation.

## Where This Fits In This Repo

- Continual updates without forgetting: `reinforcement-learning/continual-learning/`
- Teacher-guided continual learning variant: `on-policy-distillation.md`

## References (TODO)

- Add primary sources / technical notes for “reinforcement distillation / reward distillation / RLAIF” once pinned.
