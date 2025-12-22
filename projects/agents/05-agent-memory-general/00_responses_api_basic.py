"""
Minimal Responses API call with Azure OpenAI env vars.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
model = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

client = OpenAI(api_key=api_key, base_url=f"{endpoint}/openai/v1/")


if __name__ == "__main__":
    resp = client.responses.create(
        model=model,
        input=[{"role": "user", "content": "What is a black hole?"}],
    )
    print(f"response.id={resp.id}")
    print(resp)
