"""
In-memory short-term chat: reuse a thread so the agent remembers prior turns.
"""

import asyncio
import os
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIResponsesClient

load_dotenv()


async def main() -> None:
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    ).create_agent(
        name="threaded-agent",
        instructions="Be concise.",
    )

    thread = agent.get_new_thread()

    r1 = await agent.run("My favourite black hole is Sagittarius A*. Remember that.", thread=thread)
    print("[call 1 - with thread]", r1.text)

    r2 = await agent.run("Which black hole did I say I like?", thread=thread)
    print("[call 2 - with thread]", r2.text)


if __name__ == "__main__":
    asyncio.run(main())
