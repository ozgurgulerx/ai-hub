from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from agent_framework import (
    AgentRunUpdateEvent,
    ChatAgent,
    ChatMessage,
    Role,
    SequentialBuilder,
    WorkflowOutputEvent,
)

try:
    from agent_framework import GroupChatBuilder
except ImportError:  # Older agent_framework build without group chat builder
    GroupChatBuilder = None

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestrations.common import build_chat_client

MIN_NATIVE_ROUNDS = 4
MAX_NATIVE_ROUNDS = 10
MAX_FALLBACK_TURNS = 10
APPROVAL_TOKEN = "approved"


def _has_reviewer_approval(conversation: list[ChatMessage]) -> bool:
    for message in conversation:
        author = (message.author_name or "").lower()
        text = (message.text or "").lower()
        if "reviewer" in author and APPROVAL_TOKEN in text:
            return True
    return False


def _writer_message_count(conversation: list[ChatMessage]) -> int:
    return sum(1 for message in conversation if (message.author_name or "").lower() == "writer")


def _last_writer_tagline(conversation: list[ChatMessage]) -> str:
    for message in reversed(conversation):
        author = (message.author_name or "").lower()
        if author == "writer" and message.text:
            return message.text.strip()
    return "Conversation completed."


async def _run_native_group_chat() -> None:
    """Use GroupChatBuilder with a custom selector so both agents take turns."""

    writer = ChatAgent(
        name="Writer",
        description="Punchy slogan specialist",
        instructions=(
            "Pitch playful two-sentence visions under 35 words. "
            "Each time you speak, offer a fresh twist that reacts to the reviewer's latest feedback."
        ),
        chat_client=build_chat_client(),
    )
    reviewer = ChatAgent(
        name="Reviewer",
        description="Snappy reviewer",
        instructions=(
            "Reply in ≤2 sentences with upbeat critique. Suggest at least two tweaks before saying 'Approved'."
        ),
        chat_client=build_chat_client(),
    )

    def select_next_speaker(state) -> str | None:
        round_index = state["round_index"]
        conversation = state["conversation"]

        if round_index >= MAX_NATIVE_ROUNDS:
            return None

        if (
            round_index >= MIN_NATIVE_ROUNDS
            and _has_reviewer_approval(conversation)
            and _writer_message_count(conversation) >= 3
        ):
            return None

        history = state["history"]
        if not history:
            return "writer"
        last = history[-1].speaker
        return "reviewer" if last == "writer" else "writer"

    def final_message(state) -> ChatMessage:
        tagline = _last_writer_tagline(state["conversation"])
        return ChatMessage(
            role=Role.ASSISTANT,
            author_name="Coordinator",
            text=f"Great collaboration! Final tagline: {tagline}",
        )

    workflow = (
        GroupChatBuilder()
        .select_speakers(select_next_speaker, display_name="Coordinator", final_message=final_message)
        .participants(writer=writer, reviewer=reviewer)
        .build()
    )

    task = (
        "Invent a whimsical theme for a neighborhood hackathon. Trade ideas and end with a short approved tagline."
    )

    print("\nStarting Group Chat Workflow...\n")
    print(f"TASK: {task}\n")

    final_response: str | None = None
    last_executor_id: str | None = None

    async for event in workflow.run_stream(task):
        if isinstance(event, AgentRunUpdateEvent):
            speaker = event.executor_id
            if speaker != last_executor_id:
                if last_executor_id is not None:
                    print()
                print(f"{speaker}: ", end="", flush=True)
                last_executor_id = speaker
            print(event.data, end="", flush=True)
        elif isinstance(event, WorkflowOutputEvent):
            final_response = getattr(event.data, "text", str(event.data))

    if final_response:
        print("\n" + "=" * 60)
        print("FINAL RESPONSE")
        print("=" * 60)
        print(final_response)
        print("=" * 60)
    else:
        print("Workflow completed without a final response payload.")


async def _run_fallback_round_robin(prompt: str) -> None:
    client = build_chat_client()
    writer = ChatAgent(
        name="Writer",
        chat_client=client,
        instructions="Produce a single concise slogan or idea per turn.",
    )
    reviewer = ChatAgent(
        name="Reviewer",
        chat_client=client,
        instructions="Critique the previous assistant response and say 'Approved' when satisfied.",
    )

    workflow = SequentialBuilder().participants([writer, reviewer]).build()
    conversation: list[ChatMessage] = [ChatMessage(role=Role.USER, text=prompt)]

    for turn in range(MAX_FALLBACK_TURNS):
        print(f"\n=== Round {turn + 1} ===")
        async for event in workflow.run_stream(list(conversation)):
            if isinstance(event, AgentRunUpdateEvent):
                continue  # Skip streaming chunks for older fallback
            if isinstance(event, WorkflowOutputEvent):
                conversation = event.data
                for message in conversation[-2:]:
                    name = message.author_name or message.role.value
                    print(f"{name}: {message.text}")
                break

        if (
            turn + 1 >= MIN_NATIVE_ROUNDS
            and _has_reviewer_approval(conversation)
            and _writer_message_count(conversation) >= 3
        ):
            print("\nReviewer approved the concept. Ending early.")
            break

    print("\n=== Final Transcript ===")
    for message in conversation:
        name = message.author_name or message.role.value
        print(f"{name}: {message.text}")


async def main() -> None:
    if GroupChatBuilder is not None:
        await _run_native_group_chat()
    else:
        print(
            "GroupChatBuilder is unavailable in this agent_framework version. "
            "Falling back to a sequential round-robin simulation."
        )
        await _run_fallback_round_robin("Pitch a whimsical theme for a neighborhood hackathon.")


if __name__ == "__main__":
    asyncio.run(main())
