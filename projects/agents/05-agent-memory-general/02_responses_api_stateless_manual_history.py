"""
Stateless contrast: store=False and manual history replay.
We resend the whole history each turn instead of using previous_response_id.
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
    history = [
        {
            "role": "user",
            "content": "Remember this: my favourite black hole is Sagittarius A*. Explain briefly what it is.",
        }
    ]

    first = client.responses.create(model=MODEL, input=history, store=False)
    print(f"[1] id={first.id} (store=False)")
    print(first.output_text)

    # Append assistant reply locally so we can replay it next time.
    for item in first.output:
        if item.type == "message":
            text = item.content[0].text
            history.append({"role": item.role, "content": text})

    history.append(
        {
            "role": "user",
            "content": "Remind me which black hole I like and why it's interesting, without repeating too much.",
        }
    )

    second = client.responses.create(model=MODEL, input=history, store=False)
    print(f"\n[2] id={second.id} (store=False)")
    print(second.output_text)


if __name__ == "__main__":
    main()
