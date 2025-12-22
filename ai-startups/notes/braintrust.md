# Braintrust (EvalOps / Observability) — Notes

Primary site: `https://www.braintrust.dev/`

This note is intentionally lightweight. It captures only what was stated/implicit in prior prompts: Braintrust is discussed as an EvalOps/observability layer for building, measuring, and iterating on LLM apps. Treat details as **to verify** until pinned to primary sources (docs, benchmarks, or case studies).

## What it is (as described)

- An AI observability / EvalOps platform focused on:
  - evaluations
  - logging/tracing
  - iteration loops (datasets/experiments) for prompts and models

## Why it matters (in this repo’s framing)

- “Measure → iterate → win” depends on repeatable evals and production traces, not vibes.

Related:
- EvalOps workshop: `../../workshops/09-evalops-and-costops-measure-iterate-win/README.md`
- Verification at scale (judge compute, rubric-first): `../../ai-product-strategy/notes/last-mile-ai-verification-verdict-noiz-summary.md`

## Open questions (to verify)

- What primitives are first-class (traces, datasets, eval runs, graders/judges)?
- What integrations exist (LLM SDKs, RAG frameworks, CI/CD hooks)?
- What self-hosting / data residency options exist?
- Pricing model and operational overhead at scale.

