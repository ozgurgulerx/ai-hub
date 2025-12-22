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
