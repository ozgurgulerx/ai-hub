# RLFT / RFT — Concepts, Capabilities, and Applications

Reinforcement Learning Fine-Tuning (RLFT), often shortened to Reinforcement Fine-Tuning (RFT), adapts a pre-trained model using a **reward-driven loop** (sample → grade → update) instead of supervised imitation from fixed “right answers”.

This note supports `days/Day01/README.md` (Azure AI Foundry RLFT lab) with the broader mental model, use cases, and practical constraints.

Long-form companion: `planning/rlft_longform_notes.md`.

<details>
<summary><strong>Quick navigation</strong></summary>

- [RLFT in one sentence](#1-rlft-in-one-sentence)
- [How RLFT works](#2-how-rlft-works-end-to-end)
- [RLFT vs SFT vs RLHF](#3-rlft-vs-supervised-fine-tuning-sft-vs-rlhf-relationship)
- [Best-fit use cases](#4-best-fit-use-cases-where-rlft-is-highest-leverage)
- [Practical considerations](#5-practical-considerations-what-breaks-rlft-in-the-real-world)
- [Platform landscape](#6-platform-landscape-where-rlft-shows-up)
- [Getting started checklist](#7-getting-started-checklist-operator-version)
- [How this repo uses it](#8-how-this-repo-uses-this-note)
- [References](#references)
</details>

---

## 1) RLFT in one sentence

The model generates candidate outputs, a grader assigns a numeric reward, and training updates the model so **high-reward outputs become more likely** while low-reward outputs fade (repeat many times).  
Primary reference: OpenAI RLFT guide ([OpenAI docs][OAI-RLFT]); Azure specifics: Foundry RLFT how-to ([Microsoft Learn][MS-RLFT]).

---

## 2) How RLFT works (end-to-end)

```mermaid
flowchart LR
  D[Prompts + item fields] --> S[Sample outputs]
  S --> G[Grader(s) -> reward]
  G --> U[Policy update]
  U --> E[Auto-evals + validation]
  E -->|iterate| S
```

Core components:

- **Training items**: prompts plus any extra `item.*` fields needed for grading (targets, allowed vocab, rubrics). ([Microsoft Learn][MS-RLFT])
- **Graders (reward functions)**: deterministic code checks, string/similarity checks, model-as-judge, or combinations. ([Microsoft Learn][MS-RLFT])
- **Optimization**: policy-gradient-style updates under platform guardrails (metrics, constraints, checkpoints). ([OpenAI docs][OAI-RLFT])
- **Validation/evaluation**: run regularly during training (Foundry can auto-run evals at intervals). ([Microsoft Learn][MS-RLFT])

Minimal “mental model” loop (Python-ish pseudocode):

```python
for item in dataset:
    samples = [policy.generate(item.prompt) for _ in range(K)]
    rewards = [grader(sample, item) for sample in samples]
    policy = policy.update(samples, rewards)  # increase p(high-reward)
```

Why this can teach “how to think” (not just mimic):

- RLFT optimizes for an outcome metric, so the model can discover internal strategies that generalize within the domain (constraint satisfaction, self-checking, tool discipline).
- You aren’t forcing one reference answer; you’re shaping the space of acceptable behavior via reward.

---

## 3) RLFT vs supervised fine-tuning (SFT) vs RLHF (relationship)

### RLFT vs SFT

SFT trains the model to imitate reference answers; RLFT trains the model to **optimize a goal** defined by reward.

Practical differences:

- **Data efficiency**: RLFT can work with dozens/hundreds of examples because each example is reused many times with sampling; SFT typically needs larger labeled sets for coverage.
- **Behavior shape**: RLFT can induce “strategy” (constraint satisfaction, search, self-checking) because the model is optimizing reward rather than matching one output.
- **Engineering effort**: RLFT shifts work from labeling to **grader engineering** (design, anti-cheat, stability).
- **Cost**: RLFT is often far more compute-intensive than SFT because of repeated sampling + grading; budget guardrails matter. (See cost discussion in Azure docs: [Microsoft Learn][MS-COST])

Quick comparison table:

| Dimension | SFT | RLFT |
| --- | --- | --- |
| Signal | “match this output” | “maximize this score” |
| Data | larger labeled corpora | smaller prompt sets reused many times |
| Best for | formatting, style, basic competence | verifiable correctness, hard constraints, expert-level reliability |
| Failure mode | memorization, brittle generalization | reward hacking, over-optimization, cost blowups |

### RLHF as a special case

RLHF is RLFT where the reward is derived from human judgments (directly or via a learned reward model). RLFT generalizes the feedback source: verifiable programmatic checks (RLVR) and AI-as-judge feedback (RLAIF) also fit under the umbrella.

---

## 4) Best-fit use cases (where RLFT is highest leverage)

RLFT works best when:

- the task is **unambiguous** (experts agree on what “good” is),
- and the reward is **guess-proof** (random guessing can’t score well). ([OpenAI docs][OAI-USECASES])

High-signal categories:

1) **Structured outputs with strict constraints**

- JSON extraction, routing, compliance forms, tool-call JSON validity.
- Use strict `response_format` schemas and deterministic graders. ([Microsoft Learn][MS-RLFT])

2) **Code / config generation with tests**

- grade by compilation, unit tests, schema validation, or static checks.
- RLFT is strong when you can run a reliable checker.

3) **Information extraction / classification with high accuracy needs**

- medical coding, incident triage, fraud tagging, policy classification.
- deterministic graders can compare labels (exact-match, F1-like surrogates).

4) **Rule-heavy domains**

- compliance, tax logic, safety policy application.
- reward = “follow the rulebook exactly”, with explicit penalties for violations.

5) **Agentic/tool-using tasks (hard mode)**

- multi-step tool use where SFT often underperforms because success is long-horizon and sparse.
- RLFT can help when you can compute a reliable terminal success signal (but cost rises).

Common thread: if you can write a reliable checker, RLFT can push “pretty good” to “consistently right”.

---

## 5) Practical considerations (what breaks RLFT in the real world)

### Grader design is the moat

If the grader is wrong, the model learns the wrong thing faster than you can notice.

Rules of thumb:

- Start with a **deterministic** grader (Python / rule checks) for correctness.
- Fail closed on parse/eval errors.
- Reduce hack surface: strict schemas (`additionalProperties: false`), tight enums, length constraints.
- If you add “soft” graders (style), **gate them behind correctness** (don’t pay for pretty wrong answers). ([Microsoft Learn][MS-RLFT])

Common grader failure modes (and how they show up):

- **Schema drift**: invalid JSON spikes → enforce strict `response_format` and fail-closed parsing.
- **Verbosity/length hacks**: reasoning tokens ↑, reward ↑, real quality flat → add constraints + gate rewards.
- **Keyword stuffing**: model learns to include magic strings → replace substring checks with structured checks.
- **Train/valid divergence**: train reward ↑, valid reward ↓/flat → reward hacking or valid distribution mismatch.

### Base model must have non-zero skill

If the base model’s success rate is effectively 0%, RLFT usually can’t bootstrap; you may need prompt work or an initial SFT pass to establish a foothold. ([OpenAI docs][OAI-RLFT])

### Ambiguity kills reward signal

If humans don’t agree on the right answer, the reward becomes noisy and unstable; RLFT will chase inconsistent signals.

### Cost and monitoring are not optional

RLFT is expensive because you pay for sampling + grading + repeated iterations. On Azure Foundry, understand billed vs non-billed steps and the $5k auto-pause behavior. ([Microsoft Learn][MS-COST])

### Stability, drift, and safety

Always monitor training/validation curves and run targeted evals for regressions; reward hacking and distribution shift look like train↑/valid↓. ([Microsoft Learn][MS-RLFT])

---

## 6) Platform landscape (where RLFT shows up)

Primary (official) surfaces:

- **Azure AI Foundry (Azure OpenAI)** RLFT/RFT: models, data contract, grader types, response_format, metrics, job lifecycle, cost controls. ([Microsoft Learn][MS-RLFT])
- **OpenAI RFT/RLFT**: general RLFT mental model + use-case guidance + grader patterns. ([OpenAI docs][OAI-RLFT], [OpenAI docs][OAI-USECASES])

Also relevant:

- **AWS Bedrock RLFT** (model-as-judge or custom code reward).
- **Open-source**: TRL (RLHF-style), Open-Instruct / RLVR-style codebases, and emerging multimodal RLFT variants.

---

## 7) Getting started checklist (operator version)

Use this before you burn money:

1. Define success as a computable score (pass-rate, constraint satisfaction).
2. Build a tiny eval set first (10–50 cases); confirm the base model is non-zero.
3. Enforce strict structured output (`response_format`) wherever possible.
4. Write a deterministic Python grader; add anti-cheat checks; fail closed.
5. Run a small RLFT job; watch train vs valid reward and reasoning-token curves.
6. If train↑ and valid↓, assume reward hacking or valid OOD; fix reward/data before scaling.
7. Add cost guardrails (budgets/alerts) and practice pause/resume + checkpoint selection.

---

## 8) How this repo uses this note

- Day 01 RLFT lab (Azure-first): `days/Day01/README.md`
- Day 01 “dashboard literacy”: `days/Day01/THEORY.md`

---

## References

- [MS-RLFT] https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reinforcement-fine-tuning?view=foundry-classic
- [MS-COST] https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning-cost-management?view=foundry-classic
- [MS-FT] https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning?view=foundry-classic
- [OAI-RLFT] https://platform.openai.com/docs/guides/reinforcement-fine-tuning
- [OAI-USECASES] https://platform.openai.com/docs/guides/rft-use-cases
