# MCP (Model Context Protocol)

MCP is a protocol for connecting LLM/agent applications to **external tools and context providers** through a consistent client↔server interface. Practically, it standardizes how an agent:

- Discovers capabilities (what tools/resources exist)
- Fetches context/resources (files, docs, database-like resources)
- Invokes tools (actions with structured inputs/outputs)

## Why It Matters For Agents

- **Portability**: swap tools/providers without rewriting agent logic.
- **Separation of concerns**: keep domain integrations in MCP servers, keep reasoning/orchestration in the agent.
- **Operational control**: centralize auth, rate limits, auditing, and approvals at the boundary.

## What To Capture Here

- Client/server architecture patterns and deployment options
- Tool/resource design conventions (schemas, idempotency, error contracts)
- Security model (authn/authz, least privilege, sandboxing, audit logs)
- Failure handling (timeouts, retries, partial failures, circuit breakers)
- Operational safety controls (kill switches, safe mode)
- Testing (contract tests for servers; replayable traces for clients)

## Related

- Governance controls: `../../../../ai-security-and-governance/docs/agent-governance/README.md`
- Kill switches: `../../../../ai-security-and-governance/docs/agent-governance/kill-switches.md`
- MCP security threat model + controls: `../../../../ai-security-and-governance/docs/mcp-security/README.md`
- MCP server design (tool surface, examples, evals; Noiz summary, to verify): `server-design-for-llms-noiz-summary.md`
- MCP Dev Days (Day 1, DevTools; Noiz summary, to verify): `mcp-dev-days-day1-devtools-noiz-summary.md`
- MCP 201 (Code w/ Claude; Noiz summary, to verify): `mcp-201-code-with-claude-noiz-summary.md`
- Neo4j MCP: build a knowledge-graph agent + memory (Noiz summary, to verify): `road-to-nodes-neo4j-mcp-knowledge-graph-agent-workshop-noiz-summary.md`
- Realtime voice model notes (GPT Realtime; MCP mention; Noiz summary, to verify): `../../../../model-space/multi-modal-models/notes/introducing-gpt-realtime-api-noiz-summary.md`
- Claude agent loop framing (Claude Code SDK + MCP; Noiz summary, to verify): `../../notes/building-more-effective-ai-agents-claude-noiz-summary.md`
- Workshop: `../../../../workshops/04-mcp-on-azure-ai-foundry/README.md`
