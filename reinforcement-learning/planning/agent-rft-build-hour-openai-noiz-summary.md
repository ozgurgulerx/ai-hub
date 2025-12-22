# Build Hour: Agent RFT (OpenAI) — Notes

Sources: https://youtu.be/1s_7RMG4O4U (as provided)  
Transcript/summary source (Noiz): https://noiz.io  
Status: **To verify**

## What Agent RFT Is (As Described)

- Agent RFT is described as training reasoning models to become tool-using agents by training directly on production workflows. [Unverified]
- Training operates on agent rollouts: call tools, generate reasoning steps, and receive real-time feedback via customer-provided endpoints. [Unverified]
- Mirroring production behavior (e.g., hosting tools as endpoints) is described as improving transfer of training gains to product behavior. [Unverified]

## Optimization and Efficiency Claims

- Recommended sequence: start with prompt engineering, simplify tasks, and improve tools before using Agent RFT. [Unverified]
- Agent RFT is described as sample-efficient and low-latency, useful when training data is scarce. [Unverified]
- Efficiency metrics cited:
  - tool calls per trace reduced 6.9 → 4.2, attributed to learning efficient tool usage. [Unverified]
  - repeated tool calls with different parameters reduced 1000 → 500. [Unverified]
  - using F1 reward is described as balancing precision/recall and avoiding context pollution. [Unverified]

## Training and Benchmark Claims

- Modified “financial QA” benchmark: find relevant reports among 2,800 documents within 10 tool calls. [Unverified]
- Training run claim: batch size 16 and compute multiplier 1 improved validation reward 0.59 → 0.63 in 10 steps. [Unverified]
- Parallel tool calling is described as learned behavior; claimed ~4× fewer back-and-forths vs baseline. [Unverified]

## Practical Applications (Claims)

- Ambience: +0.05 F1 in ICD10 coding and −18% latency using Agent RFT. [Unverified]
- Mako: +72% improvement in GPU kernel writing vs SOTA using ~100 PyTorch prompts. [Unverified]
- Rogo: +21% improvement in core ML performance using a custom LLM grader. [Unverified]

## Monitoring, Safety, and Graders

- Isolated VMs per rollout are described as preventing destructive actions during training. [Unverified]
- Monitoring is emphasized for detecting tool failures and model issues that can yield zero reward. [Unverified]
- “Hard-to-game” graders aligned with domain knowledge are described as enabling partial credit for correct reasoning paths. [Unverified]

## Quality Over Quantity

- Claim: ~150 high-quality samples can be sufficient for success. [Unverified]

## Related (In This Repo)

- Post-training + fine-tuning overview: `post-training-and-fine-tuning-mit-6s191-liquid-ai-noiz-summary.md`
- EvalOps (eval sets + scoring/rubrics): `../../evalops/README.md`

