"""
Compare stateless calls vs Responses-backed thread memory.
"""

import asyncio
import os
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIResponsesClient

load_dotenv()


async def main() -> None:
    client = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )

    agent = client.create_agent(name="responses-demo", instructions="Be concise.")

    # Part A: stateless (no thread)
    a1 = await agent.run("My favourite black hole is Sagittarius A*. Remember it.", thread=None)
    print("[A1 no thread]", a1.text)
    a2 = await agent.run("Which black hole did I say I like?", thread=None)
    print("[A2 no thread]", a2.text)

    # Part B: service-managed thread
    thread = agent.get_new_thread()
    b1 = await agent.run("My favourite black hole is Sagittarius A*. Remember it.", thread=thread)
    print("\n[B1 thread]", b1.text)
    print("[thread service id]", thread.service_thread_id)

    b2 = await agent.run("Which black hole did I say I like?", thread=thread)
    print("[B2 thread]", b2.text)
    print("[thread service id again]", thread.service_thread_id)


if __name__ == "__main__":
    asyncio.run(main())
