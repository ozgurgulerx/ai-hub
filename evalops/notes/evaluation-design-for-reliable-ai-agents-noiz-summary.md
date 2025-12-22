# Evaluation Design for Reliable AI Agents — Notes

Summary for: https://youtu.be/-T6uZYYzkWw  
Generated from subtitles tooling (Noiz): https://noiz.io/tools/youtube-subtitles  
Status: **To verify**

## Eval Design Philosophy (Outcome-First)

- Reverse engineer evaluations from product experience and business outcomes, not abstract metrics.
- Example framing: for customer support bots, track escalation rates rather than only “factuality” (a grounded-but-wrong answer still fails users).

## Build Evals Early + Iterate

- Define evaluations early and refine continuously through failure analysis.
- Use failure analysis to distinguish between “bad tests” and “bad solutions” and drive iteration.

## LLM-Assisted Eval Generation (As Described)

- Use LLMs to generate diverse question variations with persona context while keeping expected answers consistent.
- Create detailed correctness criteria that can be evaluated by LLMs (and validated) to enable confident experimentation.

## Solution-Specific Testing Strategies (Examples)

- Use mock databases for text-to-SQL/graph query systems.
- Use simple match tests for classifiers.
- Include guardrail scenarios: questions that should not be answered, need different handling, or have no answer in materials.

## Goal: Reliability Through Coverage

- Turn POCs into production-ready systems by iteratively adding tests and using evals as the reliability foundation.

