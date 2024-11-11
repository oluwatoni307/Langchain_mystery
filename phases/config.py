from langchain_openai import ChatOpenAI
import os

api_key = os.getenv("api_key")


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.4,
    max_tokens=400,
    timeout=None,
    max_retries=2,
    api_key=api_key,  # if you prefer to pass api key in directly instaed of using env vars
)
summary = ChatOpenAI(
    model="gpt-4o",
    temperature=0.4,
    max_tokens=500,
    timeout=None,
    max_retries=2,
    api_key=api_key,  # if you prefer to pass api key in directly instaed of using env vars
)
