# Causal ML

This folder is for notes and references on **causal inference** and **causal machine learning**: how to estimate the effect of interventions, reason about counterfactuals, and avoid common pitfalls when learning from observational data.

## What This Should Cover

- **Causal fundamentals**: potential outcomes, counterfactuals, identifiability.
- **Graphs**: DAGs, backdoor/frontdoor, d-separation, do-calculus (conceptual).
- **Estimation**: matching, stratification, regression adjustment, IPW, doubly robust estimators.
- **Causal ML**: uplift modeling, CATE/HTE, causal forests, meta-learners, representation learning (high-level).
- **Experimentation**: A/B testing design, sequential testing, interference, spillovers.
- **Product & decisioning**: attribution vs causality, policy evaluation, bandits (links to RL section where relevant).
- **Failure modes**: selection bias, unmeasured confounding, collider bias, post-treatment bias.

## Suggested Structure (Planned)

- `notes/` — distilled notes and reading summaries
- `patterns/` — reusable causal “checklists” (assumptions, DAG workflows)
- `examples/` — small worked examples (synthetic, toy) where appropriate
- `references/` — pointers to books/papers (keep short; prefer primary sources)

## Related (In This Repo)

- RL & bandits: `../reinforcement-learning/README.md`
- Privacy (DP, federated learning): `../ai-security-and-governance/docs/privacy/README.md`

## Notes

- Traversal (causal ML × RL) — placeholder: `notes/traversal-causal-ml-and-reinforcement-learning.md`
