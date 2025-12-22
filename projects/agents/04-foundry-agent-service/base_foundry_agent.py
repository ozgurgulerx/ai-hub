"""
Basic Azure AI Foundry agent using the low-level AgentsClient (no Agent Framework helpers).

Environment (any of the compatible names will work):
- Endpoint: AZURE_OPENAI_PROJECT_ENDPOINT or AZURE_AI_PROJECT_ENDPOINT or PROJECT_ENDPOINT
- Deployment (optional, defaults to "gpt-4.1"): AZURE_OPENAI_DEPLOYMENT_NAME or AZURE_AI_MODEL_DEPLOYMENT_NAME

Auth: DefaultAzureCredential() (works with `az login`, managed identity, etc.) or project key via AZURE_AI_PROJECT_KEY/PROJECT_KEY.
"""

import os

from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def _env_first(*names: str) -> str:
    for name in names:
        val = os.getenv(name)
        if val:
            return val
    raise RuntimeError(f"Missing required environment variable. Tried: {', '.join(names)}")


def main() -> None:
    load_dotenv()

    endpoint = _env_first(
        "AZURE_OPENAI_PROJECT_ENDPOINT",
        "AZURE_AI_PROJECT_ENDPOINT",
        "PROJECT_ENDPOINT",
    )
    # Hardcode model to gpt-4.1 for reliability (ignore other deployment env vars).
    deployment = "gpt-4.1"
    # AgentsClient requires a token credential (AAD); project keys are not supported.
    agents_client = AgentsClient(endpoint=endpoint, credential=DefaultAzureCredential(), api_version="2025-05-01")

    # Keep the agent minimal for reliability (no optional tools by default).
    agent = agents_client.create_agent(
        model=deployment,
        name="my-agent",
        instructions="You are a helpful assistant.",
    )
    print("Agent:", agent.id)

    thread = agents_client.threads.create()
    agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content="What is a blackhole?",
    )

    run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print("Run status:", run.status)

    if str(run.status).upper() != "COMPLETED":
        error = getattr(run, "error", None) or getattr(run, "last_error", None)
        if error:
            print(f"Run error: code={getattr(error, 'code', None)} message={getattr(error, 'message', error)}")
        try:
            steps = list(agents_client.run_steps.list(thread_id=thread.id, run_id=run.id))
            for step in steps:
                print(f"Step: {step.type} status={step.status} details={getattr(step, 'status_details', None)}")
        except Exception as ex:  # best-effort diagnostics
            print(f"Could not list run steps: {ex}")

    for msg in agents_client.messages.list(thread_id=thread.id):
        if msg.content and hasattr(msg.content[0], "text"):
            print(f"{msg.role}: {msg.content[0].text.value}")
        else:
            print(f"{msg.role}: [no text]")

    # Optional cleanup:
    # agents_client.delete_agent(agent.id)


if __name__ == "__main__":
    main()
