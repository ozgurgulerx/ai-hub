# Model APIs

Notes on model-provider APIs and interface design choices that shape real-world LLM applications (state, tool calling, streaming, caching, multimodal I/O, and eval/observability hooks).

## What this section covers

- **Provider surfaces**: request/response schemas, auth, rate limits, streaming, state.
- **Inference controls (hyperparameters)**: sampling and decoding knobs.
- **Tool calling**: schema design, tool selection reliability, failure handling.
- **Runtime patterns**: retries, timeouts, caching, cost controls.
- **Observability hooks**: logs/traces/metrics to debug and evaluate behavior.

## Inference controls (hyperparameters)

- Temperature: `../../docs/ai-model-space/model-apis/inference-controls/temperature.md`
- Top-p (nucleus sampling): `../../docs/ai-model-space/model-apis/inference-controls/top_p.md`
- Structured outputs (JSON, schemas): `../../docs/ai-model-space/model-apis/inference-controls/structured-outputs.md`

## Reliability patterns

- Retries & timeouts: `../../docs/ai-model-space/model-apis/patterns/retries-timeouts.md`

## Providers

- OpenAI: `../../docs/ai-model-space/model-apis/openai/index.md`
