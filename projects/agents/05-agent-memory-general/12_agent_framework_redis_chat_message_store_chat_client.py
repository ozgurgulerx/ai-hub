"""
Use RedisChatMessageStore with a ChatAgent and chat client.

Demonstrates:
- Plugging a Redis-backed ChatMessageStore via chat_message_store_factory
- Persisting chat history under a stable thread_id in Redis

Requires:
- agent-framework[redis] extras installed
- A running Redis instance reachable at REDIS_URL
"""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient  # requires agent-framework[openai]
from agent_framework.redis import RedisChatMessageStore  # type: ignore[import]

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
THREAD_KEY = os.getenv("REDIS_THREAD_KEY", "agent-memory-chatclient-thread")


def _resolve_model_id(default: str = "gpt-4o-mini") -> str:
    return os.getenv("OPENAI_MODEL") or default


async def main() -> None:
    def store_factory() -> RedisChatMessageStore:
        # All messages for this logical thread are stored under THREAD_KEY in Redis.
        return RedisChatMessageStore(
            redis_url=REDIS_URL,
            thread_id=THREAD_KEY,
            max_messages=100,
        )

    chat_client = OpenAIChatClient(model_id=_resolve_model_id())

    agent = ChatAgent(
        name="redis-store-chat-agent",
        instructions="Be concise.",
        chat_client=chat_client,
        chat_message_store_factory=store_factory,
    )

    thread = agent.get_new_thread()

    r1 = await agent.run(
        "My favourite black hole is Sagittarius A*. Remember it in Redis.",
        thread=thread,
    )
    print("[call 1]", r1.text)

    r2 = await agent.run("Which black hole did I say I like?", thread=thread)
    print("[call 2]", r2.text)

    print(f"[redis] history stored under thread_id={THREAD_KEY} at {REDIS_URL}")


if __name__ == "__main__":
    asyncio.run(main())
