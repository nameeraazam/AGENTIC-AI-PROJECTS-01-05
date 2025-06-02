import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

# Load environment variables
load_dotenv()

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

MODEL = 'gemini/gemini-2.0-flash'

@function_tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    print(f"[debug] getting weather for {city}")
    # This is a mock response - replace with real API call
    return f"The weather in {city} is sunny with 72°F temperature."

def main():
    """Main function to run the agent."""
    # Create agent
    agent = Agent(
        name="Haiku Assistant",
        instructions="You only respond in haikus. Always format your response as a traditional 5-7-5 syllable haiku.",
        model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
    )
    
    # Add the weather function to the agent
    agent.functions = [get_weather]
    
    # Run the agent
    print("Running LiteLLM Agent with Google Gemini...")
    print("=" * 50)
    
    result = Runner.run_sync(agent, "What's the weather in Tokyo?")
    print("Agent Response:")
    print(result.final_output)
    print("=" * 50)

if __name__ == "__main__":
    main()