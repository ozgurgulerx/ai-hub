# Agent Framework Orchestration Playbook

Concise reference distilled from the Agent Framework documentation inside `docu/agent-framework_.pdf`. It captures the core vocabulary you need before layering in orchestration patterns, then outlines the five built-in agent collaboration styles we will implement next.

## Table of Contents
- [Core Concepts](#core-concepts)
- [Orchestration Overview](#orchestration-overview)
- Pattern blueprints (each links to the folder where the runnable samples will live):
  - [Concurrent Orchestration](./orchestrations/concurrent/) — see [details](#concurrent-orchestration)
  - [Sequential Orchestration](./orchestrations/sequential/) — see [details](#sequential-orchestration)
  - [Group Chat Orchestration](./orchestrations/group-chat/) — see [details](#group-chat-orchestration)
  - [Handoff Orchestration](./orchestrations/handoff/) — see [details](#handoff-orchestration)
  - [Magentic Orchestration](./orchestrations/magentic/) — see [details](#magentic-orchestration)

## Core Concepts

### Building blocks
- **Executors** are typed processing units (`IMessageHandler<TIn[, TOut]>`, typically created by inheriting `ReflectingExecutor`). They can return values or push messages via `context.SendMessageAsync`.
- **Edges** wire executors together, enforcing message type compatibility while enabling conditional routing and fan-out.
- **Workflows** are directed graphs made of executors and edges. They run locally via `InProcessExecution` or in hosted schedulers, keeping per-run state and telemetry.
- **Events** (`WorkflowStartedEvent`, `ExecutorCompleteEvent`, `WorkflowCompletedEvent`, etc.) surface everything that happens, which is vital when debugging multi-agent flows.

### Execution model & observability
- Workflows use a Pregel-style superstep loop: collect pending messages, route by type/conditions, execute matching executors concurrently, emit events, repeat.
- Superstep isolation plus runtime type validation keeps orchestration deterministic and replayable—critical when durable schedulers (like Azure Durable Task Scheduler) rehydrate history.
- Event streams are uniform regardless of whether you subscribe locally or via observability tooling, which lets you trace how agents collaborate turn by turn.

### Durability & integration features
- **Checkpointing:** snapshots happen at the end of each superstep, capturing executor state, queued messages, requests, and shared state. Runs can resume in-place or be rehydrated elsewhere.
- **Requests & responses:** `InputPort` enables executors to pause for external approvals or services. Pending requests survive checkpoints and replay as `RequestInfoEvent`.
- **Shared state & context providers:** executors can persist shared artifacts (e.g., cached files, routing hints) outside the strict message flow.

### Why this matters for orchestrations
- Orchestrations are composed by plugging AI agents in as executors. Agents receive buffered messages until a `TurnToken` arrives, then stream output via `AgentRunUpdateEvent`.
- Because workflows are typed graphs with deterministic replay, every orchestration pattern—parallel, sequential, conversational, or dynamic—benefits from the same durability, routing, and observability guarantees.

## Orchestration Overview

Multi-agent orchestration coordinates multiple AI agents (or agents plus classical executors) so that complex tasks stay deterministic, inspectable, and fault-tolerant.

- **Agents as executors:** `ChatClientAgent` instances drop directly into the workflow graph and inherit all workflow behaviors (turn-taking, checkpointing, streaming).
- **Pattern builders:** `AgentWorkflowBuilder` exposes helpers like `BuildConcurrent`, `BuildSequential`, `CreateGroupChatBuilderWith`, and `StartHandoffWith`, which emit fully formed graphs with minimal boilerplate.
- **Durable hosting:** When deployed with Azure Durable Functions or the Durable Task Scheduler, orchestrations gain out-of-the-box HTTP control plane APIs, dashboards, and the ability to wait for human input or external events for days without losing state.

The remainder of this file focuses on five orchestration patterns referenced throughout the documentation. Each pattern summary below includes a compact example that we can later translate into runnable code inside the folders listed in the table of contents.

## Concurrent Orchestration

Concurrent orchestration fans out the same prompt to several specialists, runs them simultaneously, and aggregates their responses. Use it when you want diverse perspectives, ensembles, or quick voting.

**Key traits**
- `AgentWorkflowBuilder.BuildConcurrent(...)` links every agent to the same input source and automatically aggregates their outputs.
- Executors run in the same superstep, so slow agents do not block fast ones; the workflow finishes when every branch reports back or a timeout fires.
- Aggregation output is typically a list of `ChatMessage` objects you can post-process (e.g., deduplicate or rank).

**Example: Instant Polyglot Reviewer**

| Agent | Instruction (trimmed) |
| --- | --- |
| `EnglishReviewer` | “Detect the source language, critique the writing, respond in English.” |
| `FrenchReviewer` | “Detect the source language, translate to French, keep the tone.” |
| `SpanishReviewer` | “Detect the source language, translate to Spanish, keep the tone.” |

Execution sketch:
1. Worker submits `User: "Draft: Hello, world!"` plus a `TurnToken`.
2. All three reviewers run concurrently, emitting `AgentRunUpdateEvent` chunks so telemetry shows progress in parallel.
3. `WorkflowCompletedEvent` carries an aggregated list: original user message followed by each reviewer’s answer.
4. A coordinator function can pick the highest-confidence translation or merge them into a final payload.

This example mirrors the documentation’s translation ensemble while keeping the agents extremely simple—each is a single-instruction translation reviewer.

## Sequential Orchestration

Sequential orchestration chains agents so the output of one becomes the input of the next. Ideal for multi-stage reasoning, policy review, or pipelines where every step enriches the artifact.

**Key traits**
- `AgentWorkflowBuilder.BuildSequential(...)` builds the pipeline; agents execute in deterministic order across supersteps.
- The workflow preserves complete conversation history so downstream agents see both the original user input and upstream agent rationale.
- Paired with checkpoints, you can resume mid-pipeline without rerunning earlier steps.

**Example: Safety → Localization Pipeline**

| Stage | Agent | Responsibility |
| --- | --- | --- |
| 1 | `SafetyReviewer` | Flag or soften unsafe wording. Returns updated prompt and a status note. |
| 2 | `LegalReviewer` | Ensure claims comply with policy; append compliance tags. |
| 3 | `LocalizationBot` | Translate to the target locale named in metadata. |

Execution sketch:
1. User submits launch copy plus metadata: `targetLocale = "es-ES"`.
2. `SafetyReviewer` rewrites risky text and forwards both the fixed copy and notes.
3. `LegalReviewer` augments the notes (e.g., “claims appear factual”) and hands off to `LocalizationBot`.
4. Final output is a tidy bundle: sanitized copy, localized translation, and an audit trail from each stage.

This keeps the agents straightforward—each one is narrowly scoped, yet the chain demonstrates how sequential workflows pass evolving context downstream.

## Group Chat Orchestration

Group chat orchestration simulates a panel of agents talking to each other under the supervision of a manager. Think iterative brainstorming or critique sessions where agents need to see the whole conversation.

**Key traits**
- `AgentWorkflowBuilder.CreateGroupChatBuilderWith(...)` accepts a manager factory. Built-in managers like `RoundRobinGroupChatManager` rotate speakers, enforce `MaximumIterationCount`, and decide when to stop.
- Every participant gets the full shared history, so suggestions, critiques, and approvals are transparent.
- Custom managers can enforce additional termination logic (e.g., stop when the reviewer says “approved”).

**Example: Copywriter + Reviewer Loop**

| Participant | Instruction |
| --- | --- |
| `CopyWriter` | “Produce concise product slogans, one per turn.” |
| `Reviewer` | “Critique slogans for clarity, suggest edits, approve when satisfied.” |

Execution sketch:
1. Workflow manager seeds the conversation with the user brief.
2. CopyWriter proposes a slogan; Reviewer provides feedback.
3. Manager alternates agents for up to five iterations *or* stops early when Reviewer says “Approved.”
4. Final transcript (user brief + agent turns) is emitted via `WorkflowOutputEvent`, ready for downstream storage.

The example reflects the documentation flow: tight instructions, round-robin moderation, and a clean finish when the reviewer approves.

## Handoff Orchestration

Handoff orchestration lets agents explicitly transfer control to one another without a central manager. It shines in triage scenarios where a router chooses the right specialist, and specialists can return control once done.

**Key traits**
- `AgentWorkflowBuilder.StartHandoffWith(router)` picks the opening agent, and `.WithHandoff(...)` / `.WithHandoffs(...)` configure which agents are allowed to pass control to whom.
- When an agent hands off, the receiving agent inherits the full conversation history, so no context is lost.
- Because there is no supervising manager, the agents themselves are responsible for deciding when to end.

**Example: Homework Triage Desk**

| Agent | Purpose |
| --- | --- |
| `triage_agent` | Identify subject (math vs history) and immediately hand off. |
| `math_tutor` | Solve math questions, then hand control back to triage. |
| `history_tutor` | Answer history questions, then return to triage. |

Execution sketch:
1. Student asks, “What is the derivative of x^2?” → triage logs context and hands off to `math_tutor`.
2. `math_tutor` replies with derivative steps and returns control to triage.
3. Student’s follow-up, “Remind me what triggered World War II,” is routed to `history_tutor`.
4. Conversation continues indefinitely with triage orchestrating handoffs, and every turn is checkpointed so the workflow can resume mid-dialog if needed.

This mirrors the documentation sample and keeps agents extremely focused on their domain knowledge while demonstrating dynamic control transfer.

## Magentic Orchestration

Magentic orchestration is inspired by Magentic-One. A Magentic manager dynamically decides which specialist should act next, adapting as the task evolves. Perfect for open-ended missions where the solution path is unknown.

**Key traits**
- The manager maintains shared context, progress state, and callbacks for streaming updates or human-in-the-loop approvals.
- Agents register their capabilities (research, planning, execution, QA). The manager picks the next actor based on unmet goals, confidence, or tool availability.
- Because orchestration is deliberately dynamic, it benefits heavily from the workflow system’s deterministic replay and checkpointing.

**Example: Research → Build → Test Sprint**

| Agent | Capability |
| --- | --- |
| `Researcher` | Gather requirements, cite sources. |
| `Planner` | Break work into actionable tasks, request approvals if necessary. |
| `Builder` | Generate artifacts (code/doc) based on the current plan. |
| `QA` | Validate outputs, raise follow-up tasks. |

Execution sketch:
1. Magentic manager receives a vague brief (“Draft a launch FAQ for our new API”).
2. `Researcher` is scheduled first to collect product facts; manager appends findings to shared context.
3. Manager routes to `Planner`, who produces a checklist and asks for human approval via `InputPort`. Once approved, the manager resumes automatically.
4. `Builder` and `QA` alternate until QA signals confidence ≥ threshold; manager emits the consolidated FAQ as workflow output.

Even though the official documentation’s Magentic section calls out that tutorials are “coming soon,” this pattern summary keeps our example simple while highlighting the orchestration hallmarks: adaptive scheduling, shared context, and optional human checkpoints.

---

Use this playbook as the narrative layer for the runnable samples that will live under `./orchestrations/*/`. Each section is written so you can lift the scenario directly into agent instructions and workflow builder code without re-reading the full PDF.
