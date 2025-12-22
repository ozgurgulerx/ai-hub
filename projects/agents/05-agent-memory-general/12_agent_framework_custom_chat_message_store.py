"""
Custom ChatMessageStore that persists messages to a JSON file (per thread).
Shows app-owned short-term memory outside the service.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Sequence

from dotenv import load_dotenv
from agent_framework import ChatMessage
from agent_framework._threads import ChatMessageStoreProtocol
from agent_framework.azure import AzureOpenAIResponsesClient

load_dotenv()

STORE_DIR = Path("chat_store")
STORE_DIR.mkdir(exist_ok=True)


class FileChatMessageStore(ChatMessageStoreProtocol):
    def __init__(self, path: Path):
        self.path = path
        self._messages: list[ChatMessage] = []
        if path.exists():
            data = json.loads(path.read_text())
            for m in data.get("messages", []):
                role = m.get("role")
                text = m.get("text")
                if role and text:
                    self._messages.append(ChatMessage(role=str(role), text=str(text)))

    async def list_messages(self) -> list[ChatMessage]:
        return self._messages

    async def add_messages(self, messages: Sequence[ChatMessage]) -> None:
        def msg_text(msg: ChatMessage) -> str:
            if msg.text:
                return str(msg.text)
            if msg.contents:
                parts = []
                for c in msg.contents:
                    val = getattr(c, "text", None)
                    if val:
                        parts.append(str(val))
                if parts:
                    return " ".join(parts)
            return ""

        self._messages.extend(messages)
        payload = {
            "messages": [
                {"role": str(getattr(m, "role", "")), "text": msg_text(m)}
                for m in self._messages
            ]
        }
        self.path.write_text(json.dumps(payload, indent=2))

    @classmethod
    async def deserialize(cls, serialized_store_state, **kwargs):
        # For simplicity, just start empty when deserializing in this demo.
        return cls(Path(serialized_store_state["path"]))

    async def update_from_state(self, serialized_store_state, **kwargs) -> None:
        # Not used in this minimal demo.
        return

    async def serialize(self, **kwargs):
        return {"path": str(self.path)}


async def main() -> None:
    def store_factory() -> FileChatMessageStore:
        thread_file = STORE_DIR / f"thread_{os.urandom(4).hex()}.json"
        return FileChatMessageStore(thread_file)

    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    ).create_agent(
        name="file-store-agent",
        instructions="Be brief.",
        chat_message_store_factory=store_factory,
    )

    thread = agent.get_new_thread()

    r1 = await agent.run("My favourite black hole is Sagittarius A*. Remember it.", thread=thread)
    print("[call 1] reply:", r1.text)

    r2 = await agent.run("Which black hole did I say I like?", thread=thread)
    print("[call 2] reply:", r2.text)

    store = getattr(thread, "_message_store", None)
    store_path = getattr(store, "path", None)
    if store_path:
        print(f"[store path] {store_path}")


if __name__ == "__main__":
    asyncio.run(main())
