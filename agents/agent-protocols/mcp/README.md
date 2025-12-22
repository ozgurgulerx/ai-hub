# MCP (Model Context Protocol)

MCP is a protocol for connecting LLM/agent applications to **external tools and context providers** through a consistent client↔server interface. Practically, it standardizes how an agent:

- Discovers capabilities (what tools/resources exist)
- Fetches context/resources (files, docs, database-like resources)
- Invokes tools (actions with structured inputs/outputs)

## A Useful Mental Model

Treat MCP like a “USB‑C port” for AI apps: instead of building one-off connectors per tool/data source, you connect to a server that speaks a standard protocol and exposes a stable surface area (tools, resources, prompt templates).

## The Real Problem MCP Solves (M×N → M+N)

Without a standard, integrating **M** AI apps (chat, RAG, agents, IDE copilots) with **N** external systems (GitHub, Slack, CRMs, DBs, internal APIs) becomes an **M×N** connector problem. MCP pushes you toward:

- **N servers**: tool/system owners expose one MCP server per system/integration boundary.
- **M clients**: app/agent owners implement one MCP client per host runtime.

Any compliant client can talk to any compliant server, reducing duplicated integration work and long-term maintenance.

## Core Pieces

- **Host**: the app users interact with (IDE, desktop app, custom agent runtime). The model and orchestration live here.
- **Client**: the host-side component that manages a connection to one MCP server (lifecycle, errors, request/response).
- **Server**: a focused program that exposes capabilities (tools/resources/prompts) and mediates access to underlying systems (files, DBs, SaaS APIs).

## Function Calling vs MCP (How They Fit)

- **Function/tool calling** is a *model API feature*: given a tool schema, the model can choose to call it.
- **MCP** is a *protocol boundary*: it standardizes how tools/resources are **discovered**, **invoked**, and **returned** across servers, transports, and vendors.

In practice: the host uses function calling (or equivalent) to decide *what to do*, and MCP is often the interface used to *do it* safely and consistently.

## How Clients Talk To Servers

MCP commonly uses JSON-RPC 2.0 message shapes:

- **Request** (expects a response)
```json
{ "jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": { "name": "weather", "arguments": { "location": "San Francisco" } } }
```
- **Response** (answers a request `id`)
```json
{ "jsonrpc": "2.0", "id": 1, "result": { "temperature": "72°F", "condition": "sunny" } }
```
- **Notification** (no `id`, no response expected; often progress/logging)
```json
{ "jsonrpc": "2.0", "method": "$/progress", "params": { "message": "Processing…", "progress": 0.8 } }
```

## Transports (How Bytes Move)

- **stdio**: client starts the server process locally and communicates over stdin/stdout. Great for local tools and dev workflows.
- **streamable HTTP**: client uses HTTP POST for requests; servers may use SSE for streaming back updates. Better for remote/multi-client deployments.

## Minimal End-to-End Example

See `mcp-mental-model-and-minimal-example.md` for a tiny Python server + client sketch (FastMCP-style) you can adapt.

## Additional Notes

- Reality check + adoption notes: `mcp-reality-check-and-adoption-notes.md`

## MCP In Agentic SaaS (Patterns That Matter)

- **Per-tenant tool access**: remote MCP servers can centralize tenant routing, credentials, and policy for “customer-specific connectors”.
- **Vendor neutrality**: keep your agent runtime portable while evolving models/providers behind the host.
- **Streaming UX**: transports that support streaming (e.g., SSE) help latency-sensitive, tool-heavy interactions feel responsive.
- **Small spec, big leverage**: MCP is intentionally narrow; you can wrap it with your own orchestration, governance, and observability layers.

## Why It Matters For Agents

- **Portability**: swap tools/providers without rewriting agent logic.
- **Separation of concerns**: keep domain integrations in MCP servers, keep reasoning/orchestration in the agent.
- **Operational control**: centralize auth, rate limits, auditing, and approvals at the boundary.

## What MCP Is NOT (Reality Check)

MCP is infrastructure, not intelligence. It does **not** provide:

- Planning/reasoning (“agent brain”) or task decomposition
- Workflow/state-machine execution, retries, or rollback semantics
- Security policy by default (TLS, RBAC, audit logs, tenant isolation are on you)
- Cost/rate-limit enforcement (you must implement budgets/quotas/guardrails)
- Error-handling framework (classification, fallbacks, user-safe messaging)
- Consent/governance UX (scopes, approvals, and explainable prompts are host/server responsibilities)
- Observability (traces/metrics/log conventions are implementation choices)
- A test/simulation story (mocks, contract tests, replay harnesses are up to you)

This is why MCP shows up as “plumbing”: it standardizes I/O between agents and systems, but you still build the rest of the house.

## Common Gaps To Design Around

- **Performance/cost**: tool-heavy tasks can require many discrete calls; caching, indexing, and batching matter.
- **Model awareness**: many models won’t “know MCP” unless your host teaches tool semantics and when to call them.
- **Metadata/versioning**: treat tool surfaces as APIs; consider explicit versions and compatibility tests.

## What Might Emerge Over Time

Teams often want conventions like:

- Structured error vocabularies (e.g., timeout vs auth vs invalid input)
- Tool metadata/versioning fields (read-only, side-effecting, deprecations)
- Explicit consent flags (to drive consistent approval UX)
- Trace IDs and minimal telemetry fields (to make debugging and audit easier)

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
