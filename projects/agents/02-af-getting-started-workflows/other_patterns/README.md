# Other Workflow Patterns

Support samples that highlight critical workflow capabilities beyond orchestration:

| Folder | Focus | Entry point |
| --- | --- | --- |
| `workflows-as-agents/` | Wrap a workflow as an Agent so it can be addressed like any other assistant. | `python other_patterns/workflows-as-agents/sample.py` |
| `shared-states/` | Demonstrates `ctx.set_shared_state` / `ctx.get_shared_state` for cross-executor data. | `python other_patterns/shared-states/sample.py` |
| `checkpoints/` | Shows how to enable checkpointing, capture checkpoint IDs, and resume later. | `python other_patterns/checkpoints/sample.py` |
| `observability/` | Enables OpenTelemetry via `setup_observability` and logs emitted workflow events. | `python other_patterns/observability/sample.py` |

Each script is intentionally minimal so you can see the core API surface for the concept before wiring in more complex agents or external systems.
