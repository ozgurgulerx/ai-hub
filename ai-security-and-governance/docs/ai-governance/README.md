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

## Ontologies (Semantic Layer for Governed AI Retrieval)

For enterprise LLM systems, reliability is often limited less by prompting and more by **data governance**: consistent definitions, lineage, permissions, policy enforcement, and source authority. Ontologies help by making “business meaning” explicit and machine-readable.

What an ontology provides:

- **Concept model**: business entities (Customer, Transaction, Policy) and their properties, independent of physical schemas.
- **Relationships**: joins and dependencies expressed explicitly (including hierarchies and transitive relations).
- **Governance hooks**: concept-level classifications, allowed uses, ownership, and policy bindings (e.g., “PII”, “gold source”, “region restricted”).
- **Metric definitions**: standardized measures (e.g., “Revenue”) defined once and reused consistently.

Why it matters for LLM + RAG:

- Improves **source selection** (authoritative vs. non-authoritative) and reduces definition drift.
- Enables **policy-aware retrieval** (filtering/pruning by user permissions and data classification).
- Makes multi-system governance more consistent by expressing rules at the semantic layer, not per-tool.

Practical note: “SQL-based ontologies” are increasingly discussed because they can express semantic models and governed views while fitting existing warehouse/lakehouse workflows (and avoiding specialized query languages in many teams).

### Epistemology (What Ontologies Can and Can’t “Fix”)

Ontology projects often fail for a non-technical reason: teams mix up **facts**, **inferences**, and **unknowns**, then expect reasoning to “fill in” missing data. A useful mental model (especially when combining OWL + SHACL) is captured in:

- Deep dive: `ontology-epistemology-owl-shacl.md`

Key idea: **reasoning exposes implications of what you already know; it does not acquire missing facts**. Completeness for action must be **declared and governed**, not inferred.
