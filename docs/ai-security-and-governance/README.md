# ai-security-and-governance

My work on AI security methods and everything on AI security.

## Day001

- Checklist + commands: `docs/day001/checklist.md`
- Threat matrix: `docs/day001/threat-matrix.md`
- Optional red teaming tools (garak + PyRIT): `docs/day001/red-teaming-tools.md`

## Docs (Index)

- Start here: `docs/README.md`

## Privacy-preserving ML (P1)

- Overview: `docs/privacy/README.md`
- Federated learning: `../docs/ai-security-and-governance/privacy/federated-learning.md`
- Differential privacy: `../docs/ai-security-and-governance/privacy/differential-privacy.md`

## What AI Security Implies

AI security covers the ways AI systems can be attacked, misused, or fail, and the methods to reduce those risks. This includes:
- Adversarial and data poisoning attacks.
- Model theft, extraction, and inversion.
- Prompt injection and tool misuse.
- Privacy, data leakage, and sensitive information exposure.
- Robustness, monitoring, and incident response for AI systems.
- Governance, compliance, and secure deployment practices.

## A Practical Trust Stack (Builder View)

Trying to “inventory all our AI” as a governance strategy fails in practice because the denominator keeps changing (new models, new agents, new tools, new workflows). The better approach is a **control plane mindset**: build trust into platform primitives and identity-native enforcement, not paperwork.

Trust also behaves like an **SRE/DevOps loop**, not a one-time review:

- **Pre-deploy testing**: evals, red-team scenarios, regression diffs
- **Runtime protection**: boundary filters, least-privilege tool access, containment
- **Post-deploy monitoring + feedback**: detect false positives/negatives, iterate quickly

One high-signal implication: **user behavior is part of the security model**. If users don’t inspect citations, warnings, or tool receipts, your “trust UX” is failing even if the backend controls are correct.

### Agents Change the Threat Model

Agents introduce new attack surfaces beyond “model safety”:

- **Prompt injection (direct + indirect)**: malicious instructions from users, retrieved docs, web pages, or tool outputs.
- **Tool sprawl / permissioning**: too many tools, overly broad scopes, weak separation between read/write capabilities.
- **Memory manipulation**: poisoning what the agent stores/retrieves as long-term state so compromise persists across sessions.

So the trust problem is no longer “model safety” only — it’s **agent-system security**.

## AI Governance

AI governance is how organizations turn **responsible AI principles** into **enforceable controls** across the AI lifecycle (policies, roles, risk management, evaluations, monitoring, incident response, and audit evidence).

- Read: `docs/ai-governance/README.md`

## MCP Security

Security considerations for systems using the Model Context Protocol (MCP): trust boundaries, common failure modes, and concrete controls.

- Read: `docs/mcp-security/README.md`

## GenAI Attacks

A taxonomy of common GenAI/agent attack classes (prompt injection, jailbreaks, tool abuse, exfiltration, multi-agent attacks, etc.).

- Read: `genai-attacks/README.md`

## Agent Governance

Agent governance is the set of controls and operating practices for **AI agents that take actions via tools/APIs** (not just generate text). It bridges security, safety, and operational reliability:

- Read: `docs/agent-governance/README.md`

## Papers

- (Add papers here)

## References

- [Trustworthy AI at Microsoft: From commitments to capabilities | BRK212](https://www.youtube.com/watch?v=QQCQyq48USM&list=PLQXpv_NQsPIDKFpgLPXmtPSa15JyCWZKM&index=41)
