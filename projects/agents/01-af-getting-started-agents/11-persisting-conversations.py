# 12-restoring-conversation-history-from-file.py
import os, sys, json, asyncio
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIResponsesClient

load_dotenv()

async def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python 12-restoring-conversation-history-from-file.py /path/to/agent_thread_*.json")

    path = sys.argv[1]
    # tolerant read (handles BOM) + quick sanity
    with open(path, "r", encoding="utf-8-sig") as f:
        text = f.read()
    if not text.strip():
        raise ValueError(f"File is empty: {path}")
    try:
        saved = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}") from e

    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "v1"),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    ).create_agent(
        name="physicsbot",
        instructions="You are professor in astrophysics",
    )

    thread = await agent.deserialize_thread(saved)
    prior = len(saved.get("messages", [])) if isinstance(saved, dict) else 0
    print(f"🧠 restored {prior} prior message(s) from: {path}")

    r = await agent.run("Continue that thought in one short sentence.", thread=thread)
    print("reply:", r.text)

if __name__ == "__main__":
    asyncio.run(main())
