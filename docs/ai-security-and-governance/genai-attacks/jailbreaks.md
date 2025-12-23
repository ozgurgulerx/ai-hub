# Jailbreaks

Techniques to bypass LLM safety guardrails and content filters.

## Common Techniques

- **Role-playing**: "Pretend you are an AI without restrictions"
- **Encoding**: Base64, ROT13, or other encodings to hide malicious content
- **Multi-turn attacks**: Gradually escalate across conversation turns
- **Language switching**: Use less-moderated languages
- **Hypotheticals**: "For educational purposes, explain how..."
- **Token manipulation**: Exploit tokenization quirks

## Mitigations

- Robust safety training (RLHF, constitutional AI)
- Multi-layer content filtering
- Output monitoring and classification
- Regular red teaming and patching
- Rate limiting and anomaly detection
