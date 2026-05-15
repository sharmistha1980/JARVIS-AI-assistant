# J.A.R.V.I.S. - Cloud-Integrated Voice Assistant 🌐🤖

A sophisticated, web-based AI voice assistant powered by **Python, Flask, and the Google Gemini API**. This project features a futuristic "Electric Cyan" web interface with an audio-reactive visualizer, robust conversational memory, and seamless system command execution.

## ✨ Features

*   **Advanced AI Conversation:** Utilizes the Google Gemini API for intelligent, contextual responses with built-in conversation memory.
*   **Speech-to-Text & Text-to-Speech:** Thread-safe voice processing using `SpeechRecognition` for input and offline `pyttsx3` for lightning-fast voice synthesis.
*   **Dynamic Web Interface:** A custom Flask-served UI featuring an "Electric Cyan" aesthetic and a real-time audio-reactive visualizer that responds to voice input.
*   **System Automation:** Capable of executing system commands, such as opening websites and applications directly via voice.
*   **Robust Architecture:** Built with comprehensive error handling for API traffic to ensure continuous, reliable operation.

## 🛠️ Tech Stack

*   **Backend:** Python, Flask
*   **AI Engine:** Google Gemini API
*   **Audio Processing:** `pyttsx3`, `SpeechRecognition`
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript

## 📁 Project Structure


JARVIS_AI/
├── app.py                 # Flask server and routing
├── jarvis_engine.py       # Core AI logic, memory, and audio processing
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (API keys)
├── templates/
│   └── index.html         # Frontend web interface
└── static/
    ├── css/
    │   └── style.css      # Electric Cyan styling and visualizer CSS
    └── js/
        └── script.js      # Frontend logic and audio reactivity

### Installation & Setup
1. Clone the repository


git clone [https://github.com/sharmistha1980/JARVIS-AI-Assistant.git](https://github.com/sharmistha1980/JARVIS-AI-Assistant.git)

cd JARVIS-AI-Assistant
2. Set up a Virtual Environment


python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the root directory and add your Google Gemini API key:

Code snippet
GEMINI_API_KEY=your_google_gemini_api_key_here

5. Run the Application

python app.py
The server will start locally. Open your browser and navigate to http://127.0.0.1:5000 to interact with J.A.R.V.I.S.


### How It Works
Audio Capture: The frontend or local microphone captures user input via SpeechRecognition.

Processing: jarvis_engine.py analyzes the text. If it's a system command (e.g., "Open YouTube"), it executes locally.

AI Generation: Complex queries are routed to the Gemini API, maintaining chat history for contextual awareness.

Response & Visualization: The text response is converted to speech via pyttsx3 while the Flask backend triggers the frontend visualizer to animate in sync with the interaction.        