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

