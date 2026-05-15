from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import jarvis_engine as jarvis

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_jarvis')
def handle_jarvis():
    emit('status', {'msg': 'LISTENING...', 'color': '#ff4444'})
    user_input = jarvis.listen()
    
    if user_input:
        emit('chat_update', {'user': user_input})
        emit('status', {'msg': 'THINKING...', 'color': '#00FFFF'})
        
        response = jarvis.get_ai_response(user_input)
        emit('chat_update', {'jarvis': response})
        
        emit('status', {'msg': 'SPEAKING...', 'color': '#00ff00'})
        jarvis.speak(response)
        emit('status', {'msg': 'IDLE', 'color': '#00FFFF'})
    else:
        emit('status', {'msg': 'IDLE (NO INPUT)', 'color': '#00FFFF'})

if __name__ == '__main__':
    socketio.run(app, debug=True)