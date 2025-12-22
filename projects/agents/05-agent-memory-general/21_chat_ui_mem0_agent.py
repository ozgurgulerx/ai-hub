"""
21_chat_ui_mem0_agent.py

Interactive supply-chain planner copilot demo with long-term memory
(Mem0 + Azure AI Search) and agent-framework ChatAgent.

Key features:
- Mem0 open-source `Memory` configured with Azure AI Search + Azure OpenAI embeddings.
- Custom `Mem0EpisodeContextProvider` injects episodic memories before each turn
  and stores new ones after each run.
- Planner copilot ChatAgent (Azure OpenAI Responses client) is exposed via a
  simple terminal chat UI:
    - /new   : start a new thread (fresh session)
    - /exit  : quit
    - /quit  : quit
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
# TRACE LOGGING SETUP - writes to 21_trace.log for demo visibility
# Run: tail -f 21_trace.log in another terminal to watch live
# ─────────────────────────────────────────────────────────────────────────────
LOG_FILE = Path(__file__).with_name("21_trace.log")
LOG_FILE.write_text(f"=== Chat UI trace started at {datetime.now().isoformat()} ===\n\n")

trace = logging.getLogger("demo_trace")
trace.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
fh.setFormatter(logging.Formatter("%(asctime)s | %(message)s", datefmt="%H:%M:%S"))
trace.addHandler(fh)


def log_section(title: str) -> None:
    """
    Convenience helper to visually separate sections in the log file.
    """
    trace.info("")
    trace.info("=" * 70)
    trace.info(f"  {title}")
    trace.info("=" * 70)


def log_json(label: str, obj: Any) -> None:
    """
    Log an object as pretty-printed JSON for easier inspection.
    """
    try:
        formatted = json.dumps(obj, indent=2, default=str)
    except Exception:
        formatted = str(obj)
    trace.debug(f"{label}:\n{formatted}")


# ─────────────────────────────────────────────────────────────────────────────
# AGENT-FRAMEWORK + MEM0 IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
from agent_framework import ChatAgent, ChatMessage
from agent_framework._memory import Context, ContextProvider
from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework.exceptions import ServiceResponseException
from mem0 import Memory

# Load environment variables from .env (Azure + Mem0 settings)
load_dotenv()


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def require_env(name: str) -> str:
    """
    Fetch an environment variable or raise a clear error if missing.
    This keeps misconfigurations obvious.
    """
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_memory_config() -> dict[str, Any]:
    """
    Build the Mem0 configuration for Azure AI Search + Azure OpenAI embeddings.

    Assumptions (align with Mem0 Azure docs):
    - `vector_store.provider='azure_ai_search'` 
    - Keys: service_name, api_key, collection_name (index)
    - `embeddings.provider='azure_openai'` 
    - Keys: api_key, api_version, azure_endpoint, deployment_name
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
        raise RuntimeError(
            "Set AZURE_SEARCH_SERVICE_NAME or AZURE_SEARCH_ENDPOINT "
            "for Mem0 Azure AI Search config."
        )

    embedding_deployment = os.getenv("AZURE_TEXT_EMBEDDING_DEPLOYMENT_NAME") or os.getenv(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
    )
    if not embedding_deployment:
        raise RuntimeError("Set AZURE_TEXT_EMBEDDING_DEPLOYMENT_NAME for Mem0 embeddings.")

    collection_name = os.getenv("AZURE_SEARCH_COLLECTION_NAME") or require_env(
        "AZURE_SEARCH_INDEX_NAME"
    )
    
    # LLM deployment for fact extraction (Mem0 needs this to extract facts from messages)
    llm_deployment = require_env("AZURE_OPENAI_DEPLOYMENT_NAME")

    return {
        "llm": {
            "provider": "azure_openai",
            "config": {
                "model": llm_deployment,
                "temperature": 0.1,
                "max_tokens": 2000,
                "azure_kwargs": {
                    "azure_deployment": llm_deployment,
                    "api_version": require_env("AZURE_OPENAI_API_VERSION"),
                    "azure_endpoint": require_env("AZURE_OPENAI_ENDPOINT"),
                    "api_key": require_env("AZURE_OPENAI_API_KEY"),
                },
            },
        },
        "vector_store": {
            "provider": "azure_ai_search",
            "config": {
                "service_name": service_name,
                "api_key": require_env("AZURE_SEARCH_ADMIN_KEY"),
                # Mem0 Azure AI Search expects `collection_name` (index name).
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

    Priority:
    - MEM0_DEMO_USER_ID
    - MEM0_USER_ID
    - fallback: 'user-ozgur'
    """
    return os.getenv("MEM0_DEMO_USER_ID") or os.getenv("MEM0_USER_ID") or "user-ozgur"


def create_mem0_context_provider(memory: Memory) -> "Mem0EpisodeContextProvider":
    """
    Wire up the Mem0EpisodeContextProvider with the configured Memory and demo user id.
    """
    user_id = resolve_user_id()
    return Mem0EpisodeContextProvider(
        memory=memory,
        user_id=user_id,
        max_results=int(os.getenv("MEM0_MAX_RESULTS", "3")),
        min_score=float(os.getenv("MEM0_MIN_SCORE", "0.0")),
    )


def create_planner_agent(context_provider: "Mem0EpisodeContextProvider") -> ChatAgent:
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
            "You are a supply chain planning copilot. You help planners resolve over-capacity "
            "issues and demand spikes. You may receive additional 'episodic memories' about "
            "past incidents; use them when relevant."
        ),
        context_providers=[context_provider],
    )
    return agent


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS FOR MESSAGE HANDLING
# ─────────────────────────────────────────────────────────────────────────────
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
    Extract the latest user and assistant text payloads from a run.
    """
    all_msgs: List[ChatMessage] = _to_list(request_messages)
    if response_messages:
        all_msgs.extend(_to_list(response_messages))

    last_user = None
    last_assistant = None
    for msg in reversed(all_msgs):
        role = getattr(msg, "role", None)
        role_val = role.value if hasattr(role, "value") else role
        if role_val == "assistant" and last_assistant is None and getattr(
            msg, "text", None
        ):
            last_assistant = str(msg.text)
        if role_val == "user" and last_user is None and getattr(msg, "text", None):
            last_user = str(msg.text)
        if last_user and last_assistant:
            break
    return last_user, last_assistant


# ─────────────────────────────────────────────────────────────────────────────
# MEM0 CONTEXT PROVIDER
# ─────────────────────────────────────────────────────────────────────────────
class Mem0EpisodeContextProvider(ContextProvider):
    """
    ContextProvider that pulls episodic memories from Mem0 before each run
    and stores new incidents after each run.

    READ path (invoking):
        - Look at latest user message in the current agent run.
        - Call Mem0.search(query=latest_user_text, user_id=...).
        - Inject retrieved memories as a system message.

    WRITE path (invoked):
        - Combine latest user + assistant messages into a single text.
        - Add as a new memory to Mem0.add(..., user_id=..., metadata=...).
    """

    def __init__(
        self,
        memory: Memory,
        user_id: str,
        max_results: int = 3,
        min_score: float = 0.0,
    ) -> None:
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

    # ──────────────────────── READ PATH ────────────────────────
    async def invoking(
        self,
        messages: ChatMessage | Iterable[ChatMessage],
        **_: Any,
    ) -> Context:
        """
        Before each run, fetch relevant memories for the latest user text
        and inject them as system instructions.
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
            trace.info("No user message found, skipping Mem0 search.")
            return Context(messages=None)

        trace.info(f"[MEM0 SEARCH] user_id: {self._user_id}")
        trace.info(f"[MEM0 SEARCH] query: {latest_user_text}")

        # Call Mem0 search
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

        # Normalize search_result into a list of documents
        results = []
        if isinstance(search_result, dict) and "results" in search_result:
            results = search_result.get("results", []) or []
        elif isinstance(search_result, list):
            results = search_result

        trace.info(f"[MEM0 SEARCH] {len(results)} memories found")

        if not results:
            print("[mem0] search returned no memories.")
            return Context(messages=None)

        # Build a textual summary of retrieved memories
        lines = []
        for idx, item in enumerate(results, start=1):
            memory_text = None
            score = item.get("score") if isinstance(item, dict) else None
            if isinstance(item, dict):
                memory_text = (
                    item.get("memory")
                    or item.get("text")
                    or item.get("content")
                )
            if memory_text:
                line = f"- [{idx}] {memory_text}"
                lines.append(line)
                if len(str(memory_text)) > 80:
                    trace.info(
                        f"  #{idx} (score={score}): {memory_text[:80]}..."
                    )
                else:
                    trace.info(f"  #{idx} (score={score}): {memory_text}")

        print("[mem0] retrieved memories:")
        for line in lines:
            print(f"  {line}")

        if not lines:
            return Context(messages=None)

        # Inject as a single system message
        instructions = (
            "Relevant past incidents:\n"
            + "\n".join(lines)
            + "\n\nUse them as prior episodes when proposing a plan."
        )
        trace.info(
            f"[CONTEXT INJECTION] Injecting {len(lines)} memories as system message"
        )
        return Context(messages=[ChatMessage(role="system", text=instructions)])

    # ──────────────────────── WRITE PATH ────────────────────────
    async def invoked(
        self,
        request_messages: ChatMessage | Sequence[ChatMessage],
        response_messages: Optional[ChatMessage | Sequence[ChatMessage]] = None,
        invoke_exception: Optional[Exception] = None,
        **_: Any,
    ) -> None:
        """
        After each run, store the latest user/assistant exchange into Mem0.
        """
        trace.info("")
        trace.info("─" * 50)
        trace.info("CONTEXT PROVIDER: invoked() → WRITE PATH")
        trace.info("─" * 50)

        if invoke_exception:
            trace.error(f"Skipping storage due to exception: {invoke_exception!r}")
            print(f"[mem0] skipping add due to exception: {invoke_exception!r}")
            return

        last_user, last_assistant = _last_user_assistant_text(
            request_messages, response_messages
        )

        trace.info(f"[MEM0 ADD] user_id: {self._user_id}")
        trace.info(
            f"[MEM0 ADD] user msg: {last_user[:100]}..."
            if last_user and len(last_user) > 100
            else f"[MEM0 ADD] user msg: {last_user}"
        )
        trace.info(
            f"[MEM0 ADD] assistant msg: {last_assistant[:100]}..."
            if last_assistant and len(last_assistant) > 100
            else f"[MEM0 ADD] assistant msg: {last_assistant}"
        )

        if not last_user and not last_assistant:
            trace.warning("No messages to store.")
            print("[mem0] no user/assistant messages to store.")
            return

        combined_text = f"User: {last_user or ''}\nAssistant: {last_assistant or ''}".strip()
        metadata = {
            "source": "supply_chain_chat_ui",
            "category": "incident_episode",
        }

        try:
            add_result = self._memory.add(
                messages=combined_text,
                user_id=self._user_id,
                metadata=metadata,
            )
            log_json("[MEM0 ADD] result", add_result)
            print(
                f"[mem0] stored new memory for user_id={self._user_id}: {add_result}"
            )
        except Exception as exc:
            trace.error(f"[MEM0 ADD] FAILED: {exc!r}")
            print(f"[mem0] add failed: {exc!r}")


# ─────────────────────────────────────────────────────────────────────────────
# SIMPLE TERMINAL CHAT UI
# ─────────────────────────────────────────────────────────────────────────────
async def chat_loop(agent: ChatAgent) -> None:
    """
    Very simple terminal chat loop over a single agent.

    Features:
    - Maintains an agent-framework thread for conversation context.
    - /new   : start a new thread (fresh session, but same Mem0 long-term memory)
    - /exit  : quit
    - /quit  : quit
    """
    log_section("CHAT UI START")
    print(f"\n📝 Trace log: tail -f {LOG_FILE}\n")
    print("Supply-chain planner copilot (Mem0 + Azure AI Search)")
    print("Commands:")
    print("  /new   → start a new session (new thread)")
    print("  /exit  → exit")
    print("  /quit  → exit")
    print("Type your message and press Enter.\n")

    # Create initial thread
    current_thread = agent.get_new_thread()
    trace.info("Created initial thread for chat UI.")

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[system] Exiting chat.")
            break

        if not user_input:
            # ignore empty lines
            continue

        # Handle simple meta-commands
        if user_input.lower() in ("/exit", "/quit"):
            print("[system] Goodbye.")
            break

        if user_input.lower() == "/new":
            # Start a fresh thread; Mem0 episode provider will still reuse long-term memory.
            current_thread = agent.get_new_thread()
            log_section("NEW THREAD CREATED (user command /new)")
            print("[system] Started a new session (new thread).")
            continue

        # Send the message to the agent
        trace.info(f"[USER PROMPT] {user_input}")
        trace.info("[LLM] Calling Azure OpenAI via agent-framework...")
        try:
            # We can pass the user text directly; agent-framework will wrap as ChatMessage internally.
            response = await agent.run(user_input, thread=current_thread)
        except ServiceResponseException as exc:
            print(
                "[error] Chat service call failed. Verify AZURE_OPENAI_DEPLOYMENT_NAME "
                "matches an actual chat deployment and AZURE_OPENAI_ENDPOINT is correct."
            )
            print(exc)
            trace.error(f"[LLM ERROR] {exc!r}")
            continue

        answer = response.text
        trace.info(f"[LLM RESPONSE] {answer}")
        print(f"agent> {answer}\n")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRYPOINT
# ─────────────────────────────────────────────────────────────────────────────
async def main() -> None:
    """
    Entry point: initialize Mem0, ContextProvider, ChatAgent, then start chat loop.
    """
    log_section("DEMO STARTING")
    trace.info(f"Log file: {LOG_FILE}")

    memory = setup_mem0_memory()
    context_provider = create_mem0_context_provider(memory)
    agent = create_planner_agent(context_provider)

    try:
        await chat_loop(agent)
    except ServiceResponseException as exc:
        print(
            "[error] Chat service initialization failed. "
            "Check your Azure OpenAI config. Details:"
        )
        print(exc)


if __name__ == "__main__":
    asyncio.run(main())
