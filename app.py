import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import jarvis_engine as jarvis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fallback-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('stop_speech')
def handle_stop_speech():
    jarvis.stop_speech()

@socketio.on('submit_text')
def handle_text_input(data):
    """Handles keyboard interaction with unique tracking IDs."""
    jarvis.stop_speech()
    user_input = data.get('text', '').strip()
    msg_id = data.get('msgId')
    
    if not user_input:
        return

    emit('status', {'msg': 'Analyzing query...'})

    def process_text():
        response_text = jarvis.get_ai_response(user_input)
        socketio.emit('chat_update_replace', {'msgId': msg_id, 'jarvis': response_text})
        socketio.emit('status', {'msg': 'Standing by.'})

    socketio.start_background_task(process_text)

@socketio.on('start_voice')
def handle_voice_input():
    """Handles voice interaction with unique tracking IDs."""
    jarvis.stop_speech()
    
    def process_voice():
        socketio.emit('status', {'msg': 'Listening...'})
        user_text = jarvis.listen_and_transcribe()
        
        msg_id = f"msg-{int(time.time() * 1000)}"
        
        if user_text:
            socketio.emit('voice_transcribed', {'userText': user_text, 'msgId': msg_id})
            socketio.emit('status', {'msg': 'Analyzing query...'})
            
            response_text = jarvis.get_ai_response(user_text)
            socketio.emit('chat_update_replace', {'msgId': msg_id, 'jarvis': response_text})
            socketio.emit('status', {'msg': 'Standing by.'})
        else:
            socketio.emit('voice_transcribed', {
                'userText': '[VOICE CAPTURE FAILED / SILENCE DETECTED]', 
                'msgId': msg_id
            })
            socketio.emit('chat_update_replace', {
                'msgId': msg_id, 
                'jarvis': "I could not detect any speech. Please check your microphone and try again, ma'am."
            })
            socketio.emit('status', {'msg': 'Standing by.'})
            
    socketio.start_background_task(process_voice)

if __name__ == '__main__':
    socketio.run(app, debug=True)