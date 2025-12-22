# How to Succeed in Vertical AI — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/9CHktrroCDU`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat named people/org examples and prescriptive strategy as **to verify** until corroborated by primary sources (talk recording, case studies, or reproducible evidence).

## Core claim (as described)

Vertical AI wins are less about chasing the newest model and more about building a tight **domain-expert → eval → improvement** loop with production-grounded sampling, plus pragmatic prompting/context strategies.

## Domain expert integration (claims)

- Domain experts are described as high-leverage because they can:
  - review outputs and provide performance metrics
  - identify failure modes
  - propose improvements
  - create input–output pairs
- The goal is to prioritize work based on **representative production data**, not public model benchmarks.

### Review dashboards as core infrastructure (claims)

- Review dashboards are described as needing to optimize for:
  - high-quality reviews
  - minimal review time
  - actionable data generation
- Raw traces or spreadsheets are described as insufficient because they don’t present complex context well.

### “Principal domain expert” role (claims; example to verify)

- A principal domain expert with management + statistics + product skill is described as crucial for:
  - quickly recruiting reviewers
  - defining sampling strategy
  - steering product priorities
  - accelerating organizational progress
- Example mentioned: Chris Lovejoy at “Anterior” leveraging a medical background and network. (To verify.)

## Prompting vs fine-tuning (claims)

- Prompting is described as beating fine-tuning in the vast majority of vertical AI cases because:
  - out-of-the-box models already do a lot of domain reasoning (due to diverse pretraining)
  - fine-tuning adds operational complexity and requires ongoing monitoring

### Context augmentation (claims)

- “Context augmentation” is described as injecting domain-expert-curated knowledge bases at inference time (retrieval), e.g. region-specific definitions for “high net worth” in banking.

### Few-shot prompting (claims)

- Few-shot examples (including corrected examples from domain reviews) are described as enabling in-context learning and real-time retrieval of domain knowledge during inference.

## Continuous improvement loop (claims)

Described flywheel:

1) Domain experts review production outputs.
2) A domain-expert PM prioritizes failure modes.
3) Engineers build targeted fixes using failure-mode datasets.
4) Performance testing validates improvements.
5) Repeat.

### Performance monitoring (claims)

- Sampling strategies should prioritize high-impact cases.
- Customer trust is described as improving via periodic production output review and transparent metrics (example metric mentioned: judge alignment). (To verify specifics.)
- Protocols are described for responding to performance deviations.

## Architecture decisions (claims)

### Separate “extraction” vs “triage”

- Separating data extraction from data triage during ingestion is described as improving performance for large, diverse datasets (example domain: medical records) because it builds semantic understanding and improves retrieval of relevant information.

### Latency vs accuracy is contextual (agentic RAG)

- Whether to prioritize latency or accuracy depends on the workflow context (background vs real-time, e.g., patient consultation).
- Use case-specific performance metrics should drive trade-offs.

## Data + security management (claims)

- LLM-specific security topics mentioned include:
  - prompt injection prevention (input filtering + classifier LLMs)
  - output validation
  - human approvals for high-risk actions
  - PII sanitization
  - protection against poisoning (data/model) and adversarial attacks

### Recency and authority (claims)

- In fast-changing domains (example: healthcare), recency and authority of knowledge bases are described as critical.
- Domain experts are described as reviewing KBs; metadata extraction and similarity-based chunking are described as supporting recency weighting. (To verify.)

## Practical checklist (distilled)

- Put domain experts “in the loop” with a purpose-built review dashboard.
- Sample production outputs intentionally; prioritize failure modes by impact.
- Start with prompting + context augmentation + few-shot; add fine-tuning only when needed and budgeted.
- Separate extraction vs triage for large, diverse ingests.
- Treat recency/authority and injection/PII/poisoning as first-class requirements.

## Cross-links (in this repo)

- Document automation at scale (HITL-first, true automation rate, ontology): `document-automation-lessons-at-scale-noiz-summary.md`
- Production monitoring (signals + intents, deep search): `production-reality-vs-testing-signals-intents-noiz-summary.md`
- AI verification “last mile” (rubrics + judge agents): `last-mile-ai-verification-verdict-noiz-summary.md`
- Agent governance controls (approvals, logging, kill switches): `../../ai-security-and-governance/docs/agent-governance/README.md`

## Appendix: Raw Notes (Preserved)

- “Domain experts supercharge AI development…”
- “Prompting beats fine-tuning…”
- “Context augmentation… few-shot…”
- “Continuous improvement flywheel…”
