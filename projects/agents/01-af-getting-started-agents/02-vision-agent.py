import os
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient
from dotenv import load_dotenv
from agent_framework import ChatMessage, TextContent, UriContent, Role

load_dotenv()

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
        name="VisionAgent",
        instructions="What do you see in this image?",
    )

    message = ChatMessage(
        role=Role.USER,
        contents=[
            TextContent(text="Tell me a joke about this image?"),
            UriContent(uri="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg", media_type="image/jpeg")
        ]
    )

    response = await agent.run(message)
    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
