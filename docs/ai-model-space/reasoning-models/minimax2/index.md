# MiniMax M2

Efficiency-focused open-weight reasoning + coding model from MiniMax.

## Key Features

- **~10B activated parameters** — MoE-style sparse execution (low “active compute”)
- **Low latency** — snappy interactive coding
- **Self-hosted friendly** — data never leaves your infra
- **Agent-ready** — strong tool use + instruction following (reported)
- **Full attention** — reported decoder-style Transformer attention (not “efficient/lightning” attention)
- **Per-head QK-Norm** — reported per-layer QK-Norm variant with unique norms per attention head
- **Sliding-window attention** — present in config but disabled by default (reported)

## Use Cases

- Regulated environments (finance/healthcare)
- Internal codebases with privacy requirements
- High-volume agent workflows

## Architecture snapshot (reported)

![MiniMax-M2 vs Qwen3 architecture comparison](minimax2.jpeg)

Detailed notes: [MiniMax-M2 (full README)](README.md)
