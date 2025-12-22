"""
Tag responses with metadata and user to align server memory with app-level IDs.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=f"{endpoint}/openai/v1/",
)
MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


def main() -> None:
    conversation_id = "demo-convo-physics"
    user_id = "user-ozgur"

    first = client.responses.create(
        model=MODEL,
        input="Start a short physics chat: explain event horizons in one sentence.",
        store=True,
        metadata={"conversation_id": conversation_id, "topic": "astrophysics"},
        user=user_id,
    )
    print(f"[1] id={first.id} metadata={first.metadata}")
    print(first.output_text)

    second = client.responses.create(
        model=MODEL,
        input="Now relate it to Sagittarius A* in two sentences.",
        previous_response_id=first.id,
        store=True,
        metadata={"conversation_id": conversation_id, "topic": "astrophysics"},
        user=user_id,
    )
    print(f"\n[2] id={second.id} metadata={second.metadata}")
    print(second.output_text)


if __name__ == "__main__":
    main()
