# SYS.JARVIS // Offline AI Assistant

## About the Project
Developed by a final-year B.Tech Computer Science student with a strong focus on Natural Language Processing (NLP) and Deep Learning, this project is a fully localized, offline AI voice assistant. It is designed to process speech, generate intelligent conversational responses, and execute local operating system commands with sub-second latency, without relying on cloud APIs.

## Tech Stack
*   **Backend:** Python, Flask, Flask-SocketIO
*   **Large Language Model (LLM):** Ollama running Llama 3.2 (3B parameters)
*   **Speech-to-Text (STT):** Faster-Whisper (base.en) utilizing INT8 CPU quantization
*   **Text-to-Speech (TTS):** pyttsx3 (SAPI5)
*   **Frontend:** HTML, CSS, Vanilla JavaScript, Socket.IO

## System Architecture
The application follows a real-time, event-driven architecture designed to prevent thread deadlocks and ensure a highly responsive user interface:
*   **Real-Time UI:** The browser communicates with the server via WebSockets, allowing instant, bidirectional streaming of status updates and text without page reloads.
*   **Asynchronous Traffic Controller:** The Flask backend spawns non-blocking background tasks for every user input. This keeps the main server thread open to listen for interrupts or new commands.
*   **Deterministic Command Interceptor:** Before passing prompts to the AI, a Python rule-engine scans for system keywords (e.g., "open word", "open gmail") and executes OS-level subprocesses directly. 
*   **Isolated Speech Threads:** To bypass Windows COM threading freezes, the text-to-speech engine is offloaded into a completely isolated Python subprocess that can be instantly terminated by the user.

## Engineering Challenges & Solutions
*   **Hardware Driver Conflicts:** Encountered CUDA DLL driver issues when running STT on the GPU. Resolved by migrating the Whisper model to execute on the CPU using INT8 quantization, maintaining real-time speeds while stripping away complex driver dependencies.
*   **UI Thread Blocking:** The TTS engine initially deadlocked the Flask server. Solved by decoupling the audio generation into a `subprocess.Popen` task, allowing the written response to render instantly on the frontend while audio plays asynchronously.
*   **AI System Hallucinations:** The LLM would pretend to launch applications without executing OS code. Fixed by engineering a Python intercept layer to catch specific phrases and execute native `subprocess` and `webbrowser` calls prior to LLM inference.

## Setup & Installation
1. Install Ollama and pull the Llama 3.2 model: `ollama pull llama3.2`
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment and install dependencies: `pip install -r requirements.txt`
4. Run the server: `python app.py`
5. Navigate to `http://127.0.0.1:5000` to access the Forensic Terminal.
