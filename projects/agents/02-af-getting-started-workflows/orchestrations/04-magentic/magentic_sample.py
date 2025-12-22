from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

from agent_framework import (
    ChatAgent,
    HostedCodeInterpreterTool,
    MagenticAgentDeltaEvent,
    MagenticAgentMessageEvent,
    MagenticBuilder,
    MagenticFinalResultEvent,
    MagenticOrchestratorMessageEvent,
    WorkflowOutputEvent,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestrations.common import build_chat_client

logging.basicConfig(level=logging.INFO)


def create_specialists() -> dict[str, ChatAgent]:
    """Create a researcher, planner, builder, and QA reviewer for a full Magentic mission."""

    researcher = ChatAgent(
        name="ResearcherAgent",
        description="Collects facts and surfaces unknowns.",
        instructions=(
            "You are a field researcher building a competitive dossier. Gather updated city data, cite sources, "
            "and highlight unknowns that the planner should resolve."
        ),
        chat_client=build_chat_client(),
    )

    planner = ChatAgent(
        name="PlannerAgent",
        description="Breaks down launches into actionable workstreams.",
        instructions=(
            "You are a launch planner. Turn the latest research into a phase-by-phase plan with owners, timelines, "
            "and success metrics. Flag any gaps before handing off to the builder."
        ),
        chat_client=build_chat_client(),
    )

    builder_tools = HostedCodeInterpreterTool()
    builder = ChatAgent(
        name="BuilderAgent",
        description="Synthesizes answers using analysis tools.",
        instructions=(
            "You are a customer-success builder. Use the plan to create structured FAQs, budgets, and go-to-market "
            "assets. Run calculations or data cleanup with the hosted code interpreter when needed."
        ),
        chat_client=build_chat_client(prefer_responses=True),
        tools=builder_tools,
    )

    qa = ChatAgent(
        name="QAAgent",
        description="Launch QA reviewer",
        instructions=(
            "You are the QA reviewer. Inspect the builder's work, verify numbers, and request revisions until the "
            "deliverable is launch-ready. Approve with a short summary when satisfied."
        ),
        chat_client=build_chat_client(),
    )

    return {"researcher": researcher, "planner": planner, "builder": builder, "qa": qa}


async def main() -> None:
    participants = create_specialists()

    workflow = (
        MagenticBuilder()
        .participants(**participants)
        .with_standard_manager(
            chat_client=build_chat_client(),
            max_round_count=10,
            max_stall_count=3,
            max_reset_count=2,
        )
        .build()
    )

    task = (
        "You're designing a multi-city launch for our climate-monitoring platform. "
        "Research weather/smart-city programs in Austin, Singapore, and Berlin, "
        "build a phased rollout plan with budgets and partner requirements, "
        "generate customer-ready FAQ content, and have QA sign off. "
        "Highlight risks and escalation paths."
    )

    print("\nBuilding Magentic workflow...")
    print(f"TASK: {task}\n")

    last_stream_agent: str | None = None
    stream_open = False
    final_output: str | None = None

    async for event in workflow.run_stream(task):
        if isinstance(event, MagenticOrchestratorMessageEvent):
            print(f"\n[ORCH:{event.kind}]\n{event.message.text}\n{'-' * 40}")
        elif isinstance(event, MagenticAgentDeltaEvent):
            if event.agent_id != last_stream_agent or not stream_open:
                if stream_open:
                    print()
                print(f"[STREAM:{event.agent_id}] ", end="", flush=True)
                last_stream_agent = event.agent_id
                stream_open = True
            if event.text:
                print(event.text, end="", flush=True)
        elif isinstance(event, MagenticAgentMessageEvent):
            if stream_open:
                print()
                stream_open = False
            message = event.message
            if message and message.text:
                print(f"\n[AGENT:{event.agent_id}] {message.role.value}\n{message.text}\n{'-' * 40}")
        elif isinstance(event, MagenticFinalResultEvent):
            stream_open = False
            if event.message:
                print("\n" + "=" * 60)
                print("FINAL RESULT (manager synthesis)")
                print("=" * 60)
                print(event.message.text)
                print("=" * 60)
        elif isinstance(event, WorkflowOutputEvent):
            final_output = str(event.data) if event.data is not None else None

    if stream_open:
        print()

    if final_output:
        print("\nWorkflow completed with output:\n")
        print(final_output)
    else:
        print("\nWorkflow finished without emitting WorkflowOutputEvent data.")


if __name__ == "__main__":
    asyncio.run(main())
