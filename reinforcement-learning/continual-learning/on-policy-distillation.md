# On-Policy Distillation (Reverse Distillation) for Continual Learning

This note summarizes a proposed continual-learning recipe often described as **on-policy distillation** (sometimes framed as “reverse distillation”):

1) **Train a specialist teacher** with RL (or RL-style search) to become very good at a target capability (e.g., math).
2) **Train the student on-policy** by sampling the student’s own outputs, while using the teacher to provide **dense scoring feedback** (token-level or step-level) so the student improves on that capability **without drifting as hard** from its baseline behaviors.

The key idea is: the student stays “in its own world” (on-policy), but receives rich guidance (dense reward/critique) from a stronger teacher.

## Why This Is Relevant

Continual updates in LLMs commonly fail because:

- RL can rapidly improve a targeted behavior, but often induces **catastrophic forgetting** (instruction-following regressions, safety regressions, generality loss).
- Plain supervised fine-tuning can be data-efficient, but tends to be **mode-seeking** and can overfit or collapse stylistic diversity.

On-policy distillation aims to combine:

- **On-policy learning benefits** (the model improves based on its own distribution)
- **Dense supervision benefits** (fast learning via teacher feedback, instead of sparse end-of-episode rewards)

## The Mechanism (Student-Centered)

Compared to classic “teacher generates demonstrations → student imitates”, on-policy distillation flips the direction:

- **Student proposes** outputs.
- **Teacher evaluates** them (often continuously).
- **Student updates** to increase teacher-scored quality while keeping baseline behavior stable via constraints.

This can be implemented with:

- A reward/score model derived from the RL-trained teacher
- KL constraints or reference-policy regularization to reduce drift
- Replay of “core” behaviors (instruction-following, safety, style)

## Forward vs Reverse KL (Intuition)

Distillation can be thought of as matching distributions:

- **Forward KL** (common in imitation/distillation): student tries to match teacher outputs broadly (“live in the teacher’s world”).
- **Reverse KL** (intuition for “reverse distillation”): student improves its own outputs to score well under the teacher, without collapsing into direct imitation.

The practical takeaway: when you want to add a new skill without overwriting everything else, you often want **student-led sampling + strong evaluation**, rather than pure imitation.

## Practical Enterprise Angle

This pattern is attractive for “enterprise adaptation” because it offers a path to:

- teach task-specific behaviors (ticket resolution, workflow compliance)
- while maintaining general instruction-following and safety expectations

But it still requires:

- strict evaluation gates (to detect regressions)
- governance for training data + reward definitions
- rollback/containment plans (a bad continual update is a production incident)

## What To Track / Add Here

- A minimal algorithm sketch (loss terms, KL constraints, replay mix)
- How to measure forgetting (before/after capability suite; safety regressions)
- When it fails (teacher mismatch, reward hacking, distribution shift)
- References to official technical material (paper/blog) once pinned

## References (TODO)

- Technical report / blog from the proposing lab (Thinking Machines Labs)
- Commentary / explainer articles (summaries only; avoid relying on hype)
