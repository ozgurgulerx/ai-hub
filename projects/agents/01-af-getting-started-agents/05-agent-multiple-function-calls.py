import os
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from dotenv import load_dotenv


load_dotenv()

from typing import Annotated
from pydantic import Field

class WeatherTools:
    def __init__(self):
        self.last_location = None

    def get_weather(
        self,
        location: Annotated[str, Field(description="The location to get the weather for.")],
    ) -> str:
        """Get the weather for a given location."""
        return f"The weather in {location} is cloudy with a high of 15°C."

    def get_weather_details(self) -> int:
        """Get the detailed weather for the last requested location."""
        if self.last_location is None:
            return "No location specified yet."
        return f"The detailed weather in {self.last_location} is cloudy with a high of 15°C, low of 7°C, and 60% humidity."

tools = WeatherTools()
async def main():
    # Initialize a chat agent with Azure OpenAI Responses
    # the endpoint, deployment name, and api version can be set via environment variables
    # or they can be passed in directly to the AzureOpenAIResponsesClient constructor
    # make sure you are using "AZURE_OPENAI_VERSION=v1"
    agent = AzureOpenAIResponsesClient(
        endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],  # Optional if using AzureCliCredential

    ).create_agent(
        name="weather-bot",
        instructions="You are a helpful assistant",
        tools=[tools.get_weather, tools.get_weather_details]
    )

    result = await agent.run("What is the weather like in Amsterdam?")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
