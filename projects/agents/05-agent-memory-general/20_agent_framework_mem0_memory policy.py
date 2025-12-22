"""
Supply-chain planner copilot demo with long-term memory (Mem0 + Azure AI Search).

This script mirrors the requested `demo_mem0_agent.py` flow:
- Mem0 open-source `Memory` is configured with Azure AI Search and Azure OpenAI embeddings.
- A custom `ContextProvider` injects episodic memories before each turn and stores new ones after.
- A planner copilot ChatAgent (Azure OpenAI chat client) runs three scenes to show recall across sessions.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, List, Optional, Sequence, Tuple

from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# TRACE LOGGING SETUP - writes to 20_trace.log for demo visibility
# Run: tail -f 20_trace.log in another terminal to watch live
# ─────────────────────────────────────────────────────────────────────────────
LOG_FILE = Path(__file__).with_name("20_trace.log")
LOG_FILE.write_text(f"=== Demo trace started at {datetime.now().isoformat()} ===\n\n")

trace = logging.getLogger("demo_trace")
trace.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s | %(message)s", datefmt="%H:%M:%S"))
trace.addHandler(fh)


def log_section(title: str) -> None:
    trace.info("")
    trace.info("=" * 70)
    trace.info(f"  {title}")
    trace.info("=" * 70)


def log_json(label: str, obj: Any) -> None:
    try:
        formatted = json.dumps(obj, indent=2, default=str)
    except Exception:
        formatted = str(obj)
    trace.debug(f"{label}:\n{formatted}")


from agent_framework import ChatAgent, ChatMessage
from agent_framework._memory import Context, ContextProvider
from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework.exceptions import ServiceResponseException
from mem0 import Memory

load_dotenv()


def require_env(name: str) -> str:
    """
    Fetch an environment variable or raise a clear error.
    """
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_memory_config() -> dict[str, Any]:
    """
    Build the Mem0 configuration for Azure AI Search + Azure OpenAI embeddings.

    Notes on assumptions:
    - `vector_store.provider='azure_ai_search'` and keys like `service_name`, `api_key`,
      and `index_name` are based on Mem0's documented Azure AI Search integration.
    - `embeddings.provider='azure_openai'` uses typical Azure OpenAI embedding fields.
      If your installed Mem0 version expects different field names (e.g., `collection_name`
      instead of `index_name`, or `deployment` instead of `deployment_name`), adjust them
      accordingly; the rest of the script remains the same.
    """
    service_name = os.getenv("AZURE_SEARCH_SERVICE_NAME")
    if not service_name:
        endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
        # Derive service name from endpoint like https://<service>.search.windows.net
        if endpoint.startswith("https://"):
            endpoint = endpoint[len("https://") :]
        if endpoint:
            service_name = endpoint.split(".search.windows.net")[0].split(".")[0]
    if not service_name:
        raise RuntimeError("Set AZURE_SEARCH_SERVICE_NAME or AZURE_SEARCH_ENDPOINT for Mem0 Azure AI Search config.")

    embedding_deployment = os.getenv("AZURE_TEXT_EMBEDDING_DEPLOYMENT_NAME") or os.getenv(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
    )
    if not embedding_deployment:
        raise RuntimeError("Set AZURE_TEXT_EMBEDDING_DEPLOYMENT_NAME for Mem0 embeddings.")

    collection_name = os.getenv("AZURE_SEARCH_COLLECTION_NAME") or require_env("AZURE_SEARCH_INDEX_NAME")

    return {
        "vector_store": {
            "provider": "azure_ai_search",
            "config": {
                "service_name": service_name,
                "api_key": require_env("AZURE_SEARCH_ADMIN_KEY"),
                # Mem0's Azure AI Search integration expects `collection_name` (synonymous with index name).
                "collection_name": collection_name,
            },
        },
        "embeddings": {
            "provider": "azure_openai",
            "config": {
                "api_key": require_env("AZURE_OPENAI_API_KEY"),
                "api_version": require_env("AZURE_OPENAI_API_VERSION"),
                "azure_endpoint": require_env("AZURE_OPENAI_ENDPOINT"),
                "deployment_name": embedding_deployment,
            },
        },
    }


def setup_mem0_memory() -> Memory:
    """
    Initialize the Mem0 open-source Memory with Azure AI Search as the backing vector store.
    """
    log_section("INITIALIZING MEM0")
    config = build_memory_config()
    trace.info(f"Vector store: {config['vector_store']['provider']}")
    trace.info(f"Embeddings: {config['embeddings']['provider']}")
    trace.info(f"Collection/Index: {config['vector_store']['config']['collection_name']}")
    memory = Memory.from_config(config)
    trace.info("Mem0 Memory initialized successfully.")
    return memory


def resolve_user_id() -> str:
    """
    Resolve the demo user id from environment variables with sensible fallbacks.

    Prefers MEM0_DEMO_USER_ID, then MEM0_USER_ID, else defaults to 'user-ozgur'
    to mirror other Mem0 samples in this repo.
    """
    return os.getenv("MEM0_DEMO_USER_ID") or os.getenv("MEM0_USER_ID") or "user-ozgur"


def create_mem0_context_provider(memory: Memory) -> "Mem0EpisodeContextProvider":
    """
    Wire up the Mem0EpisodeContextProvider with the configured Memory and user id.
    """
    user_id = resolve_user_id()
    return Mem0EpisodeContextProvider(
        memory=memory,
        user_id=user_id,
        max_results=int(os.getenv("MEM0_MAX_RESULTS", "3")),
        min_score=float(os.getenv("MEM0_MIN_SCORE", "0.0")),
    )


def create_planner_agent(context_provider: "Mem0EpisodeContextProvider"):
    """
    Build the planner copilot agent using Azure OpenAI Responses client.
    """
    log_section("CREATING PLANNER AGENT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not deployment:
        raise RuntimeError("Set AZURE_OPENAI_DEPLOYMENT_NAME for the chat model.")

    trace.info(f"LLM Deployment: {deployment}")
    trace.info(f"LLM Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    trace.info(f"LLM API Version: {os.getenv('AZURE_OPENAI_API_VERSION')}")

    print(f"[config] Using deployment: {deployment}")
    print(f"[config] Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")

    client = AzureOpenAIResponsesClient(
        endpoint=require_env("AZURE_OPENAI_ENDPOINT"),
        deployment_name=deployment,
        api_key=require_env("AZURE_OPENAI_API_KEY"),
        api_version=require_env("AZURE_OPENAI_API_VERSION"),
    )

    agent = client.create_agent(
        name="planner-copilot",
        instructions=(
            "You are a supply chain planning copilot. You help planners resolve over-capacity issues "
            "and demand spikes. You may receive additional 'episodic memories' about past incidents; "
            "use them when relevant."
        ),
        context_providers=[context_provider],
    )
    return agent


def _to_list(messages: ChatMessage | Iterable[ChatMessage]) -> List[ChatMessage]:
    """
    Normalize ChatMessage input into a list for easier processing.
    """
    if isinstance(messages, ChatMessage):
        return [messages]
    return list(messages)


def _last_user_assistant_text(
    request_messages: ChatMessage | Sequence[ChatMessage],
    response_messages: Optional[ChatMessage | Sequence[ChatMessage]],
) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract the latest user and assistant text payloads.
    """
    all_msgs: List[ChatMessage] = _to_list(request_messages)
    if response_messages:
        all_msgs.extend(_to_list(response_messages))

    last_user = None
    last_assistant = None
    for msg in reversed(all_msgs):
        role = getattr(msg, "role", None)
        role_val = role.value if hasattr(role, "value") else role
        if role_val == "assistant" and last_assistant is None and getattr(msg, "text", None):
            last_assistant = str(msg.text)
        if role_val == "user" and last_user is None and getattr(msg, "text", None):
            last_user = str(msg.text)
        if last_user and last_assistant:
            break
    return last_user, last_assistant


class Mem0EpisodeContextProvider(ContextProvider):
    """
    ContextProvider that pulls episodic memories from Mem0 and stores new incidents after runs.
    """

    def __init__(self, memory: Memory, user_id: str, max_results: int = 3, min_score: float = 0.0) -> None:
        super().__init__()
        self._memory = memory
        self._user_id = user_id
        self._max_results = max_results
        self._min_score = min_score

    @property
    def user_id(self) -> str:
        """
        Expose the configured user identifier for caller convenience.
        """
        return self._user_id

    async def invoking(
        self,
        messages: ChatMessage | Iterable[ChatMessage],
        **_: Any,
    ) -> Context:
        """
        Before each run, fetch relevant memories for the latest user text and inject them as instructions.
        """
        trace.info("")
        trace.info("─" * 50)
        trace.info("CONTEXT PROVIDER: invoking() → READ PATH")
        trace.info("─" * 50)

        msg_list = _to_list(messages)

        latest_user_text = None
        for msg in reversed(msg_list):
            role = getattr(msg, "role", None)
            role_val = role.value if hasattr(role, "value") else role
            if role_val == "user" and getattr(msg, "text", None):
                latest_user_text = str(msg.text)
                break

        if not latest_user_text:
            trace.info("No user message found, skipping search.")
            return Context(messages=None)

        trace.info(f"[MEM0 SEARCH] user_id: {self._user_id}")
        trace.info(f"[MEM0 SEARCH] query: {latest_user_text}")

        try:
            search_result = self._memory.search(
                query=latest_user_text,
                user_id=self._user_id,
                limit=self._max_results,
            )
            log_json("[MEM0 SEARCH] raw response", search_result)
        except Exception as exc:
            trace.error(f"[MEM0 SEARCH] FAILED: {exc!r}")
            print(f"[mem0] search failed: {exc!r}")
            return Context(messages=None)

        results = []
        if isinstance(search_result, dict) and "results" in search_result:
            results = search_result.get("results", []) or []
        elif isinstance(search_result, list):
            results = search_result

        trace.info(f"[MEM0 SEARCH] {len(results)} memories found")

        if not results:
            print("[mem0] search returned no memories.")
            return Context(messages=None)

        lines = []
        for idx, item in enumerate(results, start=1):
            memory_text = None
            score = item.get("score") if isinstance(item, dict) else None
            if isinstance(item, dict):
                memory_text = item.get("memory") or item.get("text") or item.get("content")
            if memory_text:
                lines.append(f"- [{idx}] {memory_text}")
                trace.info(f"  #{idx} (score={score}): {memory_text[:80]}..." if len(str(memory_text)) > 80 else f"  #{idx} (score={score}): {memory_text}")

        print("[mem0] retrieved memories:")
        for line in lines:
            print(f"  {line}")

        if not lines:
            return Context(messages=None)

        instructions = (
            "Relevant past incidents:\n"
            + "\n".join(lines)
            + "\n\nUse them as prior episodes when proposing a plan."
        )
        trace.info(f"[CONTEXT INJECTION] Injecting {len(lines)} memories as system message")
        return Context(messages=[ChatMessage(role="system", text=instructions)])

    async def invoked(
        self,
        request_messages: ChatMessage | Sequence[ChatMessage],
        response_messages: Optional[ChatMessage | Sequence[ChatMessage]] = None,
        invoke_exception: Optional[Exception] = None,
        **_: Any,
    ) -> None:
        """
        After each run, store the latest user/assistant exchange into Mem0 as a simple episodic memory.
        """
        trace.info("")
        trace.info("─" * 50)
        trace.info("CONTEXT PROVIDER: invoked() → WRITE PATH")
        trace.info("─" * 50)

        if invoke_exception:
            trace.error(f"Skipping storage due to exception: {invoke_exception!r}")
            print(f"[mem0] skipping add due to exception: {invoke_exception!r}")
            return

        last_user, last_assistant = _last_user_assistant_text(request_messages, response_messages)

        trace.info(f"[MEM0 ADD] user_id: {self._user_id}")
        trace.info(f"[MEM0 ADD] user msg: {last_user[:100]}..." if last_user and len(last_user) > 100 else f"[MEM0 ADD] user msg: {last_user}")
        trace.info(f"[MEM0 ADD] assistant msg: {last_assistant[:100]}..." if last_assistant and len(last_assistant) > 100 else f"[MEM0 ADD] assistant msg: {last_assistant}")

        if not last_user and not last_assistant:
            trace.warning("No messages to store.")
            print("[mem0] no user/assistant messages to store.")
            return

        combined_text = f"User: {last_user or ''}\nAssistant: {last_assistant or ''}".strip()
        metadata = {
            "source": "supply_chain_demo",
            "category": "incident_episode",
        }

        try:
            add_result = self._memory.add(messages=combined_text, user_id=self._user_id, metadata=metadata)
            log_json("[MEM0 ADD] result", add_result)
            print(f"[mem0] stored new memory for user_id={self._user_id}: {add_result}")
        except Exception as exc:
            trace.error(f"[MEM0 ADD] FAILED: {exc!r}")
            print(f"[mem0] add failed: {exc!r}")


async def run_scene_1(agent: ChatAgent) -> Any:
    """
    Scene 1: first incident, no prior memories.
    """
    log_section("SCENE 1: First incident (no memory yet)")
    print("\n=== Scene 1: first incident (no memory yet) ===")
    thread = agent.get_new_thread()
    initial_prompt = (
        "We have a 30% demand spike for SKU 123 at Plant A in week 12. "
        "Capacity is already at 95%. What options do we have?"
    )
    trace.info(f"[USER PROMPT] {initial_prompt}")
    trace.info("[LLM] Calling Azure OpenAI...")
    response = await agent.run(initial_prompt, thread=thread)
    trace.info(f"[LLM RESPONSE] {response.text}")
    print("[agent] response:", response.text)
    print("[scene 1] retrieved memories should be empty (see mem0 logs above).")
    return thread


async def run_scene_2(agent: ChatAgent, thread: Any, memory: Memory, user_id: str) -> None:
    """
    Scene 2: store the resolution playbook as a memory using the same thread.
    """
    log_section("SCENE 2: Storing the episode")
    print("\n=== Scene 2: storing the episode ===")
    follow_up = (
        "Let's allocate 10% to Plant B and cover the remaining 20% with weekend overtime at Plant A. "
        "Please remember this as the playbook for SKU 123 at Plant A."
    )
    trace.info(f"[USER PROMPT] {follow_up}")
    trace.info("[LLM] Calling Azure OpenAI...")
    response = await agent.run(follow_up, thread=thread)
    trace.info(f"[LLM RESPONSE] {response.text}")
    print("[agent] response:", response.text)
    print(f"[scene 2] Stored new memory in Mem0 for user_id={user_id} (see mem0 add log above).")

    # Verification search
    trace.info("[VERIFICATION] Confirming memory was stored...")
    try:
        verify = memory.search(query="playbook for SKU 123", user_id=user_id, limit=3)
        log_json("[VERIFICATION] search result", verify)
        print(f"[scene 2] verification search result: {verify}")
    except Exception as exc:
        trace.error(f"[VERIFICATION] failed: {exc!r}")
        print(f"[scene 2] verification search failed: {exc!r}")


async def run_scene_3(agent: ChatAgent) -> None:
    """
    Scene 3: new session/thread; Mem0 should provide the prior playbook via the context provider.
    """
    log_section("SCENE 3: New session (memory retrieval)")
    print("\n=== Scene 3: new session (memory retrieved) ===")
    new_thread = agent.get_new_thread()
    trace.info("Created NEW thread (simulating fresh session)")
    prompt = (
        "Plant A is again over capacity for SKU 123 due to a promo in week 20. "
        "Any proven playbook from earlier cases?"
    )
    trace.info(f"[USER PROMPT] {prompt}")
    trace.info("[LLM] Calling Azure OpenAI...")
    response = await agent.run(prompt, thread=new_thread)
    trace.info(f"[LLM RESPONSE] {response.text}")
    print("[agent] response:", response.text)
    print("[scene 3] Retrieved memories should appear above from mem0 context provider.")


async def main() -> None:
    """
    Run all three scenes sequentially to demonstrate Mem0-backed long-term memory.
    """
    log_section("DEMO STARTING")
    print(f"\n📝 Trace log: tail -f {LOG_FILE}\n")
    trace.info(f"Log file: {LOG_FILE}")

    memory = setup_mem0_memory()
    context_provider = create_mem0_context_provider(memory)
    agent = create_planner_agent(context_provider)

    try:
        thread = await run_scene_1(agent)
        await run_scene_2(agent, thread, memory, context_provider.user_id)
        await run_scene_3(agent)
    except ServiceResponseException as exc:
        print(
            "[error] Chat service call failed. Verify AZURE_OPENAI_DEPLOYMENT_NAME matches "
            "an actual chat deployment in your Azure resource, and AZURE_OPENAI_ENDPOINT is correct. Details:"
        )
        print(exc)


if __name__ == "__main__":
    asyncio.run(main())
