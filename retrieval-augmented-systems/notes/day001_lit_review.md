# Day001 Lit Review (minimum viable canon)

Write your own 10 bullets per source after you read. Use these as a starting scaffold.

## OWASP Top 10 for LLM Applications (threat taxonomy backbone)

- Prompt injection is the *root class* enabling many downstream failures.
- Output handling is security-critical: treat model output as untrusted input.
- Sensitive data can leak via prompts, retrieval, tools, and logs (not just training).
- Plugins/tools turn “text mistakes” into real side effects (money, writes, exfil).
- Excessive agency is a design flaw: constrain autonomy with explicit permissions.
- DoS includes economic DoS (token costs) and latency blowups.
- Supply chain risk spans deps, models, datasets, prompts, and eval sets.
- Overreliance: humans trust fluent output; require evidence and uncertainty handling.
- Model theft/extraction becomes practical without auth, throttles, and monitoring.
- The Top 10 is most useful when mapped into testable requirements and CI gates.

## “Not what you’ve signed up for” (Indirect Prompt Injection)

- Retrieved content is attacker-controlled input once you fetch from untrusted sources.
- “Data vs instruction” is not reliably separable by an LLM without additional structure.
- Indirect injection scales: a single poisoned document can affect many queries.
- Attacks can target policy override, tool misuse, or data exfil.
- RAG pipelines widen the attack surface vs. pure chat.
- Defensive prompting alone is fragile; you need gates and transformations.
- Provenance and trust scoring become first-class security features.
- Sanitization is imperfect; prefer reducing authority of retrieved text.
- Robustness requires regression tests for known injection patterns.
- Security posture must assume retrieval corpora can be poisoned.

## Automated / universal prompt injection attacks (modern)

- Attack optimization can discover prompts that reliably bypass common guardrails.
- “Universal” strings can transfer across prompts and sometimes across models.
- Defenses must be evaluated against adaptive attackers, not static examples.
- Multiple objective functions exist: jailbreak, tool call, exfil, refusal bypass.
- Attack success should be measured by task-level outcomes, not just “unsafe words”.
- Randomization and diversity in eval prompts reduce overfitting to a fixed set.
- Gating tool execution limits blast radius even when the model is fooled.
- Logging and telemetry are needed to detect novel attack families.
- Model upgrades can regress security; continuously re-baseline.
- The assurance loop (red team → fix → regression) is the only durable pattern.

## Secure RAG / RAG poisoning (modern)

- Poisoning can occur at ingestion (docs), indexing, or query-time injection.
- RAG trust must be earned: provenance, freshness, author, signing, review status.
- Ranking is a security control: you can down-rank low-trust sources.
- “Safe transform” patterns (summarize, extract facts, normalize) reduce instruction carryover.
- Separating retrieval from reasoning (and limiting what is injected) helps.
- Use allowlists and parsers for structured data; avoid raw HTML injection.
- Monitor for “instructional” language inside retrieved content.
- Store corpus metadata and enforce it at retrieval time.
- Keep a quarantine lane for new/unknown docs until reviewed.
- Treat poisoning tests like unit tests; fixes add regressions.

## Survey (security/privacy/ethics threats in LLM apps)

- Most real failures are **system failures** (interfaces, tools, data), not “model evilness”.
- Threats cluster into: injection, leakage, agency/tooling, supply chain, misuse/abuse.
- Evaluation is immature; you must build your own metrics and harnesses.
- Safety and security overlap but are not the same; map both.
- Privacy risks include logging, telemetry, and RAG corpora, not just model training.
- Operational controls (auth, rate limits, monitoring) matter as much as prompts.
- “Human in the loop” is not a control unless it is measurable and enforced.
- Defense-in-depth beats single-guardrail designs.
- Residual risk should be documented with explicit acceptance.
- Continuous improvement loops separate serious teams from demos.

