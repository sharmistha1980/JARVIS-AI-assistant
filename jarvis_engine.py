import speech_recognition as sr
import pyttsx3
from google import genai
from google.genai import types
import os
import time
import webbrowser
import datetime
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# FEATURE 1: MEMORY
# We initialize a persistent chat session so JARVIS remembers the conversation
chat_session = client.chats.create(
    model='gemini-2.5-flash',
    config=types.GenerateContentConfig(
        system_instruction="You are JARVIS, a highly advanced personal AI assistant. Be concise, professional, and helpful.",
    )
)

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def listen():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300 
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            return r.recognize_google(audio, language='en-in')
        except Exception:
            return None

# FEATURE 2: SYSTEM CONTROL
# This intercepts specific commands before asking the AI
def execute_command(prompt):
    prompt_lower = prompt.lower()
    
    if "open youtube" in prompt_lower:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube right away, sir."
    
    elif "open google" in prompt_lower:
        webbrowser.open("https://google.com")
        return "Accessing Google, sir."
    
    elif "time" in prompt_lower and "what" in prompt_lower:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}, sir."
        
    return None # If no command matches, it moves on to the AI

def get_ai_response(prompt, max_retries=2):
    # 1. Check if it's a computer command
    sys_response = execute_command(prompt)
    if sys_response:
        return sys_response
        
    # 2. If not, use the AI with Memory
    for attempt in range(max_retries):
        try:
            # send_message appends to the history automatically!
            response = chat_session.send_message(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "429" in error_msg:
                print(f"\n--- Servers busy. Retrying... (Attempt {attempt + 1}/{max_retries}) ---")
                time.sleep(2)
            else:
                print(f"\n--- GEMINI ERROR: {error_msg} ---\n")
                return "I'm having trouble connecting to my neural network, sir."
                
    return "Sir, the Google neural network is currently overwhelmed. Please try again."