import asyncio
from openai import AsyncOpenAI

# Test script to verify OpenRouter connection
async def test_openrouter():
    client = AsyncOpenAI(
        api_key="",
        base_url="https://openrouter.ai/api/v1"
    )
    
    # Test different model IDs
    models_to_test = [
        "openai/gpt-3.5-turbo",
        "openai/gpt-3.5-turbo-1106",
        "openai/gpt-3.5-turbo-0125",
        "meta-llama/llama-2-70b-chat"
    ]
    
    for model in models_to_test:
        try:
            print(f"Testing model: {model}")
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say 'Hello' in a haiku format"}],
                max_tokens=50
            )
            print(f"✅ {model} works!")
            print(f"Response: {response.choices[0].message.content}")
            print("-" * 50)
            break
        except Exception as e:
            print(f"❌ {model} failed: {e}")
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_openrouter())
