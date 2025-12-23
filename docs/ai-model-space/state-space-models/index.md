# State Space Models

State Space Models (SSMs) are sequence models that maintain a compact **state** that updates over time, often enabling **linear-time** processing and efficient **streaming** inference.

**Major vendors / ecosystems**

- **AI21 Labs** (Jamba: hybrid attention + Mamba-style SSM blocks)
- **NVIDIA** (GPU ecosystem; many high-performance SSM kernels target CUDA)
- **Hugging Face ecosystem** (open-source checkpoints + libraries/implementations)
- **Together AI** (often hosts open-weight model families, including Mamba-class variants)
- **Fireworks.ai** (often hosts open-weight model families, including Mamba-class variants)

## What they are

SSMs model a sequence by evolving a hidden state:

- Each input token updates the state.
- Outputs are computed from the current state.

Modern deep SSMs use structured parameterizations (and fast kernels) that make this practical at large scale.

## When they’re useful

- **Very long context** where quadratic attention becomes costly
- **Streaming / online inference** where you want constant memory per step
- **Throughput-focused workloads** where linear-time sequence processing helps
- **Hybrid designs** where a small amount of attention is kept for “global” interactions

## Model families (click to expand)

??? info "Mamba (Selective SSM)"
    A “selective” SSM that learns to gate/control state updates based on the input, improving quality while keeping linear-time sequence processing.

    Useful when you need long-context efficiency and good throughput. See: [Mamba](mamba.md).

??? info "Mamba-2 (Improved Mamba variants)"
    Follow-up work that refines the Mamba approach (architecture and kernels) to improve training/inference efficiency and stability in practice.

    Useful when you want Mamba-like benefits with better performance characteristics. See: [Mamba](mamba.md).

??? info "Jamba (Hybrid Attention + SSM)"
    A hybrid architecture that interleaves attention layers with Mamba-style SSM layers, aiming to keep attention’s “global” capability while reducing overall cost for long sequences.

    Useful when you want a more transformer-like behavior but need better long-context efficiency. See: [Jamba](jamba.md).

??? info "S4 (Structured State Space Models)"
    A foundational deep SSM family that uses structured state space parameterizations to make long-range sequence modeling efficient.

    Useful for understanding the modern SSM lineage and core ideas (stability, discretization, structured kernels). See: [S4](s4.md).

??? info "S5 (Simplified State Space Models)"
    A simplification of structured SSM ideas that can be easier to implement and train, while retaining strong long-sequence properties.

    Useful when you want an S4-like approach with fewer moving parts.

??? info "DSS (Diagonal State Space) and related variants"
    Variants that constrain the state dynamics (e.g., diagonal parameterizations) to make training and inference simpler/faster while still capturing long-range dependencies.

    Useful as a stepping stone between classical SSMs and higher-performance selective/hybrid designs.
