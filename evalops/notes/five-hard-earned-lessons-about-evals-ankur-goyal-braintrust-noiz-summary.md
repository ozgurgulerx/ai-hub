# Five Hard-Earned Lessons About Evals (Ankur Goyal, Braintrust) — Notes

Summary for: https://youtu.be/a4BV0gGmXgA  
Transcript/summary source (Noiz): https://noiz.io/tools/youtube-summary and https://noiz.io/tools/youtube-transcript  
Status: **To verify**

## Evaluation Engineering (Evals as Continuous Ops)

- Effective evals are framed as enabling fast model updates (e.g., within 24 hours) by incorporating user feedback via clear complaint paths and by assessing use-case viability pre-launch. [Unverified]
- Great evals are framed as requiring continuous engineering that reconciles datasets with real user experience. [Unverified]
- Custom scoring functions are emphasized: scoring should be tailored to the application rather than relying on generic off-the-shelf / open-source scores. [Unverified]

## Context Optimization (Tools Dominate Token Budgets)

- In modern agentic systems, tools are described as dominating the LLM token budget; performance depends on precise tool interface and output definitions rather than mirroring existing API structures. [Unverified]
- New model releases are framed as potentially changing feasibility overnight: a model swap can make previously unviable features viable. [Unverified]

## System-Wide Optimization (Not Just Prompts)

- Optimizing eval performance is framed as holistic optimization of the whole system: data, tasks, and scoring functions, not prompt tweaks alone. [Unverified]

## Automated Evals Optimization (Braintrust “Loop” Feature)

- The “Loop” feature is described as auto-optimizing evals by generating prompts, datasets, and scores. [Unverified]
- It’s framed as enabling targeted questions such as: improving prompts, identifying missing dataset elements, and adjusting scoring criteria. [Unverified]

## Related (In This Repo)

- Eval design philosophy (outcome-first): `evaluation-design-for-reliable-ai-agents-noiz-summary.md`
- DSPy optimization loop notes: `fireside-chat-dspy-creator-omar-khattab-noiz-summary.md`
