"""
Basic Mem0Provider usage with ChatAgent + chat client.

Demonstrates:
- Using agent_framework.mem0.Mem0Provider instead of a custom ContextProvider
- Cross-thread recall of user facts via Mem0

Chat-client counterpart to 15_agent_framework_long_term_mem0_cross_threads.py.
"""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.mem0 import Mem0Provider  # type: ignore[import]
from agent_framework.openai import OpenAIChatClient  # requires agent-framework[openai]

load_dotenv()


def _resolve_model_id(default: str = "gpt-4o-mini") -> str:
    return os.getenv("OPENAI_MODEL") or default


async def main() -> None:
    api_key = os.getenv("MEM0_API_KEY") or os.getenv("MEM0_KEY")
    if not api_key:
        raise RuntimeError("Set MEM0_API_KEY or MEM0_KEY in .env for Mem0Provider.")

    memory_provider = Mem0Provider(
        api_key=api_key,
        user_id="user-ozgur",
        application_id="agent-memory-demo",
    )

    chat_client = OpenAIChatClient(model_id=_resolve_model_id())

    agent = ChatAgent(
        name="mem0provider-chatclient-demo",
        instructions="Be concise and use your long-term memory.",
        chat_client=chat_client,
        context_providers=memory_provider,
    )

    # Thread A: teach facts.
    thread_a = agent.get_new_thread()
    print("[Thread A] teach facts")
    await agent.run("My name is Ozgur. I like Sagittarius A* and vegetarian food.", thread=thread_a)
    await agent.run("Summarize what you know about me in one sentence.", thread=thread_a)

    # Thread B: new thread, should still recall via Mem0Provider.
    thread_b = agent.get_new_thread()
    print("[Thread B] recall facts")
    r = await agent.run("What do you already know about me?", thread=thread_b)
    print("[Thread B reply]", r.text)


if __name__ == "__main__":
    asyncio.run(main())
