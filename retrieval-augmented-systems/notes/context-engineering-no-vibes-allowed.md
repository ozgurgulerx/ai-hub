# “No Vibes Allowed” — Context Engineering for Complex Codebases (Dex Horthy / HumanLayer)

Source video (YouTube): `https://youtu.be/rmvDxxNubIg`

This note distills claims from a **Noiz** YouTube summary provided in the prompt. Treat specifics (numbers, study details) as **to verify** until corroborated by primary sources.

## Core claim: context beats “vibes” on hard codebases

For complex, established codebases, reliable AI coding performance is framed as a **context engineering** problem more than a “pick the best model” problem:

- Keep context windows small and relevant.
- Reduce “searching the entire repo in-chat” by creating compact, structured context artifacts.

## Techniques (Distilled)

### 1) Frequent intentional compaction

Claim: repeatedly compress current working context into tagged markdown files, then start a fresh agent using those files as the new system context.

Purported benefits:

- Avoid repeated repo-wide searching.
- Sustain work across very large codebases (example claim: ~300k LOC Rust codebase).
- Preserve quality (claim: passes expert review).

### 2) The “dumb zone” (context saturation)

Claim: once the context window is “~40% full” with irrelevant information, performance degrades and steering within the same window has diminishing returns; starting a fresh window with compacted context is more effective.

### 3) RPI workflow (Research → Plan → Implement)

Claimed workflow to keep context tight:

- **Research**: understand the system, locate relevant files.
- **Plan**: compact intent + include specific code snippets so execution is high-confidence.
- **Implement**: execute with alignment on the plan (across humans/agents).

## Codebase-scale challenges (Claims)

- A Stanford study presented at “AI Engineer 2025” is cited as finding that AI coding agents struggle with complex legacy codebases, sometimes reducing productivity; a pattern mentioned is shipping “extra code” that reworks prior “slop”.

## Multi-agent pattern (Distilled)

Claim: use sub-agents primarily to **find files and snippets**, but have the parent agent read specific files directly (rather than delegating all reading/search to one agent). This is framed as improving both quality and context efficiency.

## On-demand compressed context (Distilled)

Claim: build “snapshot” research docs based on vertical slices of the codebase relevant to the feature being built, instead of relying on (possibly stale) documentation.

## Terminology warning (as framed)

“Semantic diffusion” is described as diluting terms like “agent” and “spec-driven development” into vague labels; the note emphasizes:

- **context engineering** (what goes into the window, when)
- **harness engineering** (integrating tools/workflows)

as the practical levers that make AI coding effective.

## Practical checklist (Derived from the claims)

- If the agent is flailing, **stop** and compact: write a short markdown “state” file (goal, constraints, files, snippets, next steps).
- Restart with only that compacted context + the minimal files needed.
- Use sub-agents for search; keep the parent responsible for reading and final diffs.
- Keep “plan” as a first-class artifact; don’t implement until the plan includes concrete file edits/snippets.

## Related (in this repo)

- Filesystem-backed context engineering patterns: `context-engineering-filesystem.md`
- AI-assisted development best practices (home): `../../ai-coding/README.md`

## Appendix: Raw Notes (Preserved)

- “Frequent intentional compaction… compressing existing context into markdown files…”
- “The ‘dumb zone’ occurs when context window exceeds 40% full with irrelevant information…”
- “Research, Plan, Implement (RPI) workflow…”
- “Stanford study presented at AI Engineer 2025…”
- “Sub-agents should find relevant files… parent agent reads specific files directly…”
- “Semantic diffusion… context engineering and harness engineering…”
