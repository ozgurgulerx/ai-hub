# Context Engineering with Filesystems (for agentic RAG)

This note distills a post titled **“How agents can use filesystems for context engineering”** (Nick Huang, Nov 21, 2025).

No URL/source was provided in the input; treat this as a **secondary note** until the canonical link is pinned.

## Core framing (as described)

Agents fail for two broad reasons:

- The model is not good enough.
- The agent does not have access to the right context.

“Context engineering” is described as the art/science of putting the right information in the context window for the next step.

## A simple mental model: total → needed → retrieved

The post frames three sets:

- **Total context**: everything the agent could access (all docs, all code, etc.).
- **Needed context**: the smallest subset required to answer the question correctly.
- **Retrieved context**: what the agent actually pulls into the context window.

Goal: make retrieved context a small superset of needed context (“fit red to green”).

## Failure modes (agent context can fail in multiple ways)

1) **Needed context not in total context**
   - Example: a required doc page was never indexed/available.
2) **Retrieved context doesn’t include the needed context**
   - Example: the right page exists but is not retrieved.
3) **Retrieved context is far larger than needed context**
   - Example: the agent retrieves 100 pages to answer a question requiring one.

## Common challenges (why this happens)

- **Too many tokens**: retrieved context ≫ necessary context (tool outputs bloat conversation history).
- **Context window limits**: necessary context can exceed what fits in the model’s window.
- **Niche information**: semantic search may miss API refs/code where meaning is sparse.
- **Learning over time**: needed context may be revealed by users during interaction but not persisted.

## Why a filesystem helps (the central claim)

The key proposal: a filesystem gives an agent a single interface to store/retrieve/update an effectively unbounded amount of context, while only loading a small slice at a time.

### Pattern 1: Offload large tool outputs to disk

Instead of keeping large tool call outputs (e.g., web search results) in the conversation history, store them as files and later retrieve only the relevant parts via:

- directory traversal (`ls`, glob)
- keyword search (grep)
- partial reads (read specific files/lines)

This reduces persistent token bloat and lets the agent “page” context in and out.

### Pattern 2: Persist plans and long-horizon state

For longer tasks, the agent can write its plan to a file and re-load it later to:

- keep the plan stable across steps
- remind itself what it is doing without re-stating everything in the prompt

### Pattern 3: Subagents write to shared files (avoid “telephone” loss)

When subagents are used, they can write findings to the filesystem instead of only summarizing via chat messages. The main agent can later read the relevant files directly.

### Pattern 4: Store instructions/skills as files and load on demand

Instead of stuffing all instructions into the system prompt, store instruction bundles as files and have the agent read them only when needed (linked in the post to “skills” patterns).

### Pattern 5: Learning over time by writing new context

The post suggests that when users provide corrective feedback or preferences, agents can write those into files as future context (an emerging pattern; not described as solved).

## Relationship to RAG (how this fits “Advanced RAG”)

Filesystem-backed context is complementary to retrieval indexes:

- **Vector/keyword retrieval** is great for *finding candidate sources* at scale.
- **Filesystem operations** are great for *navigating structured corpora* (codebases, API references) and *controlling token budget* by reading only relevant slices.

The post suggests combining both when helpful.

## Practical implications (distilled)

- Treat “context” as a first-class resource with **storage** and **paging**, not just chat history.
- Optimize for **token budget discipline**: write big artifacts, read small slices.
- Prefer workflows that preserve **traceability** (files capture intermediate steps and can be reviewed).

## Open questions / unknowns (as stated or implied)

- How to safely and reliably “learn over time” (persisting new instructions) without drifting or accumulating harmful rules.
- How to prevent sensitive data leakage when writing tool outputs to disk (requires governance and access controls). [Inference]

## Related (in this repo)

- Agent protocols and tool interfaces: `../../projects/agents/agent-protocols/README.md`
- Agent governance controls (logging/retention/kill switches): `../../ai-security-and-governance/docs/agent-governance/README.md`
- Claude Skills notes (progressive disclosure concept): `../../projects/agents/agent-protocols/claude-skills/README.md`
- Context compaction + RPI workflow (“No vibes allowed”): `context-engineering-no-vibes-allowed.md`

## Appendix: Raw Notes (Preserved)

- “Context engineering is the ‘delicate art and science of filling the context window with just the right information for the next step’.”
- The post uses the mental model total context → needed context → retrieved context and focuses on minimizing waste and failure modes.
