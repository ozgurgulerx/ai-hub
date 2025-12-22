# First Principles for Building the Next Generation of Agents — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/4BatCFWsTFM`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat model/version references, named systems (“AMP”), and prescriptive design advice as **to verify** until corroborated by primary sources (talk recording, docs, or reproduced experiments).

## Agentic era: what changes (claims)

- The “agentic era” is described as a paradigm shift (models named: “3.7 Sonnet”, “Claude 4”).
- Focus shifts toward:
  - inverting context fetching (the agent actively pulls/constructs context)
  - tightly coupling models with tools
- Interaction shifts from “human-in-the-loop” to **upfront intent articulation**, with agents executing tasks (validation, file manipulation, command execution).

## The agentic feedback loop becomes central (claims)

- The feedback loop is described as the core design surface:
  - runtime design
  - agent/sub-agent integration
  - tool connectivity
- Resulting product shape is described as:
  - thinner clients
  - less monolithic “context engines”

## RAG and tool evolution (claims)

- RAG is described as evolving beyond retrieval into “molding” underlying models for applications.
- Tools are described as falling into functional categories:
  - context retrieval
  - feedback
  - planning
  - context management
  - sub-agent usage

## Tool choice and primitives (claims)

- Tool choice is described as critically shaping agent behavior.
- “Primitive tools” (named: grep/glob/search sub-agents) are emphasized for building agentic flows.
- The recommendation framing: choose models intentionally for each agent/sub-agent rather than defaulting to one model everywhere.

## Architecture example: “AMP” coding agent (claims)

- “AMP” is described as a coding agent with:
  - a simple VS Code extension + CLI
  - focus on feedback loops over complex UI
- Design choices are described as “controversial”:
  - no model selector
  - variable pricing

## Anti-pattern: cargo-culting chat-era best practices (claim)

- “Cargo-culting” practices from the chat LLM era is described as potentially harming agent performance; agent design should be intentional rather than optimized for beginner-friendly interfaces.

## Context and sub-agents (claims)

- Context expands beyond documents into:
  - feedback loops
  - planning tools
  - environmental validation
- Sub-agents are described as an intentional way to manage context, used for tasks like:
  - code-based search
  - thread summarization
  - unit test generation

## Evaluation guidance (claims)

- Evaluation should emphasize **unit tests and smoke tests** for workflow continuity, rather than relying only on evals to guide product development.

## Future directions (claims)

- Agentic models are described as enabling new workflows and generalizing to new domains beyond “retrieval + search”.
- “Background agents” are described as promising but should be:
  - simple
  - composable
  - easy to reason about
  - not vertically integrated / overly opinionated

## Cross-links (in this repo)

- Context engineering (filesystem-backed, compaction, sub-agents): `../../../retrieval-augmented-systems/README.md`
- “No vibes allowed” (RPI + compaction; sub-agent search pattern): `../../../retrieval-augmented-systems/notes/context-engineering-no-vibes-allowed.md`
- MCP and tool boundaries: `../agent-protocols/mcp/README.md`
- Agent governance controls (approvals, audits, kill switches): `../../../ai-security-and-governance/docs/agent-governance/README.md`

## Appendix: Raw Notes (Preserved)

- “Agentic era… invert context fetching… tightly coupling models with tools…”
- “Tools categorized into context retrieval, feedback, planning, context management, sub-agent use…”
- “Evaluate with unit tests and smoke tests…”
