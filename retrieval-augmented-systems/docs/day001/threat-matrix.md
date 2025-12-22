# Day001 Threat Matrix (LLM/RAG security map)

This repo uses **5 layers** (attack surface) + **2 lifecycles** (where flaws enter).

Layers: Model · Prompt/Orchestration · Retrieval/Data · Tools/Actions · Runtime/Ops  
Lifecycles: Supply chain · Assurance loop

| Threat (what breaks) | Layer(s) | OWASP LLM Top 10 (suggested) | Example in this repo | What to measure | What to do (control) |
|---|---|---|---|---|---|
| Direct prompt injection overrides intent | Prompt/Orch | LLM01 Prompt Injection | Attack prompts that request secret/tool misuse | ASR, policy violation rate | Strong system policy + structured tool router |
| Indirect prompt injection via retrieved text | Retrieval/Data + Prompt/Orch | LLM01 Prompt Injection | Poisoned doc injects “ignore above” | ASR per “indirect” family | Retrieval firewall + safe transforms |
| Tool misuse / privilege escalation | Tools/Actions | LLM07 Insecure Plugin Design + LLM08 Excessive Agency | Model calls `get_customer_record()` for unauthorized ID | Tool abuse rate | Data-driven tool permission gate (deny by default) |
| Sensitive data exposure (secrets/PII) | Runtime/Ops + Retrieval/Data | LLM06 Sensitive Info Disclosure | Logs capture prompts/responses + tool outputs | Leakage score | Redaction, minimization, secrets hygiene, logging policy |
| Insecure output handling (HTML/SQL/SSRF) | Prompt/Orch + Tools/Actions | LLM02 Insecure Output Handling | “Tool args” treated as trusted | Output policy violations | Strict schema validation + allowlists |
| RAG data poisoning (corpus/index) | Retrieval/Data + Supply chain | LLM03 Training Data Poisoning | Poisoned docs shipped in repo | Poisoning success rate | Provenance, signing, review gates, quarantine |
| Denial of service (cost/latency) | Runtime/Ops | LLM04 Model DoS | Long prompts / tool loops | p95 latency, cost/1k attacks | Rate limits, budgets, timeouts |
| Supply chain compromise (deps/models) | Supply chain | LLM05 Supply Chain | Unpinned deps / unverified models | SBOM, drift | Pinning, checksums, signing |
| Overreliance / false confidence | Prompt/Orch | LLM09 Overreliance | Model fabricates citations | Citation accuracy | Require evidence + “no-answer” policy |
| Model extraction / theft | Model + Runtime/Ops | LLM10 Model Theft | Unthrottled endpoint | Query similarity, abuse | Auth, rate limits, watermarking (as needed) |

