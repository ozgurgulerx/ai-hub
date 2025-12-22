# Trends in Deep Learning Hardware (Bill Dally) — Notes

Summary for: https://youtu.be/4u8iMr3iXR4  
Generated from transcript tooling (Noiz): https://noiz.io/tools/download-youtube-transcript  
Status: **To verify**

## Why GPUs “Unlocked” Deep Learning (Claims)

- The deep learning “revolution” is framed as being enabled by GPUs that made older algorithms (DNNs/CNNs/backprop/SGD) practical at scale with datasets like ImageNet. [Unverified]

## Performance Gains and Where They Came From (Claims)

- NVIDIA GPUs are described as achieving ~5,000× inference performance increase over ~12 years via process, number formats, instruction complexity, and sparsity. [Unverified]
- MLPerf is cited as showing large generation-to-generation improvements (Hopper → Blackwell) and additional gains from software tuning on the same hardware. [Unverified]

## Blackwell Architecture (Claims)

- Blackwell is described as using two large dies connected by high-bandwidth interconnect and paired with very high HBM bandwidth. [Unverified]
- Racks with dozens of GPUs are described as pushing power density beyond 100kW and using electrical links (not optical) for cost/energy/reliability. [Unverified]

## Parallelism Dimensions (Claims)

- Three parallelism dimensions are described: data parallelism, pipeline parallelism, tensor parallelism. [Unverified]

## Inference Bottleneck Framing (Claims)

- LLM inference is framed as highly memory-bandwidth constrained, with large KV cache per user and stringent latency for interconnect communication. [Unverified]
- Energy breakdown is described as dominated by math and data movement, motivating bandwidth/locality optimizations. [Unverified]

## Compression: Quantization + Sparsity (Claims)

- FP4 (Blackwell) is described as a major contributor to performance/efficiency by reducing bit-width and partial products. [Unverified]
- Structured sparsity is described as enabling regular compute while skipping zeros via metadata and selection. [Unverified]

## Model Architecture Levers (Claims)

- Mixture-of-experts is described as reducing bandwidth by routing tokens to a small subset of parameters (conditional computation). [Unverified]
- Attention is framed as quadratic; sparse/pruned attention is described as a path to reducing complexity. [Unverified]

