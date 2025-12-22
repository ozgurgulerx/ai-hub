# Agentic AI MOOC (UC Berkeley CS294-196, Clay Bavor) — Practical Lessons from Deploying Customer-Facing Agents — Notes

Summary for: https://youtu.be/sfJM4LaiYsM  
Generated from transcript tooling (Noiz): https://noiz.io/tools/youtube-transcript  
Status: **To verify**

## Business Model: Outcomes-Based Pricing (Claims)

- Sierra is described as charging only when agents successfully resolve customer problems, aligning incentives and “proving” value via savings/revenue rather than SaaS seats. [Unverified]
- Sierra is described as targeting Fortune 500 customer service domains (returns/exchanges/tech support/recommendations/activation/upsell/troubleshooting). [Unverified]
- A taxonomy is described: personal agents, role-based agents (coding/legal), and customer-facing agents; customer-facing agents are predicted to become standard. [Unverified]

## Production Agent Challenges (Claims)

- Reliable agent deployment is described as requiring new SDLC approaches for non-deterministic systems: versioning/release management, observability, preventing illegal advice, latency, transcription accuracy, and blocking bad actors. [Unverified]
- Prompt injection is described as requiring layered defenses: deterministic checks, LLM supervisors, and internal agent rules to protect systems of record. [Unverified]
- Simulation-based testing with messy inputs, tool interactions, policy adherence, and multi-turn conversations is described as essential; Tau-bench is mentioned as a standardized benchmark. [Unverified]

## Voice Agents: System Requirements (Claims)

- Voice agents are described as requiring interruptibility, speaker separation, and custom UX metrics (traditional WER is described as insufficient). [Unverified]
- Chat-style model outputs are described as failing in voice contexts without tuning for cadence, phrasing, and pronunciation (names/numbers). [Unverified]
- A “voice sommelier” concept is described: match voice properties (graveliness, breathiness, enunciation) to brand personality. [Unverified]

## Platform Capabilities (Claims)

- Sierra’s “Agent Data Platform” is described as combining long-term memory, customer-data integration, and proactive outbound engagement (calls/messages). [Unverified]
- Sierra is described as providing both a code-based SDK (engineering) and no-code tools (ops) for defining behavior/knowledge/tools, plus “expert answers” synthesized from contact center experts. [Unverified]

## Related (In This Repo)

- EvalOps and simulation-driven testing: `../../../evalops/README.md`
- Agent governance controls: `../../../ai-security-and-governance/docs/agent-governance/README.md`
- Conversational interfaces (voice): `../../../workshops/06-conversational-interfaces-web-voice-realtime/README.md`

