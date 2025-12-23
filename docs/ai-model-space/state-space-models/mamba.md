# Mamba

Mamba is a modern **selective state space model (SSM)** designed to model long sequences efficiently with **linear-time** sequence processing and strong throughput.

## What it is

- Uses an SSM-style hidden **state** updated at each step.
- Adds **input-dependent selection/gating** so the model can adapt its state updates to the current token/context.

## When it’s useful

- Long-context workloads where attention’s quadratic cost is a bottleneck
- Streaming/online inference where constant per-step memory is important
- High-throughput batch inference on long sequences

## Considerations

- Tooling and post-training recipes are still less mature than “standard” transformer stacks.
- Many production systems use **hybrids** (some attention + some SSM blocks) to balance global interactions and efficiency.

