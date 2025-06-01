import os
from dotenv import load_dotenv
import chainlit as cl
from litellm import completion
import json

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    await cl.Message(
        content="Welcome to the **Translator Agent By Syeda Nameera**!\n\nPlease tell me **what you want to translate** and **into which language?**"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="Translating......!")
    await msg.send()
    
    history = cl.user_session.get("chat_history") or []
    
    # Add user message to history
    history.append({"role": "user", "content": message.content})
    
    # Add system message for translation context
    messages = [
        {"role": "system", "content": "You are a helpful translator. Translate the user's text into the requested language. If no target language is specified, ask what language they want to translate to."},
        *history
    ]
    
    try:
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=gemini_api_key,
            messages=messages
        )
        
        response_content = response.choices[0].message.content
        msg.content = response_content
        await msg.update()
        
        # Add assistant response to history
        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()

@cl.on_chat_end
async def on_chat_end():
    history = cl.user_session.get("chat_history") or []
    
    try:
        with open("translation_chat_history.json", "w") as f:
            json.dump(history, f, indent=2)
        
        print("Chat history saved")
    except Exception as e:
        print(f"Error saving chat history: {str(e)}")