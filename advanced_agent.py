import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = 'gemini/gemini-2.0-flash'

@function_tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    print(f"[debug] Fetching weather for {city}")
    # Mock weather data - replace with real API
    weather_data = {
        "Tokyo": "Sunny, 75°F",
        "New York": "Cloudy, 68°F", 
        "London": "Rainy, 60°F",
        "Paris": "Partly cloudy, 72°F"
    }
    return weather_data.get(city, f"Weather data not available for {city}")

@function_tool
def get_time(timezone: str = "UTC") -> str:
    """Get current time in specified timezone."""
    print(f"[debug] Getting time for {timezone}")
    from datetime import datetime
    return f"Current time in {timezone}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

async def run_interactive_agent():
    """Run an interactive agent session."""
    agent = Agent(
        name="Haiku Weather Assistant",
        instructions="""You are a helpful assistant that responds in haikus (5-7-5 syllable format).
        You can help with weather information and time queries.
        Always format your responses as traditional haikus.""",
        model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
        functions=[get_weather, get_time]
    )
    
    print("🤖 Haiku Weather Assistant is ready!")
    print("Ask me about weather or time (type 'quit' to exit)")
    print("=" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye! 🌸")
            break
            
        if user_input:
            try:
                result = await Runner.run(agent, user_input)
                print(f"\n🌸 Assistant:\n{result.final_output}")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(run_interactive_agent())