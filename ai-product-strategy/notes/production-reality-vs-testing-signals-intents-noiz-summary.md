# Production Reality vs Testing (Signals, Intents, and Issue Discovery) — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/nKmPZVxfzY0`

Additional related video (YouTube): `https://youtu.be/s6qJXvFB5cM`

This note distills claims from **Noiz** YouTube transcripts/summaries provided in the prompt. Treat specifics, numbers, named tools/frameworks, and case studies as **to verify** until corroborated by primary sources (talk recordings, slides, docs, or an implementation write-up).

## Why offline evals break down in production (claims)

- Offline evaluations can fail because users interact with AI systems in unexpected ways, revealing new intents and frustrations you didn’t anticipate.
- Offline evals are framed as “unit tests”: useful for local iteration and CI/CD regression checks, but insufficient to catch the full range of production issues.
- A shift toward aggregate analysis of exceptions and emerging patterns is described (analogy: Sentry-like monitoring for AI apps), including a reference to “OpenAI’s postmortem” as motivation. (To verify which postmortem and details.)
- A real-world-style failure mode is described where a chatbot can make **legally binding promises** (e.g., refunds), creating direct liability. (Anecdote; to verify.)
- As agents gain longer contexts (days/weeks/months), memory systems, and tool access, the number of possible states grows so large that defining “expected outputs” for “inputs” becomes increasingly difficult.
- Production monitoring is described as harder because many failures are not explicit “errors”; you must infer breakage from signals in behavior and outcomes.

Design implication:
- “AI magic” must be engineered so that improvements are **repeatable, testable, and attributable** across model releases; this requires systematic experimentation, not hoping offline scores translate to production.
- “LLM judges” are described as a footgun: using them incorrectly can create false confidence if your definitions of “good/bad” are not grounded in real user behavior and production signals.

## Signals + intents: the core mental model (claims)

- Define **signals** as ground-truth indicators of app performance (e.g., error rates, user complaints, thumbs up/down, drop-offs, retries).
- Signals are described as both:
  - **explicit**: thumbs up/down, regen, error messages
  - **implicit**: frustration, task failure, abandonment, “forgetting” (memory misses)
- Issues emerge from combining:
  - **Signals** (explicit feedback and implicit behavioral indicators), and
  - **Intents** (what the user is trying to achieve turn-by-turn and across a whole conversation).
- When analyzing issues, count impact by **% of users affected** rather than raw event counts to avoid being misled by high-volume segments.

## Issue discovery at scale (“deep search”) (claims)

- “Deep search” is described as combining semantic search with LLM reranking to automate issue detection across millions of events per day.
- The approach is described as finding problems affecting a meaningful fraction of users (example figure mentioned: **8%**). (Quantitative claim; to verify.)

## Monitoring beyond latency/cost (claims)

Monitoring AI products is described as extending beyond infrastructure metrics to answer:

- Does the app actually perform well in production?
- Does prompt A outperform prompt B for real users?
- Which model performs better in real-world usage?

Tooling implication:
- Track **tool usage**, invocation frequency, and **tool error rates** because tools act as extensions of the prompt and strongly affect agent reliability.

## Iterative refinement loop (claims)

- Issue definitions should be refined continuously:
  - examine non-flagged events alongside flagged ones,
  - incorporate user feedback,
  - adjust definitions as you learn what “breakage” really looks like.
- Refinement is described as including collecting “hard positives/negatives” and edge cases so detection improves over time.

## The “Trellis” framing (bucketing an infinite output space) (claims)

- A framework called “Trellis” is described as organizing an AI app’s effectively infinite output space into **discrete buckets** so you can monitor, prioritize, and fix systematically.
- Buckets are described as being prioritized using company-specific metrics such as:
  - volume
  - negative sentiment / frustration
  - achievable improvement
  - strategic relevance
- The trellis is described as something you continuously refine as you learn more from production.

## From clusters → semi-deterministic workflows (claims)

- Start with a minimally viable agent (described as using vector search) guided by initial user/market knowledge.
- Cluster interactions by **intent** to learn what users actually value.
- Convert high-value clusters into **semi-deterministic workflows** with predefined steps (expressive but constrained), then iterate based on production signals.

## Issue investigation using metadata (claims)

- Investigation is described as leveraging metadata (examples named: browser, plan type, intent) and keywords to contextualize failures and segment patterns (e.g., frustration clustered around math vs pricing-plan/signup).

## Architecture and fixes beyond prompting (claims)

- Fixes are described as going beyond prompt edits by decomposing an app into independent “buckets” with sub-agents for specific tasks (a framework called “Trellis” is mentioned). (To verify; treat as a pattern, not a prescription.)
- Domain-specific data models are described as enabling LLMs to query company data through SQL-like queries tied to the company’s data model and access scope (moving beyond toy tools like `get_weather`).
- For AI companions, memory systems should explicitly track **what agents forget** (situational details vs user “friend” information) to surface user frustrations and guide improvements via concrete failure patterns.

## Resolution strategies (claims)

- Fixes are described as including:
  - prompt changes
  - offloading subtasks to specialized models or tools
  - fine-tuning using production-grounded signals (“ground truth” signals)
- Some claims reference open-source models benefiting from this loop. (To verify.)

## Practical checklist (derived from the claims)

- Define your **signal catalog** (explicit + implicit) and normalize by **% users impacted**.
- Model **intent** at turn-level and conversation-level; analyze failures along both axes.
- Add “deep search” over production events (semantic retrieval + reranking) to find clusters you wouldn’t pre-specify.
- Instrument and monitor tools like first-class product dependencies (invocations, errors, latency, fallbacks).
- Avoid judge-only eval confidence: validate “good/bad” definitions against user behavior and production outcomes.
- Treat offline evals as regression tests; rely on production clustering/triage for discovery.
- Treat fixes as design/architecture changes when prompting isn’t sufficient (decompose, reduce cross-talk, constrain scopes).

## Related (in this repo)

- Self-improving retrieval loops (behavior signals → backtests/simulations → shipping retrieval changes): `../../retrieval-augmented-systems/notes/self-improving-retrieval-algolia-noiz-summary.md`
- Production hallucinations are often data/context failures; track context relevance/usage (Noiz summary, to verify): `../../retrieval-augmented-systems/notes/production-hallucinations-context-metrics-noiz-summary.md`

## Appendix: Raw Notes (Preserved)

- “Offline evaluations fundamentally fail… users interact in unexpected ways…”
- “AI agents with longer contexts spanning days/weeks/months… impossibly high number of states…”
- “Define signals… cluster… count by percentage of users affected…”
- “Deep search combines semantic search with LLM reranking… identifying problems affecting 8% of users…”
- “Track tool usage… since tools function as extensions of the prompt…”
- “Frameworks like Trellis… decompose app functionality into independent buckets with sub-agents…”
- “Offline evals function like unit tests… but won’t catch all production issues…”
- “Production monitoring… implicit signals… explicit signals…”
- “Trellis… organize infinite output space into discrete buckets… prioritize by volume/negative sentiment/achievable improvement/strategic relevance…”
