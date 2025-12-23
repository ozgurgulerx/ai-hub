# Federated Learning (P1)

Federated learning (FL) trains a shared model across multiple parties **without centralizing raw data**. It’s most useful in **cross-silo** settings (enterprises, banks, hospitals) where data can’t leave its boundary but collaboration is still valuable.

## What FL is (and isn’t)

- FL **reduces data movement**, not risk: gradients/updates can still leak information without additional protections.
- FL is an **architecture**: you still choose optimizers, evals, access control, secure transport, and often privacy tech (secure aggregation / DP / TEEs).

## Common flavors

- **Cross-silo FL**: tens/hundreds of reliable clients (orgs/regions); stable networks; strongly identified participants.
- **Cross-device FL**: millions of unreliable clients (phones); privacy + robustness are first-class; much harder ops.

## Threat model (why “privacy” isn’t automatic)

- **Gradient inversion / membership inference**: reconstruct or infer training examples/participation from updates.
- **Malicious clients**: poisoning/backdoors, sybil behavior, collusion.
- **Curious server / coordinator**: sees updates, metadata, participation patterns.
- **Metadata leakage**: even if updates are protected, *who trained when* can be sensitive.

## Design checklist

- **Data boundary**: what *must not* leave each party? (raw data, features, labels, derived stats)
- **Coordinator trust**: do you trust a central server, or do you need cryptographic protection?
- **Aggregation**:
  - baseline: weighted FedAvg / FedAdam
  - hardened: secure aggregation (server can’t read individual updates)
- **Privacy hardening**:
  - DP on client updates (often DP-SGD or clipped/noised updates)
  - TEEs for aggregation or for running sensitive evaluation steps
- **Robustness/security**:
  - client authentication + attestation (where applicable)
  - anomaly detection on updates (norms, cosine similarity, clustering)
  - backdoor/poisoning tests in eval suite
- **Evaluation**:
  - global test set (if allowed) + per-silo holdout
  - fairness/representation: performance per client/silo

## NVIDIA dependency (practical note)

FL itself is not “GPU-specific”, but in practice FL orchestration often couples to DL training stacks.

- If your implementation standardizes on **NVIDIA GPUs/CUDA**, you may prefer using an NVIDIA-supported FL stack (e.g., **NVIDIA FLARE**) to reduce operational friction.
- Treat this as an **optional dependency choice**: the architectural decision is FL; the vendor/tooling decision is separate.

## When to use / when not to

- Use FL when:
  - data sharing is blocked (policy/regulation/contract) but shared learning is valuable
  - each silo has enough data/compute to contribute meaningfully
  - you can afford coordination overhead + more complex evaluation
- Avoid FL when:
  - a clean centralized dataset is feasible (it’s simpler and usually better)
  - silos are tiny/biased and aggregation amplifies skew
  - you need fast iteration but can’t invest in infra + governance

## Pitfalls

- “No raw data leaves” ≠ “private”: protect updates + metadata if needed.
- Heterogeneous silos cause unstable training (non-IID): you’ll need personalization strategies or careful weighting.
- Security is not optional: poisoning/backdoors are easier in federated settings without strong controls.

