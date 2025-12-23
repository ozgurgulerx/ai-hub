# Agent Governance

Agent governance is the **security + operational control layer** for AI agents (systems that plan and take actions via tools/APIs). In this repo, it lives under `ai-security-and-governance/` because governance is how security and safety requirements become enforceable controls in production.

## Positioning (How To Think About It)

- **AI security** identifies risks (prompt injection, tool misuse, data exfiltration, unsafe actions).
- **Agent governance** turns those risks into **policy, permissions, approvals, monitoring, and incident response** so the agent can run with bounded autonomy.
- **Goal**: make agent behavior *reviewable, reversible, least-privilege, auditable*, and *measurably safe* across the lifecycle.

## Scope

This folder focuses on governance for agents that can:

- Call tools/APIs (internal or external)
- Modify state (tickets, code, infrastructure, customer data)
- Spend money / consume quota (LLM usage, cloud resources)
- Act on behalf of a user or service identity

## Control Domains (Topics This Should Cover)

- **Definitions & autonomy tiers**: what counts as an agent; tier rubric (informational → recommend → act with approval → act autonomously).
- **Accountability**: RACI, owners/maintainers, approvers, escalation paths, decision logs.
- **Risk management**: agent-specific threat models; impact/likelihood scoring; risk acceptance and sign-off.
- **Policy & guardrails**: acceptable use, prohibited actions, user consent, transparency, safety constraints.
- **Identity & access**: agent/service identities, least privilege, scoped tokens, secrets management, network boundaries.
- **Action controls**: human-in-the-loop approvals, allowlists/denylists, spend/rate limits, environment separation, kill switches, safe/read-only mode.
- **Data governance**: classification, retention, redaction, PII handling, trace/audit privacy, training/eval data hygiene.
- **Evaluation & assurance**: pre-deploy gates, red-teaming, safety/security eval suites, regression tests, canaries, rollback criteria.
- **Observability**: structured logs and traces, prompt/tool-call recording (privacy-aware), anomaly detection, drift monitoring.
- **Incident response**: runbooks for agent-caused incidents, containment/rollback, forensics, postmortems, controls hardening loop.
- **Compliance & evidence**: mapping controls to SOC2/ISO/GDPR/AI Act (as applicable), audit artifacts, periodic access reviews.
- **Change management**: versioning prompts/policies/tools, approvals for rollout, controlled experimentation and feature flags.
- **Third-party & supply chain**: model/provider review, tool/plugin review, dependency integrity, prompt/policy asset integrity.

## Suggested Artifacts To Add Here

- Autonomy tier rubric + required controls per tier
- Tool registry (purpose, scopes, permissions, owners, audit requirements)
- MCP server registry (server inventory, exposed tools/resources, scopes, owners, review status)
- Approval matrix (which actions require human approval vs. auto-execute)
- Logging/retention policy for traces and tool outputs (with privacy constraints)
- “Break glass” + kill switch procedures and drills (see `../../../docs/ai-security-and-governance/agent-governance/kill-switches.md`)
- Red-team scenario pack + evaluation checklist
- Zero-click + agent abuse scenarios: `../../../docs/ai-security-and-governance/agent-governance/zero-click-attacks-ai-agents-noiz-summary.md`

## Next Files (Good Starting Point)

- `threat-model.md` (agent-specific threat model template)
- `approval-matrix.md` (action categories → required approvals/controls)
- `incident-runbook.md` (containment, rollback, evidence collection)
- `../../../docs/ai-security-and-governance/agent-governance/kill-switches.md` (feature flags, safety files, outage containment)

Related:
- MCP security notes: `../mcp-security/README.md`
- Product note (deterministic “agent builder” pattern; claims to verify): `../../../docs/ai-products/strategy-gtm/index.md`
- Zero-click attacks and agent amplification (Noiz summary, to verify): `../../../docs/ai-security-and-governance/agent-governance/zero-click-attacks-ai-agents-noiz-summary.md`
