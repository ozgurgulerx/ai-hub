# Data Exfiltration

Attacks that leak sensitive data through model outputs.

## Attack Vectors

- **Training data extraction**: Prompt model to regurgitate training data
- **Context leakage**: Expose data from conversation context or RAG retrieval
- **Tool-based exfiltration**: Use tools (email, HTTP) to send data externally
- **Steganography**: Hide data in seemingly benign outputs

## Sensitive Data at Risk

- PII (names, emails, SSNs)
- API keys and credentials
- Proprietary business data
- Conversation history
- Retrieved documents

## Mitigations

- Output filtering and PII detection
- Data classification and access controls
- Network egress controls
- Logging and anomaly detection
- Minimize sensitive data in context
