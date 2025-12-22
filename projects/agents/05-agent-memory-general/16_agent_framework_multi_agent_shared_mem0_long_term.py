"""
Two agents sharing the same Mem0-backed long-term memory (platform client, v2 API).
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

# Keep mem0 data local to the workspace.
os.environ.setdefault("MEM0_DIR", str(Path("mem0_cache").resolve()))
Path(os.environ["MEM0_DIR"]).mkdir(parents=True, exist_ok=True)

# Populate MEM0_API_KEY after .env is loaded, falling back to MEM0_KEY.
if not os.getenv("MEM0_API_KEY") and os.getenv("MEM0_KEY"):
    os.environ["MEM0_API_KEY"] = os.environ["MEM0_KEY"]


class SimpleMem0Provider(ContextProvider):
    """
    Minimal Mem0 context provider using the platform MemoryClient (v2 API).
    Shared instance = shared long-term memory across agents.
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

    async def invoking(self, messages: Sequence[ChatMessage] | ChatMessage, **_: Any) -> Context:
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
        except Exception as exc:
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
            await asyncio.to_thread(
                self._client.add,
                all_msgs,
                user_id=self._user_id,
                version="v2",
            )
            print(f"[Mem0 add] messages={all_msgs}")
        except Exception as exc:
            print(f"[Mem0 warning] add failed: {exc!r}")


async def main() -> None:
    if not os.getenv("MEM0_API_KEY"):
        raise RuntimeError("Set MEM0_API_KEY or MEM0_KEY in .env for Mem0Provider.")

    provider = SimpleMem0Provider(
        api_key=os.environ["MEM0_API_KEY"],
        user_id="user-ozgur",
        org_id=os.getenv("MEM0_ORG_ID"),
        project_id=os.getenv("MEM0_PROJECT_ID"),
    )

    def make_agent(name: str, instructions: str):
        return AzureOpenAIResponsesClient(
            endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
        ).create_agent(
            name=name,
            instructions=instructions,
            context_providers=provider,
        )

    tutor = make_agent("tutor", "Be a friendly physics tutor.")
    examiner = make_agent("examiner", "Be a strict examiner.")

    tutor_thread = tutor.get_new_thread()
    print("[Tutor thread] teach facts")
    await tutor.run("My name is Ozgur. I study black holes and avoid spicy food.", thread=tutor_thread)
    await tutor.run("Acknowledge you stored that.", thread=tutor_thread)

    examiner_thread = examiner.get_new_thread()
    print("[Examiner thread] recall facts")
    r = await examiner.run("What do you already know about me?", thread=examiner_thread)
    print("[Examiner reply]", r.text)


if __name__ == "__main__":
    asyncio.run(main())
