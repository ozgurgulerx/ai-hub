# MCP reality check + adoption notes

This is a practical add-on to the MCP overview: what MCP *does*, what it *doesn’t*, and how it tends to show up in real stacks.

## MCP is plumbing

- MCP moves **structured requests and responses** between an agent host and external systems.
- It does not make the agent “smart”; it makes the agent **connected**.

If your product needs planning, memory, workflows, safety, or evaluation, you layer those on top of MCP.

## Integration economics (why it matters)

MCP is mainly a standardization play:

- Without a standard: every new AI app must re-integrate with every system (the connector matrix grows as M×N).
- With MCP: each system exposes one MCP server, and each host implements one MCP client (closer to M+N).

## Function calling vs MCP (common confusion)

- Function calling/tool use is a *model capability* (“pick a tool and produce arguments”).
- MCP is a *protocol boundary* (“discover tools and call them over a transport”).

Many stacks use both: model decides *which* tool to call; MCP defines *how* to call it and receive results.

## Adoption: where MCP usually appears

- **Developer tools**: IDEs and coding assistants use MCP servers to safely expose repo access, shell actions, and developer services.
- **Enterprise connectors**: MCP servers front internal APIs/DBs with policy, logging, and tenant configuration.
- **Agent platforms**: MCP becomes a portable “tool bus” that multiple agent runtimes can reuse.

## Security checkpoints to internalize

- Treat servers as **integration boundaries**: they are where you should concentrate auth, policy, auditing, and least-privilege scope.
- Remote transports typically inherit the same risks as any API + auth system (token handling, redirects, OAuth footguns, secret storage).
- “Human-in-the-loop” approvals only help if prompts/scopes are clear and enforced consistently.

For deeper coverage, see `../../../../ai-security-and-governance/docs/mcp-security/README.md`.

## Common limitations teams hit

- **No workflow semantics**: MCP won’t coordinate multi-step jobs, retries, or compensating actions.
- **No built-in guardrails**: you must add budgets, rate limits, allowlists, and safe-mode behavior.
- **No observability standard**: you need trace IDs, logs, and metrics if you want to debug tool-heavy agents.
- **Cost/latency cliffs**: naive “list everything then read everything” patterns can explode in calls and tokens.

## Pragmatic guidance

- Design tools like stable APIs: clear names, schemas, and error contracts; document side effects.
- Prefer small, focused servers over “do-everything” servers; it simplifies review and reduces blast radius.
- Build contract tests and replay harnesses for tool calls; treat MCP traffic as something you can record and analyze.

