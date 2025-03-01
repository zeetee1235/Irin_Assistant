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
            messages.forEach(message => addMessage('user', message));
        })
        .catch(error => console.error('Error:', error));
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

        // Simulate bot response
        setTimeout(() => {
            addMessage('bot', 'This is a bot response.');
        }, 1000);
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