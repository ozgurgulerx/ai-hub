"""
Use the built-in ChatMessageStore with a ChatAgent and chat client.

Demonstrates:
- Wiring ChatMessageStore via chat_message_store_factory
- Short-term memory that can be serialized independently of the underlying service

This sample is the ChatAgent+chat client counterpart to
12_agent_framework_custom_chat_message_store.py, which uses Azure Responses.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

from dotenv import load_dotenv
from agent_framework import ChatAgent, ChatMessageStore
from agent_framework.openai import OpenAIChatClient  # requires agent-framework[openai]

load_dotenv()


def _resolve_model_id(default: str = "gpt-4o-mini") -> str:
    return os.getenv("OPENAI_MODEL") or default


async def main() -> None:
    print("=== Built-in ChatMessageStore chat demo (OpenAI chat client) ===")

    def store_factory() -> ChatMessageStore:
        # Built-in in-memory store that supports serialize/deserialize.
        return ChatMessageStore()

    chat_client = OpenAIChatClient(model_id=_resolve_model_id())

    agent = ChatAgent(
        name="builtin-store-chat-agent",
        instructions=(
            "Be playful and concise. When the user shares a fact, acknowledge you'll remember it. "
            "Later, weave that fact back into a creative response."
        ),
        chat_client=chat_client,
        chat_message_store_factory=store_factory,
    )

    thread = agent.get_new_thread()

    # First turn: ask the user for a favorite star.
    user_msg1 = input("🧑‍🚀 You: What's your favorite star (or constellation) and why? ")
    r1 = await agent.run(user_msg1, thread=thread)
    print("🤖 Agent:", r1.text, "(I'll remember this.)")

    # Second turn: ask the agent to remember and be creative.
    user_msg2 = "Craft a short, fun adventure where that star guides a lost spaceship home."
    print("🧑‍🚀 You:", user_msg2)
    r2 = await agent.run(user_msg2, thread=thread)
    print("🤖 Agent:", r2.text)

    # Third turn: ask a follow-up that prompts explicit recall.
    user_msg3 = "What did I tell you about my favorite star, and how would you use it to name a cafe on Mars?"
    print("🧑‍🚀 You:", user_msg3)
    r3 = await agent.run(user_msg3, thread=thread)
    print("🤖 Agent:", r3.text)

    # Access the underlying store and show that it can be serialized.
    store = getattr(thread, "_message_store", None)
    if store is not None:
        state: Any = await store.serialize()
        print("\n[builtin store] Serialized in-memory history (ChatMessageStore):")
        print(state)
        print("[builtin store] Memory is currently held in-process; serialize() shows how you'd persist it.")
    else:
        print("[builtin store] no message store attached")


if __name__ == "__main__":
    asyncio.run(main())
