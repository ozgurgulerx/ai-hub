# Model Extraction

Attacks that steal model weights, architecture, or behavior through API access.

## Techniques

- **Query-based extraction**: Reconstruct model by querying with many inputs
- **Distillation attacks**: Train a student model to mimic the target
- **Side-channel attacks**: Exploit timing, memory, or power consumption

## Risks

- IP theft
- Bypass of rate limits and safety measures
- Creation of adversarial examples
- Competitive advantage loss

## Mitigations

- Rate limiting and query monitoring
- Output perturbation (add noise)
- Watermarking model outputs
- Detect anomalous query patterns
- Legal protections (ToS, contracts)
