# When Knowledge Graphs Fail, It’s Not the Ontology — It’s the Epistemology

This note distills a practical point for enterprise knowledge graphs and ontology-based governance:

- **Facts**, **inferences**, and **unknowns** are different things.
- **Reasoning** (OWL / Open World Assumption) does not “fill in” unknowns.
- **Validation** (SHACL / Closed World Assumption) checks whether information is sufficient for a constraint/compliance need.

When teams treat these as interchangeable, they end up expecting reasoning to fix data quality, or interpreting validation failures as “false facts”.

## Key Distinction 1: Facts vs. Inferences vs. Unknowns

- **Facts**: what is explicitly stated/known in the graph.
- **Inferences**: what can be logically deduced from existing facts.
- **Unknowns**: what is not present in the system.

Important implication: **OWL never converts unknowns into facts**. Inference exposes implications of the knowledge you already have; it does not acquire missing information.

## Key Distinction 2: Data vs. Information vs. Knowledge

These are often used as synonyms in business conversations, but separating them clarifies system behavior:

- **Data**: raw symbols without context.
- **Information**: data organized and contextualized.
- **Knowledge**: structured information usable for deduction/decision-making.

A helpful framing:

- **Inference** happens in the “knowledge” layer (deriving implications).
- **Validation** happens in the “information” layer (checking constraint readiness/completeness).
- **Acquisition** expands what you have (data/information boundary); it is not produced by reasoning.

## What OWL and SHACL Do (And Don’t)

- **OWL** (Open World Assumption / OWA): “what is not stated is **unknown**, not false.” OWL is used to infer what follows logically from the current knowledge base.
- **SHACL** (Closed World Assumption / CWA for validation): “if required information is not present, the constraint **fails**.” SHACL is used to validate whether current information meets required shapes/constraints.

They do not contradict reality; they operate on different needs:

- OWL answers: “What follows logically from what we know?”
- SHACL answers: “Do we have enough information to satisfy a requirement?”

## Why This Matters in Real Systems

If you don’t keep these categories explicit, teams often end up expecting:

- reasoning to fix incomplete data
- validation to contradict reasoning
- ontologies to behave like data quality rules
- SHACL violations to mean “false facts”
- inference to replace acquisition processes

## A Practical Mental Model (Hybrid OWL + SHACL)

Instead of “reason first, validate later”, treat it as a lifecycle:

1) Acquire data → becomes information
2) Contextualize information → becomes knowledge
3) Infer implications → enrich knowledge
4) Validate completeness/readiness → ensure constraints for action are met

Core takeaway: **completeness is not produced by reasoning**. It must be declared and governed.

Engineering hotspots the model surfaces:

- provenance
- trust
- context binding
- scopes of completeness
- lifecycle of knowledge objects

## Appendix: Glossary (Distilled)

- **Knowledge Graph (KG)**: structured representation of things and their relationships.
- **Ontology**: the schema/dictionary defining types, properties, and allowed relationships.
- **Epistemology**: clarity about what is known, inferred, or unknown—and how the system treats each.
- **OWL**: ontology language enabling logical inference under OWA.
- **SHACL**: constraint language used to validate shapes/completeness under a closed-world validation lens.
- **OWA**: “not stated” ≠ false; it’s unknown.
- **CWA (for validation)**: “not stated” means the required statement is absent (constraint failure in that context).

## Appendix: Raw Notes (Preserved)

- “OWL tells us what follows logically from our current knowledge. SHACL tells us whether our current information is sufficient for a constraint.”
- “OWL never converts unknowns into facts. Inference exposes implications, not missing data.”
- “Completeness is not produced by reasoning — it must be declared or governed.”
