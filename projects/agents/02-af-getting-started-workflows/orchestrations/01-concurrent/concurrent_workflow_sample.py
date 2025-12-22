from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any, Sequence

from agent_framework import ChatMessage, ConcurrentBuilder

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from orchestrations.common import build_chat_client


async def main() -> None:
    """
    Fan-out/fan-in orchestration following the official `concurrent_agents.py` sample.

    Three domain agents receive the same prompt in parallel and the workflow aggregates
    their conversations into a single `list[ChatMessage]`.
    """

    chat_client = build_chat_client()

    researcher = chat_client.create_agent(
        instructions=(
            "You're an expert product researcher. Provide concise insights, opportunities, and risks for the prompt."
        ),
        name="researcher",
    )
    marketer = chat_client.create_agent(
        instructions=(
            "You're a creative marketing strategist. Craft crisp value props and targeting guidance aligned to the prompt."
        ),
        name="marketer",
    )
    legal = chat_client.create_agent(
        instructions=(
            "You're a compliance reviewer. Highlight constraints, disclaimers, and policy concerns raised by the prompt."
        ),
        name="legal",
    )

    workflow = ConcurrentBuilder().participants([researcher, marketer, legal]).build()

    task = "We are launching a budget-friendly commuter e-bike. Provide research, marketing, and legal guidance."
    events = await workflow.run(task)
    outputs = events.get_outputs()

    if not outputs:
        print("Workflow completed without aggregated messages.")
        return

    print("===== Final Aggregated Conversation =====")
    for output in outputs:
        messages: Sequence[ChatMessage] | Any = output
        for idx, message in enumerate(messages, start=1):
            author = message.author_name or ("assistant" if message.role.value == "assistant" else "user")
            print(f"{'-' * 60}\n{idx:02d} [{author}]\n{message.text}")


if __name__ == "__main__":
    asyncio.run(main())
