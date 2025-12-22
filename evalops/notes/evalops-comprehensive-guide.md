# EvalOps: A Comprehensive Guide

Evaluation is the foundation of reliable AI systems. Without rigorous evals, you're flying blind—shipping based on vibes rather than evidence. This guide distills lessons from practitioners who've built evaluation systems at scale.

---

## The Core Insight

**Evals are not a phase—they're continuous operations.** Great evals require engineering that reconciles datasets with real user experience, not one-time benchmark runs.

---

## Evaluation Design Philosophy

### Outcome-First Design

Reverse engineer evaluations from product experience and business outcomes, not abstract metrics.

**Example:** For customer support bots, track escalation rates rather than only "factuality"—a grounded-but-wrong answer still fails users.

### Build Early, Iterate Continuously

- Define evaluations early and refine through failure analysis
- Use failure analysis to distinguish "bad tests" from "bad solutions"
- Turn POCs into production systems by iteratively adding tests

### Reliability Through Coverage

Evals are the reliability foundation. Each test you add increases confidence in production behavior.

---

## The Data Quality Crisis

### Synthetic Data Alone Is Insufficient

**Claim from practitioners:** 99% of 10–20M pieces of synthetic data gathered by customers were not useful.

Human feedback remains crucial as an external signal to align models to real objectives. Models "think differently" and need validators.

### Quality Over Quantity

- Quality is domain-specific and subjective
- Requires technology to separate great from terrible outputs
- 5-second evals train "clickbait"—careful assessment is essential
- Scaling "mediocrity" happens when throwing humans at tasks without first-principles quality measurement

### Future Training Mix

Effective training combines:
- RL environments
- Expert reasoning traces
- High-quality human data

Relying on one alone is insufficient.

---

## LLM-Assisted Evaluation

### Generating Test Cases

Use LLMs to:
- Generate diverse question variations with persona context
- Keep expected answers consistent across variations
- Create detailed correctness criteria that can be evaluated by LLMs

### Custom Scoring Functions

**Critical:** Scoring should be tailored to your application, not generic off-the-shelf scores.

### Validation Loop

LLM-generated evals must be validated against human judgment to ensure alignment.

---

## Solution-Specific Testing

| System Type | Testing Strategy |
|-------------|-----------------|
| Text-to-SQL / Graph queries | Mock databases |
| Classifiers | Simple match tests |
| Guardrails | Questions that should not be answered, need different handling, or have no answer |
| Agents | Tool interaction traces, multi-step correctness |

---

## DSPy and Compound AI Systems

### AI Engineering as a Field

AI engineering is distinct from ML research—focused on building **compound AI systems** (many components) rather than single models.

### Decoupling Architecture from Models

**DSPy philosophy:** Decouple information flow/architecture from underlying ML paradigm so architectures remain modular while aligning to whichever model is used.

Separates:
- **Task definition** via signatures
- **I/O structure control** via adaptives

Enables transformations like chain-of-thought and tool usage without coupling low-level concerns.

### Optimization Approaches

DSPy optimizers (few-shot, RL with PPO, behavior cloning) can run overnight to improve last-mile performance:
- GRPO and instruction rewriting operate in prompt space
- Analogous to RL on high-variance examples

### Development Workflow

1. **Start with error analysis** — Understand limitations before adding complexity
2. **Treat components as sketches** — Let framework fill details
3. **Iterate fast** — Simplest working solution first
4. **Intervene on right failure modes** — Use high-level tools and combinations
5. **Expand signatures over time** — Add structure, field descriptions, richer types as needed

### Practical Tips

- Use agents/ReAct for future-proofing, but replace with manual decomposition when tool order is known
- Avoid copying overly complex "optimized prompts"—reduces portability across models
- Build evaluation sets through error analysis and model output comparison

---

## Context Optimization

### Tools Dominate Token Budgets

In modern agentic systems, tools dominate the LLM token budget. Performance depends on:
- Precise tool interface definitions
- Precise output definitions
- Not mirroring existing API structures

### Model Swaps Change Feasibility

New model releases can change feasibility overnight—a model swap can make previously unviable features viable.

---

## System-Wide Optimization

Optimizing eval performance is **holistic optimization**:
- Data
- Tasks
- Scoring functions

Not just prompt tweaks.

### Automated Eval Optimization

Tools like Braintrust's "Loop" auto-optimize by:
- Generating prompts
- Generating datasets
- Adjusting scores

Enable targeted questions:
- How to improve prompts?
- What dataset elements are missing?
- How to adjust scoring criteria?

---

## Benchmark Stack (2025)

### Classic Benchmarks (Sanity Checks)

| Benchmark | Capability | Status |
|-----------|------------|--------|
| **MMLU** | 57-subject multi-choice exam | Near-saturated |
| **GSM8K** | Grade-school math word problems | Near-saturated |
| **BIG-Bench Hard** | Diverse quirky reasoning tasks | Still useful |
| **HumanEval / MBPP** | Toy code synthesis | Near-saturated |

### Frontier Reasoning Benchmarks

| Benchmark | What It Tests | Why It Matters |
|-----------|---------------|----------------|
| **HLE (Humanity's Last Exam)** | 2.5K+ expert-level, multi-domain questions | Broad expert reasoning under exam pressure |
| **GPQA Diamond** | 198 PhD-level science MCQs (bio/chem/physics) | Deep graduate-level scientific reasoning |
| **ARC-AGI-2** | Grid-based pattern puzzles | Abstract pattern formation—"fluid intelligence" proxy |
| **FrontierMath** | Competition-style hard math | Long, brittle chains of symbolic reasoning |

**For slides/model cards:** HLE, GPQA-Diamond, ARC-AGI-2 (still report MMLU, GSM8K for continuity)

### Framing for Communication

- **"Old layer"** — MMLU, GSM8K, HumanEval → "Can it pass standard exams and write toy code?"
- **"New layer"** — HLE, GPQA-Diamond, ARC-AGI-2, FrontierMath → "Can it handle grad-level science and human-style pattern abstraction without overfitting to old benchmarks?"

---

## RAG Evaluation

### Key Metrics

- **Contextual recall** — Does the answer include important facts from retrieval?
- **Contextual precision** — Does it avoid introducing unsupported details?
- **Faithfulness** — How well does the model stick to retrieved facts?

### Hallucination Detection Tools

| Tool | Description |
|------|-------------|
| **HHEM (Vectara)** | Open-source classifier for factual inconsistency detection |
| **LettuceDetect** | Token-level hallucination detector for RAG |
| **SelfCheckGPT** | Self-consistency method (query multiple times, flag variance) |

### LLM-as-Judge

Use strong models (GPT-4) to critique outputs against known facts/references. Research shows LLMs approximate human judgment well for factual accuracy.

---

## Robustness and Adversarial Testing

### Adversarial Prompt Testing

Include in eval suite:
- Prompt injection attacks
- Jailbreak prompts
- Input perturbations (typos, slang, out-of-distribution)
- Multi-turn consistency checks

### Red-Teaming Platforms

Frameworks like DeepTeam provide:
- Libraries of known exploits
- Plug-and-play adversarial test cases
- OWASP Top 10–style vulnerability coverage

### Agent Evaluation

For tool-using agents:
- Task completion rate
- Tool selection correctness
- Efficient sequence of steps
- Recovery from failures

---

## Trust and Safety Metrics

### Responsible AI Checks

| Metric | Implementation |
|--------|----------------|
| **Toxicity** | Detoxify (BERT-based), OpenAI content filter |
| **Bias** | Scan for racial, gender, political bias |
| **Policy compliance** | Refusal rate when appropriate |

### Trust & Safety Test Sets

Maintain collections of prompts for:
- Self-harm
- Medical/legal advice
- Personal data
- Policy edge cases

Verify model outputs comply with guidelines for each case.

---

## Integration into Development Lifecycle

### Continuous Evaluation Pipelines

Run evaluations on each model build or prompt change:
```bash
deepeval test run llm_tests/
```

If any eval test fails (e.g., hallucination rate increased), block the update.

### Regression and A/B Testing

Side-by-side comparisons via evaluation suites:
- Incumbent vs candidate model
- Large eval set covering various dimensions
- Detailed reports showing where one model is better/worse

### LLM Observability

Production monitoring:
- Log inputs/outputs
- Compute metrics in real time
- Dashboard drift and anomalies
- Feed problematic cases back into training

### Human-in-the-Loop Refinement

- User ratings (thumbs up/down)
- Domain expert review for borderline cases
- RLHF as evaluation-driven training

---

## Tools and Platforms

| Tool | Focus |
|------|-------|
| **OpenAI Evals** | Open-source eval framework with community tasks |
| **EleutherAI LM Eval Harness** | Zero/few-shot evaluation on academic benchmarks |
| **DeepEval** | LLM "unit tests" with CI integration |
| **LangSmith** | Trace LLM calls and measure performance |
| **Arize Phoenix** | Open-source observability for LLM decisions |
| **Guardrails AI** | Output validation and policy enforcement |

---

## Safety Benchmarking

### Infrastructure Requirements

| Component | Purpose |
|-----------|---------|
| High-quality diverse datasets | Coverage |
| Metrics and criteria | Definitions |
| Enhancement solutions | Mitigations |
| Automated pipeline | Connection |

### Human-in-the-Loop

Automation alone is insufficient—HITL remains necessary in evaluation.

### Threat Landscape

Three challenges:
- Copyright/privacy violations
- Jailbreak attacks
- Emerging threats

Solutions combine technical measures (detection/prevention) with policy/regulatory measures.

### The Measurement Challenge

**Defining good metrics is the hardest part.** Requires justification combining objective and subjective assessment.

---

## Scalable Oversight

### Humans + Models Collaborating

- Humans edit model outputs
- Specialized interfaces for different tasks
- Complementary strengths leveraged

### Rich RL Environments

Building RL environments requires:
- Many consistent messages across channels
- Evolving time/events
- Significant complexity to maintain

---

## Practical Checklist

### Starting Evals

- [ ] Define evaluations from business outcomes (not abstract metrics)
- [ ] Build eval infrastructure before shipping
- [ ] Create failure analysis pipeline
- [ ] Distinguish "bad tests" from "bad solutions"

### Improving Evals

- [ ] Custom scoring functions for your application
- [ ] LLM-assisted test generation with human validation
- [ ] Solution-specific testing strategies
- [ ] Guardrail scenarios included

### Scaling Evals

- [ ] Continuous engineering to reconcile with user experience
- [ ] Clear complaint paths for user feedback
- [ ] Fast model update capability (24-hour target)
- [ ] System-wide optimization (not just prompts)

---

## Summary

Effective EvalOps requires:

1. **Outcome-first design** — Metrics tied to business impact
2. **Continuous operation** — Evals evolve with the system
3. **Custom scoring** — Generic metrics don't work
4. **Human-in-the-loop** — Automation alone is insufficient
5. **System-wide optimization** — Data + tasks + scoring, not just prompts
6. **Fast iteration** — Error analysis → intervention → validation

The goal is not passing benchmarks—it's reliable production behavior that serves users.
