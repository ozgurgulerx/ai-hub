"""
Long-term memory across threads using Mem0 Platform (custom provider).
Thread A teaches facts; Thread B (fresh) recalls via Mem0.
"""

import asyncio
import os
from pathlib import Path
from typing import Sequence, Any

from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework import ChatMessage
from agent_framework._memory import Context, ContextProvider
from mem0 import MemoryClient  # platform client (v2 API)

load_dotenv()

# Optional: keep Mem0 cache / temp files scoped to this repo
os.environ.setdefault("MEM0_DIR", str(Path("mem0_cache").resolve()))
Path(os.environ["MEM0_DIR"]).mkdir(parents=True, exist_ok=True)

# Allow either MEM0_API_KEY or MEM0_KEY in .env
if not os.getenv("MEM0_API_KEY") and os.getenv("MEM0_KEY"):
    os.environ["MEM0_API_KEY"] = os.environ["MEM0_KEY"]


class SimpleMem0Provider(ContextProvider):
    """
    Minimal Mem0 context provider using the platform MemoryClient (v2 API).

    - invoking: search Mem0 for this user and inject memories as a system message.
    - invoked: add the current turn as memories to Mem0.
    """

    def __init__(
        self,
        api_key: str,
        user_id: str,
        org_id: str | None = None,
        project_id: str | None = None,
    ) -> None:
        super().__init__()
        self._user_id = user_id
        self._client = MemoryClient(api_key=api_key, org_id=org_id, project_id=project_id)

    async def invoking(
        self,
        messages: Sequence[ChatMessage] | ChatMessage,
        **_: Any,
    ) -> Context:
        # Use the last user message as the search query.
        if isinstance(messages, ChatMessage):
            msgs = [messages]
        else:
            msgs = list(messages)
        last_user = None
        for m in reversed(msgs):
            role = getattr(m, "role", None)
            role_val = role.value if hasattr(role, "value") else role
            if role_val == "user":
                last_user = m
                break
        query = last_user.text if (last_user and last_user.text) else ""
        if not query:
            return Context(messages=None)

        # v2 search API requires filters; simplest: AND[user_id]
        filters: dict[str, Any] = {"AND": [{"user_id": self._user_id}]}

        try:
            res = await asyncio.to_thread(
                self._client.search,
                query,
                version="v2",
                filters=filters,
            )
            print(f"[Mem0 search] query='{query}', filters={filters}")
            print(f"[Mem0 search] response={res}")
        except Exception as exc:  # pragma: no cover
            print(f"[Mem0 warning] search failed: {exc!r}")
            return Context(messages=None)

        if isinstance(res, dict) and "results" in res:
            memories = res["results"]
        elif isinstance(res, list):
            memories = res
        else:
            memories = []

        lines: list[str] = []
        for m in memories:
            if isinstance(m, dict) and m.get("memory"):
                lines.append(str(m["memory"]))

        if not lines:
            return Context(messages=None)

        memory_text = "Here are some facts about the user:\n" + "\n".join(f"- {line}" for line in lines[:8])
        return Context(messages=[ChatMessage(role="system", text=memory_text)])

    async def invoked(
        self,
        request_messages: ChatMessage | Sequence[ChatMessage],
        response_messages: ChatMessage | Sequence[ChatMessage] | None = None,
        invoke_exception: Exception | None = None,
        **_: Any,
    ) -> None:
        if invoke_exception:
            return

        def to_dicts(msgs: Sequence[ChatMessage]) -> list[dict[str, str]]:
            out: list[dict[str, str]] = []
            for m in msgs:
                txt = getattr(m, "text", None)
                role = getattr(m, "role", None)
                role_val = role.value if hasattr(role, "value") else role
                if txt and role_val in {"user", "assistant", "system"}:
                    out.append({"role": role_val, "content": txt})
            return out

        req_list = [request_messages] if isinstance(request_messages, ChatMessage) else list(request_messages)
        all_msgs = to_dicts(req_list)

        if response_messages:
            resp_list = [response_messages] if isinstance(response_messages, ChatMessage) else list(response_messages)
            all_msgs.extend(to_dicts(resp_list))

        if not all_msgs:
            return

        try:
            # Only 1 positional (messages); rest keyword per docs
            add_res = await asyncio.to_thread(
                self._client.add,
                all_msgs,
                user_id=self._user_id,
                version="v2",
            )
            print(f"[Mem0 add] messages={all_msgs}")
            print(f"[Mem0 add] response={add_res}")
        except Exception as exc:  # pragma: no cover
            print(f"[Mem0 warning] add failed: {exc!r}")


async def main() -> None:
    api_key = os.getenv("MEM0_API_KEY")
    if not api_key:
        raise RuntimeError("Set MEM0_API_KEY or MEM0_KEY in .env for Mem0.")

    provider = SimpleMem0Provider(
        api_key=api_key,
        user_id="user-ozgur",
        org_id=os.getenv("MEM0_ORG_ID"),
        project_id=os.getenv("MEM0_PROJECT_ID"),
    )

    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    ).create_agent(
        name="mem0-demo",
        instructions="Be concise and use provided long-term memory.",
        context_providers=provider,
    )

    # Thread A: teach facts.
    thread_a = agent.get_new_thread()
    print("[Thread A] teach facts")
    await agent.run("My name is Ozgur. I like Sagittarius A* and vegetarian food.", thread=thread_a)
    await agent.run("Summarize what you know about me in one sentence.", thread=thread_a)

    # Thread B: new thread, should recall via Mem0.
    thread_b = agent.get_new_thread()
    print("[Thread B] recall facts")
    r = await agent.run("What do you already know about me?", thread=thread_b)
    print("[Thread B reply]", r.text)


if __name__ == "__main__":
    asyncio.run(main())
