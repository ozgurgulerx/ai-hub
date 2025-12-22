from __future__ import annotations

import asyncio
import logging

from agent_framework import WorkflowBuilder, executor, WorkflowContext, WorkflowOutputEvent
from agent_framework.observability import setup_observability
from typing_extensions import Never

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


@executor(id="ingest")
async def ingest(text: str, ctx: WorkflowContext[str]) -> None:
    await ctx.send_message(text.title())


@executor(id="summarize")
async def summarize(text: str, ctx: WorkflowContext[Never, str]) -> None:
    sentence = f"Summary: {text[:60]}{'...' if len(text) > 60 else ''}"
    await ctx.yield_output(sentence)


async def run_observable_workflow(text: str) -> None:
    setup_observability(
        service_name="observability-sample",
        enable_sensitive_data=False,
    )

    workflow = (
        WorkflowBuilder()
        .add_edge(ingest, summarize)
        .set_start_executor(ingest)
        .build()
    )

    async for event in workflow.run_stream(text):
        logging.info("Workflow event %s", event.__class__.__name__)
        if isinstance(event, WorkflowOutputEvent):
            print("\n=== Output ===")
            print(event.data)


if __name__ == "__main__":
    asyncio.run(
        run_observable_workflow(
            "observability spans describe workflow.build, workflow.run, and executor activity."
        )
    )
