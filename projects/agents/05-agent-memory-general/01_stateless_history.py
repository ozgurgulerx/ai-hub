"""
Baseline “stateless DIY history” using the Responses API (Azure-style config).

We maintain our own `messages` list (user/assistant turns) and resend it on
every `responses.create` call. This gives us conversation memory, but we must
manage token growth and truncation ourselves.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")  # Deployment name acts as the model identifier.


def make_client() -> OpenAI:
    """
    Construct an OpenAI client from Azure environment variables.
    """
    return OpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        base_url=f"{endpoint}/openai/v1/",
    )


def extract_text(response: Any) -> str:
    """
    Pull the assistant text from a Responses API result.

    The Responses API returns `output` blocks; we join any text content for display.
    """
    chunks: List[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            # `text` is the usual field for natural-language output.
            text_value = getattr(content, "text", None)
            if isinstance(text_value, dict) and "value" in text_value:
                text_value = text_value["value"]
            if text_value:
                chunks.append(str(text_value))
    return "\n".join(chunks).strip()


def main() -> None:
    client = make_client()

    # This list is our manual "memory". We append every turn here.
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Give me a two-bullet overview of graph machine learning."},
    ]

    # First call: we send the full history (system + first user).
    first = client.responses.create(model=MODEL, input=messages)
    first_text = extract_text(first)
    print(f"[1] response.id={first.id}")
    print(first_text)

    # Append the assistant reply to our local history so the next call has context.
    messages.append({"role": "assistant", "content": first_text})

    # Second user turn. We continue to grow the history list manually.
    messages.append({"role": "user", "content": "Now compare it to knowledge graphs in one sentence."})

    # For safety, demonstrate truncation: keep only the last 4 items (system + 3 recent turns).
    truncated_history = messages[-4:]
    print("\n[Debug] Truncated history we will send:")
    for msg in truncated_history:
        print(f"  - {msg['role']}: {msg['content']}")

    second = client.responses.create(model=MODEL, input=truncated_history)
    second_text = extract_text(second)
    print(f"\n[2] response.id={second.id}")
    print(second_text)

    print(
        "\nMemory takeaway: we controlled context by resending our own `messages` list "
        "and manually truncating to stay within token limits."
    )


if __name__ == "__main__":
    main()
