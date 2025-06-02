import asyncio
import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

if not openrouter_api_key:
    raise ValueError("Please set OPENROUTER_API_KEY in your .env file")

# OpenRouter client setup
client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

set_tracing_disabled(disabled=True)

async def main():
    # Using OpenRouter with various models
    models = {
        "1": ("Llama 3.1 8B (Free)", "meta-llama/llama-3.1-8b-instruct:free"),
        "2": ("GPT-3.5 Turbo", "openai/gpt-3.5-turbo"),
        "3": ("Gemma 2 9B (Free)", "google/gemma-2-9b-it:free"),
        "4": ("Phi-3 Mini (Free)", "microsoft/phi-3-mini-128k-instruct:free"),
    }
    
    print("Available OpenRouter Models:")
    for key, (name, model_id) in models.items():
        print(f"{key}. {name}")
    
    choice = input("\nChoose a model (1-4): ").strip()
    
    if choice in models:
        model_name, model_id = models[choice]
        print(f"Using: {model_name}")
        
        agent = Agent(
            name="OpenRouter Assistant",
            instructions="You are a helpful AI assistant. Provide clear, informative, and engaging responses.",
            model=OpenAIChatCompletionsModel(model=model_id, openai_client=client),
        )

        # Interactive chat
        print(f"\n🚀 {model_name} Assistant is ready! (Type 'quit' to exit)")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("Assistant: ", end="")
                result = await Runner().run(agent, user_input)
                print(result.data)
                    
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                print("Please try again or type 'quit' to exit.")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    asyncio.run(main())