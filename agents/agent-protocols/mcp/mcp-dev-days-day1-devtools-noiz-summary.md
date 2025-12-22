# MCP Dev Days — Day 1 (DevTools) — Notes

Summary for: https://youtu.be/8-okWLAUI3Q  
Generated from transcript tooling (Noiz): https://noiz.io  
Status: **To verify**

## Core MCP Concepts (As Described)

- MCP is described as a standard protocol bridging models and tools to avoid custom point-to-point integrations.
- MCP servers are described as lightweight apps that provide context to MCP clients, exposing:
  - **resources** (e.g., API responses, files, screenshots),
  - **tools** (actions with structured inputs),
  - and prompt-related utilities (as referenced).
- MCP is described as supporting NL-driven workflows for testing/debugging by standardizing how agents access tools and context.

## Ecosystem + Platform Integration (Claims to Verify)

- MCP is described as being integrated across Windows (server support, registration, predefined servers).
- Azure AI Foundry is described as a platform for building/deploying agents with MCP, with human oversight patterns.
- The ecosystem is described as partner-driven (e.g., Anthropic and others).

## Server Management + Registry (As Described)

- A local MCP JSON config is described as listing installed servers and tools for discovery.
- Servers are described as installable via stdio (local) or remote URL (remote).
- A registry is described as a centralized database of servers with filtering/ranking, designed to be secure and spam-resistant.

## Security / Enterprise Integration (As Described)

- An authorization server is described as separable from the MCP server (physical separation; formalized spec).
- “Dynamic client registration” is described as enabling bring-your-own servers to clients without pre-existing relationships.
- “Enterprise managed authorization profile” is described as a concept for governed enterprise integration.
- Security best practices mentioned include logging, auditing, secure storage, and token validation; enterprise servers require curation/limited access.

## Open Questions / Needs

- Reference architectures and deployment patterns for different security profiles are called out as needed.
- Client identity is described as a core open problem (e.g., identity tied to domains; policy application).

