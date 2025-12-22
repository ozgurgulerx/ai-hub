import asyncio
from pathlib import Path

from agent_framework import (
    Executor,
    FileCheckpointStorage,
    WorkflowBuilder,
    WorkflowContext,
    WorkflowOutputEvent,
    handler,
)
from typing_extensions import Never

try:
    from agent_framework import SuperStepCompletedEvent
except ImportError:  # Older versions may not expose this event
    SuperStepCompletedEvent = None  # type: ignore[assignment]

CHECKPOINT_DIR = Path(".af-checkpoints")


class ProcessingExecutor(Executor):
    def __init__(self) -> None:
        super().__init__(id="processor")

    @handler
    async def process(self, text: str, ctx: WorkflowContext) -> None:
        """Uppercase the text and persist local/shared state for checkpoint recovery."""

        await ctx.set_shared_state("latest_input", text)
        await ctx.send_message(text.upper())


class FinalizeExecutor(Executor):
    def __init__(self) -> None:
        super().__init__(id="finalize")

    @handler
    async def finalize(self, text: str, ctx: WorkflowContext) -> None:
        latest_input = await ctx.get_shared_state("latest_input")
        await ctx.yield_output(f"Original: {latest_input}\nProcessed: {text}")


def build_checkpointed_workflow(storage: FileCheckpointStorage):
    processor = ProcessingExecutor()
    finalizer = FinalizeExecutor()
    return (
        WorkflowBuilder()
        .add_edge(processor, finalizer)
        .set_start_executor(processor)
        .with_checkpointing(checkpoint_storage=storage)
        .build()
    )


async def run_with_checkpointing(text: str) -> None:
    storage = FileCheckpointStorage(storage_path=str(CHECKPOINT_DIR))
    workflow = build_checkpointed_workflow(storage)

    checkpoint_ids: list[str] = []
    async for event in workflow.run_stream(text):
        if SuperStepCompletedEvent and isinstance(event, SuperStepCompletedEvent):
            checkpoint = event.completion_info.checkpoint if event.completion_info else None
            if checkpoint:
                checkpoint_ids.append(checkpoint.checkpoint_id)
        elif isinstance(event, WorkflowOutputEvent):
            print("\n=== Final Output ===")
            print(event.data)

    if not checkpoint_ids:
        checkpoint_ids = await storage.list_checkpoint_ids()
        if not checkpoint_ids:
            print("No checkpoints captured.")
            return

    resume_id = checkpoint_ids[-1]
    print(f"\nResuming from checkpoint {resume_id} ...")
    if hasattr(workflow, "run_stream_from_checkpoint"):
        stream = workflow.run_stream_from_checkpoint(resume_id, checkpoint_storage=storage)  # type: ignore[attr-defined]
    else:
        stream = workflow.run_stream(checkpoint_id=resume_id)
    async for event in stream:
        if isinstance(event, WorkflowOutputEvent):
            print("\n=== Resumed Output ===")
            print(event.data)


if __name__ == "__main__":
    CHECKPOINT_DIR.mkdir(exist_ok=True)
    asyncio.run(run_with_checkpointing("Collect error budgets and summarize the trend."))
