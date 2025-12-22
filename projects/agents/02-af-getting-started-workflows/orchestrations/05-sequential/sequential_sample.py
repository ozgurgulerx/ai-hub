from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import List, cast

from agent_framework import ChatMessage, Role, SequentialBuilder, WorkflowOutputEvent

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestrations.common import build_chat_client


async def main() -> None:
    """
    Sequential translation pipeline modeled after the documentation example.

    Three translation agents (French -> Spanish -> English) run in order, each seeing the
    conversation history produced by the previous agent.
    """

    chat_client = build_chat_client()

    languages = ["French", "Spanish", "English"]
    translators = [
        chat_client.create_agent(
            instructions=(
                f"You are a translation assistant who only responds in {lang}. "
                "Always inspect the most recent assistant message in the conversation; if none exists, use the user's prompt. "
                "Detect that message's language, state it explicitly, then translate only that content to "
                f"{lang}. Keep responses concise."
            ),
            name=f"{lang.lower()}_translator",
        )
        for lang in languages
    ]

    workflow = SequentialBuilder().participants(translators).build()

    outputs: list[list[ChatMessage]] = []
    async for event in workflow.run_stream("Hello, world!"):
        if isinstance(event, WorkflowOutputEvent):
            outputs.append(cast(list[ChatMessage], event.data))

    if not outputs:
        print("Workflow completed with no conversation output.")
        return

    print("===== Final Conversation =====")
    for idx, message in enumerate(outputs[-1], start=1):
        speaker = message.author_name or ("assistant" if message.role == Role.ASSISTANT else "user")
        print(f"{'-' * 60}\n{idx:02d} [{speaker}]\n{message.text}")


if __name__ == "__main__":
    asyncio.run(main())
