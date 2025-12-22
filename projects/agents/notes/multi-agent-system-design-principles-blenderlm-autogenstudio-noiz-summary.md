# Multi-Agent System Design Principles (BlenderLM, AutoGen Studio) — Notes

Summary for: https://youtu.be/fmZWvE7yDZo  
Generated from transcript tooling (Noiz): https://noiz.io/tools/youtube-transcript  
Status: **To verify**

## Design Principles (Semi-Autonomous Multi-Agent UX)

Five design principles are highlighted:
- **Capability discovery**: itemize reliable agent capabilities.
- **Proactive suggestions**: parse user context to suggest next steps.
- **Observability**: stream activity logs to the UI.
- **Interruptibility**: pause/resume functionality.
- **Cost-aware delegation**: estimate action costs before execution and delegate expensive operations to users.

## When Multi-Agent Is Worth It

- Multi-agent systems are described as increasing the error surface across setup, agent configs, and delegation.
- A recommended strategy: inspect the problem space and confirm ROI first; only a subset of tasks benefit from multi-agent architecture.

## Eval-Driven Development Strategy

- “Eval-driven design” is described as: define tasks/metrics first, build a baseline unrelated to agents, then iterate.
- Example referenced: BlenderLM evolving from simple loops to include verification and planning agents validated via interactive evaluation.

## Task Fit (Heuristics)

Tasks are described as benefiting from multi-agent approaches when they:
- require planning,
- can be decomposed into multiple perspectives,
- require processing extensive context,
- must adapt to environmental changes in real-time.

## Tooling Note

- AutoGen Studio is described as a low-code framework for composing agent teams using primitives (models/tools), built on AutoGen.

