# MCP Security

MCP (Model Context Protocol) connects a host application (often an agent) to one or more **MCP servers** that expose tools, resources, and prompts. This creates a powerful integration surface — and a new security boundary: **every MCP server is effectively code you are choosing to trust**.

This note focuses on practical security for MCP-based systems: what can go wrong, and what controls to put in place.

## Threat Model (Trust Boundaries)

Typical components:
- **Host app** (your product/runtime): owns user sessions, auth, policies, logs.
- **Model**: generates plans, selects tools, and composes inputs.
- **MCP server(s)**: implement tool calls and data/resource access.
- **Downstream systems**: APIs, databases, internal services, SaaS, file systems.

Key boundary: treat **MCP servers and downstream tools** as untrusted until proven otherwise (even if “internal”), because they can:
- Exfiltrate data (intentionally or via bugs)
- Perform unintended actions (overprivileged permissions)
- Return adversarial outputs that manipulate the model (“tool output prompt injection”)

## Common Risks

- **Supply-chain risk**: installing or running an MCP server is equivalent to running third-party code.
- **Overprivileged tools**: “convenience” servers that can read files, run shell commands, or access broad cloud scopes.
- **Prompt/tool injection via tool output**: MCP responses include attacker-controlled strings that can override system intent.
- **Data exfiltration**: secrets, tokens, PII, or proprietary data leaking via tool calls, logs, or model context.
- **SSRF / internal pivoting**: tools that can fetch URLs may reach internal metadata endpoints or private services.
- **Cross-tenant/session mixups**: caching, shared state, or weak session scoping in MCP servers.
- **Non-repudiation gaps**: weak audit trails (who/what triggered the action, with which approvals).

## Controls (Practical Defaults)

### 1) Treat MCP servers as “code” (not “plugins”)

- Pin versions, review source, and scan dependencies.
- Prefer **allowlisted, vetted servers** over arbitrary user-installed servers.
- Require ownership metadata: maintainer, repo, release process, security contact.

### 2) Isolation and least privilege

- Run MCP servers in a **sandbox** (container/VM) with:
  - Read-only file system where possible
  - Minimal OS permissions
  - No ambient credentials
- Use **scoped credentials** per server/tool:
  - Separate identities for each server
  - Short-lived tokens
  - Minimum API permissions

### 3) Network egress controls

- Default-deny outbound network for MCP servers unless explicitly required.
- If network is needed, enforce **domain allowlists** and block link-local and metadata IP ranges (SSRF hardening).

### 4) Tool permissioning and approvals

Classify tools by impact and gate them:
- **Read-only** (low risk): safe to auto-run with logging.
- **Writes / external side effects** (medium/high): require explicit user confirmation and/or policy approval.
- **High-risk** (shell execution, credential access, admin APIs): avoid; if required, isolate heavily and add multi-step approvals.

Implement:
- Allowlist/denylist of tools per environment (dev/stage/prod)
- Spend/rate limits and timeouts
- “Kill switch” / safe-mode to disable tool execution quickly (see `../agent-governance/kill-switches.md`)

### 5) Input validation + output handling (anti-injection)

- Validate tool inputs (types, lengths, patterns) and enforce schemas.
- Treat **tool outputs as untrusted data**, not instructions:
  - Prefer structured outputs (JSON) with schema validation
  - Strip/ignore any “instructions” coming from tools
  - Keep system/developer policy separate from tool-returned text

### 6) Data governance and logging hygiene

- Redact secrets/PII from:
  - Tool inputs/outputs
  - Model context
  - Logs/traces
- Define retention and access controls for agent/tool traces.
- For RAG/resource tools: apply classification-aware filtering and per-user authorization checks.

### 7) Observability and auditability

Log enough to answer:
- Which user/session initiated the run?
- Which tools were called, with what parameters (redacted), and what responses?
- What approvals were granted and by whom?

Add detection for:
- Unusual tool call patterns (bursting, new endpoints, unexpected tools)
- Repeated failures (possible probing)

## Recommended “Minimum Bar” Checklist

- MCP servers run sandboxed with least privilege and no ambient creds.
- Network egress is restricted; SSRF defenses in place for any fetch tool.
- Tool catalog is allowlisted; risky tools are gated by approvals.
- Tool I/O is schema-validated; tool outputs are treated as untrusted data.
- Traces are privacy-aware, access-controlled, and retained per policy.
- A kill switch exists to disable tools/servers quickly.

## Where This Fits in This Repo

- Agent operational controls: `../agent-governance/README.md`
- Broader governance model: `../ai-governance/README.md`

## Talk notes (to verify)

- “The Dark Side of MCP: Why Adoption Is Outpacing Safety” (Vitor Balocco) — Noiz summary notes: `dark-side-of-mcp-vitor-balocco-noiz-summary.md`
