# Building Jamba 3B: the Tiny Hybrid Transformer State Space Reasoning Model (AI21) — Notes

Summary for: https://youtu.be/k6EIE325SgA  
Generated from transcript tooling (Noiz): https://noiz.io  
Status: **To verify**

## Hybrid Architecture (Attention + Mamba) (Claims)

- Jamba 3B is described as using a hybrid architecture with a 1:8 attention-to-Mamba layer ratio discovered via ablations, combining attention’s quadratic cost with Mamba’s linear memory scaling for long context. [Unverified]
- A 3B dense variant is described as using a 1:12 attention-to-Mamba ratio with very few attention heads to maximize long-context efficiency in small memory. [Unverified]
- Hybrid models are predicted (in the talk) to dominate long-context use cases, and future full-attention models are predicted to reduce attention layer count to manage costs. [Unverified]

## Edge/On-Device Context Pressure (Claims)

- On-device multimodal applications are described as being token-heavy (example: “4 images require thousands of tokens”), motivating long-context, memory-efficient architectures. [Unverified]

## Enterprise System Framing: Models as Actions (Claims)

- AI21’s “Maestro” system is described as treating models as actions with statistical properties (cost/latency/accuracy) to enable model-agnostic orchestration and avoid vendor lock-in. [Unverified]
- Models are described as “statistical beasts” not designed for reliability; enterprise systems are described as needing robustness and policy enforcement beyond model outputs. [Unverified]
- Enterprises are described as needing controllability over certainty/detail and enforcing their own policies rather than inheriting model-maker constraints. [Unverified]

## Related (In This Repo)

- Model Space index: `../../README.md`
- MCP as orchestration boundary: `../../../projects/agents/agent-protocols/mcp/README.md`

