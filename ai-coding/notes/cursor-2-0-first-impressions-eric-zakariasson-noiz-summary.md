# Cursor 2.0 First Impressions (Eric Zakariasson) — Notes

Summary for: https://youtu.be/bFILlpq7qdA  
Generated from transcript tooling (Noiz): https://noiz.io/tools/youtube-video-transcript  
Status: **To verify** (treat as a starting point; confirm details from the talk/product docs).

## Semantic Search & Infrastructure

- Cursor’s semantic search uses **search feedback** to improve code retrieval quality in large codebases.
- Practical infra challenges include **indexing pipelines**, **code chunking**, **encryption**, **security**, and **permissions** at scale.

## Code Review & Bug Detection

- Cursor’s “Bugbot” is described as a code review agent aiming to find real bugs with **few false positives** for high-velocity teams.
- Cursor’s debug mode can:
  - insert console logs at key runtime context points,
  - collect logs when issues are reproduced,
  - analyze logs to identify problems (example claim: finding memory leaks during internal experimentation).
- Code review UX direction:
  - call out important changes,
  - unify related frontend + backend PRs for review,
  - address large PR review (thousands of LOC).

## Workflow Evolution & Agent Architecture

- Fast models enable synchronous, iterative work (smaller prompts/changes).
- Slower models are better suited for asynchronous background agents handling complex tasks.
- Cursor is described as developing **subagents** (plan mode) that can parallelize work by creating separate agents based on change scope.
- Plans referencing old plans as examples (reusable “plan snippets”) is described as evolving into a “product” collection to improve multi-plan workflows.

## Developer Experience & Context Management

- A built-in browser helps developers stay in flow and encourages structured planning/best practices.
- Workflows evolve from copy/paste chat loops to integrated, agentic environments enabling more complex asynchronous tasks.

## Attribution & Intent Tracking

- Git blame can be insufficient for agent coding because it records only a primary author.
- Proposed improvement: track which agent generated which lines and the prompts used.
- Capture **user intent** beyond diffs by annotating changes with the prompting context that led to the code.

## Multi-Agent Collaboration

- Use multiple AI agents/models to generate solutions, compare outputs, and cherry-pick the best parts into a final implementation.

## Automation & Integration

- Example automation pattern: Slack → create Linear tickets for stale feature flags → assign to creators → automatically merge related PRs.

## Practical “Try This” Ideas

- Add a lightweight “why this changed” field to PR descriptions (prompt/intent summary) for agent-authored diffs.
- Define a PR size policy + “review bundle” pattern for linked frontend/backend changes.
- Treat code search/indexing as production infra: access controls, encryption, and per-repo permissioning.
