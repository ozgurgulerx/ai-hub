# MCP Security

MCP connects agents to servers that expose tools/resources. **Every MCP server is code you choose to trust.**

## Common Risks

- **Supply-chain risk**: running MCP server = running third-party code
- **Overprivileged tools**: servers with shell access, broad cloud scopes
- **Prompt injection via tool output**: adversarial strings manipulate model
- **Data exfiltration**: secrets, PII leaking via tool calls or logs
- **SSRF / internal pivoting**: tools that fetch URLs reach internal services

## Controls

1. **Treat MCP servers as code** — pin versions, review source, scan dependencies
2. **Isolation** — run sandboxed with least privilege, no ambient creds
3. **Network egress controls** — default-deny, domain allowlists
4. **Tool permissioning** — classify by impact, gate high-risk actions
5. **Anti-injection** — validate inputs, treat outputs as untrusted data
6. **Logging hygiene** — redact secrets/PII, define retention

## Notes

- [Dark side of MCP](dark-side-of-mcp-vitor-balocco-noiz-summary.md)
