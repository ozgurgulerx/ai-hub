# RLFT / RFT — Long-Form Notes (Concepts, Use Cases, and Resources)

This is a cleaned, repo-friendly version of a long-form RLFT overview. Use it as background reading alongside:

- RLFT summary + checklist: `planning/rlft_concepts.md`
- Azure AI Foundry RLFT lab: `days/Day01/README.md`

<details>
<summary><strong>Quick navigation</strong></summary>

- [What is RLFT?](#what-is-rlft)
- [How RLFT works](#how-rlft-works-in-practice)
- [RLFT vs SFT (and RLHF)](#rlft-vs-sft-and-how-rlhf-fits)
- [Best-fit use cases](#best-fit-use-cases-for-rlft)
- [Practical considerations](#practical-considerations-and-failure-modes)
- [Platforms and resources](#rlft-platforms-and-resources)
</details>

---

## What is RLFT?

Reinforcement Learning Fine-Tuning (RLFT), often shortened to Reinforcement Fine-Tuning (RFT), is a post-training method where a model is optimized using a **reward signal on its outputs** rather than being trained to imitate fixed “correct answers”.

High-level loop:

1. The model generates candidate outputs.
2. A grader scores each output with a numeric reward.
3. Training updates the model so high-reward outputs become more likely (repeat many times).

Primary references:

- OpenAI RLFT guide: https://platform.openai.com/docs/guides/reinforcement-fine-tuning
- Azure AI Foundry RLFT/RFT: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reinforcement-fine-tuning?view=foundry-classic

---

## How RLFT works (in practice)

### 1) Define a grader (reward function)

The grader is an automated judge that maps `(sample, item)` to a scalar score (commonly 0..1).

Common grader types (Azure Foundry / OpenAI-style surfaces):

- deterministic code grader (Python) for verifiable tasks
- exact/string checks for hard constraints
- text similarity metrics for fuzzy matching
- model-as-judge for subjective scoring (style, coherence, rubric adherence)
- multigrader (combine multiple sub-scores into one reward)

The engineering reality: **grader engineering is the moat**. If the grader is wrong or gameable, RLFT will optimize the wrong thing quickly.

### 2) Prepare training data (prompts + grading fields)

Unlike SFT, you don’t need to provide “the answer” as the training target for the model to imitate.

Instead:

- provide prompts/messages
- include any extra fields needed for grading (targets, allowed vocab, policies, rubrics)

In Azure Foundry RLFT, extra fields become `item.*` in templating/grader contexts (see the doc).  
Validator constraints (Foundry) typically include JSONL formatting, message-role requirements, and having both train and validation sets.

### 3) The iterative RLFT loop (sample → grade → update)

RLFT repeatedly:

- samples multiple candidates per prompt
- grades them
- updates the policy to increase probability of higher-reward outputs

This repeats for many iterations (often far more passes over the same examples than SFT).

### 4) Evaluation + checkpoints + deployment

Operational loop:

- monitor training and validation reward curves
- inspect checkpoints (deployable candidates)
- pause/resume jobs as needed
- deploy the checkpoint that hits your target metrics with acceptable drift

Azure Foundry specifics include checkpoints, pause/resume, events, and downloadable artifacts; see:

- Fine-tuning workflow: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning?view=foundry-classic

---

## RLFT vs SFT (and how RLHF fits)

### RLFT vs SFT

SFT teaches by imitation: “match this answer”.

RLFT teaches by optimization: “maximize this score”.

Practical differences:

- Data: RLFT can be effective with fewer examples (dozens/hundreds) because each example is reused many times; SFT often needs larger labeled datasets for coverage.
- Behavior: RLFT can induce goal-seeking strategies (constraint satisfaction, self-checking) rather than only mimicking patterns.
- Cost: RLFT is usually more expensive than SFT due to repeated sampling + grading; budget controls are mandatory.

### RLHF relationship

RLHF is RLFT where the reward comes from human judgments (or a learned reward model trained on preferences). RLFT is the broader idea: the “feedback” can be human, programmatic (verifiable rewards), or AI-as-judge.

---

## Best-fit use cases for RLFT

RLFT works best when tasks are:

- unambiguous (experts agree on what counts as good)
- guess-proof (random guessing can’t reliably score well)
- evaluable by an automated signal (grader)

High-leverage categories:

1) Structured outputs and extraction

- JSON extraction, routing, classification with strict schemas and enumerated outputs.
- Deterministic reward: schema validity + exact label match + rule checks.

2) Code/config generation with tests

- Reward = compilation + unit tests + static constraints.
- RLFT is strongest when “pass/fail” is reliable.

3) Rule-heavy domains (compliance, finance, policy)

- Reward = correct application of rulebook and penalties for violations.
- Example patterns: moderation classification, tax logic, policy adherence.

4) High-accuracy classification/extraction

- Medical coding, fraud tagging, incident triage.
- Reward = match expert labels, plus penalties for incorrect/missing fields.

5) Agentic and tool-using tasks (advanced)

- Multi-step success signals (achieve goal state, solve task, pass integration tests).
- RLFT can outperform SFT in long-horizon settings when success can be computed.

---

## Practical considerations and failure modes

### 1) Task formulation

If you can’t define success clearly, RLFT won’t save you.

Good graders:

- deterministic where possible
- fail-closed on parse/eval errors
- hard to game (anti-cheat checks, strict schemas)
- aligned with your real evaluation metric

### 2) Base model competence

RLFT is a refinement method: the base model needs non-zero ability. If the base model is ~0% success, you often need prompt work or an initial SFT step.

### 3) Ambiguity and inconsistency

If humans disagree on the “right” answer, reward is noisy and RLFT can become unstable or chase spurious signals.

### 4) Cost and operational discipline

RLFT can be expensive: you pay for sampling, grading, and many iterations. Use cost guardrails and understand what’s billed:

- Azure Foundry cost management: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning-cost-management?view=foundry-classic

### 5) Reward hacking / over-optimization

Classic symptoms:

- train reward rises while validation reward stagnates/drops
- reasoning-token usage grows without corresponding correctness gains
- outputs become templated, verbose, or exploit grader loopholes

Fix pattern:

1. tighten schema + fail-closed parsing
2. add anti-cheat checks
3. align validation distribution with training
4. re-run small and verify curves before scaling

---

## RLFT platforms and resources

Primary references (highest-signal):

- Azure AI Foundry RLFT/RFT: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reinforcement-fine-tuning?view=foundry-classic
- Azure fine-tuning workflow: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning?view=foundry-classic
- Azure cost management: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning-cost-management?view=foundry-classic
- OpenAI RLFT guide: https://platform.openai.com/docs/guides/reinforcement-fine-tuning
- OpenAI RLFT use-cases guidance: https://platform.openai.com/docs/guides/rft-use-cases

Broader landscape (useful context):

- AWS Bedrock RLFT (model-as-judge or custom reward functions)
- Open-source RLHF/RLVR tooling (TRL, Open-Instruct-style codebases)
- Emerging multimodal RLFT (vision-language variants)
