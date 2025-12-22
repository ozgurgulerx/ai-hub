# Threat Model Template (LLM / RAG / Agents)

Use this template to build a living, test-driven threat model that maps directly to evals.

## 1) System overview

- Product purpose:
- Users / roles:
- High-level flow (1–2 paragraphs):

## 2) Assets (what you protect)

- Secrets (API keys, tokens, signing keys):
- PII / customer records:
- Proprietary corpora / embeddings / indexes:
- Tool credentials and side effects (payments, writes, emails):
- Logs and telemetry:

## 3) Trust boundaries (where you must gate)

- User input boundary:
- Retrieval boundary (documents → prompt):
- Tool boundary (model → action):
- Runtime boundary (logs, secrets, telemetry):

## 4) Attack surface map (5 layers)

For each layer, list entry points and controls.

1. Model:
2. Prompt & orchestration:
3. Retrieval & data:
4. Tools & actions:
5. Runtime & ops:

## 5) Lifecycles (where vulnerabilities enter)

- Supply chain: datasets, deps, prompts, eval sets, docs
- Assurance loop: red team → mitigations → regression tests

## 6) Threats (use + adapt)

For each threat, record: abuse case → impact → detection → mitigation → test.

- Prompt injection (direct/indirect):
- Tool abuse / confused deputy:
- Sensitive data exposure (training/runtime/logging):
- RAG poisoning (corpus/index/query-time):
- Insecure output handling:
- DoS / cost blowups:
- Supply chain:
- Monitoring gaps:

## 7) Evals as controls (the important part)

- What is your attack pack?
- What are your success metrics (ASR, leakage, tool abuse)?
- What’s your regression gate in CI?

## 8) Residual risk + acceptance

- What remains unsafe and why?
- What compensating controls exist?
- Owner + review date:

