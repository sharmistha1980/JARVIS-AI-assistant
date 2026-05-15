const socket = io();
let audioContext, analyser, microphone, javascriptNode;

async function startJarvis() {
    socket.emit('start_jarvis');
    document.getElementById('status-text').innerText = "LISTENING...";
    document.getElementById('status-text').style.color = "#ff4444";
    
    // FEATURE 3: AUDIO-REACTIVE VISUALIZER
    if (!audioContext) {
        try {
            // Request microphone access for the browser visualizer
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioContext.createAnalyser();
            microphone = audioContext.createMediaStreamSource(stream);
            javascriptNode = audioContext.createScriptProcessor(256, 1, 1);
            
            analyser.smoothingTimeConstant = 0.8;
            analyser.fftSize = 1024;
            
            microphone.connect(analyser);
            analyser.connect(javascriptNode);
            javascriptNode.connect(audioContext.destination);
            
            // This runs continuously while listening, scaling the ring based on volume
            javascriptNode.onaudioprocess = function() {
                const array = new Uint8Array(analyser.frequencyBinCount);
                analyser.getByteFrequencyData(array);
                let values = 0;
                let length = array.length;
                for (let i = 0; i < length; i++) {
                    values += (array[i]);
                }
                let average = values / length;
                
                // Calculate scale (Base size 1 + volume offset)
                let scale = 1 + (average / 30);
                if (scale > 2.5) scale = 2.5; // Prevent it from getting too massive
                
                document.getElementById('main-ring').style.transform = `scale(${scale})`;
            }
        } catch (err) {
            console.error("Mic access denied for visualizer: ", err);
        }
    }
}

function stopAndProcess() {
    document.getElementById('status-text').innerText = "PROCESSING...";
    document.getElementById('status-text').style.color = "#FFFF00";
    document.getElementById('main-ring').style.transform = `scale(1)`; // Reset ring
}

socket.on('status', function(data) {
    const statusEl = document.getElementById('status-text');
    statusEl.innerText = data.msg;
    statusEl.style.color = data.color;
    
    // Snap ring back to normal when not listening
    if (data.msg === "IDLE" || data.msg === "THINKING...") {
        document.getElementById('main-ring').style.transform = `scale(1)`;
    }
});

socket.on('chat_update', function(data) {
    const chatBox = document.getElementById('chat-history');
    if (data.user) {
        chatBox.innerHTML += `<p style="color: white;"><b>YOU:</b> ${data.user}</p>`;
    } else {
        chatBox.innerHTML += `<p style="color: #00FFFF;"><b>JARVIS:</b> ${data.jarvis}</p>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;
});