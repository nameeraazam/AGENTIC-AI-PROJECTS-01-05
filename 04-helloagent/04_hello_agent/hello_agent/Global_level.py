import os
from openai import AsyncOpenAI
from agents import Agent, Runner, set_default_openai_client, set_tracing_disabled
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Please set GEMINI_API_KEY in your .env file")

# Global configuration
set_tracing_disabled(True)

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set global default client
set_default_openai_client(external_client)

def main():
    # Agent uses global configuration - no need to specify model details
    agent = Agent(
        name="Assistant", 
        instructions="You are a helpful assistant that provides creative and engaging responses.", 
        model="gemini-2.0-flash-exp"
    )

    result = Runner.run_sync(agent, "Write a short story about a robot learning to paint.")

    print("Global Level Configuration Result:")
    print(result.data)

def multiple_agents_demo():
    """Demonstrate multiple agents using global configuration"""
    
    # Creative Agent
    creative_agent = Agent(
        name="Creative Writer",
        instructions="You are a creative writer. Write imaginative and engaging content.",
        model="gemini-2.0-flash-exp"
    )
    
    # Technical Agent  
    tech_agent = Agent(
        name="Tech Explainer",
        instructions="You explain technical concepts in simple, easy-to-understand terms.",
        model="gemini-2.0-flash-exp"
    )
    
    # Code Agent
    code_agent = Agent(
        name="Code Helper",
        instructions="You help with programming questions and provide clean, well-commented code.",
        model="gemini-2.0-flash-exp"
    )
    
    agents = {
        "1": ("Creative Writer", creative_agent, "Tell me a story about time travel"),
        "2": ("Tech Explainer", tech_agent, "How does machine learning work?"),
        "3": ("Code Helper", code_agent, "Write a Python function to find prime numbers")
    }
    
    print("🌟 Multiple Agents Demo using Global Configuration")
    print("=" * 60)
    
    for key, (name, agent, sample_question) in agents.items():
        print(f"\n{key}. {name}")
        print(f"Sample: {sample_question}")
    
    while True:
        try:
            choice = input("\nChoose an agent (1-3) or 'quit': ").strip()
            
            if choice.lower() in ['quit', 'exit']:
                break
                
            if choice in agents:
                name, agent, _ = agents[choice]
                question = input(f"Ask {name}: ").strip()
                
                if question:
                    print(f"\n{name}: ", end="")
                    result = Runner.run_sync(agent, question)
                    print(result.data)
            else:
                print("Invalid choice. Please select 1, 2, 3, or 'quit'")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Choose mode:")
    print("1. Single demo")
    print("2. Multiple agents demo")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        multiple_agents_demo()
    else:
        main()