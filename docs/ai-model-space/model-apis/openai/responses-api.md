# Responses API

The Responses API is OpenAI's next-generation API designed for reasoning models and agentic workflows. It replaces the pattern of Chat Completions + Assistants with a unified, stateful, multimodal interface.

**Reference:** [Why we built the Responses API](https://developers.openai.com/blog/responses-api/) (Sep 22, 2025)

---

## Why Responses API Exists

Each API generation reflects how models work:

| API | Era | Design |
|-----|-----|--------|
| `/v1/completions` | Pre-RLHF | Prompt → completion |
| `/v1/chat/completions` | ChatGPT | Turn-based chat with roles |
| `/v1/responses` | GPT-5 / Reasoning | Agentic loop with persistent reasoning |

**Problem with Chat Completions for reasoning models:** Reasoning state is dropped between calls—like a detective forgetting clues every time they leave the room.

---

## Key Concepts

### Agentic Loop (not just chat)
Responses gives you a structured loop for reasoning and acting:
1. You provide evidence (input)
2. Model investigates (reasoning)
3. Model consults experts (tools)
4. Model reports back (output)

The model's **reasoning state persists** across turns via `previous_response_id`.

### Items In, Items Out
Responses emits a **list of polymorphic items** (not just a single message):
- `reasoning` — internal thought process (summarized, not raw CoT)
- `message` — assistant response
- `function_call` — tool invocation

This makes the ordering of actions clear and enables richer debugging/auditing.

### Hosted Tools
Server-side tool execution reduces latency and round-trips:
- `file_search` — RAG without building your own pipeline
- `code_interpreter` — model writes and runs code
- `web_search` — live web access
- `image_gen` — image generation
- `MCP` — Model Context Protocol integration

---

## Why Reasoning is Hidden

Raw chain-of-thought (CoT) is **not exposed** to clients:
- Hallucinations and harmful content may appear in reasoning but not final output
- Allows monitoring for manipulation without training compliance into CoT
- Competitive protection

Reasoning is preserved internally (encrypted) and can be continued via `previous_response_id` or reasoning items.

---

## Benefits vs Chat Completions

| Aspect | Chat Completions | Responses |
|--------|------------------|-----------|
| Reasoning persistence | ❌ Dropped between calls | ✅ Preserved |
| Output structure | Single message | List of items (reasoning, message, tool calls) |
| Multimodal | Bolted on | Native (text, images, audio, functions) |
| Hosted tools | ❌ | ✅ (file_search, code_interpreter, web, MCP) |
| Cache utilization | Baseline | 40–80% better |
| TAUBench (agentic) | Baseline | +5% with preserved reasoning |

---

## Practical Guidance

- **Stateful by default**: Use `previous_response_id` to continue conversations
- **Append-only context**: Keep appending items to preserve caching benefits
- **Streaming**: Semantic streaming events for real-time UI
- **SDK helpers**: `output_text` instead of `choices[0].message.content`

---

## Future

> "Just as Chat Completions replaced Completions, we expect Responses to become the default way developers build with OpenAI models."

Chat Completions isn't going away, but Responses is the API OpenAI will build on going forward.

---

# Build Hour: Responses API — Notes

Summary for: https://youtu.be/hNr5EebepYs  
Generated from transcript tooling (Noiz): https://noiz.io  
Status: **To verify**

## Agentic Loop and API Design (As Described)

- Responses API is described as supporting an “agentic loop” that enables multiple actions in one request and allows the model to sample multiple times. [Unverified]
- “Items in, items out”: the API is described as using a union of item types representing model actions and outputs to simplify coding across scenarios. [Unverified]
- Stateful by default: the API is described as being able to rehydrate chain-of-thought from a database to maintain context across requests. [Unverified]

## Performance and Efficiency (Claims)

- In long tool-calling rollouts, Responses API is claimed to be ~20% faster and more cost-efficient than Chat Completions because the model can plan once and execute multiple functions. [Unverified]
- A ~5% tool-calling performance improvement is claimed vs Chat Completions by preserving reasoning across requests. [Unverified]
- Cache hit rates are claimed to improve because the model can move through rollouts with less re-thinking, producing fewer output tokens. [Unverified]

## Multimodal and Tool Integration (As Described)

- Simplifies multimodal usage (images as base64 or URLs) and is described as capable of extracting content from files like PDFs. [Unverified]
- “First-class support for MCP” is claimed, enabling multiple tools per request. Note: MCP name/meaning in the source should be verified against Model Context Protocol usage elsewhere in this repo. [Unverified]

## Persistent Reasoning and Context (As Described)

- “Persistent reasoning” is described as allowing rehydration of chain-of-thought from previous requests (including for ZDR customers or stateless use cases). [Unverified]
- Reasoning summaries are described as a UI feature while the model processes (especially with GPT‑5). [Unverified]
- Prompt caching guidance: treat context as an append-only list and keep appending items to preserve caching benefits. [Unverified]

## GPT‑5 and Future Capabilities (As Framed)

- Responses API is positioned as a flagship API for GPT‑5, enabling persistent reasoning, hosted tools, and multimodal workflows. [Unverified]
- Designed to support more complex agentic applications that preserve reasoning and context across interactions. [Unverified]

## Practical Implementation Notes (As Described)

- Rehydrate chain-of-thought using a previous response ID helper, or by creating a conversation object (mention: “post v1 conversations”). [Unverified]
- Focus on long tool-calling rollouts where the model “thinks extensively” before executing multiple functions sequentially. [Unverified]
- Append incremental input items to maintain context and prompt-caching benefits. [Unverified]

## Related (In This Repo)

- Agent examples using Responses API (Azure-style): `../../projects/agents/05-agent-memory-general/README.md`
- GPT‑5 Build Hour notes (mentions Responses API; Noiz summary, to verify): `../../model-space/reasoning-models/gpt-5/README.md`

