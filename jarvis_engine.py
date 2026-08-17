import os
import sys
import datetime
import threading
import subprocess
import webbrowser
import speech_recognition as sr
from faster_whisper import WhisperModel
import ollama

# Initialize STT on CPU
stt_model = WhisperModel("base.en", device="cpu", compute_type="int8")

chat_history = []
current_tts_process = None

def get_system_time_context():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%A, %B %d, %Y")
    hour = now.hour
    if 5 <= hour < 12:
        period = "Morning"
    elif 12 <= hour < 17:
        period = "Afternoon"
    elif 17 <= hour < 22:
        period = "Evening"
    else:
        period = "Night"
    return f"Current System Time: {current_time}. Date: {current_date}. Period of day: {period}."

def stop_speech():
    """Instantly terminates any active speech process on Windows."""
    global current_tts_process
    if current_tts_process and current_tts_process.poll() is None:
        try:
            current_tts_process.terminate()
            current_tts_process.wait(timeout=0.2)
        except Exception:
            pass
        current_tts_process = None

def speak(text):
    """Spawns an isolated Python subprocess for text-to-speech."""
    global current_tts_process
    stop_speech()  # Kill any ongoing speech first
    
    clean_text = text.replace('"', '\\"').replace("'", "\\'").replace("\n", " ")
    
    py_cmd = (
        f"import pyttsx3; "
        f"engine = pyttsx3.init(); "
        f"engine.setProperty('rate', 175); "
        f"engine.setProperty('volume', 1.0); "
        f"engine.say('{clean_text}'); "
        f"engine.runAndWait()"
    )
    
    try:
        current_tts_process = subprocess.Popen(
            [sys.executable, "-c", py_cmd],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"TTS Process Error: {e}")

def execute_command(prompt):
    """Intercepts local system commands before passing to Ollama."""
    prompt_lower = prompt.lower()
    
    # --- System Automation Commands ---
    # Microsoft Word
    if any(phrase in prompt_lower for phrase in ["open word", "word 2013", "microsoft word"]):
        try:
            subprocess.Popen(["start", "winword"], shell=True)
            return "Opening Microsoft Word for you now, ma'am."
        except Exception as e:
            return f"Failed to launch Microsoft Word: {e}"

    # Microsoft Excel
    if any(phrase in prompt_lower for phrase in ["excel", "ms excel", "microsoft excel", "mx xl", "ms xl", "open xl"]):
        try:
            subprocess.Popen(["start", "excel"], shell=True)
            return "Opening Microsoft Excel for you now, ma'am."
        except Exception as e:
            return f"Failed to launch Microsoft Excel: {e}"

    # Notepad
    if "open notepad" in prompt_lower:
        subprocess.Popen(["notepad"], shell=True)
        return "Opening Notepad, ma'am."

    # Calculator
    if "open calculator" in prompt_lower or "open calc" in prompt_lower:
        subprocess.Popen(["calc"], shell=True)
        return "Opening Calculator, ma'am."

    # Gmail
    if "open gmail" in prompt_lower or "check my email" in prompt_lower:
        webbrowser.open("https://mail.google.com")
        return "Opening your Gmail now, ma'am."

    # Browser
    if "open google" in prompt_lower or "open browser" in prompt_lower:
        webbrowser.open("https://www.google.com")
        return "Opening your web browser, ma'am."

    # System Time
    if "time" in prompt_lower and "what" in prompt_lower:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}, ma'am."

    return None

def get_ai_response(prompt):
    sys_response = execute_command(prompt)
    if sys_response:
        speak(sys_response)
        return sys_response
        
    try:
        time_context = get_system_time_context()
        system_instruction = (
            f"You are JARVIS, a highly advanced local AI assistant. Address the user as ma'am. "
            f"Be concise, direct, and professional. {time_context} Always address greetings appropriately for the local time of day."
        )
        
        messages = [{"role": "system", "content": system_instruction}] + chat_history + [{"role": "user", "content": prompt}]
        
        response = ollama.chat(
            model='llama3.2', 
            messages=messages,
            options={
                'num_predict': 120,
                'temperature': 0.7
            }
        )
        ai_reply = response['message']['content']
        
        chat_history.append({"role": "user", "content": prompt})
        chat_history.append({"role": "assistant", "content": ai_reply})
        
        speak(ai_reply)
        return ai_reply
        
    except Exception as e:
        print(f"Error communicating with local LLM: {e}")
        error_msg = "I encountered an error processing the request locally, ma'am."
        speak(error_msg)
        return error_msg

def listen_and_transcribe():
    """Captures audio from mic and transcribes using faster-whisper."""
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("Calibrating background noise...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=6, phrase_time_limit=10)
            
            with open("temp_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            print("Transcribing...")
            segments, info = stt_model.transcribe("temp_audio.wav", beam_size=5)
            transcription = "".join([segment.text for segment in segments])
            return transcription.strip()
            
        except sr.WaitTimeoutError:
            print("Audio capture error: Listening timed out.")
            return ""
        except Exception as e:
            print(f"Audio capture error: {e}")
            return ""