document.addEventListener('DOMContentLoaded', (event) => {
    const input = document.getElementById('chat-input');
    input.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Fetch and display all messages on page load
    fetch('http://localhost:3000/get-messages')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(messages => {
            console.log('All messages:', messages); // 콘솔에 저장된 모든 메시지 출력
            displayMessages(messages);
        })
        .catch(error => console.error('Error:', error));

    // Periodically check for new bot responses
    setInterval(fetchBotResponses, 5000);
});

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    console.log('Sending message:', message); // 디버깅을 위한 로그 추가
    if (message) {
        addMessage('user', message);
        input.value = '';
        // Save message to server
        fetch('http://localhost:3000/save-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
    }
}

function fetchBotResponses() {
    fetch('http://localhost:3000/get-messages')
        .then(response => response.json())
        .then(messages => {
            displayMessages(messages);
        })
        .catch(error => console.error('Error:', error));
}

function displayMessages(messages) {
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.innerHTML = ''; // 기존 메시지 초기화

    const userMessages = messages.user_input || [];
    const botResponses = messages.llm_response || [];

    const maxLength = Math.max(userMessages.length, botResponses.length);

    for (let i = 0; i < maxLength; i++) {
        if (i < userMessages.length) {
            addMessage('user', userMessages[i]);
        }
        if (i < botResponses.length) {
            addMessage('bot', botResponses[i]);
        }
    }
}

function addMessage(sender, text) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = text;
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}