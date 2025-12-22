# Model APIs

Notes on model-provider APIs and interface design choices.

## Topics

- **State Management** — Conversations, threads, sessions
- **Tool Calling** — Function calling, structured outputs
- **Streaming** — Token-by-token, server-sent events
- **Caching** — Prompt caching, KV-cache
- **Multimodal I/O** — Images, audio, video
- **Observability** — Logging, tracing, evaluation hooks

## Providers

| Provider | Key Features |
|----------|--------------|
| **OpenAI** | Responses API, function calling, assistants |
| **Anthropic** | Claude, long context, computer use |
| **Google** | Gemini, multimodal, grounding |
| **Azure OpenAI** | Enterprise, compliance, regional |

## Key Patterns

- **Structured Outputs** — JSON mode, function calling for reliable parsing
- **Prompt Caching** — Reduce latency and cost for repeated prefixes
- **Tool Use** — Define tools, let model decide when to call
- **Streaming** — Real-time token delivery for UX
