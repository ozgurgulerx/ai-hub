# Reasoning Models: A Comprehensive Guide

Reasoning models represent a fundamental shift in how AI systems approach complex problems—from pattern matching to deliberate, step-by-step thinking. This guide distills insights from researchers at OpenAI, Google DeepMind, and Stanford on how reasoning works and where it's headed.

---

## The Core Insight

**Reasoning is revealed, not added.** Techniques like chain-of-thought prompting don't inject new capabilities—they reshape output probabilities to surface step-by-step paths that already exist in the model's learned patterns.

---

## How Reasoning Models Work

### Chain-of-Thought Generation

Modern reasoning models (like o1/GPT-5.1) generate chain-of-thought tokens primarily for their own reasoning, not for users. During internal thinking, they:
- Use tools (browsing, code execution) to verify facts
- Extract information to inform next steps
- Build up to conclusions through explicit intermediate steps

### Reinforcement Learning for Reasoning

RL "differentiates through the reasoning part"—pushing the model toward actions that lead to better answers in verifiable domains:
- Math
- Coding
- Science

This increases capability faster than pre-training alone by using more tokens to think.

### Self-Consistency

Sample multiple reasoning paths and majority vote:
- Dramatically improves accuracy
- Provides confidence signal
- **Key finding:** >80% agreement across samples correlates with near-100% final-answer accuracy

---

## Verifier's Law

### The Core Principle

**AI capability on a task is proportional to how easily the task can be verified.**

Easily verifiable tasks (Sudoku, code with tests, math with proofs) are automated sooner.

### Verification Asymmetry

Different domains have different verification difficulty:

| Domain | Verification Difficulty |
|--------|------------------------|
| Code with tests | Low (automated) |
| Competition math | Low (answer key) |
| Factual essays | Medium (fact-checking) |
| Creative writing | High (subjective) |
| Novel research | Very high (no ground truth) |

### Reducing Verification Asymmetry

**Lever:** Privileged information (answer keys, test cases) reduces verification difficulty.

**Example:** Alpha Evolve leverages verification asymmetry with sampling + algorithms for hard-but-verifiable tasks.

---

## The Jagged Edge of Intelligence

### Uneven Progress

The "jagged edge" concept explains why AI progress is uneven across tasks:
- Improvement rates vary by task properties
- Ease of verification determines progress speed
- Digital tasks progress faster (faster iteration, abundant data)

### Current Limitations

Reasoning models remain jagged—strong in some areas, weak in others:
- GPT-5.1 still struggles with some simple logic puzzles
- Five-year-old math book examples can trip up frontier models
- Motivates continued human oversight in high-stakes settings

---

## Self-Teaching and IO Fine-Tuning

### Why Self-Teaching Works

IO fine-tuning (training on the model's own correct answers) outperforms supervised fine-tuning because:
- Trains on examples in the model's "native" expression patterns
- More effective than human-written explanations
- Model learns from its own successful approaches

### The Verification Dependency

**Critical limitation:** Creative tasks without clear right answers limit self-improvement loops.

Robust verification is the crucial ingredient for effective reasoning during both training and inference.

---

## Scaling and Emergence

### Reliable Scaling

LLMs show reliable improvements with scaling:
- Loss decreases predictably across seven orders of magnitude of compute
- Next-word prediction learns millions of tasks simultaneously (grammar, world knowledge, translation, spatial reasoning)

### Emergent Abilities

- Make model comparison harder
- Motivate new benchmarks for expanding capabilities
- Downstream tasks improve at different rates:
  - Some (math) improve sharply after thresholds
  - Others may plateau

### The Paradigm Shift

Progress is driven largely by:
- Investment
- Time
- Researcher count

Large-scale collaboration and engineering-heavy approaches dominate.

---

## Long-Running Agents

### Compaction for Extended Workflows

"GPT-5.1 Codex Max" is designed for long-running workflows (days/weeks):
- Uses compaction to operate across multiple context windows
- Totaling millions of tokens
- Summarizes most important information
- Forgets less relevant parts

### Managing Attention/Memory Limits

Compaction enables longer runs by:
- Preserving critical context
- Discarding noise
- Maintaining coherent reasoning across sessions

---

## Automating Discovery

### Current Limitations

**AtCoder example:** OpenAI model achieved second place by optimizing code effectively, but lost to a winner who found a novel approach outside the model's search space.

**Math Olympiad example:** Model achieved gold medal performance (5/6 problems) but failed on a hard combinatorics problem requiring a novel insight.

**The gap:** Optimizing within known solution spaces vs discovering fundamentally new approaches.

### Future Direction

"Automating research and discovery" shifts emphasis from task completion to knowledge generation:
- AI systems discovering novel insights with little effort
- "New science falls out of GPUs"

### Measurement Evolution

Measuring progress requires systems that:
- Interact with the world
- Tackle longer-horizon, fuzzier tasks
- Go beyond narrow benchmarks
- Still reflect raw intellectual capability

---

## Production Economics

### Distillation Is Necessary

Running largest models for everyday chat is unsustainably expensive. Distillation enables:
- Serving very large user bases
- Economically viable deployment
- Acceptable quality at lower cost

### Scaling Laws Shape Decisions

GPU economics and scaling laws shape:
- Research priorities
- Production model size decisions
- What gets deployed vs what stays in the lab

---

## Multimodal and Generalization

### Multimodal Lags Behind

Multimodal reasoning (text+vision+audio) lags text-only due to:
- Synthetic data generation challenges
- Base-model retraining costs
- Verification difficulty across modalities

### The Generalization Question

**Open question:** Does reasoning alone yield general generalization?

Reasoning models work best in verifiable domains. Subjective domains (poetry, creative writing) are harder to optimize via RL because "better" is not objective.

---

## Intelligence as Commodity

### The Thesis

Intelligence is commoditizing:
- Near-zero-cost, instant access to public information
- Coding, personal health, general knowledge
- Increasing relative value of private/insider knowledge

### The Agents Era

Frictionless, personalized access to knowledge across domains, enabled by:
- Decreasing intelligence costs
- Adaptive compute (resources allocated per task)
- Tool use and environmental interaction

---

## Quick Reference

### When Reasoning Models Excel

- Verifiable domains (math, code, science)
- Multi-step problems with clear success criteria
- Tasks where more thinking time helps
- Domains with abundant training signal

### When Reasoning Models Struggle

- Novel insight generation (outside training distribution)
- Subjective/creative tasks
- Simple logic puzzles (surprisingly)
- Tasks requiring world interaction beyond tools

### Implications for Builders

1. **Leverage verification** — Design tasks with clear success criteria
2. **Use self-consistency** — Sample multiple paths for confidence
3. **Expect jaggedness** — Test edge cases, don't assume uniform capability
4. **Plan for distillation** — Production models will be smaller than lab models
5. **Maintain human oversight** — Especially in high-stakes settings

---

## Summary

Reasoning models advance AI by:

1. **Revealing latent capability** — Chain-of-thought surfaces existing knowledge
2. **Scaling with compute** — More thinking time improves results
3. **Leveraging verification** — Progress is fastest where answers can be checked
4. **Self-teaching** — Models learn from their own successful reasoning
5. **Compaction for scale** — Summarization enables long-running workflows

The fundamental limitation remains **verification**—tasks without clear right answers resist the self-improvement loops that drive reasoning model progress.
