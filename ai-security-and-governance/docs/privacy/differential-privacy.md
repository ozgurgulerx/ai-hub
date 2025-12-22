# Differential Privacy (P1)

Differential privacy (DP) is a formal guarantee that limits what can be learned about **any single individual** from a released output (statistics, model parameters, embeddings, logs).

## What DP gives you

- A math-backed bound on privacy loss, typically summarized by **(ε, δ)**.
- A way to reason about privacy even under strong adversaries (who know “everything else”).

DP does **not** guarantee:

- security (you still need access control, encryption, audit)
- fairness (DP can degrade minority-group performance if not handled carefully)
- zero leakage (it bounds *incremental* risk, not absolute secrecy)

## Where DP is most useful in this repo’s context

- **Training / fine-tuning**: DP-SGD or clipped + noised updates to limit memorization of sensitive samples.
- **Telemetry / analytics**: privacy-preserving aggregates for product metrics or safety signals.
- **Data release**: synthetic data or sanitized statistics with explicit privacy budgets.

## Core mechanisms (mental model)

- **Sensitivity**: how much can one person change the output?
- **Noise**: add calibrated randomness (Laplace/Gaussian mechanisms) proportional to sensitivity.
- **Composition**: privacy loss accumulates; you need a budget strategy.

## DP-SGD in one paragraph

DP-SGD clips per-example gradients to a norm bound and adds Gaussian noise before applying the optimizer step. You track the privacy budget over training steps (accountant).

## Design checklist

- **Define the unit of privacy**: person, device, session, document?
- **Pick the release target**: trained weights, adapter weights (LoRA), metrics, embeddings?
- **Set a privacy budget**: acceptable (ε, δ) and how you’ll account for it.
- **Plan utility trade-offs**: more privacy (lower ε) generally means lower accuracy.
- **Test for memorization**: membership inference probes, canary insertion, leakage evals.

## Pitfalls

- DP only covers what’s inside the mechanism: if you log raw prompts/labels elsewhere, DP doesn’t help.
- Budgets get consumed quickly with long training runs; plan composition early.
- For LLM fine-tuning, DP can be expensive (per-example gradients); consider parameter-efficient approaches (adapters) and smaller batch strategies where appropriate.

