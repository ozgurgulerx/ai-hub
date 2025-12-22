import asyncio
from dataclasses import dataclass

from agent_framework import WorkflowBuilder, executor, WorkflowContext

STATE_KEY = "document_stats"


@dataclass
class DocumentStats:
    word_count: int
    average_length: float


@executor(id="stats_collector")
async def stats_collector(document: str, ctx: WorkflowContext) -> None:
    """Compute statistics once and store them in shared state."""

    tokens = [token.strip(".,!?") for token in document.split()]
    stats = DocumentStats(
        word_count=len(tokens),
        average_length=sum(len(token) for token in tokens) / max(len(tokens), 1),
    )
    await ctx.set_shared_state(STATE_KEY, stats)
    await ctx.send_message(document)


@executor(id="summary_generator")
async def summary_generator(document: str, ctx: WorkflowContext) -> None:
    """Generate a summary that references the shared stats."""

    stats: DocumentStats = await ctx.get_shared_state(STATE_KEY)
    summary = (
        f"Summary: {document[:60]}{'...' if len(document) > 60 else ''}\n"
        f"Words: {stats.word_count}"
    )
    await ctx.send_message(summary)


@executor(id="qa_reviewer")
async def qa_reviewer(summary: str, ctx: WorkflowContext) -> None:
    """QA reviewer reads the summary and accesses shared stats without recomputing."""

    stats: DocumentStats = await ctx.get_shared_state(STATE_KEY)
    verdict = (
        f"{summary}\nAverage token length verified: {stats.average_length:.2f}\n"
        "QA: Ready to publish."
    )
    await ctx.yield_output(verdict)


async def run_shared_state_example(text: str) -> None:
    workflow = (
        WorkflowBuilder()
        .add_edge(stats_collector, summary_generator)
        .add_edge(summary_generator, qa_reviewer)
        .set_start_executor(stats_collector)
        .build()
    )

    result = await workflow.run(text)
    outputs = result.get_outputs()
    if outputs:
        print(outputs[-1])


if __name__ == "__main__":
    asyncio.run(
        run_shared_state_example(
            "Design tokens allow product teams to share spacing, color, and typography primitives."
        )
    )
