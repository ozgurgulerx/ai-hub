# AI Coding

Best practices, checklists, and patterns for using AI assistants to **write, review, and maintain code** in real projects.

## What This Should Cover

- **Problem framing**: requirements, acceptance criteria, and “what good looks like”.
- **Repo navigation**: how to quickly locate the right files, owners, and constraints.
- **Change strategy**: smallest safe change, root-cause fixes, and avoiding scope creep.
- **Prompting patterns**: constraints, examples, invariants, and progressive disclosure.
- **Verification**: tests to run, minimal repros, and regression guardrails.
- **Code review**: diff hygiene, risk assessment, and readability.
- **Security**: secrets hygiene, supply-chain risk, and safe tool use.
- **Operational safety**: kill switches, feature flags, rollout/rollback basics.
- **Documentation**: when to update READMEs, runbooks, and usage notes.

## Suggested Structure (Planned)

- `checklists/` — practical “do this before merging” lists
- `patterns/` — reusable prompting + workflow patterns
- `examples/` — small before/after examples and playbooks
- `notes/` — links and summaries of learnings

## Related Notes (In This Repo)

- Context engineering for big codebases (“No vibes allowed”): `../retrieval-augmented-systems/notes/context-engineering-no-vibes-allowed.md`
- GPT‑5 coding/agent notes (Build Hour; Noiz summary, to verify): `../model-space/reasoning-models/gpt-5/README.md`
- Automating discovery (novel insight limits; Jakub Pachocki; Noiz summary, to verify): `../model-space/reasoning-models/notes/automating-discovery-jakub-pachocki-noiz-summary.md`
- Retrieval for autonomous coding agents (why “RAG for code” can backfire; Noiz summary, to verify): `notes/retrieval-for-autonomous-coding-agents-cline-noiz-summary.md`
- Cursor 2.0 first impressions (Eric Zakariasson; Noiz summary, to verify): `notes/cursor-2-0-first-impressions-eric-zakariasson-noiz-summary.md`
- Building Cursor Composer (Ray Summit 2025 keynote; Noiz summary, to verify): `notes/building-cursor-composer-ray-summit-2025-sasha-rush-noiz-summary.md`
- AIE CODE 2025 AI leadership (agents, evals, ROI, risk; Noiz summary, to verify): `notes/aie-code-2025-ai-leadership-noiz-summary.md`
- Claude Code playbook (Cloud.md, MCP, GitHub workflows; Noiz summary, to verify): `notes/claude-code-playbook-cloud-md-mcp-noiz-summary.md`
- Claude Code (beginner→expert in 19 minutes; Noiz summary, to verify): `notes/claude-code-beginner-to-expert-19-min-noiz-summary.md`
