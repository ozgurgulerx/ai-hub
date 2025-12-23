# Kill Switches (Operational Control for Automation)

In production, every automation path that can create meaningful load or external side effects should have a **kill switch**: a way to disable it quickly **without a code deploy**.

## What a Kill Switch Is

A kill switch is a fast operational control that turns off a feature/job/tool execution path when it:

- runs too often or consumes too many resources
- causes harmful side effects (e.g., destructive writes, spammy actions)
- is being misused (LLM jailbreaks / prompt-injection-driven actions)
- amplifies an outage (retry storms, thundering herds)

## Common Implementations

- **Feature flag**: check a flag at the top of the job/request path and return early when disabled.
  - Useful because toggling a flag is typically faster than deploying.
- **Feature-flag example (pseudo-code)**:
  - `return if feature_enabled?(pdf_converter_job_killswitch)`
- **Safety file**: automation runs only if a file exists; deleting the file stops it.
- **“Phone home” gate**: packaged automation must reach an external control API before it runs.

## When You’ll Use It

- **Bug containment**: stop a runaway automation that’s deleting data or producing bad writes.
- **Safety containment**: disable an LLM-powered feature quickly when outputs/actions go unsafe.
- **Outage recovery**: turn off high-volume, non-essential work to let core services recover.

## Why It’s Especially Important for LLM Features

LLM-driven features can have wide and hard-to-enumerate failure modes (prompt injection, jailbreaks, tool misuse). When something goes unsafe, the ability to disable the feature immediately is often the highest-leverage mitigation.

## Pair With Backoff + Jitter

A kill switch is the fastest stop, but good automation also avoids making outages worse:

- **Exponential backoff**: spread retries out over time (5s → 10s → 20s → …).
- **Jitter**: randomize retry delays so clients don’t retry in lockstep.

## “Going Down Fast, Coming Up Slow”

During outages, recovery is often harder than the initial failure because:

- users refresh broken pages
- jobs retry in loops
- queues attempt to drain simultaneously

Kill switches complement backoff/jitter by letting you disable **high-volume, low-importance** work so core dependencies (databases, queues) can recover.

## Keep It Working (The Real Failure Mode)

Kill switches are often broken when you need them most because they’re rarely exercised.

Practical guidance:

- Keep kill switch logic **simple** and close to the entry point (job trigger / request handler).
- Add a lightweight, regular check that the switch still works (e.g., a periodic test in a safe environment).
- Prefer switches that are **operable during incidents** (when deploys are risky/slow).

## Scope: Don’t Add It Everywhere

Not every code path should be kill-switchable. Some systems are essential and must stay on; they are the systems you disable other systems to protect.

Prioritize kill switches for:

- event-driven automation
- scheduled jobs
- high-volume user-triggered features
- tool/action execution paths in agents

## Appendix: Raw Notes (Preserved)

- “The most experienced and paranoid engineers I know build a killswitch into every single piece of automation.”
- “Enabling a feature flag is usually many minutes quicker than a code deploy… during an incident… it can be hours quicker.”
- A (non-linked) example is mentioned where a “killswitch not working” contributed to an incident and on-call responders shipped a fix during the incident.
- “The biggest problem with killswitches is that you don’t use them. Any code that isn’t regularly executed is a problem waiting to happen…”
