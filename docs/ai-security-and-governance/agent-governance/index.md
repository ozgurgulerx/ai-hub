# Agent Governance

Security + operational control layer for AI agents that plan and take actions via tools/APIs.

## Positioning

- **AI security** identifies risks (prompt injection, tool misuse, data exfiltration)
- **Agent governance** turns risks into **policy, permissions, approvals, monitoring**
- **Goal**: make agent behavior *reviewable, reversible, least-privilege, auditable*

## Control Domains

- **Autonomy tiers**: informational → recommend → act with approval → autonomous
- **Accountability**: RACI, owners, approvers, escalation paths
- **Risk management**: agent threat models, impact scoring, sign-off
- **Policy & guardrails**: acceptable use, prohibited actions, safety constraints
- **Identity & access**: agent identities, least privilege, scoped tokens
- **Action controls**: human-in-the-loop, allowlists, spend limits, kill switches
- **Observability**: structured logs, anomaly detection, drift monitoring

## Notes

- [Kill switches](kill-switches.md)
- [Zero-click attacks on AI agents](zero-click-attacks-ai-agents-noiz-summary.md)
