from google import genai
from google.genai import types
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize a persistent chat session for conversational memory
chat_session = client.chats.create(
    model='gemini-2.5-flash',
    config=types.GenerateContentConfig(
        system_instruction="You are JARVIS, a highly advanced personal AI assistant. Be concise, professional, and helpful.",
    )
)

def execute_command(prompt):
    prompt_lower = prompt.lower()
    if "time" in prompt_lower and "what" in prompt_lower:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}, sir."
    return None

def get_ai_response(prompt):
    sys_response = execute_command(prompt)
    if sys_response:
        return sys_response
        
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"Error communicating with Gemini: {e}")
        return "I encountered an error connecting to my core servers, sir."