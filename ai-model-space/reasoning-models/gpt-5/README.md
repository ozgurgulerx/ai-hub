# GPT-5 (“Build Hour”) — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/ITMouQ_EuXI`

This note distills claims from a **Noiz** summary provided in the prompt. Treat benchmarks, product comparisons, and API feature descriptions as **to verify** until corroborated by primary sources (official docs, release notes, or the talk itself).

## Claimed capability deltas (as described)

- A step-function improvement in:
  - code quality
  - front-end / UI generation
  - agentic task reliability
- Benchmarks/examples named in the summary:
  - Sweetbench (benchmark; to verify)
  - “Ador Polyglot” multilingual code editing (to verify)

### “Autonomous coding agent” anecdotes (claims; to verify)

- “Charlie Labs” autonomous coding agent is described as outperforming “Cloud Code” in 10/10 comparisons for generating PRs from GitHub issues, attributed to:
  - steerability
  - tool decision boundaries
- GPT-5 is described as generating a functioning landing page from a single one-shot prompt.

## API and parameters mentioned (claims; to verify)

### “Minimal reasoning” parameter

- A “minimal reasoning” parameter is described as enabling the least amount of reasoning needed while maintaining a latency profile similar to non-reasoning models, helping with efficient tool calls and JSON adherence.

### Free-form function calling

- “Free-form function calling” is described as simplifying tool integration by combining instruction following and tool calls in a single workflow.

### Responses API (“stateful v2”)

- The **Responses API** is described as a stateful successor to the Completions API.
- It is described as allowing passing back “reasoning items” for maximal model intelligence and enabling better caching, cheaper usage, and faster response times by leveraging “reasoning tokens”. (Treat this as a marketing/mechanism claim until verified.)

Related (in this repo):
- Build Hour notes on Responses API (Noiz summary, to verify): `../../../model-apis/openai/responses-api-build-hour-noiz-summary.md`
- Build Hour notes on Responses API (Noiz summary, to verify): `../../../docs/ai-model-space/model-apis/openai/responses-api-build-hour-noiz-summary.md`
- Agent examples using Responses API (Azure-style): `../../../projects/agents/05-agent-memory-general/README.md`

## Prompting / control techniques (claims)

### Verbosity parameter

- The “verbosity” parameter is described as affecting instruction adherence for very long outputs (10k–100k word essays), while having less impact on shorter (≈1k word) tasks.

### Meta prompting

- “Meta prompting” is described as asking the model why it made a choice, then correcting behavior based on those reasons; claimed to be more effective than one-off edits.

### XML prompt formatting

- XML formatting is described as performing well in GPT‑5 tests, with a caveat that optimal formatting varies by use case.

## Production implementation patterns (as described)

- “Charlie Labs” is described as using:
  - Responses API + built-in web search tool
  - a VM for dependencies (TypeScript)
  - `ripgrep` for context discovery
  - patch-application tooling for edits
  - tests before commits/PRs

### “Minimizing slop” suggestions (claims)

- Provide a style guide.
- Specify a minimal feature list.
- Ask for minimal tests.
- Use summary models to compact older conversation context.
- Provide a file-tree outline for large repos so the model respects tool decision boundaries.

## Verification checklist

- Identify the official documentation / release notes for:
  - “minimal reasoning” and “verbosity” parameters
  - free-form function calling
  - Responses API behavior and caching claims
- Locate or reproduce the cited evaluations:
  - Sweetbench
  - Ador Polyglot
  - the “10/10 PR generation” comparison

## Appendix: Raw Notes (Preserved)

- “Build Hour: GPT-5 … step function increase in code quality, front-end/UI generation, and agentic task reliability…”
- “Minimal reasoning parameter…”
- “Free-form function calling…”
- “Responses API (stateful v2)… passing back reasoning items… caching…”
