const socket = io();

const chatLog = document.getElementById('chat-log');
const textInput = document.getElementById('text-input');
const sendBtn = document.getElementById('send-btn');
const voiceBtn = document.getElementById('voice-btn');
const statusIndicator = document.getElementById('status-indicator');
const waveform = document.getElementById('waveform');

function createMessagePair(userText, msgId) {
    // 1. Create User Input Element
    const userDiv = document.createElement('div');
    userDiv.className = 'message user';
    userDiv.innerText = userText;
    chatLog.appendChild(userDiv);

    // 2. Create JARVIS Response Element directly below user input
    const jarvisDiv = document.createElement('div');
    jarvisDiv.className = 'message jarvis pending';
    jarvisDiv.id = msgId;
    jarvisDiv.innerText = 'Processing query...';
    chatLog.appendChild(jarvisDiv);

    chatLog.scrollTop = chatLog.scrollHeight;
}

function submitText() {
    const text = textInput.value.trim();
    if (text !== '') {
        const msgId = 'msg-' + Date.now();
        createMessagePair(text, msgId);
        socket.emit('submit_text', { text: text, msgId: msgId });
        textInput.value = '';
    }
}

sendBtn.addEventListener('click', submitText);
textInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') submitText();
});

voiceBtn.addEventListener('click', () => {
    statusIndicator.innerText = "STATUS: LISTENING...";
    waveform.classList.add('active');
    voiceBtn.innerText = "MIC // [REC]";
    voiceBtn.style.color = "#ff4c4c";
    
    socket.emit('stop_speech');
    socket.emit('start_voice');
});

socket.on('voice_transcribed', (data) => {
    createMessagePair(data.userText, data.msgId);
});

socket.on('chat_update_replace', (data) => {
    const jarvisElement = document.getElementById(data.msgId);
    if (jarvisElement) {
        jarvisElement.innerText = data.jarvis;
        jarvisElement.classList.remove('pending');
    } else {
        const jarvisDiv = document.createElement('div');
        jarvisDiv.className = 'message jarvis';
        jarvisDiv.innerText = data.jarvis;
        chatLog.appendChild(jarvisDiv);
    }
    chatLog.scrollTop = chatLog.scrollHeight;
});

socket.on('status', (data) => {
    statusIndicator.innerText = `STATUS: ${data.msg.toUpperCase()}`;
    if (data.msg.includes('Listening')) {
        waveform.classList.add('active');
        voiceBtn.innerText = "MIC // [REC]";
        voiceBtn.style.color = "#ff4c4c";
    } else {
        waveform.classList.remove('active');
        voiceBtn.innerText = "MIC // [OFF]";
        voiceBtn.style.color = "#a9a9a9";
    }
});