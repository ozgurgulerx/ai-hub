import os
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from dotenv import load_dotenv


load_dotenv()

from typing import Annotated
from pydantic import Field

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."

async def main():
    # Initialize a chat agent with Azure OpenAI Responses
    # the endpoint, deployment name, and api version can be set via environment variables
    # or they can be passed in directly to the AzureOpenAIResponsesClient constructor
    # make sure you are using "AZURE_OPENAI_VERSION=v1"
    weather_agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],  # Optional if using AzureCliCredential

    ).create_agent(
        name="weather-bot",
        description= "An agent that answers questions about weather",
        instructions="You answer questions about the weather",
        tools=get_weather
    )

    main_agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],  # Optional if using AzureCliCredential
    ).create_agent(
        instructions= "You are a helpful agent that responds in French",
        tools=weather_agent.as_tool()
    )

    result = await main_agent.run("What is the weather like in Amsterdam?")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
