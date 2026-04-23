import { GoogleGenerativeAI } from "https://esm.run/@google/generative-ai";

// CẤU HÌNH API
const API_KEY = "AIzaSyCzdr1TsaLnhkqYerB-UISSYfFBO5pX-Us"; 
const genAI = new GoogleGenerativeAI(API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const chatWindow = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const loading = document.getElementById('loading');

async function handleChat() {
    const text = userInput.value.trim();
    if (!text) return;

    // Hiển thị tin nhắn người dùng
    appendMessage(text, 'user');
    userInput.value = '';
    
    // Hiện hiệu ứng đang chờ
    loading.style.display = 'block';

    try {
        const result = await model.generateContent(text);
        const response = await result.response;
        const botText = response.text();
        
        appendMessage(botText, 'bot');
    } catch (error) {
        console.error("Lỗi API:", error);
        appendMessage("⚠️ Có lỗi xảy ra: " + error.message, 'bot');
    } finally {
        loading.style.display = 'none';
    }
}

function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `msg ${sender}`;
    msgDiv.innerText = text;
    chatWindow.appendChild(msgDiv);
    
    // Tự động cuộn xuống cuối
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Lắng nghe sự kiện Click và phím Enter
sendBtn.addEventListener('click', handleChat);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleChat();
});