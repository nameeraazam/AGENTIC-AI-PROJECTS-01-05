import os
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Please set GEMINI_API_KEY in your .env file")

# Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

def main():
    agent = Agent(
        name="Assistant", 
        instructions="You are a helpful assistant that explains complex topics clearly and concisely."
    )

    result = Runner.run_sync(
        agent, 
        "Explain quantum computing in simple terms.", 
        run_config=config
    )

    print("Run Level Configuration Result:")
    print(result.data)

def interactive_chat():
    """Interactive chat with run-level configuration"""
    agent = Agent(
        name="Helpful Assistant",
        instructions="You are a knowledgeable and friendly assistant. Provide clear, helpful responses."
    )
    
    print("🤖 Run Level Assistant is ready! (Type 'quit' to exit)")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("Assistant: ", end="")
            result = Runner.run_sync(agent, user_input, run_config=config)
            print(result.data)
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Single query")
    print("2. Interactive chat")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        interactive_chat()
    else:
        main()