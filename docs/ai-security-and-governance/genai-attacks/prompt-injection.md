# Prompt Injection

Attacks that hijack LLM behavior by injecting malicious instructions into prompts.

## Types

### Direct Injection
User directly provides malicious prompt to the model.

### Indirect Injection
Malicious content embedded in external data sources (documents, web pages, tool outputs) that the model processes.

## Attack Vectors

- User input fields
- Retrieved documents (RAG poisoning)
- Tool/API responses
- Email/message content
- Web page content (for browsing agents)

## Mitigations

- Input validation and sanitization
- Prompt structure (clear delimiters, instruction hierarchy)
- Output filtering
- Treat external data as untrusted
- Privilege separation (limit what injected prompts can do)
