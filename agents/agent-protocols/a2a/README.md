# A2A (Agent-to-Agent)

A2A covers patterns and protocols for **agents communicating with other agents** to delegate work, negotiate, coordinate plans, and exchange evidence/results.

Depending on the system, “A2A” can mean anything from simple message passing to structured contracts (capability discovery, task assignment, status, proofs/receipts).

## Why It Matters For Agents

- **Decomposition**: route sub-tasks to specialist agents (retrieval, coding, eval, policy).
- **Parallelism**: run multiple independent agents and merge results.
- **Robustness**: redundancy, debate, verification, and cross-checking.
- **Organizational boundaries**: allow teams/services to own agents independently while still collaborating.

## What To Capture Here

- Topologies (hub-and-spoke, hierarchical, peer-to-peer, marketplace)
- Message schemas (task request, tool result, evidence, provenance, confidence)
- Coordination mechanisms (plans, shared memory, blackboards, consensus/voting)
- Safety controls (authority/permissions, escalation, containment, prompt-injection via messages)
- Evaluation (success metrics for coordination; failure modes like deadlocks and thrashing)

## Related

- Governance controls: `../../../../ai-security-and-governance/docs/agent-governance/README.md`
- Workshop: `../../../../workshops/05-agent-to-agent-topologies-and-negotiation-on-azure/README.md`
- A2A protocol notes (Noiz summary, to verify): `a2a-protocol-noiz-summary.md`
