# Orchestration Samples

Each subfolder contains a Python sample that mirrors the orchestration patterns described in the Agent Framework documentation under `docu/agent-framework_.pdf`.

| Pattern | Entry point | What it demonstrates |
| --- | --- | --- |
| Concurrent | `python orchestrations/01-concurrent/concurrent_workflow_sample.py` | Mirrors the official concurrent agent fan-out/fan-in sample using `ConcurrentBuilder`. |
| Group Chat | `python orchestrations/02-group-chat/sample.py` | Prompt-based manager coordinating a researcher and writer via `GroupChatBuilder`. |
| Handoff | `python orchestrations/03-handoff/sample.py` | `HandoffBuilder` routing: triage agent delegates to math vs history tutors with scripted replies. |
| Magentic | `python orchestrations/04-magentic/sample.py` | `MagenticBuilder` with streaming callbacks, modeled after the official Magentic sample. |
| Sequential | `python orchestrations/05-sequential/sample.py` | Writer → reviewer pipeline using `SequentialBuilder` and shared conversation context. |

All samples rely on environment variables for Azure OpenAI (preferred) or fall back to OpenAI. Configure `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`, and `AZURE_OPENAI_DEPLOYMENT_NAME`, or set `OPENAI_API_KEY` / `OPENAI_MODEL`.
