# RAG in the Age of Agents (Agentic Retrieval) — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/IgFx6LLkTwg`

This note distills claims from a **Noiz** summary provided in the prompt. Treat benchmark conclusions, tool comparisons, and prescriptions as **to verify** until corroborated by primary sources (talk recording, SWE-Bench eval details, code, or reproduced experiments).

## Core claim (as described)

In “agentic” settings, retrieval is not a one-shot component. Agents can compensate for weaker tools through iterative exploration, so the winning approach is often:

- start with simple tools
- add an agent loop
- evaluate end-to-end
- iterate based on observed failure points

## Agent architecture & tool design (claims)

### Simple tools can beat sophisticated retrieval (SWE-Bench claim)

- On SWE-Bench, agents using basic filesystem tools (e.g., `grep`, `find`) are described as outperforming “sophisticated embedding-based retrieval systems” because **persistence** and iteration compensate for tool weakness.

### “Embedding system as a tool”

- “Agentic retrieval” is described as surfacing an embedding system to the agent as just another tool.
- This is described as helping with token budget management over long contexts (100k+ tokens) without maintaining a separate embedding database. (Ambiguous; to verify.)

### Build from “dumb” to “smart”

- Guidance framing:
  - start with the dumbest retrieval tools (basic bash commands)
  - add an agent loop
  - iterate based on customer pain points
- Tool choice is described as shaping agent behavior; avoid overly complex tool schemas that bloat codebases without clear benefit.

## Retrieval method selection (claims)

- Retrieval choice is described as depending on quality, latency, cost, reliability, index size, and maintenance effort.
- `grep`/`find` are described as fitting structured content (code).
- Embedding models are described as fitting less-structured corpora (e.g., Slack/Notion) and complex mapping tasks.
- For small codebases (SWE-Bench-sized), simple grep/find can outperform complex embedding-based retrieval; for large corpora or unstructured data, embeddings help scale.

## Evaluation & optimization (claims)

- Start with end-to-end evaluations for agentic retrieval systems.
- Improve based on observed struggle points; improving embeddings alone may not help if the agent loop is the limiting factor.
- “Vibe evals” are described as useful alongside quantitative metrics.

## Advanced techniques (claims)

### Memory as semantic cache

- Agent memory is described as acting like a semantic cache, speeding up future searches and enabling personalization.

### Hierarchical retrieval for codebases

- Hierarchical retrieval is described as summarizing files and directories.
- Agents are described as calling different retrieval tools as needed (filesystem search, embeddings, summaries), enabling hybrid systems without heavy ranking-curve tuning.

## Practical implications (distilled)

- For code agents: prioritize `grep`/`find` + good repo navigation + iteration before building an embeddings DB.
- Treat retrieval methods as tools; let the agent choose and combine them.
- Measure end-to-end task success, then optimize the bottleneck you actually see (tooling, indexing, planning, memory, reranking).

## Appendix: Raw Notes (Preserved)

- “On SWE-Bench… simple grep and find tools outperformed sophisticated embedding-based retrieval…”
- “Start with dumbest retrieval tools… add agent loop… iterate…”
- “Memories act as semantic cache…”
