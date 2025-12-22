"""
Simple in-memory ContextProvider for user preferences using ChatAgent + chat client.

Demonstrates:
- Using ContextProvider.invoking to inject dynamic instructions
- Using ContextProvider.invoked to update in-process preferences

Chat-client counterpart to the Azure Responses-based Mem0/context samples.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any, MutableSequence, Sequence

from dotenv import load_dotenv
from agent_framework import ChatAgent, ChatMessage
from agent_framework._memory import Context, ContextProvider
from agent_framework.openai import OpenAIChatClient  # requires agent-framework[openai]

load_dotenv()


def _resolve_model_id(default: str = "gpt-4o-mini") -> str:
    return os.getenv("OPENAI_MODEL") or default


class UserPreferencesMemory(ContextProvider):
    """Minimal in-process preference memory.

    - invoking: prepend a system message describing known preferences.
    - invoked: scan messages for simple "I like X" patterns and store them.
    """

    def __init__(self) -> None:
        super().__init__()
        self._prefs: dict[str, str] = {}

    async def invoking(
        self,
        messages: ChatMessage | MutableSequence[ChatMessage],
        **_: Any,
    ) -> Context:
        if not self._prefs:
            return Context(messages=None)

        summary = ", ".join(f"{k} = {v}" for k, v in self._prefs.items())
        text = f"User preferences (from prior turns in this process): {summary}"
        return Context(messages=[ChatMessage(role="system", text=text)])

    async def invoked(
        self,
        request_messages: ChatMessage | Sequence[ChatMessage],
        response_messages: ChatMessage | Sequence[ChatMessage] | None = None,
        invoke_exception: Exception | None = None,
        **_: Any,
    ) -> None:
        if invoke_exception:
            return

        all_msgs: list[ChatMessage] = []
        if isinstance(request_messages, ChatMessage):
            all_msgs.append(request_messages)
        else:
            all_msgs.extend(request_messages)
        if response_messages:
            if isinstance(response_messages, ChatMessage):
                all_msgs.append(response_messages)
            else:
                all_msgs.extend(response_messages)

        # Extremely naive preference extraction: look for "I like X" in user messages.
        for m in all_msgs:
            role = getattr(m, "role", None)
            role_val = role.value if hasattr(role, "value") else role
            if role_val != "user" or not m.text:
                continue
            text = m.text.lower()
            marker = "i like "
            if marker in text:
                idx = text.index(marker) + len(marker)
                value = text[idx:].strip().rstrip(".!")
                if value:
                    self._prefs["likes"] = value


async def main() -> None:
    provider = UserPreferencesMemory()

    chat_client = OpenAIChatClient(model_id=_resolve_model_id())

    agent = ChatAgent(
        name="prefs-chatclient-demo",
        instructions="Be concise and respect the injected user preferences.",
        chat_client=chat_client,
        context_providers=provider,
    )

    thread = agent.get_new_thread()

    r1 = await agent.run("Hi, I like vegetarian food and black holes.", thread=thread)
    print("[call 1]", r1.text)

    r2 = await agent.run("Suggest a dinner and a reading topic for me.", thread=thread)
    print("[call 2]", r2.text)


if __name__ == "__main__":
    asyncio.run(main())
