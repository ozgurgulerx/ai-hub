"""
22_intent_aware_mem0_agent.py

Intent-Aware Supply Chain Planner with Context-Specific Long-Term Memory

This demo shows how to:
1. DETECT INTENT from user message + conversation history (optimization vs forecasting)
2. STORE memories with metadata tags (category: optimization | forecasting | general)
3. RETRIEVE memories filtered by detected intent using Mem0 metadata filters

Architecture:
┌──────────────────────────────────────────────────────────────────────────────┐
│                           User Message                                       │
│                               │                                              │
│                               ▼                                              │
│                    ┌─────────────────────┐                                   │
│                    │   Intent Detector   │  ◄─── Short-term memory (thread)  │
│                    │  (keyword + history)│       helps detect context        │
│                    └─────────────────────┘                                   │
│                               │                                              │
│              ┌────────────────┼────────────────┐                             │
│              ▼                ▼                ▼                             │
│        OPTIMIZATION      FORECASTING       GENERAL                          │
│              │                │                │                             │
│              ▼                ▼                ▼                             │
│    ┌─────────────────────────────────────────────────────────┐              │
│    │              Mem0 Search with Metadata Filter           │              │
│    │   filters={"category": "optimization"}                  │              │
│    │   filters={"category": "forecasting"}                   │              │
│    │   (or no filter for general)                            │              │
│    └─────────────────────────────────────────────────────────┘              │
│                               │                                              │
│                               ▼                                              │
│                    Context-Specific Memories                                 │
│                               │                                              │
│                               ▼                                              │
│                    ┌─────────────────────┐                                   │
│                    │      ChatAgent      │                                   │
│                    │  (planner-copilot)  │                                   │
│                    └─────────────────────┘                                   │
│                               │                                              │
│                               ▼                                              │
│                    Context-Aware Response                                    │
└──────────────────────────────────────────────────────────────────────────────┘

Demo Scenario:
- User discusses OPTIMIZATION → memories about capacity planning, resource allocation
- User discusses FORECASTING → memories about demand prediction, seasonal trends
- System stores each conversation with appropriate category metadata
- On recall, only relevant memories are retrieved based on detected intent

Usage:
    python 22_intent_aware_mem0_agent.py

Commands:
    /new   - Start a new session (new thread)
    /exit  - Exit
    /quit  - Exit
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, List, Optional, Sequence, Tuple

from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# TRACE LOGGING SETUP
# ─────────────────────────────────────────────────────────────────────────────
LOG_FILE = Path(__file__).with_name("22_trace.log")
LOG_FILE.write_text(f"=== Intent-Aware Demo started at {datetime.now().isoformat()} ===\n\n")

trace = logging.getLogger("intent_demo_trace")
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


# ─────────────────────────────────────────────────────────────────────────────
# AGENT-FRAMEWORK + MEM0 IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
from agent_framework import ChatAgent, ChatMessage
from agent_framework._memory import Context, ContextProvider
from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework.exceptions import ServiceResponseException
from mem0 import Memory

load_dotenv()


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG HELPER (needed early for intent classifier)
# ─────────────────────────────────────────────────────────────────────────────
def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


# ─────────────────────────────────────────────────────────────────────────────
# INTENT CLASSIFICATION (LLM-BASED)
# ─────────────────────────────────────────────────────────────────────────────
class Intent(Enum):
    OPTIMIZATION = "optimization"
    FORECASTING = "forecasting"
    GENERAL = "general"


# We'll lazily initialize the agents
_intent_classifier_agent = None
_fact_extractor_agent = None


def _get_intent_classifier_agent():
    """
    Get or create a classifier agent using AzureOpenAIResponsesClient.
    This uses the same API as the main agent (Responses API, not Chat Completions).
    """
    global _intent_classifier_agent
    if _intent_classifier_agent is None:
        client = AzureOpenAIResponsesClient(
            endpoint=require_env("AZURE_OPENAI_ENDPOINT"),
            deployment_name=require_env("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=require_env("AZURE_OPENAI_API_KEY"),
            api_version=require_env("AZURE_OPENAI_API_VERSION"),
        )
        _intent_classifier_agent = client.create_agent(
            name="intent-classifier",
            instructions="""You are an intent classifier for a supply chain planning system.

Classify the user's intent into exactly ONE of these categories:
- OPTIMIZATION: Questions about capacity planning, resource allocation, scheduling, efficiency, 
  plant/warehouse operations, cost reduction, bottlenecks, throughput, shift planning, overtime.
- FORECASTING: Questions about demand prediction, trend analysis, seasonal patterns, sales projections,
  promotional impact, market outlook, historical patterns, growth/decline estimates.
- GENERAL: Everything else, including greetings, off-topic questions, unclear intent.

Consider the full conversation context, not just the last message.

Respond with ONLY one word: OPTIMIZATION, FORECASTING, or GENERAL""",
        )
    return _intent_classifier_agent


def _get_fact_extractor_agent():
    """
    Get or create a fact extractor agent using AzureOpenAIResponsesClient.
    This extracts memorable facts from conversations (replaces Mem0's internal LLM).
    """
    global _fact_extractor_agent
    if _fact_extractor_agent is None:
        client = AzureOpenAIResponsesClient(
            endpoint=require_env("AZURE_OPENAI_ENDPOINT"),
            deployment_name=require_env("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=require_env("AZURE_OPENAI_API_KEY"),
            api_version=require_env("AZURE_OPENAI_API_VERSION"),
        )
        _fact_extractor_agent = client.create_agent(
            name="fact-extractor",
            instructions="""You are a fact extractor for a supply chain planning memory system.

Extract key facts, preferences, decisions, and actionable information from conversations.
Focus on:
- User preferences and decisions
- Specific numbers, percentages, quantities
- Named entities (plants, SKUs, locations)
- Action items and playbooks
- Business rules and constraints

Return ONLY a JSON array of fact strings. Each fact should be a complete, standalone statement.
If no meaningful facts can be extracted, return an empty array: []

Example output:
["User plans to shift 10% of SKU 123 production to Plant B", "Weekend overtime is authorized for capacity issues"]""",
        )
    return _fact_extractor_agent


async def extract_facts(conversation_text: str) -> list[str]:
    """
    Extract facts from conversation using Responses API.
    Returns a list of fact strings.
    """
    try:
        extractor = _get_fact_extractor_agent()
        prompt = f"Extract facts from this conversation:\n\n{conversation_text}\n\nReturn ONLY a JSON array of fact strings:"
        response = await extractor.run(prompt)
        
        result_text = response.text.strip()
        trace.info(f"[FACT EXTRACTOR] Raw response: {result_text[:200]}...")
        
        # Parse JSON array
        import json
        # Handle markdown code blocks
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
            result_text = result_text.strip()
        
        facts = json.loads(result_text)
        if isinstance(facts, list):
            return [str(f) for f in facts if f]
        return []
    except Exception as exc:
        trace.error(f"[FACT EXTRACTOR] Failed: {exc!r}")
        return []


async def detect_intent(
    current_message: str,
    conversation_history: List[ChatMessage],
) -> Intent:
    """
    Detect intent using an LLM call with conversation history as context.
    
    This sends the recent conversation to Azure OpenAI (Responses API) to classify the intent.
    The conversation history (short-term memory) helps detect context when
    the current message is ambiguous (e.g., "what about last month?").
    """
    trace.info("")
    trace.info("─" * 50)
    trace.info("INTENT DETECTION (LLM-based)")
    trace.info("─" * 50)
    
    # Build conversation context for the classifier
    context_messages = []
    
    # Add recent conversation history (last 6 messages for context)
    # Skip the last message if it matches current_message (avoid duplication)
    for msg in conversation_history[-6:]:
        role = getattr(msg, "role", None)
        role_val = role.value if hasattr(role, "value") else role
        text = getattr(msg, "text", None)
        if text and role_val in ("user", "assistant"):
            # Skip if this is the current message (already in history)
            if role_val == "user" and str(text) == current_message:
                continue
            context_messages.append(f"{role_val.upper()}: {text}")
    
    # Add current message (always last)
    context_messages.append(f"USER: {current_message}")
    
    conversation_context = "\n".join(context_messages)
    
    trace.info(f"[LLM CLASSIFIER] Context ({len(context_messages)} messages):")
    trace.debug(f"\n{conversation_context}")
    
    # Call LLM for classification using Responses API
    try:
        classifier = _get_intent_classifier_agent()
        
        # Use a fresh thread for each classification (stateless)
        prompt = f"Conversation:\n{conversation_context}\n\nClassify the intent (respond with ONE word: OPTIMIZATION, FORECASTING, or GENERAL):"
        response = await classifier.run(prompt)
        
        result = response.text.strip().upper()
        trace.info(f"[LLM CLASSIFIER] Raw response: {result}")
        
        # Parse response
        if "OPTIMIZATION" in result:
            intent = Intent.OPTIMIZATION
        elif "FORECASTING" in result:
            intent = Intent.FORECASTING
        else:
            intent = Intent.GENERAL
        
        trace.info(f"[LLM CLASSIFIER] Detected intent: {intent.value}")
        return intent
        
    except Exception as exc:
        trace.error(f"[LLM CLASSIFIER] Failed: {exc!r}, defaulting to GENERAL")
        print(f"[intent] Classification failed: {exc!r}, using GENERAL")
        return Intent.GENERAL


# ─────────────────────────────────────────────────────────────────────────────
# CONFIG HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def build_memory_config() -> dict[str, Any]:
    service_name = os.getenv("AZURE_SEARCH_SERVICE_NAME")
    if not service_name:
        endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "")
        if endpoint.startswith("https://"):
            endpoint = endpoint[len("https://"):]
        if endpoint:
            service_name = endpoint.split(".search.windows.net")[0].split(".")[0]
    if not service_name:
        raise RuntimeError("Set AZURE_SEARCH_SERVICE_NAME or AZURE_SEARCH_ENDPOINT")

    embedding_deployment = os.getenv("AZURE_TEXT_EMBEDDING_DEPLOYMENT_NAME") or os.getenv(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
    )
    if not embedding_deployment:
        raise RuntimeError("Set AZURE_TEXT_EMBEDDING_DEPLOYMENT_NAME for embeddings.")

    collection_name = os.getenv("AZURE_SEARCH_COLLECTION_NAME") or require_env("AZURE_SEARCH_INDEX_NAME")
    
    # NOTE: We removed the "llm" config because:
    # 1. gpt-5-nano uses Responses API, not Chat Completions API
    # 2. Mem0's azure_openai provider doesn't support Responses API
    # 3. We do our own fact extraction using extract_facts() with AzureOpenAIResponsesClient

    return {
        "vector_store": {
            "provider": "azure_ai_search",
            "config": {
                "service_name": service_name,
                "api_key": require_env("AZURE_SEARCH_ADMIN_KEY"),
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
    log_section("INITIALIZING MEM0")
    config = build_memory_config()
    trace.info(f"Vector store: {config['vector_store']['provider']}")
    trace.info(f"Collection/Index: {config['vector_store']['config']['collection_name']}")
    memory = Memory.from_config(config)
    trace.info("Mem0 Memory initialized successfully.")
    return memory


def resolve_user_id() -> str:
    return os.getenv("MEM0_DEMO_USER_ID") or os.getenv("MEM0_USER_ID") or "user-ozgur"


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def _to_list(messages: ChatMessage | Iterable[ChatMessage]) -> List[ChatMessage]:
    if isinstance(messages, ChatMessage):
        return [messages]
    return list(messages)


def _last_user_assistant_text(
    request_messages: ChatMessage | Sequence[ChatMessage],
    response_messages: Optional[ChatMessage | Sequence[ChatMessage]],
) -> Tuple[Optional[str], Optional[str]]:
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


# ─────────────────────────────────────────────────────────────────────────────
# INTENT-AWARE MEM0 CONTEXT PROVIDER
# ─────────────────────────────────────────────────────────────────────────────
class IntentAwareMem0Provider(ContextProvider):
    """
    Context provider that:
    1. Detects intent from user message + conversation history
    2. Searches Mem0 with metadata filters based on detected intent
    3. Stores new memories with appropriate category metadata
    
    This enables context-specific memory retrieval:
    - Optimization queries → retrieve optimization-related memories
    - Forecasting queries → retrieve forecasting-related memories
    """

    def __init__(
        self,
        memory: Memory,
        user_id: str,
        max_results: int = 3,
    ) -> None:
        super().__init__()
        self._memory = memory
        self._base_user_id = user_id  # Base user ID (e.g., "user-ozgur")
        self._max_results = max_results
        self._last_detected_intent: Intent = Intent.GENERAL

    @property
    def user_id(self) -> str:
        return self._base_user_id

    @property
    def last_intent(self) -> Intent:
        return self._last_detected_intent

    def _get_user_id_for_intent(self, intent: Intent) -> str:
        """
        Get intent-specific user_id for memory segmentation.
        
        This allows filtering by intent without needing filterable metadata fields:
        - OPTIMIZATION → user-ozgur-optimization
        - FORECASTING  → user-ozgur-forecasting  
        - GENERAL      → user-ozgur
        """
        if intent == Intent.OPTIMIZATION:
            return f"{self._base_user_id}-optimization"
        elif intent == Intent.FORECASTING:
            return f"{self._base_user_id}-forecasting"
        else:
            return self._base_user_id

    async def invoking(
        self,
        messages: ChatMessage | Iterable[ChatMessage],
        **_: Any,
    ) -> Context:
        """
        READ PATH: Detect intent, then search Mem0 with metadata filter.
        """
        trace.info("")
        trace.info("─" * 50)
        trace.info("CONTEXT PROVIDER: invoking() → READ PATH")
        trace.info("─" * 50)

        msg_list = _to_list(messages)

        # Find latest user message
        latest_user_text = None
        for msg in reversed(msg_list):
            role = getattr(msg, "role", None)
            role_val = role.value if hasattr(role, "value") else role
            if role_val == "user" and getattr(msg, "text", None):
                latest_user_text = str(msg.text)
                break

        if not latest_user_text:
            trace.info("No user message found, skipping.")
            return Context(messages=None)

        # ─────────────────────────────────────────────────────────────────────
        # STEP 1: Detect intent using current message + conversation history
        # ─────────────────────────────────────────────────────────────────────
        self._last_detected_intent = await detect_intent(latest_user_text, msg_list)
        intent = self._last_detected_intent

        print(f"[intent] Detected: {intent.value.upper()}")

        # ─────────────────────────────────────────────────────────────────────
        # STEP 2: Search Mem0 using intent-specific user_id (USER ID SEGMENTATION)
        # ─────────────────────────────────────────────────────────────────────
        search_user_id = self._get_user_id_for_intent(intent)
        
        trace.info(f"[MEM0 SEARCH] base_user_id: {self._base_user_id}")
        trace.info(f"[MEM0 SEARCH] search_user_id: {search_user_id}  ← segmented by intent!")
        trace.info(f"[MEM0 SEARCH] query: {latest_user_text}")

        try:
            # Search using intent-specific user_id (no metadata filter needed)
            search_result = self._memory.search(
                query=latest_user_text,
                user_id=search_user_id,
                limit=self._max_results,
            )
            log_json("[MEM0 SEARCH] raw response", search_result)

        except Exception as exc:
            trace.error(f"[MEM0 SEARCH] FAILED: {exc!r}")
            print(f"[mem0] search failed: {exc!r}")
            return Context(messages=None)

        # Parse results
        results = []
        if isinstance(search_result, dict) and "results" in search_result:
            results = search_result.get("results", []) or []
        elif isinstance(search_result, list):
            results = search_result

        trace.info(f"[MEM0 SEARCH] {len(results)} memories found")

        if not results:
            print(f"[mem0] No {intent.value} memories found.")
            return Context(messages=None)

        # Build context injection
        lines = []
        for idx, item in enumerate(results, start=1):
            memory_text = None
            score = item.get("score") if isinstance(item, dict) else None
            cat = item.get("metadata", {}).get("category", "unknown") if isinstance(item, dict) else "unknown"
            if isinstance(item, dict):
                memory_text = item.get("memory") or item.get("text") or item.get("content")
            if memory_text:
                lines.append(f"- [{idx}] ({cat}) {memory_text}")
                trace.info(f"  #{idx} (score={score}, category={cat}): {memory_text[:60]}...")

        print(f"[mem0] Retrieved {len(lines)} {intent.value} memories:")
        for line in lines:
            print(f"  {line[:100]}...")

        if not lines:
            return Context(messages=None)

        # Inject with intent-specific framing
        if intent == Intent.OPTIMIZATION:
            prefix = "Relevant OPTIMIZATION memories (capacity planning, resource allocation):\n"
        elif intent == Intent.FORECASTING:
            prefix = "Relevant FORECASTING memories (demand prediction, trends):\n"
        else:
            prefix = "Relevant memories from past incidents:\n"

        instructions = prefix + "\n".join(lines) + "\n\nUse these as context when responding."
        trace.info(f"[CONTEXT INJECTION] Injecting {len(lines)} memories with {intent.value} framing")

        return Context(messages=[ChatMessage(role="system", text=instructions)])

    async def invoked(
        self,
        request_messages: ChatMessage | Sequence[ChatMessage],
        response_messages: Optional[ChatMessage | Sequence[ChatMessage]] = None,
        invoke_exception: Optional[Exception] = None,
        **_: Any,
    ) -> None:
        """
        WRITE PATH: Store the conversation with category metadata based on last detected intent.
        """
        trace.info("")
        trace.info("─" * 50)
        trace.info("CONTEXT PROVIDER: invoked() → WRITE PATH")
        trace.info("─" * 50)

        if invoke_exception:
            trace.error(f"Skipping storage due to exception: {invoke_exception!r}")
            return

        last_user, last_assistant = _last_user_assistant_text(request_messages, response_messages)

        if not last_user and not last_assistant:
            trace.warning("No messages to store.")
            return

        # ─────────────────────────────────────────────────────────────────────
        # STEP 3: Store using intent-specific user_id (simple, like file 21)
        # ─────────────────────────────────────────────────────────────────────
        intent = self._last_detected_intent
        store_user_id = self._get_user_id_for_intent(intent)
        
        # Simple: just store the user message (the key info to remember)
        # Mem0 will embed and store it directly
        memory_text = last_user or ''
        
        metadata = {
            "source": "intent_aware_demo",
            "category": intent.value,
        }

        trace.info(f"[MEM0 ADD] store_user_id: {store_user_id}")
        trace.info(f"[MEM0 ADD] intent: {intent.value}")
        trace.info(f"[MEM0 ADD] text: {memory_text[:100]}...")

        try:
            add_result = self._memory.add(
                messages=memory_text,
                user_id=store_user_id,
                metadata=metadata,
            )
            log_json("[MEM0 ADD] result", add_result)
            print(f"[mem0] Stored as '{intent.value}' (user_id: {store_user_id})")
        except Exception as exc:
            trace.error(f"[MEM0 ADD] FAILED: {exc!r}")
            print(f"[mem0] add failed: {exc!r}")


# ─────────────────────────────────────────────────────────────────────────────
# AGENT SETUP
# ─────────────────────────────────────────────────────────────────────────────
def create_planner_agent(context_provider: IntentAwareMem0Provider) -> ChatAgent:
    log_section("CREATING PLANNER AGENT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not deployment:
        raise RuntimeError("Set AZURE_OPENAI_DEPLOYMENT_NAME for the chat model.")

    trace.info(f"LLM Deployment: {deployment}")
    print(f"[config] Using deployment: {deployment}")

    client = AzureOpenAIResponsesClient(
        endpoint=require_env("AZURE_OPENAI_ENDPOINT"),
        deployment_name=deployment,
        api_key=require_env("AZURE_OPENAI_API_KEY"),
        api_version=require_env("AZURE_OPENAI_API_VERSION"),
    )

    agent = client.create_agent(
        name="intent-aware-planner",
        instructions=(
            "You are a supply chain planning copilot with expertise in two areas:\n\n"
            "1. OPTIMIZATION: Capacity planning, resource allocation, scheduling, "
            "cost reduction, efficiency improvements, plant/warehouse operations.\n\n"
            "2. FORECASTING: Demand prediction, trend analysis, seasonal patterns, "
            "promotional impact, sales projections, market outlook.\n\n"
            "When you receive context about past incidents, use that domain-specific "
            "knowledge to provide more relevant recommendations. Adapt your response "
            "style based on whether the user is asking about optimization or forecasting."
        ),
        context_providers=[context_provider],
    )
    return agent


# ─────────────────────────────────────────────────────────────────────────────
# CHAT LOOP
# ─────────────────────────────────────────────────────────────────────────────
async def chat_loop(agent: ChatAgent) -> None:
    log_section("CHAT UI START")
    print(f"\n📝 Trace log: tail -f {LOG_FILE}\n")
    print("=" * 60)
    print("  INTENT-AWARE Supply Chain Planner")
    print("  (Mem0 + Azure AI Search with Metadata Filtering)")
    print("=" * 60)
    print("\nThe system detects your intent (OPTIMIZATION vs FORECASTING)")
    print("and retrieves context-specific memories.\n")
    print("Commands:")
    print("  /new   → start a new session")
    print("  /exit  → exit")
    print("\nTry these example conversations:\n")
    print("  OPTIMIZATION: 'Plant A is at 95% capacity. How can we optimize?'")
    print("  FORECASTING:  'What's the demand forecast for Q4?'")
    print()

    current_thread = agent.get_new_thread()
    trace.info("Created initial thread.")

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[system] Exiting.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/exit", "/quit"):
            print("[system] Goodbye.")
            break

        if user_input.lower() == "/new":
            current_thread = agent.get_new_thread()
            log_section("NEW THREAD (user command /new)")
            print("[system] Started new session. Long-term memories persist.")
            continue

        trace.info(f"[USER PROMPT] {user_input}")
        trace.info("[LLM] Calling Azure OpenAI...")

        try:
            response = await agent.run(user_input, thread=current_thread)
        except ServiceResponseException as exc:
            print(f"[error] LLM call failed: {exc}")
            trace.error(f"[LLM ERROR] {exc!r}")
            continue

        trace.info(f"[LLM RESPONSE] {response.text}")
        print(f"\nagent> {response.text}\n")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
async def main() -> None:
    log_section("DEMO STARTING")
    trace.info(f"Log file: {LOG_FILE}")

    memory = setup_mem0_memory()
    context_provider = IntentAwareMem0Provider(
        memory=memory,
        user_id=resolve_user_id(),
        max_results=int(os.getenv("MEM0_MAX_RESULTS", "3")),
    )
    agent = create_planner_agent(context_provider)

    try:
        await chat_loop(agent)
    except ServiceResponseException as exc:
        print(f"[error] Initialization failed: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
