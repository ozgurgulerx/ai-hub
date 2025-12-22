# LLM App Threat Model Template (LLM-native)

## 1) System overview

- Product / feature:
- Users / roles:
- Trust boundaries (diagram if helpful):

## 2) Assets (what you must protect)

- Secrets (API keys, system prompts, credentials)
- Sensitive data (PII/PHI, internal docs, embeddings)
- Tooling permissions (what can cause side effects)
- Integrity (answers, records, actions)
- Availability (cost + latency + uptime)

## 3) Attack surfaces (5 layers)

- Model:
- Prompt & orchestration:
- Retrieval & data:
- Tools & actions:
- Runtime & ops:

## 4) Threats (map to OWASP LLM Top 10)

For each threat:

- Scenario:
- Preconditions:
- Impact:
- Likelihood:
- Controls:
- Tests (attack-as-test):

## 5) Controls and assurance loop

- Prevent (hard boundaries):
- Detect (logging/monitoring):
- Respond (runbook):
- Regress (continuous eval gates):

