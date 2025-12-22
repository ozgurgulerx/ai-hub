"""
Persist a Responses-backed thread and resume it later.
"""

import asyncio
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIResponsesClient

load_dotenv()

SAVE_PATH = Path("saved_responses_thread.json")


async def save_thread(agent, thread):
    data = await thread.serialize()
    SAVE_PATH.write_text(json.dumps(data, indent=2))
    print(f"Saved thread to {SAVE_PATH}")


async def restore_thread(agent):
    data = json.loads(SAVE_PATH.read_text())
    return await agent.deserialize_thread(data)


async def main() -> None:
    client = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    agent = client.create_agent(name="persist-demo", instructions="Be concise.")

    if not SAVE_PATH.exists():
        thread = agent.get_new_thread()
        r1 = await agent.run("My favourite black hole is Sagittarius A*. Remember it.", thread=thread)
        print("[first run]", r1.text)
        await save_thread(agent, thread)
        return

    # Simulate new process: rebuild agent, load thread
    restored_thread = await restore_thread(agent)
    r2 = await agent.run("Which black hole did I say I like?", thread=restored_thread)
    print("[resumed run]", r2.text)


if __name__ == "__main__":
    asyncio.run(main())
