# Causal ML

Causal inference and causal machine learning for estimating intervention effects.

## Topics

- **Fundamentals** — Potential outcomes, counterfactuals, identifiability
- **Graphs** — DAGs, backdoor/frontdoor, d-separation, do-calculus
- **Estimation** — Matching, IPW, doubly robust estimators
- **Causal ML** — Uplift modeling, CATE/HTE, causal forests, meta-learners
- **Experimentation** — A/B testing, sequential testing, interference

## Key Concepts

| Concept | Description |
|---------|-------------|
| **ATE** | Average Treatment Effect |
| **CATE/HTE** | Conditional/Heterogeneous Treatment Effects |
| **Confounding** | Variables affecting both treatment and outcome |
| **DAG** | Directed Acyclic Graph for causal structure |
| **Do-calculus** | Rules for computing interventional distributions |

## Failure Modes

- **Selection bias** — Non-random treatment assignment
- **Unmeasured confounding** — Missing variables
- **Collider bias** — Conditioning on common effects
- **Post-treatment bias** — Controlling for mediators
