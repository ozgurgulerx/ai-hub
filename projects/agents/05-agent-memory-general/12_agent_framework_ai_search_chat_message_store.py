"""
External chat history backed by Azure AI Search.

- Uses the Azure AI Search env vars from .env (AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_API_KEY, AZURE_SEARCH_INDEX_NAME).
- Writes each message into the search index and reads them back to rebuild history, so threads survive restarts.
- Requires `azure-search-documents` (pip install azure-search-documents).
"""

import asyncio
import os
import time
import uuid
from typing import Sequence

from dotenv import load_dotenv
from agent_framework import ChatMessage
from agent_framework._threads import ChatMessageStoreProtocol
from agent_framework.azure import AzureOpenAIResponsesClient

try:
    from azure.core.credentials import AzureKeyCredential
    from azure.core.exceptions import ResourceNotFoundError
    from azure.search.documents import SearchClient
    from azure.search.documents.indexes import SearchIndexClient
    from azure.search.documents.indexes.models import (
        SearchIndex,
        SimpleField,
        SearchableField,
        SearchFieldDataType,
    )
except ImportError as exc:  # pragma: no cover - runtime check for optional dependency
    raise SystemExit(
        "Install azure-search-documents to run this sample: pip install azure-search-documents"
    ) from exc

load_dotenv()

# Thread ID is kept stable so history can be reloaded after a restart.
THREAD_ID = os.getenv("AZURE_SEARCH_THREAD_ID", "roman-merchant-thread")

_search_client_singleton: SearchClient | None = None
_search_endpoint: str | None = None
_search_index_name: str | None = None


def require_env(var: str) -> str:
    val = os.getenv(var)
    if not val:
        raise RuntimeError(f"Missing required environment variable: {var}")
    return val


def get_search_client() -> SearchClient:
    """
    Lazily build and cache the SearchClient; also ensures the index exists.
    """
    global _search_client_singleton, _search_endpoint, _search_index_name
    if _search_client_singleton:
        return _search_client_singleton

    _search_endpoint = require_env("AZURE_SEARCH_ENDPOINT")
    _search_index_name = require_env("AZURE_SEARCH_INDEX_NAME")
    ensure_index(
        SearchIndexClient(
            endpoint=_search_endpoint,
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_ADMIN_KEY") or require_env("AZURE_SEARCH_API_KEY")),
        ),
        _search_index_name,
    )
    _search_client_singleton = SearchClient(
        endpoint=_search_endpoint,
        index_name=_search_index_name,
        credential=AzureKeyCredential(require_env("AZURE_SEARCH_API_KEY")),
    )
    return _search_client_singleton


def ensure_index(index_client: SearchIndexClient, index_name: str) -> None:
    """
    Create a simple index if it does not exist.
    Fields: id (key), thread_id (filter), role (filter), content (searchable), ts (sortable).
    """
    try:
        index_client.get_index(index_name)
        return
    except ResourceNotFoundError:
        pass

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="thread_id", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="role", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String, analyzer_name="en.lucene"),
        SimpleField(name="ts", type=SearchFieldDataType.Double, filterable=True, sortable=True),
    ]
    index = SearchIndex(name=index_name, fields=fields)
    index_client.create_index(index)
    print(f"[search] Created index '{index_name}' with fields: thread_id, role, content, ts")


class AISearchChatMessageStore(ChatMessageStoreProtocol):
    """
    ChatMessageStore that persists messages to Azure AI Search.
    """

    def __init__(self, search_client: SearchClient, thread_id: str, top_n: int = 50) -> None:
        self.search_client = search_client
        self.thread_id = thread_id
        self.top_n = top_n

    async def list_messages(self) -> list[ChatMessage]:
        def _fetch():
            results = self.search_client.search(
                search_text="*",
                filter=f"thread_id eq '{self.thread_id}'",
                order_by=["ts asc"],
                top=self.top_n,
            )
            out: list[ChatMessage] = []
            for doc in results:
                role = doc.get("role", "assistant")
                content = doc.get("content", "")
                out.append(ChatMessage(role=role, text=content))
            return out

        return await asyncio.to_thread(_fetch)

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

        def _upload():
            now = time.time()
            docs = []
            for i, m in enumerate(messages):
                docs.append(
                    {
                        "id": f"{self.thread_id}-{uuid.uuid4().hex}-{i}",
                        "thread_id": self.thread_id,
                        "role": str(getattr(m, "role", "")),
                        "content": msg_text(m),
                        "ts": now + i * 0.001,
                    }
                )
            if docs:
                self.search_client.upload_documents(documents=docs)

        await asyncio.to_thread(_upload)

    @classmethod
    async def deserialize(cls, serialized_store_state, **kwargs):
        # Rehydrate using env-backed client and stored thread_id.
        thread_id = serialized_store_state["thread_id"]
        client = get_search_client()
        return cls(client, thread_id)

    async def update_from_state(self, serialized_store_state, **kwargs) -> None:
        return

    async def serialize(self, **kwargs):
        return {"thread_id": self.thread_id}


def create_agent(search_client: SearchClient, thread_id: str):
    return AzureOpenAIResponsesClient(
        endpoint=require_env("AZURE_OPENAI_ENDPOINT"),
        deployment_name=require_env("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=require_env("AZURE_OPENAI_API_VERSION"),
        api_key=require_env("AZURE_OPENAI_API_KEY"),
    ).create_agent(
        name="ai-search-memory-agent",
        instructions="Be a concise Roman port clerk. Remember shipping details and recall them later.",
        chat_message_store_factory=lambda: AISearchChatMessageStore(search_client, thread_id),
    )


async def main() -> None:
    # Set up the shared Search client once (will create the index if missing).
    search_client = get_search_client()

    # First agent run: write details to AI Search.
    agent = create_agent(search_client, THREAD_ID)
    thread = agent.get_new_thread()
    await agent.run(
        "I am Lucius the grain merchant. Note that I shipped 12 crates of olive oil from Ostia to Massilia "
        "on the trireme 'Sea Falcon'. Two crates were damaged in a storm off Sardinia.",
        thread=thread,
    )
    r1 = await agent.run("Confirm you saved my shipment details for later.", thread=thread)
    print("[run 1]", r1.text)

    # Simulate a restart: build a new agent + thread with the same thread_id.
    agent2 = create_agent(search_client, THREAD_ID)
    resumed_thread = agent2.get_new_thread()
    r2 = await agent2.run("What do you recall about my olive oil shipment?", thread=resumed_thread)
    print("[run 2 - recall]", r2.text)


if __name__ == "__main__":
    asyncio.run(main())
