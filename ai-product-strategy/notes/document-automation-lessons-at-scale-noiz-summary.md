# Startups → F500: Document Automation Lessons at Scale — Noiz Summary Notes

Source video (YouTube): `https://youtu.be/TwdiUu93DPw`

This note distills claims from a **Noiz** YouTube transcript/summary provided in the prompt. Treat all numbers, case studies, and prescriptions as **to verify** until corroborated by primary sources (talk recording, docs, or a reproducible implementation).

## Core claim (as described)

Document automation at enterprise scale is mostly a **process + evaluation** problem, not just a model problem: organizations have tacit knowledge, unstructured handoffs, and long-tail document variability that must be made explicit through domain expertise, pipelines, and rigorous evals.

## Process understanding and tacit knowledge (claims)

- Organizations are described as harboring “hidden” tacit knowledge in engineering, operations, and domain experts, which makes automation hard unless you understand the full end-to-end process and the unstructured data flowing between parties.

### “Bulk ingest to see reality”

- One company is described as doing a single bulk ingest of **150k–200k documents** (~**1M pages**) to:
  - represent historical data accurately
  - detect blind spots (e.g., supplier-specific issues, pricing terms not extracted correctly)

## Incremental automation strategy (claims)

### “Automate when possible, augment otherwise”

- Start with human-in-the-loop (HITL) systems and gradually increase automation, rather than aiming for “full automation day one”.
- This framing is described as avoiding unrealistic:
  - accuracy expectations
  - change-management burdens

### Optimize “true automation rate”, not isolated accuracy

- Focus is described as achieving a high **true automation rate** where:
  - the end-to-end pipeline completes reliably, and
  - inaccuracies are caught (not silently shipped)
- This is framed as more meaningful than arbitrary extraction accuracy metrics evaluated in isolation.

## Evaluation and domain expertise (claims)

### Domain experts are a first-class dependency

- Healthcare teams are described as using in-house nurses/medical technicians to build fine-grained evaluation sets across wide doc varieties.
- Domain expertise is described as needed to encode jargon/variability into extraction schemas and prompting rules.
- AI teams are encouraged to empower product/ops teams to customize automation rather than centralizing all changes and blocking iteration.

### Task-specific evals beat generic benchmarks

- Invest early in task-specific evaluations tailored to your domain/data/process.
- “Generic landscape benchmarking” is described as insufficient for end-to-end automation outcomes.

### Ontology-driven understanding of variability

- Build an ontology with domain experts to map:
  - document types
  - terminologies
  - variability patterns (example domain: healthcare referrals)
- Goal: a shared representation of the space of documents you’ll encounter so automation can be designed intentionally.

Related (ontology / governance framing): `../../ai-security-and-governance/docs/ai-governance/README.md`

## Process redesign (claims)

- Rethink the end-to-end process around automation rather than attempting a 1:1 replacement of manual steps.
- Consider data cleaning and filtration before generative extraction; operational redesign can create more value than “automating the current mess”.

## Technical implementation pattern (claims)

### Multi-step doc pipeline

- Break processing into steps such as:
  - parsing
  - classification
  - splitting
  - extraction
- Control inputs via configuration workflows for:
  - different providers
  - recurring edge cases

### Hybrid extraction stack (layout/OCR/VLM)

- Use a multi-step approach combining:
  - layout analysis
  - OCR for text extraction
  - VLMs for figures/tables
- The claim is that relying solely on OCR or solely on VLMs is typically insufficient for accurate representation.

Related (document-heavy RAG ingestion patterns): `../../retrieval-augmented-systems/notes/better-rag-through-better-data-reducto-noiz-summary.md`

## Prioritization and ROI (claims)

- Prioritize automating the most impactful + feasible use cases first to deliver value and reduce friction.
- Tackle harder cases as automation matures, keeping ROI measurable.

## Practical checklist (distilled)

- Map the end-to-end process (including tacit knowledge and unstructured handoffs).
- Start HITL; measure “true automation rate” end-to-end (including catch mechanisms).
- Invest early in domain-specific evals and schema design with domain experts.
- Build an ontology of doc types/terms/variability for the domain.
- Use a multi-step pipeline (parse → classify → split → extract) with per-provider configs.
- Redesign the process around automation (clean/filter before extract).
- Prioritize high-ROI use cases first; expand coverage iteratively.

## Appendix: Raw Notes (Preserved)

- “Organizations harbor hidden tacit knowledge…”
- “Ingested 150,000–200,000 documents (~1M pages) in a bulk ingest…”
- “Start with automate when possible, augment otherwise…”
- “Focus on high true automation rate…”
- “Use in-house nurses/medical technicians to build evaluation sets…”
- “Build an ontology with domain experts…”
