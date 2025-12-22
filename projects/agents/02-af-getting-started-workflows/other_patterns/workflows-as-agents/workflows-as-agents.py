import asyncio
from textwrap import shorten
from typing import List

from agent_framework import ChatMessage, WorkflowBuilder, executor, WorkflowContext


@executor(id="normalize")
async def normalize_text(message: str | List[ChatMessage], ctx: WorkflowContext) -> None:
    """Trim whitespace and compact the text before analysis."""

    if isinstance(message, list):
        # When invoked as an agent, the workflow receives a conversation history.
        latest = message[-1].text if message else ""
    else:
        latest = message

    cleaned = " ".join(latest.strip().split())
    await ctx.send_message(cleaned)


@executor(id="keyword-extractor")
async def extract_keywords(text: str, ctx: WorkflowContext) -> None:
    """Extract simple keywords and forward the enriched payload."""

    tokens = {token.strip(".,!?").lower() for token in text.split() if len(token) > 3}
    summary = {
        "original": text,
        "keywords": sorted(tokens),
    }
    await ctx.send_message(summary)


@executor(id="final-writer")
async def build_report(payload: dict, ctx: WorkflowContext) -> None:
    """Convert the structured payload into a short report and return the final output."""

    original: str = payload["original"]
    keywords: list[str] = payload["keywords"]
    excerpt = shorten(original, width=80, placeholder="...")
    report = (
        f"Excerpt: {excerpt}\n"
        f"Top keywords: {', '.join(keywords) if keywords else 'n/a'}"
    )
    await ctx.yield_output(report)


async def run_workflow_agent(prompt: str) -> None:
    """Wrap the workflow as an agent and interact with it like any other agent."""

    workflow = (
        WorkflowBuilder()
        .add_edge(normalize_text, extract_keywords)
        .add_edge(extract_keywords, build_report)
        .set_start_executor(normalize_text)
        .build()
    )

    workflow_agent = workflow.as_agent(name="Content Analysis Workflow")
    thread = workflow_agent.get_new_thread()

    print("=== Workflow acting as an agent ===")
    result = await workflow_agent.run(prompt, thread=thread)
    print(result.text)


if __name__ == "__main__":
    asyncio.run(
        run_workflow_agent(
            "Draft a short overview of the Wingrave build pipeline and highlight the main goals."
        )
    )
