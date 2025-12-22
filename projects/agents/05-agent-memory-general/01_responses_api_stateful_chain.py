"""
Stateful chaining with previous_response_id (minimal).
Second call only sends new user text plus the first response ID.
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
    first = client.responses.create(
        model=MODEL,
        input="Remember this: my favourite black hole is Sagittarius A*. Explain briefly what it is.",
        store=True,
    )
    print(f"[1] id={first.id}")
    print(first.output_text)

    second = client.responses.create(
        model=MODEL,
        input="Remind me which black hole I like and why it's interesting, without repeating too much.",
        previous_response_id=first.id,
        store=True,
    )
    print(f"\n[2] id={second.id} (previous={first.id})")
    print(second.output_text)


if __name__ == "__main__":
    main()
