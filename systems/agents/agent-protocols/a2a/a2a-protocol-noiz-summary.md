# Agent-to-Agent (A2A) Protocol — Notes

Summary for: https://youtu.be/wXVvfFMTyzY  
Generated from transcript tooling (Noiz): https://noiz.io/tools/youtube-video-transcript  
Status: **To verify**

## A2A (As Described)

- A2A enables remote agents to communicate over the web for specialization, delegation, parallel processing, and complex workflows.
- Each A2A agent may have a public definition describing capabilities used by other agents for routing/selection.
- A Genkit implementation detail is mentioned: a maximum of 5 sub-agent calls per turn (as described; verify).

## MCP Relationship (As Described)

- MCP is described as a standard interface to connect agents to external context/tools (plug-in style).
- A2A is described as more appropriate for third-party tools/complex workflows, while MCP is positioned as resource/tool infrastructure.

## Architecture Notes (As Described)

- A host agent orchestrates workflows, manages context windows, keeps summaries, and discards raw data.
- Sub-agents operate with isolated contexts that grow as needed.

## Operational Gotcha

- Example failure mode mentioned: some MCP integrations can fail silently (e.g., missing default Slack channel in a Zapier Slack MCP scenario).

