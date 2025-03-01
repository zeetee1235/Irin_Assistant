const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const cors = require('cors'); // cors 패키지 추가
const app = express();
const port = 3000;

app.use(cors()); // CORS 미들웨어 추가
app.use(bodyParser.json());
app.use(express.static('src'));

const memoryFilePath = path.join(__dirname, 'memory.json'); // 경로 수정

app.post('/save-message', (req, res) => {
    const message = req.body.message;
    console.log('Received message:', message); // 디버깅을 위한 로그 추가
    if (message) {
        fs.readFile(memoryFilePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading file:', err);
                return res.status(500).send('Error reading file');
            }
            let messages = { user_input: [], llm_response: [] };
            if (data) {
                try {
                    messages = JSON.parse(data);
                } catch (parseErr) {
                    console.error('Error parsing JSON:', parseErr);
                    return res.status(500).send('Error parsing JSON');
                }
            }
            messages.user_input.push(message);
            fs.writeFile(memoryFilePath, JSON.stringify(messages, null, 2), (err) => {
                if (err) {
                    console.error('Error writing file:', err);
                    return res.status(500).send('Error writing file');
                }
                console.log('Saved message:', message); // 콘솔에 저장된 메시지 출력
                res.send('Message saved');
            });
        });
    } else {
        res.status(400).send('No message provided');
    }
});

app.get('/get-messages', (req, res) => {
    fs.readFile(memoryFilePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading file:', err);
            return res.status(500).send('Error reading file');
        }
        let messages = { user_input: [], llm_response: [] };
        if (data) {
            try {
                messages = JSON.parse(data);
            } catch (parseErr) {
                console.error('Error parsing JSON:', parseErr);
                return res.status(500).send('Error parsing JSON');
            }
        }
        console.log('All messages:', messages); // 콘솔에 저장된 모든 메시지 출력
        res.json(messages);
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});