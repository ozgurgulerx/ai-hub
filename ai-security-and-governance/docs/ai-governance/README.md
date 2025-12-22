# AI Governance

AI governance is the operating model that turns **responsible AI principles** into **enforceable controls** across the AI lifecycle: roles, policies, risk management, evaluation gates, monitoring, incident response, and audit evidence.

## Key References

- Cloud Adoption Framework (CAF) for AI (includes governance guidance): https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/ai/
- Security for AI: https://learn.microsoft.com/en-us/security/security-for-ai/
- Responsible AI Toolbox (incl. dashboards): https://github.com/microsoft/responsible-ai-toolbox
- Microsoft compliance assurance for AI: https://learn.microsoft.com/en-us/compliance/assurance/assurance-artificial-intelligence

## A Practical Lifecycle: Govern → Map → Measure → Manage

### Govern

Define the **roles, responsibilities, and policies** that guide development and deployment of AI systems, including responsible AI principles such as:
- Fairness
- Reliability & safety
- Privacy & security
- Inclusiveness
- Transparency
- Accountability

### Map

Identify and prioritize risks associated with the AI system and its use:
- Responsible AI impact assessments (potential harms + mitigations)
- Threat modeling (including agent/tool abuse paths)
- AI red teaming to simulate adversarial or misuse scenarios

### Measure

Systematically evaluate risks using defined metrics and test suites, such as:
- Content safety (policy violations, toxicity, self-harm, hate/harassment, sexual content)
- Groundedness (alignment with sources), relevance, and faithfulness (for RAG)
- Safety mitigation effectiveness (refusal quality, safe completion behavior, jailbreak resilience)
- Reliability (task success rate, tool-call correctness, regression stability)

In practice, this often combines automated evaluations (including adversarial test datasets) with human review workflows; platform tooling may be used to standardize these runs (e.g., safety evaluations in Azure AI Studio).

### Manage

Operationalize governance so controls stay effective over time:
- Monitoring and alerting (privacy-aware logs/traces)
- Change management (versioning prompts/policies/tools; approvals for rollout)
- Incident response (containment, rollback, evidence, postmortems)
- Periodic access reviews and compliance evidence collection

## Governance for AI Agents (Identity, Access, Inventory)

For agents that can take actions via tools/APIs, treat identity and access as first-class governance:
- **Conditional Access & Zero Trust**: least privilege, scoped tokens, environment separation, approval gates for high-impact actions.
- **AI agent registry**: inventory agents, owners, tool permissions, data access, evaluation gates, and audit/retention requirements.

## Microsoft Ecosystem Notes (Packaging/Names May Evolve)

Microsoft positions agent governance as an extension of its security + identity + data governance stack (e.g., Microsoft Defender, Microsoft Entra, and Microsoft Purview), paired with admin controls and productivity context. Concepts often highlighted include:
- Purview DSPM for AI capabilities (data posture/visibility for AI usage)
- Entra-based access controls for AI and agent identities
- Central administration for managing agents at scale

Some announcement/roadmap discussions also use evolving product/feature names (verify current branding before adopting them in documentation):
- “Agent 365” / agent management at scale
- “Entra Agent ID” / agent identities
- “Foundry control plane” / centralized AI platform governance
- “Work IQ” / organizational intelligence and work context for Copilot experiences
