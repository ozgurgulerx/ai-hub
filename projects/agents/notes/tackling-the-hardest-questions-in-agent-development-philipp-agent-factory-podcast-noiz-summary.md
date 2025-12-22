# Tackling the Hardest Questions in Agent Development (Philipp) — Notes

Summary for: https://youtu.be/kPVZQ3ae7-8  
Generated from summary tooling (Noiz): https://noiz.io/tools/youtube-summary  
Status: **To verify**

## Production-Ready Agent Development (Core Claims)

- Observability, monitoring, evaluation, and prompt optimization are framed as core to production agents due to LLM nondeterminism and shifting user expectations (more important than framework/model choice). [Unverified]
- Agents are framed as “living artifacts” that require continuous improvement via automated prompt-optimization pipelines as inputs/expectations evolve. [Unverified]
- Iterative development with real user feedback is emphasized as critical for finding what works and improving over time. [Unverified]

## Deep Research Agent Architecture (Pattern)

- A “deep research agent” is described as running a loop of research → report generation → self-critique, with the model deciding whether to continue or return a final answer. [Unverified]
- Pattern described: tool use (e.g., web search) + self-reflection (LLM critiques its output against criteria) while controlling iteration count and research depth. [Unverified]
- LangGraph is described as enabling complex agent architectures with control over execution, including parallel research agents for read-heavy workflows. [Unverified]
- Evaluation for deep research agents is described as time-intensive: structured testing with diverse queries, generated results, and scoring before publishing as “production examples”. [Unverified]

## Context Engineering, Function Calling, Memory

- Context engineering is framed as managing the right information, tools, time, rules/instructions, and structured outputs per iteration. [Unverified]
- Function calling (Gemini) is described as enabling structured outputs (e.g., JSON) for code execution and broader agentic use cases. [Unverified]
- Agent memory is framed as enabling persistent user information for personalization, but difficult to implement and evaluate because benefits are indirect. [Unverified]

## Gemini Capabilities and Model Selection (As Framed)

- Gemini is described as offering long context (1M tokens), multimodal I/O (image/audio/video), and strong reasoning (2.5 Pro/Light), enabling more compute/time and more information for tasks. [Unverified]
- Strategy described: start with the Gemini API for quick POC validation; consider open models for constrained environments but expect higher compute/upfront costs. [Unverified]

## Gemini CLI + MCP Servers (Dev Tooling)

- Gemini CLI is described as an open-source coding CLI agent used internally and externally for doc updates, snippet validation, and contributions. [Unverified]
- MCP servers are described as enabling code execution in ephemeral isolated Docker containers for safely running potentially untrusted code snippets, with automatic iteration on execution errors. [Unverified]
- Gemini CLI custom commands are described as using TOML templates (rules/guidelines/file links) to streamline workflows. [Unverified]

## Framework and Optimization Strategy

- Frameworks like LangGraph, CrewAI, and ADK are described as accelerating prototyping, but monitoring/eval are positioned as the production differentiators. [Unverified]
- Automated prompt optimization tools + evaluation sets are described as key to adapting prompts across models/use cases and scaling agent quality. [Unverified]
- Building the deep research agent is described as defining steps as Python functions connected by conditionals (“craft execution” pattern) with Gemini 2.5 + search integration. [Unverified]

## Related (In This Repo)

- EvalOps notes (evaluation sets + optimization loops): `../../../evalops/README.md`
- MCP protocol patterns: `../agent-protocols/mcp/README.md`
- MCP security controls: `../../../ai-security-and-governance/docs/mcp-security/README.md`
- Agent governance controls: `../../../ai-security-and-governance/docs/agent-governance/README.md`
