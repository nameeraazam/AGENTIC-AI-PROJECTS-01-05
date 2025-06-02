import asyncio
import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

set_tracing_disabled(disabled=True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=OpenAIChatCompletionsModel(model="openai/gpt-3.5-turbo", openai_client=client),
    )

    # FIXED: Use final_output instead of data
    result = await Runner.run(
        agent,
        "What is the capital of USA?.",
    )
    print(result.final_output)  # Changed from result.data

def multiple_agents_demo():
    print("Multiple agents demo would run here")

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Single query")
    print("2. Interactive chat")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "2":
        multiple_agents_demo()
    else:
        asyncio.run(main())