# 12b_resume_thread_responses.py
import os, json, asyncio, tempfile
from dotenv import load_dotenv
from agent_framework.azure import AzureOpenAIResponsesClient

load_dotenv()
THREAD_PATH = os.path.join(tempfile.gettempdir(), "agent_thread.json")
# Or hardcode the path you printed:
# THREAD_PATH = "/var/folders/h5/9glc6d8s5fn7pzq2jyhx33940000gn/T/agent_thread_20251009T153855Z.json"

async def main():
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "v1"),
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    ).create_agent(
        name="physicsbot",
        instructions="You are professor in astrophysics",
    )

    with open(THREAD_PATH, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    # Resume the exact conversation
    resumed_thread = await agent.deserialize_thread(loaded)

    # Tiny memory signal
    print(f"memory: restored {len(loaded.get('messages', [])) if isinstance(loaded, dict) else 0} message(s)")

    r2 = await agent.run("Continue that thought in one sentence.", thread=resumed_thread)
    print("reply #2:", r2.text)

if __name__ == "__main__":
    asyncio.run(main())
