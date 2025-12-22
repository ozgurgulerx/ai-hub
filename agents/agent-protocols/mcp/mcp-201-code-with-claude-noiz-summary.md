# MCP 201 (Code w/ Claude) — Notes

Summary for: https://youtu.be/HNzH5Us1Rvg  
Generated from summary tooling (Noiz): https://noiz.io/tools/youtube-summary  
Status: **To verify**

## Server Capabilities (As Described)

- **Prompts**: predefined templates executed as dynamic code on the server that inject snippets into the model context.
- **Resources**: expose raw data so applications can build embeddings and do RAG by selecting relevant data for the context window.
- **Sampling**: enables servers to request model completions from clients while clients retain control over security/privacy/cost; described as enabling chaining with managed interactions.

## Client Integration (As Described)

- **Roots**: allow servers to query open projects in the client IDE (e.g., VS Code) so actions (like git operations) run in the correct directory.

## Enterprise Deployment (As Described)

- Exposing MCP servers on the web: OAuth 2.1 for user binding and streamable HTTP for scalable interactions and SSO-aligned deployments.

