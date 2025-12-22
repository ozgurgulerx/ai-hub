# Day001 Threat Matrix (LLM/GenAI Security)

This is a 1-page working map from threat → where it lives (layer) → where it enters (lifecycle) → how you’ll test it.

## Layers (attack surface)

1. Model
2. Prompt & Orchestration
3. Retrieval & Data
4. Tools & Actions
5. Runtime & Ops

## Lifecycles (where vulns enter)

- Supply chain (data, models, deps, prompts, evals)
- Assurance loop (red team → mitigations → regression tests)

## Matrix (mapped to OWASP LLM Top 10)

| OWASP | Threat | Primary layer(s) | Lifecycle | Example failure mode | Day001 test hook |
|---|---|---|---|---|---|
| LLM01 | Prompt injection (direct/indirect) | 2, 3 | Assurance loop | Model follows attacker instructions embedded in user input or retrieved docs | `attacks/prompt_injection/` + `attacks/rag_poisoning/` |
| LLM02 | Sensitive information disclosure | 2, 3, 5 | Assurance loop | Secrets/PII leak via responses, logs, memory | Leakage regex in `eval/harness/` |
| LLM03 | Supply chain | 3, 5 | Supply chain | Poisoned corpora, compromised deps, tainted eval sets | Provenance checks in retrieval firewall (v0) |
| LLM04 | Data/model poisoning | 3, 1 | Supply chain | Malicious doc changes answers/tooling behavior | Poisoned doc in `apps/vuln_rag_agent/data/poisoned_docs/` |
| LLM05 | Insecure output handling | 2, 5 | Assurance loop | Rendering/exec of model output, unsafe parsing | “tool call as JSON” parsing in app (vuln by default) |
| LLM06 | Excessive agency | 4 | Assurance loop | Model can trigger high-impact tools without authorization | Naive tool router vs tool gate defense |
| LLM07 | Prompt leaks / system prompt extraction | 2 | Assurance loop | Model reveals hidden instructions and secrets | Direct injection cases (Day001) |
| LLM08 | DoS / resource abuse | 5 | Assurance loop | Long prompts, recursion, tool loops → cost/latency blowups | Latency + (optional) rate limiting later |
| LLM09 | Overreliance | 2, 5 | Assurance loop | Users trust incorrect/uncited answers | Add citation/provenance scoring Day002+ |
| LLM10 | Model theft | 1, 5 | Assurance loop | Query-based extraction, logging leaks | Out of scope Day001; add later |

