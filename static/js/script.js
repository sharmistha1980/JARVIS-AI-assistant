const socket = io.connect(window.location.origin);
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;
let currentTranscript = "";

// Helper function to safely find WHERE to display text on your screen
function displayMessage(heading, text, color) {
    // Try to find a chat-box, a text-area, or the main container dynamically
    let container = document.getElementById('chat-box') || 
                    document.querySelector('textarea') || 
                    document.querySelector('.container') || 
                    document.body;
                    
    // If it's a textarea or input field, change its value
    if (container.tagName === 'TEXTAREA' || container.tagName === 'INPUT') {
        container.value += `\n${heading}: ${text}`;
    } else {
        // Otherwise, append it as HTML safely
        const p = document.createElement('p');
        p.style.color = color || '#00ffff';
        p.style.margin = '10px 0';
        p.innerHTML = `<b>${heading}:</b> ${text}`;
        container.appendChild(p);
    }
}

// 1. Initialize Microphone & Speech Recognition
if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = true; 
    recognition.lang = 'en-IN';
    recognition.interimResults = false;

    recognition.onstart = () => {
        console.log("Microphone active. Talk now...");
    };

    recognition.onresult = (event) => {
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                currentTranscript += event.results[i][0].transcript + " ";
            }
        }
        console.log("Current captured speech:", currentTranscript);
    };

    recognition.onerror = (event) => {
        console.error("Speech Recognition Error:", event.error);
        displayMessage("SYSTEM ERROR", `Microphone issue (${event.error}). Ensure microphone permissions are allowed.`, '#ff4444');
    };
} else {
    alert("Your browser does not support voice recognition. Please use Google Chrome or Microsoft Edge.");
}

// 2. Global Button Click Handlers (Matches your HTML onclick functions)
window.startJarvis = function() {
    if (recognition) {
        currentTranscript = ""; 
        try {
            recognition.start();
            displayMessage("SYSTEM", "Listening... Speak into your microphone.", '#ff4444');
        } catch (e) {
            console.log("Recognition already running or starting:", e);
        }
    }
};

window.stopAndProcess = function() {
    if (recognition) {
        try {
            recognition.stop();
        } catch(e) {}
        
        setTimeout(() => {
            if (currentTranscript.trim() !== "") {
                displayMessage("YOU", currentTranscript, '#ffffff');
                socket.emit('submit_text', { text: currentTranscript });
                currentTranscript = ""; // Reset for next time
            } else {
                displayMessage("SYSTEM", "No voice captured. Try clicking INITIALIZE and speaking clearly again.", '#ffcc00');
            }
        }, 500); // Small delay to let the final speech register
    }
};

// 3. Receive Response from Backend and Speak It
socket.on('chat_update', function(data) {
    displayMessage("JARVIS", data.jarvis, '#00ffff');
    speakLikeJarvis(data.jarvis);
});

// Native Male Voice Synthesizer
function speakLikeJarvis(text) {
    const synth = window.speechSynthesis;
    if (!synth) return;
    
    // Stop any voice currently playing to avoid overlapping
    synth.cancel(); 

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.pitch = 0.85; // Robotic tone
    utterance.rate = 1.05;  // Crisp speed

    let voices = synth.getVoices();
    // Search system voices for a male voice profile
    const maleVoice = voices.find(voice => 
        voice.name.includes('Male') || 
        voice.name.includes('David') || 
        voice.name.includes('Arthur') ||
        voice.name.includes('Mark')
    );

    if (maleVoice) utterance.voice = maleVoice;
    synth.speak(utterance);
}

// Pre-load voices for browser readiness
if (typeof speechSynthesis !== 'undefined' && speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
}