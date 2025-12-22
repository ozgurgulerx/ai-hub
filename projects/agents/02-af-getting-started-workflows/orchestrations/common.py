"""Shared helpers that mirror the official Agent Framework workflow samples."""

from __future__ import annotations

import os
from typing import Protocol

try:
    from azure.identity import AzureCliCredential
except ImportError:  # pragma: no cover - optional dependency
    AzureCliCredential = None  # type: ignore[assignment]

try:
    from agent_framework.azure import AzureOpenAIChatClient
except ImportError:  # pragma: no cover - optional dependency
    AzureOpenAIChatClient = None  # type: ignore[assignment]

try:
    from agent_framework.openai import OpenAIChatClient, OpenAIResponsesClient
except ImportError:  # pragma: no cover - optional dependency
    OpenAIChatClient = None  # type: ignore[assignment]
    OpenAIResponsesClient = None  # type: ignore[assignment]

try:  # agent_framework 0.5+ exposes explicit typing helpers
    from agent_framework.typing import ChatClientProtocol
except ModuleNotFoundError:  # pragma: no cover - compatibility shim
    class ChatClientProtocol(Protocol):
        ...


def resolve_model_id(default: str = "gpt-4o-mini") -> str:
    """Pick a sensible default model/deployment name."""

    return (
        os.environ.get("AGENT_MODEL")
        or os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
        or os.environ.get("OPENAI_MODEL")
        or default
    )


def build_chat_client(*, prefer_responses: bool = False) -> ChatClientProtocol:
    """
    Instantiate clients exactly how the official samples do.

    Preference order:
    1. Azure OpenAI (if endpoint + Azure SDK available) – relies on `az login`.
    2. OpenAI Responses client (when prefer_responses=True).
    3. OpenAI Chat client.
    """

    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    if azure_endpoint and AzureOpenAIChatClient and AzureCliCredential:
        return AzureOpenAIChatClient(
            credential=AzureCliCredential(),
            model_id=resolve_model_id(),
        )

    if prefer_responses and OpenAIResponsesClient:
        return OpenAIResponsesClient(model_id=resolve_model_id("gpt-4o"))

    if OpenAIChatClient is None:
        raise RuntimeError("OpenAIChatClient is unavailable; install agent-framework[openai].")

    return OpenAIChatClient(model_id=resolve_model_id())
