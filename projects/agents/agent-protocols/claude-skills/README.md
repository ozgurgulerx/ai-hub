# Claude Skills (Anthropic)

Claude “Skills” are a **packaging and execution pattern** for giving Claude reusable, scoped capabilities: a bundle of instructions (behavior), optional code, and optional resources/templates. Skills are designed to be **loaded only when needed** (progressive disclosure) to reduce prompt/context bloat.

This folder tracks notes from the “Claude Skills Cookbook” and how Skills compare to MCP.

## What Skills Are (Conceptual Model)

- **A capability bundle**: playbook-like instructions + optional scripts + optional resources (templates, sample data).
- **On-demand loading**: a run can enable only the needed skills (instead of pasting long instructions every time).
- **Execution surface**: often paired with provider features like code execution and file generation/download.

## How Skills Differ From MCP (And Why It’s Not 1:1)

Skills and MCP can both “make an agent do things”, but they solve different layers:

- **Scope**
  - **Skills**: provider-native capability bundles inside the Claude platform/runtime.
  - **MCP**: an open-ish client↔server protocol for connecting a host app/agent to external tools/resources.
- **Portability**
  - **Skills**: typically Claude-specific (and tied to specific API features/headers).
  - **MCP**: model/provider-agnostic in principle; swap models while keeping tool servers.
- **Integration boundary**
  - **Skills**: you bring logic/resources into the “Claude execution environment”.
  - **MCP**: you keep logic in separate MCP servers you run/own, and expose capabilities over the protocol.
- **Operational model**
  - **Skills**: fastest path when you’re all-in on Claude + their files/code-exec primitives.
  - **MCP**: better when you need enterprise integrations (internal APIs/DBs), strict isolation, or multi-model support.

So the claim “Skills outperform MCP” only makes sense under specific criteria (e.g., time-to-ship document automation on Claude), not as a general statement about interoperability or security boundaries.

## “Outperforms” — What To Measure Instead

If you want to compare Skills vs MCP fairly, choose metrics:

- **Time-to-first-working-automation** (Excel/PPT/PDF generation; report workflows)
- **Context efficiency** (how much prompt/context overhead is required per run)
- **Tool reliability** (schema adherence, error recovery, determinism)
- **Security posture** (least privilege, sandboxing, auditability, supply-chain risk)
- **Portability** (can the same tool layer work across models/providers?)
- **Total cost & latency** (including tool round-trips and retries)

## When To Use Which

- Prefer **Claude Skills** when:
  - You’re building on Claude and want **packaged business workflows** (docs/spreadsheets/slides/PDFs).
  - You benefit from **progressive disclosure** and provider-managed execution primitives.
- Prefer **MCP** when:
  - You need **provider-agnostic** tools/context.
  - You need to integrate with **internal systems** (databases, ticketing, code repos) with tight controls.
  - You want MCP servers to be first-class deployable components with their own auth, logs, and SLAs.

## References (Add Links)

- Claude Skills Cookbook repo:
- Cookbook notebooks (intro, finance, custom skills):
- Provider docs for skills / files API / code execution:

## Related Notes (In This Repo)

- Building more effective agents (Claude Skills/SDK framing; Noiz summary, to verify): `../../notes/building-more-effective-ai-agents-claude-noiz-summary.md`
