from __future__ import annotations

import asyncio
import sys
from collections.abc import AsyncIterable
from pathlib import Path
from typing import List, Sequence, cast

from agent_framework import (
    ChatAgent,
    ChatMessage,
    HandoffBuilder,
    HandoffUserInputRequest,
    RequestInfoEvent,
    WorkflowEvent,
    WorkflowOutputEvent,
    WorkflowRunState,
    WorkflowStatusEvent,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestrations.common import build_chat_client


def create_agents() -> Sequence[ChatAgent]:
    """Aligns with the official triage → specialist handoff sample."""

    chat_client = build_chat_client()
    triage = ChatAgent(
        name="triage_agent",
        instructions=(
            "Route each homework question to math_tutor or history_tutor. "
            "Call the provided handoff tool instead of answering yourself."
        ),
        chat_client=chat_client,
    )
    math_tutor = ChatAgent(
        name="math_tutor",
        instructions="You are a math tutor. Explain the concepts step-by-step.",
        chat_client=chat_client,
    )
    history_tutor = ChatAgent(
        name="history_tutor",
        instructions="You are a history tutor. Focus on context, timelines, and key events.",
        chat_client=chat_client,
    )
    return triage, math_tutor, history_tutor


async def _drain(stream: AsyncIterable[WorkflowEvent]) -> list[WorkflowEvent]:
    return [event async for event in stream]


def _handle_events(events: list[WorkflowEvent]) -> list[RequestInfoEvent]:
    pending: list[RequestInfoEvent] = []

    for event in events:
        if isinstance(event, WorkflowStatusEvent) and event.state in {
            WorkflowRunState.IDLE,
            WorkflowRunState.IDLE_WITH_PENDING_REQUESTS,
        }:
            print(f"[status] {event.state.name}")
        elif isinstance(event, WorkflowOutputEvent):
            conversation = cast(list[ChatMessage], event.data)
            print("\n=== Final Conversation Snapshot ===")
            for msg in conversation:
                name = msg.author_name or msg.role.value
                print(f"- {name}: {msg.text}")
            print("===================================")
        elif isinstance(event, RequestInfoEvent):
            if isinstance(event.data, HandoffUserInputRequest):
                _print_request(event.data)
            pending.append(event)

    return pending


def _print_request(request: HandoffUserInputRequest) -> None:
    print("\n=== Tutor Workflow Needs Input ===")
    for msg in request.conversation:
        name = msg.author_name or msg.role.value
        print(f"- {name}: {msg.text}")
    print("===============================")


async def main() -> None:
    triage, math_tutor, history_tutor = create_agents()

    workflow = (
        HandoffBuilder(name="homework_handoff", participants=[triage, math_tutor, history_tutor])
        .set_coordinator("triage_agent")
        .request_prompt("Provide your next homework question.")
        .with_termination_condition(lambda conversation: sum(1 for msg in conversation if msg.role.value == "user") >= 4)
        .build()
    )

    scripted_questions = [
        "What was the turning point of WWII?"
        "What is the derivative of x^2?",
        "Can you remind me what triggered World War II?",
        "How can you prove world is round mathematically?",
        "Thank you for the help!",
    ]

    print("\n[Starting workflow with initial question...]")
    events = await _drain(workflow.run_stream("I have homework questions to delegate."))
    pending_requests = _handle_events(events)

    while pending_requests and scripted_questions:
        user_input = scripted_questions.pop(0)
        print(f"\n[User responding: {user_input}]")

        responses = {req.request_id: user_input for req in pending_requests}
        events = await _drain(workflow.send_responses_streaming(responses))
        pending_requests = _handle_events(events)


if __name__ == "__main__":
    asyncio.run(main())
