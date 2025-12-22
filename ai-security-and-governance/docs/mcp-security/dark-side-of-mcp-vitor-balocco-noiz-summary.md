# The “Dark Side” of MCP: Why Adoption Is Outpacing Safety (Vitor Balocco) — Noiz Summary Notes

Source video (YouTube): `https://www.youtube.com/watch?v=sirXgsC2Da0`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat specifics, exploit anecdotes, and future predictions as **to verify** until corroborated by primary sources (the talk itself, code, writeups, or reproduced examples).

## Core claim

MCP adoption is described as accelerating faster than safety practices, and MCP integrations expand the prompt-injection and supply-chain attack surface because:

- Tool outputs are untrusted content that gets fed back into model context.
- MCP servers are effectively third-party code running in (or adjacent to) your trust boundary.

## Attack vectors (claims)

Prompt injection is described as occurring not only through user messages, but also through:

- **Tool outputs** (strings returned by tools, resources, or prompts)
- **Schemas** and tool metadata
- **Parameter names** and descriptions (including “clever naming” to influence model behavior)

### Real-world exploit examples (as described; to verify)

The summary mentions a variety of injection paths, including:

- LinkedIn profile tool outputs containing adversarial instructions
- GitHub public issues used to influence an agent that has access to private repos
- Notion agent PDFs used for data exfiltration
- Heroku 404 logs triggering unintended calls
- “GitLab Duo image requests” leaking private sales figures

Treat these as illustrative patterns until verified.

## The “lethal trifecta” (claims)

Maximum vulnerability is described as the combination of:

1) Exposure to **untrusted content**
2) Access to **private/sensitive data**
3) Ability to **exfiltrate** information (network/file/tool channel)

If all three exist, prompt injection is described as especially dangerous and difficult to contain.

## Supply-chain and distribution risks (claims)

- “Rug pull” supply-chain attacks are described as a risk when installing MCP servers from untrusted package ecosystems (example cited: npm), where a trusted package later ships a malicious update.

## Practical defenses (distilled from the claims)

### 1) Treat tool output as hostile input

- Sanitize tool outputs before placing them into model context.
- Prefer structured, schema-validated tool outputs; isolate “raw text” outputs.
- Strip or down-rank “instruction-like” strings coming from tools/resources.

### 2) Constrain capability by default

- Use strict, workflow-specific tool subsets (least privilege).
- For hands-off flows, allow only **read-only** tools by default.
- Default to requiring confirmation for actions with side effects.

### 3) Harden servers like production software

- Run servers with minimal required access; sandbox local resource access.
- Audit installed servers for command injection, path traversal/reversal, and suspicious schemas/descriptions.
- Validate tool inputs (e.g., URL allowlists / expected formats).
- Add output filters for PII/secrets when relevant (regex/binary checks; scope depends on product requirements).

### 4) Address supply chain

- Pin tool/server versions.
- Prefer signed or containerized distributions where possible.
- Inspect tool schemas/params/descriptions before deployment (treat “weird strings” as a red flag).

## Enterprise architecture patterns (claims)

- Maintain an internal MCP catalog of audited/trusted servers.
- Proxy MCP servers through a controlled gateway for oversight:
  - tool call logging
  - audit trails
  - policy enforcement (allowlists, approvals)

## Evaluation and the “next wave” (claims)

- MCP safety maturity is described as depending on:
  - substantial evaluation datasets for prompt-injection attacks
  - “safe-by-design” agent platforms that control tool calls and output presentation
- Prompt injection is predicted to become more sophisticated as models improve.
- Rug-pull risks may decrease as the ecosystem matures and an official registry emerges. (Forward-looking; to verify.)

## Checklist (quick)

- Identify your “lethal trifecta” conditions; remove at least one by design.
- Treat tool outputs as untrusted data; sanitize + validate before context injection.
- Constrain tool sets; require approvals for side effects; add kill switches.
- Pin versions; prefer vetted distribution; run servers sandboxed with minimal privileges.
- Proxy tool traffic for logging + policy; maintain an internal allowlisted catalog.

## Appendix: Raw Notes (Preserved)

- “Prompt injection occurs through tool outputs, schemas, and parameter names…”
- “The lethal trifecta… untrusted content + private data + exfil…”
- “Rug pulls via npm… pin versions… signed/containerized…”
- “Proxy through controlled gateway… internal MCP catalog…”
