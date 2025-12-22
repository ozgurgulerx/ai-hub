"""
Delete a stored response chain and show that chaining is broken after deletion.
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
        input="Remember this: my favourite black hole is Sagittarius A*. Keep it short.",
        store=True,
    )
    print(f"[1] id={first.id}")
    print(first.output_text)

    delete_result = client.responses.delete(first.id)
    print(f"\n[Delete] {delete_result}")

    try:
        follow = client.responses.create(
            model=MODEL,
            input="Do you still remember which black hole I like?",
            previous_response_id=first.id,
            store=True,
        )
        print("\n[Follow-up after delete]")
        print(follow.output_text)
    except Exception as exc:
        print("\n[Expected failure after delete]")
        print(repr(exc))


if __name__ == "__main__":
    main()
