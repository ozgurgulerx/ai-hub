# GenAI Attacks

Taxonomy of attacks targeting generative AI systems: LLMs, agents, RAG pipelines, and multi-agent systems.

## Attack Categories

| Category | Target | Description |
|----------|--------|-------------|
| **[Prompt Injection](prompt-injection.md)** | LLM input | Hijack model behavior via malicious prompts |
| **[Jailbreaks](jailbreaks.md)** | Safety guardrails | Bypass content filters and safety constraints |
| **[Data Poisoning](data-poisoning.md)** | Training/RAG data | Corrupt model behavior via poisoned data |
| **[Model Extraction](model-extraction.md)** | Model weights | Steal model parameters or behavior |
| **[Membership Inference](membership-inference.md)** | Training data | Detect if specific data was used in training |
| **[Adversarial Examples](adversarial-examples.md)** | Model inputs | Craft inputs that cause misclassification |
| **[Tool Abuse](tool-abuse.md)** | Agent tools/APIs | Exploit agent tool access for malicious actions |
| **[Data Exfiltration](data-exfiltration.md)** | Sensitive data | Leak PII/secrets via model outputs |
| **[Multi-Agent Attacks](multi-agent-attacks.md)** | Agent coordination | Exploit trust between agents |

## Key Considerations

- **Defense in depth**: no single control stops all attacks
- **Assume breach**: design for detection and containment
- **Red teaming**: continuously probe for new attack vectors
- **Observability**: log and monitor for anomalous behavior
