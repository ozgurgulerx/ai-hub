"""
Serialize and persist an entire thread, then resume it later with full context.

Run twice:
- 1st run: create a new thread, capture details, and write the serialized thread to disk.
- 2nd run: reload the thread from disk and keep chatting with full memory intact.
"""

import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIResponsesClient

load_dotenv()

STATE_PATH = Path(__file__).with_name("thread_state_roman_incident.json")


def create_agent():
    client = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    return client.create_agent(
        name="roman-history-keeper",
        instructions="You are a lively Roman historian who retells incidents crisply and vividly. Keep answers concise.",
    )


async def save_thread(thread) -> None:
    serialized = await thread.serialize()
    STATE_PATH.write_text(json.dumps(serialized, indent=2))
    print(f"[saved] thread state -> {STATE_PATH}")


async def load_thread(agent):
    serialized = json.loads(STATE_PATH.read_text())
    return await agent.deserialize_thread(serialized)


async def first_run(agent) -> None:
    """
    Start a fresh thread, stash a Roman incident, then persist the thread.
    """
    thread = agent.get_new_thread()
    await agent.run(
        "I'm Livia, a Roman historian. Record this strange incident at the Pons Sublicius in 49 BCE: "
        "an omen of crows circling, the standard of the III Gallica briefly fell, "
        "centurion Cassius shouted 'Fortune favours the bold,' and the legion cheered as we crossed. "
        "Remember these exact details for future retellings.",
        thread=thread,
    )
    r = await agent.run(
        "Confirm you've saved the omen, the fallen standard, Cassius's shout, and which legion cheered.",
        thread=thread,
    )
    print("[first run confirmation]", r.text)
    await save_thread(thread)
    print("Run this script again to see the thread restored.")


async def resumed_run(agent) -> None:
    """
    Reload the persisted thread and keep chatting with all context intact.
    """
    restored_thread = await load_thread(agent)
    r = await agent.run(
        "Retell the incident and remind me which legion cheered and what the omen was.",
        thread=restored_thread,
    )
    print("[resumed thread]", r.text)


async def main() -> None:
    agent = create_agent()
    if not STATE_PATH.exists():
        await first_run(agent)
    else:
        await resumed_run(agent)


if __name__ == "__main__":
    asyncio.run(main())
