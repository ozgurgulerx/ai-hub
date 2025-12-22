# Inference Engineering

Building, scaling, and optimizing LLM inference stacks.

## Topics

- **vLLM, TensorRT-LLM, Triton** — Serving frameworks
- **Benchmarks** — Batch sizes, sequence lengths, quantization, hardware
- **Trade-offs** — Latency, throughput, memory, cost
- **Quantization** — INT8, INT4, FP8, AWQ, GPTQ
- **Serving patterns** — Batching, KV-cache, speculative decoding

## Key Concepts

| Concept | Description |
|---------|-------------|
| **KV-Cache** | Cached key-value tensors for efficient autoregressive generation |
| **Continuous Batching** | Dynamic batching of requests for throughput |
| **Speculative Decoding** | Draft model predicts, main model verifies |
| **Quantization** | Reduced precision for faster inference and lower memory |
| **PagedAttention** | Memory-efficient attention via virtual memory |
