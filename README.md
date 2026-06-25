# J.A.R.V.I.S. - Cloud-Integrated Voice Assistant 🌐🤖
A sophisticated, full-stack web-based AI voice assistant powered by Python, Flask, Flask-SocketIO, and the Google Gemini API. This project features a futuristic "Electric Cyan" head-up display (HUD) web interface, robust conversational memory, and low-latency voice interaction using client-side speech synthesis and recognition. Optimized for secure cloud deployment on platforms like Render.

## ✨ Features
**Advanced AI Intelligence**: Backed by the Google Gemini API (gemini-2.5-flash) for ultra-responsive, highly contextual conversations via persistent session memory.

**Low-Latency Web Speech Architecture**: Offloads speech recognition and text-to-speech synthesis entirely to the client-side browser using the native Web Speech API. This removes server-side processing overhead and eliminates audio transmission lag.

**Custom Persona & Voice**: Features a dedicated, professional JARVIS persona equipped with a native, robotic-tuned male voice synthesized straight through the browser.

**Real-Time Bi-Directional Communication**: Implements event-driven WebSockets with Flask-SocketIO to stream user speech transcripts and AI text responses instantly to the user interface.

**Cloud-Optimized Footprint**: Clean repository architecture with production-ready dependency specifications and rigorous environment variable separation (.gitignore enforcement) for safe hosting.

## 🛠️ Tech Stack
**Backend**: Python, Flask, Flask-SocketIO

**AI Engine**: Google GenAI SDK (Gemini API)

**Frontend**: HTML5, CSS3 (Electric Cyan HUD), Vanilla JavaScript (Web Speech API, Socket.io-client)

**Production Gateway**: Gunicorn, Eventlet

## 📁 Project Structure
Plaintext
JARVIS_AI/
├── app.py                 # Flask server and routing
├── jarvis_engine.py       # Core AI logic, memory, and audio processing
├── requirements.txt       # Project dependencies
├── .env                   # Deployment-safe file exclusion rules
├── templates/
│   └── index.html         # Frontend web interface
└── static/
    ├── css/
    │   └── style.css      # Cybernetic UI layout with built-in asset styling
    └── js/
        └── script.js      # Client-side audio processing, Socket.io handling, and male speech synthesis
        
## Installation & Local Setup
**1. Clone the Repository**
git clone https://github.com/sharmistha1980/JARVIS-AI-Assistant.git
JARVIS-AI-Assistant

**2. Set Up a Virtual Environment**
python -m venv .venv

### On Windows:
.venv\Scripts\activate

### On macOS/Linux:
source .venv/bin/activate

**3. Install Dependencies**
pip install -r requirements.txt

**4. Configure Environment Variables**
Create a .env file in the root directory and securely append your Google Gemini API key:

**5. Launch the Application**
python app.py
Open your browser and navigate to http://127.0.0.1:5000 to interact with JARVIS.

# 🌐 Production Cloud Deployment (Render)
This project is configured to run flawlessly on cloud platforms like Render using asynchronous worker architectures.

### Deployment Configuration Specs:

**Deployed link**: https://jarvis-ai-assistant-f9p1.onrender.com

Runtime: Python 3

Build Command: pip install -r requirements.txt

Start Command: gunicorn -k eventlet -w 1 app:app

Environment Variables Required:

GEMINI_API_KEY: (Your secure Google AI Studio Key)

SECRET_KEY: (Production Flask session key)

PYTHON_VERSION: 3.10.0 (Forces modern dependency compliance)

⚠️ Note: Modern web browsers require a secure connection (HTTPS) to grant microphone access. Deploying on Render automatically fulfills this security protocol.

# 🛠️ How It Works
[User Speech] ----> (Browser SpeechRecognition) ----> [Text Transcript]---->(Flask-SocketIO)---->[Gemini AI Response Text]----->(SpeechSynthesis Male) -----> [Audio Output]
                                                             
**Audio Capture**: When INITIALIZE is engaged, the browser captures microphone input and uses localized speech recognition engines to instantly generate text transcripts.

**WebSocket Transit**: The text is piped via an active WebSocket pipeline (submit_text event) directly to the Flask backend.

**AI Orchestration**: app.py passes the string to jarvis_engine.py, where the Gemini context engine analyzes the conversational history and produces a structured text response.

**UI Sync & Synthesis**: The response is beamed back through the socket (chat_update), instantly printing the dialog inside the center terminal window while simultaneously triggering the browser's native male synthesis engine to dictate the speech.
