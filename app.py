import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import jarvis_engine as jarvis

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('submit_text')
def handle_text_input(data):
    """Handles text-based interaction from the web UI"""
    user_input = data.get('text', '').strip()
    if not user_input:
        return
        
    # Get JARVIS's response
    response_text = jarvis.get_ai_response(user_input)
    
    # Send BOTH user input and JARVIS response back to the frontend
    emit('chat_update', {'user': user_input, 'jarvis': response_text})

if __name__ == '__main__':
    socketio.run(app, debug=True)